from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import EstimateRequest, EstimateResponse
from app.models.db import supabase
from app.services.carbon_estimator import carbon_estimator
from app.deps import get_current_farmer

router = APIRouter()


@router.post("/estimate", response_model=EstimateResponse)
async def create_estimate(payload: EstimateRequest, farmer_id: str = Depends(get_current_farmer)):
    try:
        result = carbon_estimator.estimate(
            practice_type=payload.practice_type,
            area_ha=payload.area_ha,
            district_code=payload.district_code,
            season_months=payload.season_months,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": "INVALID_DISTRICT", "message": str(e)})

    insert_result = supabase.table("estimates").insert({
        "farmer_id": farmer_id,
        "practice_type": payload.practice_type,
        "area_ha": payload.area_ha,
        "season_months": payload.season_months,
        "parcel_id": payload.parcel_id,
        "co2e_tonnes": result["co2e_tonnes"],
        "confidence_low": result["confidence_low"],
        "confidence_high": result["confidence_high"],
        "inr_estimate": result["inr_estimate"],
        "shap_breakdown": result["shap_breakdown"],
        "model_version": result["model_version"],
    }).execute()

    estimate_id = insert_result.data[0]["id"]
    return EstimateResponse(estimate_id=estimate_id, **result)

from pydantic import BaseModel, Field
class LocalEstimateRequest(BaseModel):
    practice_type: str
    area_ha: float
    season_months: int
    co2e_tonnes: float
    inr_estimate: int
    shap_breakdown: dict

@router.post("/estimate/local")
async def save_local_estimate(payload: LocalEstimateRequest, farmer_id: str = Depends(get_current_farmer)):
    """Saves a client-side calculated estimate to the DB and returns the ID."""
    insert_result = supabase.table("estimates").insert({
        "farmer_id": farmer_id,
        "practice_type": payload.practice_type,
        "area_ha": payload.area_ha,
        "season_months": payload.season_months,
        "co2e_tonnes": payload.co2e_tonnes,
        "confidence_low": payload.co2e_tonnes * 0.9,
        "confidence_high": payload.co2e_tonnes * 1.1,
        "inr_estimate": payload.inr_estimate,
        "shap_breakdown": payload.shap_breakdown,
        "model_version": "client_xgb_v1",
    }).execute()

    return {"estimate_id": insert_result.data[0]["id"]}

