from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ProfileCreate, ProfileResponse, ParcelCreate, ParcelResponse
from app.models.db import supabase
from app.deps import get_current_farmer
import uuid

router = APIRouter()

@router.post("/profiles", response_model=ProfileResponse)
async def create_profile(payload: ProfileCreate, farmer_id: str = Depends(get_current_farmer)):
    # Check if farmer exists
    farmers = supabase.table("farmers").select("*").eq("id", farmer_id).execute().data
    if not farmers:
        raise HTTPException(status_code=404, detail={"code": "FARMER_NOT_FOUND", "message": "Farmer account not found"})
    
    result = supabase.table("farmers").update({
        "full_name": payload.full_name,
        "district_code": payload.district_code,
        "village": payload.village,
        "preferred_language": payload.preferred_language,
        "profile_complete": True,
    }).eq("id", farmer_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=500, detail={"code": "UPDATE_FAILED", "message": "Failed to update profile"})
        
    return result.data[0]


@router.get("/profiles/me", response_model=ProfileResponse)
async def get_profile(farmer_id: str = Depends(get_current_farmer)):
    farmers = supabase.table("farmers").select("*").eq("id", farmer_id).execute().data
    if not farmers:
        raise HTTPException(status_code=404, detail={"code": "FARMER_NOT_FOUND", "message": "Farmer account not found"})
    return farmers[0]


@router.post("/profiles/parcels", response_model=ParcelResponse)
async def add_parcel(payload: ParcelCreate, farmer_id: str = Depends(get_current_farmer)):
    result = supabase.table("parcels").insert({
        "farmer_id": farmer_id,
        "area_ha": payload.area_ha,
        "primary_crop": payload.primary_crop,
        "soil_type": payload.soil_type,
        "district_code": payload.district_code,
    }).execute()
    
    return result.data[0]

@router.get("/profiles/parcels", response_model=List[ParcelResponse])
async def list_parcels(farmer_id: str = Depends(get_current_farmer)):
    result = supabase.table("parcels").select("*").eq("farmer_id", farmer_id).execute()
    return result.data
