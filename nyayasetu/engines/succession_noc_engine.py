"""
Multi-Heir Succession & Digital Relinquishment (NOC) Engine
Solves family transmission disputes by automating Family Tree Declarations and
SEBI Form-C Relinquishment Deeds with remote Aadhaar e-Sign.
"""

from typing import Dict, List, Any
from datetime import datetime

class SuccessionNOCEngine:
    """
    Automates statutory documentation when a deceased shareholder has multiple legal heirs.
    Enables non-claiming siblings to digitally relinquish rights in favor of the claimant.
    """

    @staticmethod
    def generate_family_tree_declaration(
        deceased_name: str,
        date_of_death: str,
        heirs_list: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generates formal Family Tree Declaration (Vamshavruksha).
        heirs_list: [{"name": "...", "relationship": "Son/Daughter/Spouse", "age": 35, "is_claiming": True/False}]
        """
        heirs_table = "\n".join([
            f"- {h['name']} | Relationship: {h['relationship']} | Age: {h.get('age', '--')} | Claiming: {'YES (Primary Claimant)' if h.get('is_claiming') else 'NO (Relinquishing Rights)'}"
            for h in heirs_list
        ])

        declaration_text = f"""BEFORE THE EXECUTIVE MAGISTRATE / NOTARY PUBLIC
STATUTORY DECLARATION OF SURVIVING LEGAL HEIRS (FAMILY TREE)
IN THE MATTER OF THE ESTATE OF LATE {deceased_name.upper()}

1. That the deceased Shri/Smt. {deceased_name} passed away intestate on {date_of_death}.
2. That the deceased is survived exclusively by the following legal heirs under Class-I of the Hindu Succession Act / Indian Succession Act:
{heirs_table}

3. That there are no other legal heirs, adopted children, or testamentary wills left by the deceased.
4. That all surviving heirs mutually agree that the securities held by the deceased shall be transmitted to the Primary Claimant.

DEPONENT: Primary Claimant on behalf of all surviving heirs.
"""
        return {
            "family_tree_declaration": declaration_text,
            "total_surviving_heirs": len(heirs_list),
            "statutory_act": "Hindu Succession Act, 1956 / Indian Succession Act, 1925"
        }

    @staticmethod
    def generate_form_c_relinquishment_deed(
        deceased_name: str,
        company_name: str,
        folio_number: str,
        shares_count: int,
        primary_claimant_name: str,
        relinquishing_heir_name: str,
        relationship_with_deceased: str
    ) -> Dict[str, Any]:
        """
        Generates SEBI Form-C (No Objection Certificate / Deed of Relinquishment).
        """
        deed_text = f"""SEBI FORM-C: NO OBJECTION CERTIFICATE / DEED OF RELINQUISHMENT
(For Transmission of Securities in favour of Nominated Claimant)

To:
The Board of Directors, {company_name}
And its designated Registrar & Transfer Agent (RTA)

I, {relinquishing_heir_name}, {relationship_with_deceased} of Late {deceased_name}, residing at _____________________________________, do hereby state and declare:

1. That Late {deceased_name} held {shares_count} equity shares under Folio No. {folio_number} in {company_name}.
2. That I am a rightful legal heir entitled to a share in the estate of the deceased.
3. That of my own free will and volition, without any undue influence, coercion, or misrepresentation, I hereby RELINQUISH, RENOUNCE, and WAIVE all my rights, titles, and interests in the said {shares_count} shares in favour of:
   PRIMARY CLAIMANT: {primary_claimant_name}

4. I have NO OBJECTION whatsoever if the Company / RTA transmits the entire holding of {shares_count} shares exclusively into the name of {primary_claimant_name}.

RELINQUISHING HEIR SIGNATURE / Aadhaar e-Sign:
Name: {relinquishing_heir_name}
Date: {datetime.now().strftime('%d/%m/%Y')}
Verification: Executed via NeSL Digital Document Execution / Aadhaar OTP eSign
"""
        return {
            "document_title": "SEBI Form-C (Deed of Relinquishment)",
            "relinquishing_heir": relinquishing_heir_name,
            "beneficiary_claimant": primary_claimant_name,
            "shares_relinquished": shares_count,
            "deed_text": deed_text,
            "remote_signing_method": "UIDAI Aadhaar e-Sign OTP (Valid under IT Act 2000 Section 5)"
        }
