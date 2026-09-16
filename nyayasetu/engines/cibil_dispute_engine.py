"""
CIBIL Negative Remark Diagnostic & CICRA 2005 Statutory Dispute Notice Engine
Diagnoses credit bureau defects (Written-Off, Settled, Wrongful DPD, Identity Theft)
and drafts formal legal notices under Section 21 of the Credit Information Companies
(Regulation) Act, 2005 (CICRA) with mandatory 30-day resolution & RBI ₹100/day penalty citations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date

class CIBILDisputeEngine:
    """
    Statutory credit reporting dispute resolution engine.
    Enforces RBI Master Direction on Credit Information Companies (CICRA 2005).
    """

    REMARK_CATALOG = {
        "WRITTEN_OFF": {
            "name": "Written Off / Loss Asset Tag",
            "score_impact_pts": -85,
            "severity": "CRITICAL",
            "description": "Lender marked the account as bad debt/loss despite full settlement or ongoing repayment.",
            "statutory_ground": "Section 21(1) CICRA 2005: Failure of Credit Institution (CI) to update accurate credit data."
        },
        "SETTLED_NOT_CLOSED": {
            "name": "Settled Instead of Closed",
            "score_impact_pts": -55,
            "severity": "HIGH",
            "description": "One-Time Settlement (OTS) concluded with bank NOC, but bureau reports 'Settled' preventing fresh loan sanctions.",
            "statutory_ground": "Breach of RBI Guidelines on Compromise Settlements (2023) and Section 21 CICRA."
        },
        "FALSE_DPD": {
            "name": "Wrongful Days Past Due (DPD 30/60/90)",
            "score_impact_pts": -65,
            "severity": "HIGH",
            "description": "Bank clearing glitch caused overdue flags (30+ DPD) despite on-time bank account debit.",
            "statutory_ground": "Erroneous submission of historical repayment information under Section 19 CICRA."
        },
        "IDENTITY_THEFT": {
            "name": "Fraudulent / Ghost Loan Account",
            "score_impact_pts": -90,
            "severity": "CRITICAL",
            "description": "A loan or credit card appears on credit report that was never applied for or sanctioned to the citizen.",
            "statutory_ground": "Severe KYC non-compliance by lender; Section 20 CICRA accuracy guarantee."
        },
        "ACTIVE_BALANCE_ON_CLOSED": {
            "name": "Active Outstanding on Closed Account",
            "score_impact_pts": -40,
            "severity": "MODERATE",
            "description": "Credit card closed with zero dues months ago continues to reflect an active limit and high utilization.",
            "statutory_ground": "Failure to furnish monthly credit update within 30 days under RBI Master Directions."
        }
    }

    @classmethod
    def diagnose_remark(
        cls,
        remark_code: str,
        bank_name: str,
        account_number: str,
        disputed_amount_inr: float = 0.0
    ) -> Dict[str, Any]:
        """
        Diagnoses credit bureau remark severity, estimated score penalty, and statutory recovery strategy.
        """
        clean_code = remark_code.strip().upper()
        info = cls.REMARK_CATALOG.get(clean_code, cls.REMARK_CATALOG["WRITTEN_OFF"])

        return {
            "remark_code": clean_code,
            "remark_name": info["name"],
            "bank_name": bank_name,
            "account_number": account_number,
            "disputed_amount_inr": disputed_amount_inr,
            "estimated_score_penalty": info["score_impact_pts"],
            "severity_level": info["severity"],
            "description": info["description"],
            "statutory_ground": info["statutory_ground"],
            "statutory_resolution_window_days": 30,
            "rbi_penalty_per_day_inr": 100.0,
            "recommended_action": "Serve statutory Section 21 CICRA notice to Bank Principal Nodal Officer and CIBIL Grievance Desk."
        }

    @classmethod
    def generate_cicra_dispute_notice(
        cls,
        complainant_name: str,
        complainant_pan: str,
        complainant_mobile: str,
        complainant_address: str,
        lender_bank_name: str,
        account_number: str,
        remark_type: str = "WRITTEN_OFF",
        disputed_amount_inr: float = 50000.0,
        settlement_date: str = "15-January-2025",
        bureau_name: str = "TransUnion CIBIL Limited"
    ) -> Dict[str, Any]:
        """
        Drafts court-admissible formal Statutory Notice of Dispute under Section 21 of CICRA 2005.
        """
        today_str = datetime.now().strftime("%d-%B-%Y")
        tracking_docket = f"NS-CICRA-{datetime.now().strftime('%Y%m')}-{abs(hash(account_number)) % 10000:04d}"
        info = cls.REMARK_CATALOG.get(remark_type.strip().upper(), cls.REMARK_CATALOG["WRITTEN_OFF"])

        notice_text = f"""STATUTORY LEGAL NOTICE UNDER SECTION 21 OF THE CREDIT INFORMATION COMPANIES (REGULATION) ACT, 2005 (CICRA)
