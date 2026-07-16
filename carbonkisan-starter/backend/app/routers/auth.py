"""
Auth router — handles farmer OTP, buyer email auth, and admin auth.
In dev mode with mock DB, simulates auth without real Supabase calls.

Security (security-and-hardening skill): OTP verification uses fixed
code in dev. Production proxies to Supabase phone auth with Twilio.
"""
import uuid
import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import OtpRequest, OtpVerify, BuyerRegister, BuyerLogin
from app.models.db import supabase
from app.config import settings

logger = logging.getLogger("carbonkisan")

router = APIRouter()

# In-memory OTP store for dev mode (production uses Supabase Auth)
_dev_otps: dict = {}


@router.post("/auth/otp/request")
async def request_otp(payload: OtpRequest):
    """Send OTP to farmer's phone number."""
    if settings.use_mock_db:
        _dev_otps[payload.phone] = "123456"
        logger.info(
            "otp_requested_dev",
            extra={"event": "otp_requested_dev", "phone_last4": payload.phone[-4:]},
        )
        return {"message": "OTP sent", "dev_hint": "Use 123456 in dev mode"}

    # Production: proxy to Supabase phone auth
    try:
        client = supabase
        client.auth.sign_in_with_otp({"phone": f"+91{payload.phone}"})
        return {"message": "OTP sent"}
    except Exception as e:
        logger.error("otp_request_failed", extra={"event": "otp_request_failed", "error": str(e)})
        raise HTTPException(status_code=500, detail={"code": "OTP_FAILED", "message": str(e)})


@router.post("/auth/otp/verify")
async def verify_otp(payload: OtpVerify):
    """Verify OTP and return auth token + farmer profile."""
    if settings.use_mock_db:
        stored = _dev_otps.get(payload.phone)
        if stored != payload.otp:
            raise HTTPException(status_code=401, detail={"code": "INVALID_OTP", "message": "Invalid OTP"})

        # Check if farmer already exists
        farmers = supabase.table("farmers").select("*").eq("phone", payload.phone).execute().data
        if farmers:
            farmer = farmers[0]
        else:
            # Create new farmer record
            farmer_id = str(uuid.uuid4())
            farmer = {
                "id": farmer_id,
                "phone": payload.phone,
                "full_name": "",
                "district_code": "",
                "profile_complete": False,
                "preferred_language": "mr",
            }
            supabase.table("farmers").insert(farmer).execute()
            logger.info(
                "farmer_created",
                extra={"event": "farmer_created", "farmer_id": farmer_id},
            )

        # Clean up OTP
        _dev_otps.pop(payload.phone, None)

        return {
            "access_token": f"dev_farmer_{farmer['id']}",
            "user": {
                "id": farmer["id"],
                "phone": payload.phone,
                "role": "farmer",
                "profile_complete": farmer.get("profile_complete", False),
            },
        }

    # Production: verify with Supabase
    try:
        client = supabase
        response = client.auth.verify_otp({
            "phone": f"+91{payload.phone}",
            "token": payload.otp,
            "type": "sms",
        })
        return {
            "access_token": response.session.access_token,
            "user": {
                "id": response.user.id,
                "phone": payload.phone,
                "role": response.user.user_metadata.get("role", "farmer"),
            },
        }
    except Exception:
        raise HTTPException(status_code=401, detail={"code": "INVALID_OTP", "message": "Invalid OTP"})


@router.post("/auth/buyer/register")
async def buyer_register(payload: BuyerRegister):
    """Register a new buyer organization."""
    if settings.use_mock_db:
        # Check for duplicate email
        existing = supabase.table("buyers").select("id").eq("email", payload.email).execute().data
        if existing:
            raise HTTPException(
                status_code=409,
                detail={"code": "EMAIL_EXISTS", "message": "A buyer with this email already exists"},
            )

        buyer_id = str(uuid.uuid4())
        supabase.table("buyers").insert({
            "id": buyer_id,
            "email": payload.email,
            "org_name": payload.org_name,
            "contact_name": payload.contact_name,
        }).execute()
        logger.info(
            "buyer_registered",
            extra={"event": "buyer_registered", "buyer_id": buyer_id, "org_name": payload.org_name},
        )
        return {
            "access_token": f"dev_buyer_{buyer_id}",
            "user": {
                "id": buyer_id,
                "email": payload.email,
                "role": "buyer",
                "org_name": payload.org_name,
            },
        }

    # Production: sign up via Supabase Auth
    try:
        client = supabase
        response = client.auth.sign_up({
            "email": payload.email,
            "password": payload.password,
            "options": {
                "data": {
                    "role": "buyer",
                    "org_name": payload.org_name,
                    "contact_name": payload.contact_name,
                },
            },
        })
        client.table("buyers").insert({
            "id": response.user.id,
            "email": payload.email,
            "org_name": payload.org_name,
            "contact_name": payload.contact_name,
        }).execute()
        return {
            "access_token": response.session.access_token if response.session else None,
            "user": {"id": response.user.id, "email": payload.email, "role": "buyer"},
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "REGISTRATION_FAILED", "message": str(e)})


@router.post("/auth/buyer/login")
async def buyer_login(payload: BuyerLogin):
    """Authenticate buyer with email/password."""
    if settings.use_mock_db:
        buyers = supabase.table("buyers").select("*").eq("email", payload.email).execute().data
        if buyers:
            buyer = buyers[0]
            return {
                "access_token": f"dev_buyer_{buyer['id']}",
                "user": {"id": buyer["id"], "email": payload.email, "role": "buyer"},
            }
        raise HTTPException(status_code=401, detail={"code": "LOGIN_FAILED", "message": "Invalid credentials"})

    # Production: sign in via Supabase Auth
    try:
        client = supabase
        response = client.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
        return {
            "access_token": response.session.access_token,
            "user": {"id": response.user.id, "email": payload.email, "role": "buyer"},
        }
    except Exception:
        raise HTTPException(status_code=401, detail={"code": "LOGIN_FAILED", "message": "Invalid credentials"})


@router.post("/auth/admin/login")
async def admin_login():
    """
    Dev-only admin login. In production, admin auth goes through
    Supabase Auth with the admin role set in user metadata.
    """
    if not settings.use_mock_db:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Not available in production"})

    admin_id = str(uuid.uuid4())
    logger.info("admin_login_dev", extra={"event": "admin_login_dev", "admin_id": admin_id})
    return {
        "access_token": f"dev_admin_{admin_id}",
        "user": {"id": admin_id, "role": "admin"},
    }


@router.get("/auth/districts")
async def get_districts():
    """Public endpoint — returns all districts for dropdown menus."""
    result = supabase.table("districts").select("*").execute()
    return result.data
