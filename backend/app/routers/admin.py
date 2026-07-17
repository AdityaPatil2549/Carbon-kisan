from fastapi import APIRouter, Depends, HTTPException
from app.models.db import supabase
from app.deps import get_current_admin

router = APIRouter()


@router.get("/queue")
async def review_queue(admin_id: str = Depends(get_current_admin)):
    result = supabase.table("listings").select("*, estimates(*)").eq("status", "pending_verification").execute()
    return result.data


@router.post("/listings/{listing_id}/approve")
async def approve_listing(listing_id: str, admin_id: str = Depends(get_current_admin)):
    result = supabase.table("listings").update({"status": "live"}).eq("id", listing_id).execute()
    supabase.table("admin_audit_log").insert({
        "admin_id": admin_id, "action": "listing_approved", "target_id": listing_id,
    }).execute()
    return {"status": "live"}


@router.post("/listings/{listing_id}/reject")
async def reject_listing(listing_id: str, reason: str, admin_id: str = Depends(get_current_admin)):
    if not reason:
        raise HTTPException(status_code=400, detail={"code": "REASON_REQUIRED", "message": "Rejection reason is required"})
    supabase.table("listings").update({"status": "rejected", "rejection_reason": reason}).eq("id", listing_id).execute()
    supabase.table("admin_audit_log").insert({
        "admin_id": admin_id, "action": "listing_rejected", "target_id": listing_id, "reason": reason,
    }).execute()
    return {"status": "rejected"}
