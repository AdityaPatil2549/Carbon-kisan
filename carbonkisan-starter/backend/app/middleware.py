"""
CarbonKisan — Production middleware stack.

Provides:
  - Request ID generation/propagation (correlation IDs)
  - Request timing with structured logging
  - In-memory rate limiting for auth endpoints
  - Security headers (HSTS, X-Content-Type-Options, X-Frame-Options)

Design decisions (from observability-and-instrumentation skill):
  - Every response includes X-Request-ID for end-to-end correlation
  - Timing is logged as structured JSON with event name + numeric fields
  - Rate limiting uses a sliding-window counter per IP, not a heavyweight
    dependency — sufficient for a single-instance hackathon deployment
"""
import time
import uuid
import logging
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("carbonkisan")


# ─── Request ID ───

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Generates or propagates an X-Request-ID header on every request/response.
    Enables correlation across logs, traces, and downstream services.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        # Store on request state so handlers can access it
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ─── Request Timing ───

class TimingMiddleware(BaseHTTPMiddleware):
    """
    Logs every request with method, path, status code, and duration in ms.
    Uses structured fields (not string interpolation) per observability skill.
    """
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        request_id = getattr(request.state, "request_id", "unknown")
        logger.info(
            "request_completed",
            extra={
                "event": "request_completed",
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
            },
        )
        # Also set the timing header for client-side debugging
        response.headers["X-Response-Time"] = f"{duration_ms}ms"
        return response


# ─── Rate Limiting (auth endpoints only) ───

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Sliding-window rate limiter for auth endpoints.
    PRD §7.1 requires 3 OTP requests per phone per 10 minutes.
    This middleware applies a broader per-IP limit on all /auth/ paths
    to prevent brute-force attacks.

    Design: in-memory dict, no Redis needed for single-instance deployment.
    Entries are lazily cleaned on access. Not suitable for multi-instance
    deployments — swap for Redis-backed slowapi in that case.
    """
    def __init__(self, app, max_requests: int = 20, window_seconds: int = 600):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Only rate-limit auth endpoints
        if not request.url.path.startswith("/auth/"):
            return await call_next(request)

        # GET endpoints like /auth/districts are read-only, don't rate-limit
        if request.method == "GET":
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        cutoff = now - self.window_seconds

        # Clean old entries and count
        hits = self._hits[client_ip]
        self._hits[client_ip] = [t for t in hits if t > cutoff]
        hits = self._hits[client_ip]

        if len(hits) >= self.max_requests:
            logger.warning(
                "rate_limit_exceeded",
                extra={
                    "event": "rate_limit_exceeded",
                    "client_ip": client_ip,
                    "path": request.url.path,
                    "limit": self.max_requests,
                    "window_seconds": self.window_seconds,
                },
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Too many requests. Try again in {self.window_seconds // 60} minutes.",
                    }
                },
            )

        hits.append(now)
        return await call_next(request)


# ─── Security Headers ───

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Sets security headers on every response.
    From security-and-hardening skill: HSTS, content-type sniffing,
    clickjacking, and XSS protection headers.
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        # HSTS only in production (not localhost)
        if request.url.hostname not in ("localhost", "127.0.0.1"):
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"

        return response
