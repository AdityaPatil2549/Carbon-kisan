"""
CarbonKisan — Authentication dependencies.

FastAPI Depends() guards that extract and validate the current user
from the Authorization header. Supports both dev tokens (mock mode)
and production Supabase JWTs.

Security note (security-and-hardening skill): these guards are the
authorization boundary. Every protected endpoint MUST use one of these
dependencies — never bypass them. Dev tokens use a strict format to
prevent injection.
"""
import re
import logging
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

logger = logging.getLogger("carbonkisan")

security = HTTPBearer(auto_error=False)

# Dev token patterns — strict regex prevents injection
_DEV_FARMER_PATTERN = re.compile(r"^dev_farmer_[0-9a-f\-]{36}$")
_DEV_BUYER_PATTERN = re.compile(r"^dev_buyer_[0-9a-f\-]{36}$")
_DEV_ADMIN_PATTERN = re.compile(r"^dev_admin_[0-9a-f\-]{36}$")


def _extract_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    """Extract and validate the bearer token, raising 401 if missing."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail={"code": "UNAUTHORIZED", "message": "Authentication required"},
        )
    return credentials.credentials


async def get_current_farmer(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """Returns farmer_id. Raises 401/403 if not authenticated as a farmer."""
    token = _extract_token(credentials)

    if settings.use_mock_db:
        if not _DEV_FARMER_PATTERN.match(token):
            raise HTTPException(
                status_code=403,
                detail={"code": "FORBIDDEN", "message": "Not authorized as a farmer"},
            )
        farmer_id = token.replace("dev_farmer_", "")
        return farmer_id

    # Production: verify Supabase JWT
    from app.models.db import supabase
    try:
        user = supabase.auth.get_user(token)
        role = user.user.user_metadata.get("role", "")
        if role != "farmer":
            raise HTTPException(
                status_code=403,
                detail={"code": "FORBIDDEN", "message": "Farmer role required"},
            )
        return user.user.id
    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )


async def get_current_buyer(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """Returns buyer_id. Raises 401/403 if not authenticated as a buyer."""
    token = _extract_token(credentials)

    if settings.use_mock_db:
        if not _DEV_BUYER_PATTERN.match(token):
            raise HTTPException(
                status_code=403,
                detail={"code": "FORBIDDEN", "message": "Not authorized as a buyer"},
            )
        buyer_id = token.replace("dev_buyer_", "")
        return buyer_id

    from app.models.db import supabase
    try:
        user = supabase.auth.get_user(token)
        role = user.user.user_metadata.get("role", "")
        if role != "buyer":
            raise HTTPException(
                status_code=403,
                detail={"code": "FORBIDDEN", "message": "Buyer role required"},
            )
        return user.user.id
    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """Returns admin_id. Raises 401/403 if not authenticated as an admin."""
    token = _extract_token(credentials)

    if settings.use_mock_db:
        if not _DEV_ADMIN_PATTERN.match(token):
            raise HTTPException(
                status_code=403,
                detail={"code": "FORBIDDEN", "message": "Admin role required"},
            )
        admin_id = token.replace("dev_admin_", "")
        return admin_id

    from app.models.db import supabase
    try:
        user = supabase.auth.get_user(token)
        role = user.user.user_metadata.get("role", "")
        if role != "admin":
            raise HTTPException(
                status_code=403,
                detail={"code": "FORBIDDEN", "message": "Admin role required"},
            )
        return user.user.id
    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )
