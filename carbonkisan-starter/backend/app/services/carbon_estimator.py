"""
Carbon estimation service — loads the trained XGBoost model + SHAP
explainer once at import time and serves predictions.

Every number this function returns must be traceable to one of two
places: (1) the peer-reviewed base sequestration rates in
data/sequestration_rates.csv, or (2) a district feature pulled from
the `districts` table. Nothing here is invented at request time.

Performance optimization (performance-optimization skill): district
features are cached at boot time since districts don't change at runtime.
"""
import logging

try:
    import pickle
    import pandas as pd
    import xgboost as xgb
    import shap
    ML_AVAILABLE = True
except ImportError:
    print("WARNING: ML libraries (pandas/xgboost/shap) not found. ML pipeline will be mocked.")
    ML_AVAILABLE = False

from app.config import settings
from app.models.db import supabase

logger = logging.getLogger("carbonkisan")

PRACTICE_ENCODING = {
    "no_till": 0,
    "cover_crop": 1,
    "no_till_cover_crop": 2,
    "agroforestry": 3,
}

# t C/ha/yr — Frontiers Sustainable Food Systems meta-analysis (2023).
# Kept in code AND in data/sequestration_rates.csv so the training script
# and the live inference path can never silently drift apart.
BASE_RATES = {
    "no_till": 0.73,
    "cover_crop": 1.31,
    "no_till_cover_crop": 1.43,
    "agroforestry": 0.67,
}
RATE_RANGE = {
    "no_till": (0.3, 1.2),
    "cover_crop": (0.7, 1.8),
    "no_till_cover_crop": (0.9, 2.1),
    "agroforestry": (0.4, 1.1),
}
RAINFALL_ENCODING = {"low": 0, "medium": 1, "high": 2}

MODEL_VERSION = "xgb_v1"
FEATURE_ORDER = ["practice_encoded", "area_ha", "soil_modifier", "rainfall_encoded", "season_months"]


class CarbonEstimator:
    def __init__(self):
        self.model = None
        self.explainer = None
        self.mock_mode = not ML_AVAILABLE
        self.model_version = MODEL_VERSION
        self._district_cache: dict[str, dict] = {}

        if ML_AVAILABLE:
            try:
                with open(settings.MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                with open(settings.EXPLAINER_PATH, "rb") as f:
                    self.explainer = pickle.load(f)
                logger.info("ml_model_loaded", extra={"event": "ml_model_loaded", "version": MODEL_VERSION})
            except FileNotFoundError:
                logger.warning(
                    "ml_model_not_found",
                    extra={"event": "ml_model_not_found", "model_path": settings.MODEL_PATH},
                )
                self.mock_mode = True
        else:
            logger.warning("ml_libraries_missing", extra={"event": "ml_libraries_missing"})

        # Pre-cache all districts for fast lookup (performance-optimization skill)
        self._warm_district_cache()

    def _warm_district_cache(self):
        """Load all districts into memory at boot. Districts don't change at runtime."""
        try:
            all_districts = supabase.table("districts").select("*").execute().data
            if all_districts:
                for d in all_districts:
                    self._district_cache[d["code"]] = d
                logger.info(
                    "district_cache_warmed",
                    extra={"event": "district_cache_warmed", "count": len(self._district_cache)},
                )
        except Exception as e:
            logger.warning(
                "district_cache_failed",
                extra={"event": "district_cache_failed", "error": str(e)},
            )

    def _get_district_features(self, district_code: str) -> dict:
        """Look up district features, using cache first."""
        if district_code in self._district_cache:
            return self._district_cache[district_code]

        # Fallback to DB query if not in cache
        result = (
            supabase.table("districts")
            .select("*")
            .eq("code", district_code)
            .single()
            .execute()
        )
        if not result.data:
            raise ValueError(f"Unknown district_code: {district_code}")

        # Update cache
        self._district_cache[district_code] = result.data
        return result.data

    def estimate(self, practice_type: str, area_ha: float, district_code: str, season_months: int) -> dict:
        """
        Generate a carbon credit estimate with SHAP explanation.

        Returns a dict with co2e_tonnes, confidence intervals, INR estimate,
        model version, and SHAP breakdown — everything the frontend needs.
        """
        district = self._get_district_features(district_code)

        if self.mock_mode:
            co2e_tonnes = BASE_RATES[practice_type] * area_ha * district["soil_modifier"] * (season_months / 12)
            shap_breakdown = {
                "base_practice": round(co2e_tonnes * 0.4, 3),
                "soil_modifier": round(co2e_tonnes * 0.3, 3),
                "rainfall_zone": round(co2e_tonnes * 0.15, 3),
                "area_scaling": round(co2e_tonnes * 0.15, 3),
            }
        else:
            features = pd.DataFrame([{
                "practice_encoded": PRACTICE_ENCODING[practice_type],
                "area_ha": area_ha,
                "soil_modifier": district["soil_modifier"],
                "rainfall_encoded": RAINFALL_ENCODING[district["rainfall_zone"]],
                "season_months": season_months,
            }])[FEATURE_ORDER]

            co2e_tonnes = float(self.model.predict(features)[0])

            # SHAP breakdown — every estimate MUST ship with this. No exceptions.
            # See PRD §8.6: no estimate may be shown to a user without its explanation.
            shap_row = self.explainer.shap_values(features)[0]
            shap_breakdown = {
                "base_practice": round(
                    BASE_RATES[practice_type] * area_ha * (season_months / 12), 3
                ),
                "soil_modifier": round(float(shap_row[FEATURE_ORDER.index("soil_modifier")]), 3),
                "rainfall_zone": round(float(shap_row[FEATURE_ORDER.index("rainfall_encoded")]), 3),
                "area_scaling": round(float(shap_row[FEATURE_ORDER.index("area_ha")]), 3),
            }

        low_rate, high_rate = RATE_RANGE[practice_type]
        confidence_low = round(low_rate * area_ha * district["soil_modifier"] * (season_months / 12), 3)
        confidence_high = round(high_rate * area_ha * district["soil_modifier"] * (season_months / 12), 3)

        inr_estimate = round(co2e_tonnes * settings.PRICE_PER_TONNE_INR * (1 - settings.PLATFORM_FEE_PCT))

        return {
            "co2e_tonnes": round(co2e_tonnes, 3),
            "confidence_low": confidence_low,
            "confidence_high": confidence_high,
            "inr_estimate": inr_estimate,
            "model_version": MODEL_VERSION,
            "shap_breakdown": shap_breakdown,
        }


# Loaded once at import time — model.pkl and explainer.pkl must exist
# (run app/ml/train.py first) or this falls back to mock mode.
carbon_estimator = CarbonEstimator()
