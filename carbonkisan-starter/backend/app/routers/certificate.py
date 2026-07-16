from fastapi import APIRouter, HTTPException
from app.models.db import supabase

router = APIRouter()


@router.get("/certificate/{certificate_id}")
async def get_certificate(certificate_id: str):
    cert = supabase.table("certificates").select("*").eq("id", certificate_id).single().execute()
    if not cert.data:
        raise HTTPException(status_code=404, detail={"code": "CERT_NOT_FOUND", "message": "Certificate not found"})
    return {"pdf_url": cert.data["pdf_url"]}


@router.get("/verify/{certificate_id}")
async def verify_certificate(certificate_id: str):
    """Public endpoint — no auth, no farmer/buyer PII in the response."""
    cert = (
        supabase.table("certificates")
        .select("*")
        .eq("id", certificate_id)
        .single()
        .execute()
    )
    if not cert.data:
        return {"valid": False}
        
    row = cert.data
    
    # Try to enrich with transaction/listing data if possible
    practice_type = None
    district_code = None
    co2e_tonnes = None
    
    if row.get("transaction_id"):
        txn = supabase.table("transactions").select("*").eq("id", row["transaction_id"]).single().execute()
        if txn.data and txn.data.get("listing_id"):
            listing = supabase.table("listings").select("*, estimates(*), farmers(district_code)").eq("id", txn.data["listing_id"]).single().execute()
            if listing.data:
                practice_type = listing.data.get("estimates", {}).get("practice_type")
                co2e_tonnes = listing.data.get("estimates", {}).get("co2e_tonnes")
                district_code = listing.data.get("farmers", {}).get("district_code")

    district_name = None
    if district_code:
        dist = supabase.table("districts").select("name").eq("code", district_code).single().execute()
        if dist.data:
            district_name = dist.data.get("name")

    return {
        "valid": row.get("status") == "active",
        "certificate_id": row.get("id"),
        "methodology_version": row.get("methodology_version"),
        "issued_at": row.get("issued_at"),
        "practice_type": practice_type,
        "district_name": district_name,
        "co2e_tonnes": co2e_tonnes,
        "status": row.get("status")
    }
