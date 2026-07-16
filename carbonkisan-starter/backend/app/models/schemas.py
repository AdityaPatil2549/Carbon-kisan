from typing import Literal, Optional, List
from pydantic import BaseModel, Field

PracticeType = Literal["no_till", "cover_crop", "no_till_cover_crop", "agroforestry"]
ListingStatus = Literal["pending_verification", "live", "sold", "expired", "rejected"]


# ─── Estimate ───

class EstimateRequest(BaseModel):
    practice_type: PracticeType
    area_ha: float = Field(..., ge=0.5, le=10, description="Land area in hectares, 0.5-10 for MVP")
    district_code: str
    season_months: Literal[6, 12]
    parcel_id: Optional[str] = None


class ShapBreakdown(BaseModel):
    base_practice: float
    soil_modifier: float
    rainfall_zone: float
    area_scaling: float


class EstimateResponse(BaseModel):
    estimate_id: str
    co2e_tonnes: float
    confidence_low: float
    confidence_high: float
    inr_estimate: int
    model_version: str
    shap_breakdown: ShapBreakdown


# ─── Listings ───

class ListingCreateRequest(BaseModel):
    estimate_id: str
    asking_price_inr: int = Field(..., gt=0)


class ListingSummary(BaseModel):
    id: str
    district_code: str
    district_name: Optional[str] = None
    practice_type: PracticeType
    co2e_tonnes: float
    asking_price_inr: int
    farmer_first_name: str
    status: str


# ─── Purchase ───

class PurchaseInitiateRequest(BaseModel):
    listing_id: str


class PurchaseConfirmRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str


# ─── Auth ───

class OtpRequest(BaseModel):
    phone: str = Field(..., pattern=r"^[6-9]\d{9}$", description="10-digit Indian mobile number")


class OtpVerify(BaseModel):
    phone: str = Field(..., pattern=r"^[6-9]\d{9}$")
    otp: str = Field(..., min_length=6, max_length=6)


class BuyerRegister(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    org_name: str
    contact_name: str


class BuyerLogin(BaseModel):
    email: str
    password: str


# ─── Profile ───

class ProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    district_code: str
    village: Optional[str] = None
    preferred_language: Literal["mr", "hi", "en"] = "mr"


class ProfileResponse(BaseModel):
    id: str
    phone: str
    full_name: str
    district_code: str
    village: Optional[str] = None
    preferred_language: str
    profile_complete: bool


class ParcelCreate(BaseModel):
    area_ha: float = Field(..., gt=0)
    primary_crop: str
    soil_type: str
    district_code: str


class ParcelResponse(BaseModel):
    id: str
    farmer_id: str
    area_ha: float
    primary_crop: str
    soil_type: str
    district_code: str


# ─── Impact ───

class TopDistrict(BaseModel):
    district_code: str
    district_name: str
    total_co2e: float


class ImpactStats(BaseModel):
    total_co2e_listed: float
    total_co2e_sold: float
    total_transactions: int
    total_farmer_income_inr: int
    farmer_count: int
    district_count: int
    top_districts: List[TopDistrict]


# ─── Certificate ───

class CertificateVerifyResponse(BaseModel):
    valid: bool
    certificate_id: Optional[str] = None
    methodology_version: Optional[str] = None
    issued_at: Optional[str] = None
    practice_type: Optional[str] = None
    district_name: Optional[str] = None
    co2e_tonnes: Optional[float] = None
    status: Optional[str] = None


# ─── Errors ───

class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
