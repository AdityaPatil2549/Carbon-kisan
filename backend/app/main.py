"""
CarbonKisan — FastAPI application entry point.

Production-grade setup with:
  - Structured JSON logging (observability-and-instrumentation skill)
  - Security middleware stack (security-and-hardening skill)
  - CORS configuration (restricted to known origins)
  - Startup/shutdown lifecycle events
  - Health check endpoint
"""
import logging
import json
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware import (
    RequestIDMiddleware,
    TimingMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)
from app.routers import auth, profiles, estimate, listings, purchase, certificate, impact, admin, vision


# ─── Structured Logging Configuration ───

class StructuredFormatter(logging.Formatter):
    """JSON log formatter — queryable, not prose (observability skill)."""
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Merge extra structured fields from middleware
        if hasattr(record, "event"):
            log_entry["event"] = record.event
        for key in ("method", "path", "status", "duration_ms", "request_id",
                     "client_ip", "limit", "window_seconds"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)
        return json.dumps(log_entry)


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())

    root = logging.getLogger("carbonkisan")
    root.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    root.addHandler(handler)
    root.propagate = False

    # Also capture uvicorn access logs
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.handlers = [handler]


# ─── Lifecycle ───

logger = logging.getLogger("carbonkisan")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle events."""
    configure_logging()
    logger.info(
        "server_starting",
        extra={
            "event": "server_starting",
            "mock_db": settings.use_mock_db,
            "log_level": settings.LOG_LEVEL,
            "platform_fee_pct": settings.PLATFORM_FEE_PCT,
        },
    )

    # Verify ML model is loaded
    try:
        from app.services.carbon_estimator import carbon_estimator
        logger.info(
            "ml_model_loaded",
            extra={
                "event": "ml_model_loaded",
                "model_version": carbon_estimator.model_version,
                "mock_mode": carbon_estimator.model is None,
            },
        )
    except Exception as e:
        logger.warning(
            "ml_model_load_failed",
            extra={"event": "ml_model_load_failed", "error": str(e)},
        )

    yield

    logger.info("server_shutting_down", extra={"event": "server_shutting_down"})


# ─── App Factory ───

app = FastAPI(
    title="CarbonKisan API",
    description="Micro-marketplace for carbon credits — connecting Indian farmers to buyers.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─── Middleware Stack ───
# Order matters: outermost first. Starlette processes them bottom-up
# on request and top-down on response.

# 1. Security headers (outermost — always applied)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Rate limiting on auth endpoints
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.RATE_LIMIT_AUTH_MAX,
    window_seconds=settings.RATE_LIMIT_AUTH_WINDOW,
)

# 3. Request timing
app.add_middleware(TimingMiddleware)

# 4. Request ID (innermost — generates the ID before timing starts)
app.add_middleware(RequestIDMiddleware)

# 5. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Response-Time"],
)


# ─── Routes ───

app.include_router(auth.router, tags=["Auth"])
app.include_router(profiles.router, tags=["Profiles"])
app.include_router(estimate.router, tags=["Estimate"])
app.include_router(listings.router, tags=["Listings"])
app.include_router(purchase.router, tags=["Purchase"])
app.include_router(certificate.router, tags=["Certificate"])
app.include_router(impact.router, tags=["Impact"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(vision.router, tags=["Vision"])


# ─── Health Check ───

@app.get("/health", tags=["System"])
async def health_check():
    """Health check — returns system status and configuration summary."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "mock_db": settings.use_mock_db,
    }


# ─── Dev Server ───

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
