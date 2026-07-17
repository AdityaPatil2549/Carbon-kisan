"""
CarbonKisan — Application configuration.

All settings loaded from environment variables with safe defaults for
local development. In production, set via .env or container environment.

Security note (security-and-hardening skill): secrets are never committed
to version control. This file provides only defaults for non-secret values.
"""
import os
from typing import List


class Settings:
    """Centralized settings — single source of truth for all configuration."""

    # ─── Database ───
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # ─── Payment ───
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "rzp_test_placeholder")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "test_secret_placeholder")

    # ─── Platform Economics ───
    PLATFORM_FEE_PCT: float = float(os.getenv("PLATFORM_FEE_PCT", "0.05"))
    PRICE_PER_TONNE_INR: int = int(os.getenv("PRICE_PER_TONNE_INR", "1800"))

    # ─── SMS / Notifications ───
    MSG91_AUTH_KEY: str = os.getenv("MSG91_AUTH_KEY", "")
    MSG91_SENDER_ID: str = os.getenv("MSG91_SENDER_ID", "CKNOTE")

    # ─── ML Model Paths ───
    MODEL_PATH: str = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "ml", "model.pkl"))
    EXPLAINER_PATH: str = os.getenv("EXPLAINER_PATH", os.path.join(os.path.dirname(__file__), "ml", "explainer.pkl"))

    # ─── Logging & Observability ───
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

    # ─── Rate Limiting ───
    RATE_LIMIT_AUTH_MAX: int = int(os.getenv("RATE_LIMIT_AUTH_MAX", "20"))
    RATE_LIMIT_AUTH_WINDOW: int = int(os.getenv("RATE_LIMIT_AUTH_WINDOW", "600"))

    # ─── CORS ───
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost:5185,https://carbon-kisan-six.vercel.app,https://carbon-kisan.vercel.app,https://carbon-kisan-app.vercel.app"
    ).split(",")


    # ─── Derived ───
    @property
    def use_mock_db(self) -> bool:
        """Use in-memory mock when Supabase credentials are not provided."""
        return not (self.SUPABASE_URL and self.SUPABASE_SERVICE_ROLE_KEY)


settings = Settings()
