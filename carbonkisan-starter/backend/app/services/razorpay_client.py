"""
Razorpay integration: order creation, signature verification, payouts.

The signature verification function is the single most important
function in this codebase from a security standpoint. A client-side
"payment successful" callback can be faked by anyone with browser
devtools. The HMAC check below is the ONLY proof that Razorpay's
servers actually processed the payment — never mark a listing 'sold'
without it passing.

Mock mode: when RAZORPAY_KEY_ID contains 'placeholder', all operations
return realistic mock responses. This lets the full purchase flow work
in dev without real Razorpay credentials.
"""
import hmac
import hashlib
import uuid
import logging

from app.config import settings

logger = logging.getLogger("carbonkisan")

_USE_MOCK = "placeholder" in settings.RAZORPAY_KEY_ID


def _get_client():
    """Lazy-load Razorpay client only when real credentials exist."""
    if _USE_MOCK:
        return None
    import razorpay
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_order(amount_inr: int, receipt: str) -> dict:
    """
    Create a Razorpay order. Amounts are always in paise (1 INR = 100 paise).
    In mock mode, returns a fake order with a deterministic ID.
    """
    if _USE_MOCK:
        order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
        logger.info(
            "mock_order_created",
            extra={"event": "mock_order_created", "order_id": order_id, "amount_paise": amount_inr * 100},
        )
        return {
            "id": order_id,
            "amount": amount_inr * 100,
            "currency": "INR",
            "receipt": receipt,
            "status": "created",
        }

    client = _get_client()
    return client.order.create({
        "amount": amount_inr * 100,
        "currency": "INR",
        "receipt": receipt,
        "payment_capture": 1,
    })


def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verify Razorpay payment signature using HMAC-SHA256.

    This is the ONLY server-side proof a payment actually occurred.
    Uses hmac.compare_digest for constant-time comparison to prevent
    timing attacks (security-and-hardening skill).

    In mock mode with "mock_signature", accepts the payment for testing.
    """
    if not signature:
        return False

    # In mock mode, accept a special test signature
    if _USE_MOCK and signature == "mock_signature":
        logger.info(
            "mock_signature_accepted",
            extra={"event": "mock_signature_accepted", "order_id": order_id},
        )
        return True

    generated_signature = hmac.new(
        key=settings.RAZORPAY_KEY_SECRET.encode(),
        msg=f"{order_id}|{payment_id}".encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison — a naive `==` is a timing-attack surface
    return hmac.compare_digest(generated_signature, signature)


def initiate_payout(account_number: str, ifsc: str, amount_inr: int, farmer_name: str) -> dict:
    """
    NOTE: Payouts require RazorpayX, a separate product from standard
    Razorpay Checkout. For the hackathon demo, mock mode returns a
    realistic response shape.
    """
    if _USE_MOCK:
        payout_id = f"pout_mock_{uuid.uuid4().hex[:12]}"
        logger.info(
            "mock_payout_created",
            extra={"event": "mock_payout_created", "payout_id": payout_id, "amount_inr": amount_inr},
        )
        return {
            "id": payout_id,
            "amount": amount_inr * 100,
            "status": "processing",
            "mode": "UPI",
        }

    client = _get_client()
    return client.payout.create({
        "account_number": account_number,
        "fund_account": {
            "account_type": "bank_account",
            "bank_account": {"name": farmer_name, "ifsc": ifsc, "account_number": account_number},
        },
        "amount": amount_inr * 100,
        "currency": "INR",
        "mode": "UPI",
        "purpose": "payout",
    })
