"""
Transactional SMS via MSG91's REST API.

ARCHITECTURE CORRECTION (read this before wiring auth):
Supabase's built-in phone-auth OTP system only supports Twilio,
Twilio Verify, MessageBird, or Vonage as SMS providers. MSG91 is NOT
a native Supabase Auth provider. 
  - Farmer LOGIN OTP  -> Supabase Auth configured with Twilio
  - Transactional SMS -> THIS backend via MSG91's REST API
"""
import httpx
import logging
from app.config import settings

logger = logging.getLogger("carbonkisan")

MSG91_BASE_URL = "https://control.msg91.com/api/v5/flow/"

TEMPLATES = {
    "listing_approved": {
        "mr": "तुमची यादी मंजूर झाली आहे आणि आता विक्रीसाठी उपलब्ध आहे.",
        "hi": "आपकी लिस्टिंग स्वीकृत हो गई है और अब बिक्री के लिए उपलब्ध है।",
        "en": "Your listing has been approved and is now live for sale.",
    },
    "listing_sold": {
        "mr": "अभिनंदन! तुमचे कार्बन क्रेडिट्स विकले गेले आहेत. पेमेंट लवकरच येईल.",
        "hi": "बधाई हो! आपके कार्बन क्रेडिट बिक गए हैं। भुगतान जल्द आएगा।",
        "en": "Congratulations! Your carbon credits have sold. Payout is on its way.",
    },
    "payout_completed": {
        "mr": "तुमचे पेमेंट यशस्वीरित्या पाठवले गेले आहे.",
        "hi": "आपका भुगतान सफलतापूर्वक भेज दिया गया है।",
        "en": "Your payout has been sent successfully.",
    },
}


async def send_sms(phone: str, template_key: str, language: str = "mr") -> bool:
    if not settings.MSG91_AUTH_KEY:
        logger.warning(
            "sms_skipped_no_config",
            extra={"event": "sms_skipped_no_config", "phone_last4": phone[-4:] if phone else "", "template": template_key}
        )
        return False

    message = TEMPLATES[template_key].get(language, TEMPLATES[template_key]["en"])
    payload = {
        "sender": settings.MSG91_SENDER_ID,
        "route": "4",
        "country": "91",
        "sms": [{"message": message, "to": [phone]}],
    }
    headers = {"authkey": settings.MSG91_AUTH_KEY, "content-type": "application/json"}

    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(MSG91_BASE_URL, json=payload, headers=headers, timeout=10.0)
            success = response.status_code == 200
            
            logger.info(
                "sms_dispatched",
                extra={
                    "event": "sms_dispatched", 
                    "phone_last4": phone[-4:] if phone else "", 
                    "template": template_key,
                    "success": success,
                    "status_code": response.status_code
                }
            )
            return success
    except Exception as e:
        logger.error(
            "sms_delivery_failed",
            extra={"event": "sms_delivery_failed", "error": str(e), "phone_last4": phone[-4:] if phone else ""}
        )
        return False
