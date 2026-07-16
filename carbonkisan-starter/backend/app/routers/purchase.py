"""
Purchase flow — initiation, confirmation, and webhook handling.

Security-critical module: Razorpay signature verification MUST pass
before any listing is marked sold or any transaction is recorded.
Idempotency check prevents double-processing from webhook + client callback.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import PurchaseInitiateRequest, PurchaseConfirmRequest
from app.models.db import supabase
from app.services.razorpay_client import create_order, verify_payment_signature
from app.services.pdf_generator import generate_certificate
from app.services.notifications import send_sms
from app.config import settings
from app.deps import get_current_buyer

logger = logging.getLogger("carbonkisan")

router = APIRouter()

# In-memory mapping of razorpay_order_id -> listing_id for mock mode.
# In production, this mapping lives in the Razorpay order's `receipt` field.
_order_to_listing: dict[str, str] = {}


@router.post("/purchase/initiate")
async def initiate_purchase(payload: PurchaseInitiateRequest, buyer_id: str = Depends(get_current_buyer)):
    """
    Step 1: Buyer selects a listing → we create a Razorpay order.
    Returns the order details the frontend needs to open Razorpay Checkout.
    """
    listing = (
        supabase.table("listings")
        .select("*, estimates(*), farmers(full_name, district_code)")
        .eq("id", payload.listing_id)
        .eq("status", "live")
        .single()
        .execute()
    )
    if not listing.data:
        raise HTTPException(
            status_code=404,
            detail={"code": "LISTING_UNAVAILABLE", "message": "Listing not found or already sold"},
        )

    order = create_order(
        amount_inr=listing.data["asking_price_inr"],
        receipt=f"listing_{payload.listing_id}",
    )

    # Store the order-to-listing mapping for confirmation
    _order_to_listing[order["id"]] = payload.listing_id

    logger.info(
        "purchase_initiated",
        extra={
            "event": "purchase_initiated",
            "listing_id": payload.listing_id,
            "order_id": order["id"],
            "buyer_id": buyer_id,
            "amount_inr": listing.data["asking_price_inr"],
        },
    )

    return {
        "razorpay_order_id": order["id"],
        "amount": order["amount"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    }


@router.post("/purchase/confirm")
async def confirm_purchase(payload: PurchaseConfirmRequest, buyer_id: str = Depends(get_current_buyer)):
    """
    Step 2: Frontend sends back the Razorpay callback data.
    We verify the HMAC signature, record the transaction, generate
    a certificate, and notify the farmer.
    """
    # Step 1 — Cryptographic proof this payment is real. Non-negotiable.
    if not verify_payment_signature(
        payload.razorpay_order_id,
        payload.razorpay_payment_id,
        payload.razorpay_signature,
    ):
        logger.warning(
            "payment_signature_invalid",
            extra={
                "event": "payment_signature_invalid",
                "order_id": payload.razorpay_order_id,
                "buyer_id": buyer_id,
            },
        )
        raise HTTPException(
            status_code=400,
            detail={"code": "SIGNATURE_INVALID", "message": "Payment could not be verified"},
        )

    # Step 2 — Idempotency check. Webhooks and client callbacks can both
    # fire for the same payment; without this check we'd double-process.
    existing = (
        supabase.table("transactions")
        .select("id")
        .eq("razorpay_payment_id", payload.razorpay_payment_id)
        .execute()
    )
    if existing.data:
        raise HTTPException(
            status_code=409,
            detail={"code": "DUPLICATE_PAYMENT", "message": "This payment was already processed"},
        )

    # Step 3 — Resolve the listing from the order mapping
    listing_id = _order_to_listing.get(payload.razorpay_order_id)
    if not listing_id:
        # Fallback: try to extract from the receipt field format
        listing_id = payload.razorpay_order_id  # best effort

    listing = (
        supabase.table("listings")
        .select("*, estimates(*), farmers(*)")
        .eq("id", listing_id)
        .single()
        .execute()
    )
    if not listing.data:
        raise HTTPException(
            status_code=404,
            detail={"code": "LISTING_NOT_FOUND", "message": "Listing not found"},
        )

    # Step 4 — Record the transaction
    price = listing.data["asking_price_inr"]
    platform_fee = round(price * settings.PLATFORM_FEE_PCT)
    farmer_payout = price - platform_fee

    txn = supabase.table("transactions").insert({
        "listing_id": listing.data["id"],
        "buyer_id": buyer_id,
        "razorpay_payment_id": payload.razorpay_payment_id,
        "amount_paid_inr": price,
        "platform_fee_inr": platform_fee,
        "farmer_payout_inr": farmer_payout,
        "payout_status": "pending",
    }).execute()

    # Step 5 — Mark listing as sold
    supabase.table("listings").update({"status": "sold"}).eq("id", listing.data["id"]).execute()

    # Step 6 — Generate certificate
    buyer_org = buyer_id  # In production, look up from buyers table
    buyers = supabase.table("buyers").select("org_name").eq("id", buyer_id).execute().data
    if buyers:
        buyer_org = buyers[0].get("org_name", buyer_id)

    pdf_bytes, certificate_id, record_hash = generate_certificate(
        farmer_district=listing.data.get("farmers", {}).get("district_code", "Unknown"),
        practice_type=listing.data.get("estimates", {}).get("practice_type", "Unknown"),
        co2e_tonnes=listing.data.get("estimates", {}).get("co2e_tonnes", 0),
        buyer_org=buyer_org,
        transaction_id=txn.data[0]["id"],
    )

    supabase.table("certificates").insert({
        "id": certificate_id,
        "transaction_id": txn.data[0]["id"],
        "record_hash": record_hash,
        "pdf_url": f"pending-upload/{certificate_id}.pdf",
        "methodology_version": "ck_v1_2026",
        "status": "active",
        "issued_at": txn.data[0].get("created_at", ""),
    }).execute()

    # Step 7 — Notify farmer
    farmer_phone = listing.data.get("farmers", {}).get("phone", "")
    farmer_lang = listing.data.get("farmers", {}).get("preferred_language", "mr")
    if farmer_phone:
        await send_sms(phone=farmer_phone, template_key="listing_sold", language=farmer_lang)

    # Cleanup order mapping
    _order_to_listing.pop(payload.razorpay_order_id, None)

    logger.info(
        "purchase_confirmed",
        extra={
            "event": "purchase_confirmed",
            "transaction_id": txn.data[0]["id"],
            "certificate_id": certificate_id,
            "listing_id": listing.data["id"],
            "buyer_id": buyer_id,
            "amount_inr": price,
        },
    )

    return {
        "transaction_id": txn.data[0]["id"],
        "certificate_id": certificate_id,
    }
