"""
Unclaimed Wealth & Deceased Estate Transmission Engine (IEPF, Physical Shares, UDGAM)
High-Ticket Contingency Recovery Core (12% - 20% Success Fee)
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class UnclaimedAssetFolio:
    folio_or_account_number: str
    company_or_bank_name: str
    asset_type: str  # 'physical_shares', 'iepf_transferred', 'dormant_bank_account'
    estimated_units: int
    current_market_price: float
    unclaimed_dividends: float
    shareholder_deceased: bool
    original_certs_lost: bool
    multiple_heirs: bool

    @property
    def total_value(self) -> float:
        return (self.estimated_units * self.current_market_price) + self.unclaimed_dividends


class IEPFTransmissionEngine:
    """
    Automates the legal and procedural recovery workflow for trapped assets in India.
    """

    @staticmethod
    def calculate_contingency_fee(total_value: float) -> Dict[str, Any]:
        """
        Calculates contingency rate based on portfolio value:
        - Below ₹2L: 20%
        - ₹2L - ₹25L: 15%
        - Above ₹25L: 12%
        """
        if total_value < 200_000:
            rate = 0.20
        elif total_value <= 2_500_000:
            rate = 0.15
        else:
            rate = 0.12

        fee = round(total_value * rate, 2)
        net_to_client = round(total_value - fee, 2)

        return {
            "gross_asset_value": total_value,
            "contingency_rate_pct": rate * 100,
            "platform_success_fee": fee,
            "net_payout_to_client": net_to_client,
            "fee_payable_timing": "Strictly upon demat credit or bank account credit"
        }

    @staticmethod
    def generate_legal_dossier_requirements(folio: UnclaimedAssetFolio) -> List[Dict[str, str]]:
        """
        Identifies mandatory statutory forms and legal affidavits required by SEBI/MCA/RTA.
        """
        docs = [
            {
                "document": "Form ISR-1",
                "purpose": "Request for registering PAN, KYC details and bank details with RTA",
                "authority": "SEBI Circular SEBI/HO/MIRSD/MIRSD_RTAMB/P/CIR/2021/655"
            },
            {
                "document": "Form ISR-2",
                "purpose": "Confirmation of Signature of securities holder by the Banker with original stamp",
                "authority": "SEBI RTA Compliance"
            }
        ]

        if folio.shareholder_deceased:
            docs.append({
                "document": "Form ISR-5 (Transmission Request)",
                "purpose": "Transmission of securities in case of deceased sole holder",
                "authority": "SEBI Master Circular"
            })
            docs.append({
                "document": "Legal Heir Affidavit (Form A)",
                "purpose": "Affidavit from all legal heirs on non-judicial stamp paper attested by Notary Public",
                "authority": "Indian Evidence Act & State Stamp Act"
            })
            docs.append({
                "document": "Indemnity Bond (Form B)",
                "purpose": "Indemnity on ₹500 NeSL e-Stamp paper with two independent sureties",
                "authority": "RTA Standard Transmission Procedure"
            })
            if folio.multiple_heirs:
                docs.append({
                    "document": "No Objection Certificate (Form C)",
                    "purpose": "NOC from non-claiming legal heirs relinquishing rights in favor of claimant",
                    "authority": "Notarized Deed of Relinquishment"
                })

        if folio.original_certs_lost:
            docs.append({
                "document": "Police NCR / FIR for Lost Share Certificates",
                "purpose": "Reporting lost physical certificates at jurisdictional police station",
                "authority": "RTA Lost Certificate Guidelines"
            })
            docs.append({
                "document": "Public Notice in English & Vernacular Newspaper",
                "purpose": "Mandatory 30-day notice for issuance of duplicate share entitlement",
                "authority": "Companies Act, 2013"
            })

        if folio.asset_type == "iepf_transferred":
            docs.append({
                "document": "MCA Form IEPF-5",
                "purpose": "Government electronic claim form for refund of shares and unclaimed dividend",
                "authority": "IEPF Authority (Accounting, Audit, Transfer and Refund) Rules, 2016"
            })
            docs.append({
                "document": "Client Digital Signature Certificate (DSC Class 3)",
                "purpose": "Affixing digital signature on MCA V3 e-filing portal",
                "authority": "MCA21 v3 Portal Requirements"
            })

        return docs

    @staticmethod
    def generate_affidavit_draft(claimant_name: str, deceased_name: str, folio: UnclaimedAssetFolio) -> str:
        """
        Auto-drafts legal affidavit for transmission.
        """
        return f"""BEFORE THE NOTARY PUBLIC / EXECUTIVE MAGISTRATE
AFFIDAVIT FOR TRANSMISSION OF SECURITIES
(As per SEBI Circular & IEPF Rules)

I, {claimant_name}, Son/Daughter of Late {deceased_name}, aged about __ years, residing at ____________________, do hereby solemnly affirm and declare on oath as follows:

1. That Late {deceased_name} was the registered holder of {folio.estimated_units} equity shares of {folio.company_or_bank_name} under Folio No. {folio.folio_or_account_number}.
2. That the said registered shareholder passed away on __/__/____ at ________ leaving behind the deponent as the rightful legal heir.
3. That the total estimated market value of the said securities is approximately Rs. {folio.total_value:,.2f}.
4. That I hereby request the Company / Registrar and Transfer Agent (RTA) to transmit the said securities into my Demat Account and credit all accrued unpaid dividends.
5. I hereby undertake to indemnify and hold harmless the Company, the RTA, and the IEPF Authority against any third-party claims.

DEPONENT: {claimant_name}
VERIFICATION:
Verified at ________ on this __ day of ________, 2026, that the contents above are true to the best of my knowledge.
DEPONENT
"""
