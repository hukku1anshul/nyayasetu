"""
Web & Mobile Browser Lead Intake Engine
Handles direct online web intake forms, document OCR parsing, and instant docket generation.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class WebLeadIntakePayload(BaseModel):
    service_type: str = Field(..., description="'GAZETTE_NAME_CHANGE', 'UNCLAIMED_WEALTH', 'MEA_APOSTILLE'")
    applicant_full_name: str
    contact_phone: str
    contact_email: str
    state: str
    city: str
    
    # Gazette specific
    old_name: Optional[str] = None
    new_name: Optional[str] = None
    father_or_spouse_name: Optional[str] = None
    
    # Wealth specific
    deceased_holder_name: Optional[str] = None
    company_name: Optional[str] = None
    folio_number: Optional[str] = None
    estimated_shares_count: Optional[int] = None

    # Apostille specific
    destination_country: Optional[str] = None
    document_types: Optional[List[str]] = None


class WebIntakeEngine:
    """
    Validates and stores web/mobile onboarding leads, assigning unique dockets
    and triggering automated downstream workflows.
    """
    ACTIVE_DOCKETS: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def process_web_intake(cls, payload: WebLeadIntakePayload) -> Dict[str, Any]:
        prefix = "NS-WEB"
        if payload.service_type == "GAZETTE_NAME_CHANGE":
            prefix = "NS-GAZ"
        elif payload.service_type == "UNCLAIMED_WEALTH":
            prefix = "NS-IEPF"
        elif payload.service_type == "MEA_APOSTILLE":
            prefix = "NS-APOS"

        docket_id = f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

        docket_record = {
            "docket_id": docket_id,
            "created_at": datetime.now().isoformat(),
            "service_type": payload.service_type,
            "applicant": payload.applicant_full_name,
            "phone": payload.contact_phone,
            "email": payload.contact_email,
            "state": payload.state,
            "city": payload.city,
            "status": "DOCKET_CREATED",
            "next_action": "Awaiting Identity Sign-off",
            "payload_data": payload.model_dump()
        }

        cls.ACTIVE_DOCKETS[docket_id] = docket_record

        return {
            "status": "SUCCESS",
            "docket_id": docket_id,
            "message": f"Lead intake successfully processed. Case #{docket_id} is active.",
            "tracking_url": f"https://nyayasetu.in/track/{docket_id}",
            "docket_details": docket_record
        }

    @classmethod
    def get_docket_status(cls, docket_id: str) -> Optional[Dict[str, Any]]:
        return cls.ACTIVE_DOCKETS.get(docket_id.upper())