AND RBI CIRCULAR RBI/2023-24/72 (FRAMEWORK ON COMPENSATION FOR DELAYS IN RECTIFICATION OF CREDIT INFORMATION)

Docket Ref: {tracking_docket}
Date of Dispatch: {today_str}

TO:
1. The Principal Nodal Grievance Officer,
   {lender_bank_name},
   Corporate & Retail Banking Operations.

2. The Chief Grievance Officer,
   {bureau_name},
   One World Center, Tower 19th Floor, Senapati Bapat Marg, Mumbai - 400013.

COPY TO:
The RBI Integrated Banking Ombudsman,
Reserve Bank of India, Mumbai / New Delhi.

FROM:
{complainant_name}
PAN: {complainant_pan}
Mobile: {complainant_mobile}
Address: {complainant_address}

SUBJECT: STATUTORY DEMAND FOR IMMEDIATE RECTIFICATION OF ERRONEOUS/DEFAMATORY NEGATIVE CREDIT REPORTING IN RESPECT OF ACCOUNT NO. {account_number} WITHIN 30 DAYS MANDATORY STATUTORY WINDOW.

Sir / Madam,

1. The Complainant is a law-abiding citizen and consumer whose credit record has been severely damaged due to gross negligence and inaccurate data transmission by {lender_bank_name} to {bureau_name}.

2. PARTICULARS OF DISPUTE:
   a. Credit Institution (CI): {lender_bank_name}
   b. Disputed Account / Card Number: {account_number}
   c. Defective Reporting Tag: {info['name']}
   d. Disputed Outstanding Claim: Rs. {disputed_amount_inr:,.2f}
   e. Date of Full Settlement / Closure: {settlement_date}

3. STATUTORY INFRINGEMENT UNDER CICRA 2005:
   Under Section 21(1) of the Credit Information Companies (Regulation) Act, 2005, every credit institution is under a strict statutory obligation to ensure that credit information provided to credit bureaus is accurate, complete, and updated on a monthly cycle.
   The retention of the '{info['name']}' tag on the Complainant's credit report is factually false, defamatory, and in direct violation of Section 21 of CICRA, causing an arbitrary drop of {abs(info['score_impact_pts'])} points in the Complainant's CIBIL score.

4. MANDATORY 30-DAY STATUTORY TIMELINE & RBI COMPENSATION:
   Under RBI Circular RBI/2023-24/72 dated October 26, 2023, you are jointly and severally required to resolve this dispute and update the credit bureau records within THIRTY (30) CALENDAR DAYS from the date of receipt of this notice.
   FAILURE TO RESOLVE WITHIN 30 DAYS: {lender_bank_name} and {bureau_name} shall be liable to pay statutory compensation of Rs. 100/- (Rupees One Hundred Only) per calendar day of delay directly to the Complainant.

5. DEMAND FOR RELIEF:
   You are hereby called upon to:
   a. Immediately delete the '{info['name']}' and negative DPD remarks on Account No. {account_number}.
   b. Update the status to 'CLOSED' with 'NIL' outstanding balance in the monthly bureau submission.
   c. Issue an updated TransUnion CIBIL credit report reflecting the rectified score.

Failing which, the Complainant shall file a formal complaint with the RBI Banking Ombudsman and initiate civil damages litigation before the appropriate Consumer Disputes Redressal Commission for reputational damage and mental agony.

Yours faithfully,

____________________________________
{complainant_name}
(Complainant / Affected Consumer)
"""

        return {
            "success": True,
            "docket_number": tracking_docket,
            "complainant_name": complainant_name,
            "lender_bank_name": lender_bank_name,
            "account_number": account_number,
            "notice_text": notice_text,
            "statutory_period_days": 30,
            "daily_penalty_rbi_inr": 100.0,
            "legal_citation": "Section 21 CICRA 2005 read with RBI/2023-24/72 Compensation Framework"
        }
