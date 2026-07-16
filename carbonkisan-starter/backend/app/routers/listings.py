from typing import Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.schemas import ListingCreateRequest
from app.models.db import supabase
from app.deps import get_current_farmer

logger = logging.getLogger("carbonkisan")

router = APIRouter()


@router.post("/listings")
async def create_listing(payload: ListingCreateRequest, farmer_id: str = Depends(get_current_farmer)):
    estimate = (
        supabase.table("estimates").select("*").eq("id", payload.estimate_id).single().execute()
    )
    if not estimate.data:
        raise HTTPException(
            status_code=404,
            detail={"code": "ESTIMATE_NOT_FOUND", "message": "Estimate does not exist"},
        )
    
    # Check if a listing already exists for this estimate
    existing = supabase.table("listings").select("id").eq("estimate_id", payload.estimate_id).execute()
    if existing.data:
        raise HTTPException(
            status_code=409,
            detail={"code": "LISTING_EXISTS", "message": "A listing already exists for this estimate"},
        )

    suggested = estimate.data["inr_estimate"]
    if not (suggested * 0.6 <= payload.asking_price_inr <= suggested * 1.4):
        raise HTTPException(status_code=400, detail={
            "code": "PRICE_OUT_OF_BAND",
            "message": f"Asking price must be within 40% of the suggested price (₹{suggested})",
            "field": "asking_price_inr",
        })

    result = supabase.table("listings").insert({
        "estimate_id": payload.estimate_id,
        "farmer_id": farmer_id,
        "asking_price_inr": payload.asking_price_inr,
        "status": "live",
        "published_at": "now()",
    }).execute()

    logger.info("listing_created", extra={"event": "listing_created", "listing_id": result.data[0]["id"]})

    return {"listing_id": result.data[0]["id"], "status": result.data[0]["status"]}


@router.get("/listings")
async def browse_listings(
    state: Optional[str] = None,
    district: Optional[str] = None,
    practice: Optional[str] = None,
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
):
    query = supabase.table("listings").select("*, estimates(*), farmers(full_name, district_code)").eq("status", "live")
    if min_price:
        query = query.gte("asking_price_inr", min_price)
    if max_price:
        query = query.lte("asking_price_inr", max_price)

    result = query.execute()
    rows = result.data

    # Manual filtering for joined tables
    if state:
        rows = [r for r in rows if r.get("farmers", {}).get("district_code", "").startswith(f"{state}_")]
    if district:
        rows = [r for r in rows if r.get("farmers", {}).get("district_code") == district]
    if practice:
        rows = [r for r in rows if r.get("estimates", {}).get("practice_type") == practice]

    return rows


@router.get("/listings/{listing_id}")
async def get_listing(listing_id: str):
    """Get a specific listing by ID with full details."""
    result = supabase.table("listings").select("*, estimates(*), farmers(full_name, district_code, village)").eq("id", listing_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": "LISTING_NOT_FOUND", "message": "Listing not found"})
    return result.data


@router.get("/my-listings")
async def my_listings(farmer_id: str = Depends(get_current_farmer)):
    result = supabase.table("listings").select("*, estimates(*)").eq("farmer_id", farmer_id).execute()
    return result.data
