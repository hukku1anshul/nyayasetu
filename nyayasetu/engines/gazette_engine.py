"""
Central Gazette & Name Rectification Engine
High-Volume National Micro-Service (₹3,499 Flat Fee, >60% Margin)
"""

from typing import Dict, Any
from datetime import datetime

class GazetteEngine:
    """
    Automates the 3-step Gazette Notification and Public Notice workflow.
    """

    @staticmethod
    def draft_name_change_affidavit(
        old_name: str,
        new_name: str,
        father_or_spouse_name: str,
        residential_address: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Drafts statutory affidavit compliant with Controller of Publications, Delhi guidelines.
        """
        timestamp = datetime.now().strftime("%d-%m-%Y")
        affidavit_text = f"""BEFORE THE NOTARY PUBLIC / OATH COMMISSIONER
AFFIDAVIT FOR CHANGE OF NAME / RECTIFICATION

I, {new_name}, formerly known as {old_name}, Son/Daughter/Wife of {father_or_spouse_name}, aged about __ years, residing at {residential_address}, do hereby solemnly affirm and state on oath as follows:

1. That my name is recorded as "{old_name}" in my educational certificates, birth certificate, or existing identification records.
2. That due to reason of: {reason}, I have intentionally and definitively changed my name from "{old_name}" to "{new_name}".
3. That henceforth, I shall at all times and on all occasions, transactions, documents, and proceedings be known and called exclusively by the name "{new_name}".
4. That I hereby authorize the Department of Publication, Ministry of Housing and Urban Affairs, Government of India, to publish this declaration in Part-IV of the official Gazette of India.

DEPONENT: {new_name} (formerly {old_name})

VERIFICATION:
Verified at ________________ on this {timestamp} that the contents of the above affidavit are true and correct to the best of my knowledge and belief. No material fact has been concealed.

DEPONENT
"""
        return {
            "affidavit_text": affidavit_text,
            "required_nesl_stamp_value_inr": 100.0,
            "article_code": "Affidavit / Declaration (Article 4)",
            "signing_method": "Aadhaar eSign via UIDAI OTP"
        }

    @staticmethod
    def generate_newspaper_ad_payload(old_name: str, new_name: str, father_or_spouse_name: str, address: str) -> Dict[str, Any]:
        """
        Generates syndication payload for 1 National English + 1 State Vernacular newspaper.
        """
        notice_body = (
            f"I, {new_name}, S/o {father_or_spouse_name}, R/o {address}, have changed my name "
            f"from {old_name} to {new_name} for all future official and legal purposes vide affidavit "
            f"dated {datetime.now().strftime('%d/%m/%Y')}."
        )
        return {
            "english_national_publication": "The Financial Express / Indian Express",
            "vernacular_publication": "State Regional Daily",
            "ad_word_count": len(notice_body.split()),
            "classified_category": "Change of Name / Public Notices",
            "text": notice_body,
            "syndication_cost_estimate_inr": 850.0
        }

    @staticmethod
    def compile_central_gazette_manifest(old_name: str, new_name: str) -> Dict[str, Any]:
        """
        Builds the filing package manifest for Controller of Publications (Civil Lines, Delhi).
        """
        return {
            "proforma_part_iv": "Completed and signed by applicant",
            "cd_declaration": "Soft copy text formatted in MS Word / ISO standard",
            "two_witness_signatures": "Required on physical declaration sheet",
            "government_gazette_fee_inr": 1100.0,
            "batch_courier_dispatch": "NyayaSetu Delhi Central Legal Hub"
        }
