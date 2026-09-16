"""
MEA Apostille & Cross-Border Document Vault Engine
High-Volume National Service with Premium Logistics Moat
"""

from typing import Dict, List, Any
import uuid
from datetime import datetime

class ApostilleVaultEngine:
    """
    Manages the multi-tier physical and digital authentication pipeline:
    Home Dept / HRD -> MEA Apostille -> Embassy Legalization.
    """

    DESTINATIONS = {
        "usa": {"type": "hague_apostille", "embassy_required": False, "base_fee": 4999},
        "uk": {"type": "hague_apostille", "embassy_required": False, "base_fee": 4999},
        "germany": {"type": "hague_apostille", "embassy_required": False, "base_fee": 4999},
        "uae": {"type": "embassy_legalization", "embassy_required": True, "base_fee": 9499},
        "qatar": {"type": "embassy_legalization", "embassy_required": True, "base_fee": 8999},
        "kuwait": {"type": "embassy_legalization", "embassy_required": True, "base_fee": 8999},
    }

    @classmethod
    def create_consignment(cls, user_id: str, document_names: List[str], destination_country: str) -> Dict[str, Any]:
        dest_info = cls.DESTINATIONS.get(destination_country.lower(), {"type": "embassy_legalization", "embassy_required": True, "base_fee": 8999})
        vault_id = f"VAULT-IN-{uuid.uuid4().hex[:8].upper()}"

        milestones = [
            {"step": 1, "name": "Doorstep Vault Pickup", "status": "PENDING", "location": "Customer Residence"},
            {"step": 2, "name": "University / Institution OCR Verification", "status": "QUEUED", "location": "e-Sanad / Home Univ"},
            {"step": 3, "name": "State Secretariat (HRD/Home) Attestation", "status": "QUEUED", "location": "State Capital Hub"},
            {"step": 4, "name": "MEA Apostille / Authentication", "status": "QUEUED", "location": "MEA CPV Division, New Delhi"}
        ]

        if dest_info["embassy_required"]:
            milestones.append({
                "step": 5, "name": f"{destination_country.upper()} Embassy Legalization", "status": "QUEUED", "location": "Chanakyapuri, New Delhi"
            })

        milestones.append({
            "step": len(milestones) + 1, "name": "Insured Return Delivery", "status": "QUEUED", "location": "Customer Residence"
        })

        return {
            "vault_consignment_id": vault_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "documents": document_names,
            "destination_country": destination_country.upper(),
            "compliance_type": dest_info["type"],
            "insurance_guarantee_inr": 100_000,
            "pricing_inr": dest_info["base_fee"],
            "pipeline_milestones": milestones
        }
