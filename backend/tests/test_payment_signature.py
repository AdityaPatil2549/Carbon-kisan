"""
Tests for the single most security-critical function in the codebase.
Run: pytest tests/test_payment_signature.py -v
"""
import hmac
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test-key")
os.environ.setdefault("RAZORPAY_KEY_ID", "rzp_test_dummy")
os.environ.setdefault("RAZORPAY_KEY_SECRET", "test_secret_key")

from app.services.razorpay_client import verify_payment_signature


def _sign(order_id: str, payment_id: str, secret: str) -> str:
    return hmac.new(
        key=secret.encode(),
        msg=f"{order_id}|{payment_id}".encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()


def test_valid_signature_passes():
    secret = "test_secret_key"
    order_id, payment_id = "order_ABC123", "pay_XYZ789"
    signature = _sign(order_id, payment_id, secret)
    assert verify_payment_signature(order_id, payment_id, signature) is True


def test_tampered_signature_fails():
    order_id, payment_id = "order_ABC123", "pay_XYZ789"
    fake_signature = "0" * 64
    assert verify_payment_signature(order_id, payment_id, fake_signature) is False


def test_signature_for_different_order_fails():
    secret = "test_secret_key"
    real_signature = _sign("order_ABC123", "pay_XYZ789", secret)
    # attacker reuses a valid signature against a different (higher-value) order
    assert verify_payment_signature("order_DIFFERENT", "pay_XYZ789", real_signature) is False


def test_empty_signature_fails():
    assert verify_payment_signature("order_ABC123", "pay_XYZ789", "") is False
