import hashlib
import uuid
import logging
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

logger = logging.getLogger("carbonkisan")

METHODOLOGY_VERSION = "ck_v1_2026"


def generate_certificate(
    farmer_district: str,
    practice_type: str,
    co2e_tonnes: float,
    buyer_org: str,
    transaction_id: str,
) -> tuple[bytes, str, str]:
    """Returns (pdf_bytes, certificate_id, record_hash)."""
    certificate_id = str(uuid.uuid4())
    raw = f"{certificate_id}|{farmer_district}|{practice_type}|{co2e_tonnes}|{transaction_id}"
    record_hash = hashlib.sha256(raw.encode()).hexdigest()

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Better branding and styling
    c.setFillColor(colors.HexColor("#064E3B"))  # Emerald 900
    c.setFont("Helvetica-Bold", 24)
    c.drawString(20 * mm, height - 30 * mm, "CarbonKisan Verified Certificate")

    c.setFillColor(colors.HexColor("#047857"))  # Emerald 600
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 42 * mm, "Carbon Credit Retirement Record")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    
    y = height - 60 * mm
    
    details = [
        ("Certificate ID", certificate_id),
        ("Buyer Organisation", buyer_org),
        ("Sourcing District", farmer_district),
        ("Agricultural Practice", practice_type.replace("_", " ").title()),
        ("Carbon Offset", f"{co2e_tonnes} tonnes CO2e"),
        ("Methodology", METHODOLOGY_VERSION),
        ("Cryptographic Hash", record_hash),
    ]

    for label, value in details:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20 * mm, y, f"{label}:")
        c.setFont("Helvetica", 11)
        # Shift value to the right to align
        c.drawString(70 * mm, y, str(value))
        y -= 10 * mm

    y -= 10 * mm
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.HexColor("#4B5563"))  # Gray 600
    c.drawString(20 * mm, y, "This certificate confirms the permanent retirement of the listed carbon credits.")
    
    y -= 8 * mm
    c.drawString(20 * mm, y, f"Verify authenticity at: https://carbonkisan.vercel.app/verify/{certificate_id}")

    c.showPage()
    c.save()
    
    logger.info(
        "certificate_generated",
        extra={"event": "certificate_generated", "certificate_id": certificate_id, "buyer_org": buyer_org}
    )

    buffer.seek(0)
    return buffer.read(), certificate_id, record_hash
