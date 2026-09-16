"""
High-Volume Citizen Everyday Legal & CA Engines:
1. ConsumerForumEngine: e-Daakhil & Consumer Protection Act 2019 Petition Drafter
2. RTIApplicationEngine: Right to Information Act 2005 Section 6(1) Application Builder
3. CyberCrimeEngine: Section 66D IT Act Cyber Fraud Statement & 1930 Helpline Bridge
4. AffidavitEngine: Standard Notarized Sworn Affidavit & Self-Declaration Generator
5. TaxRectificationEngine: Section 154 Income Tax Act CPC Rectification & Refund Drafter
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

class ConsumerForumEngine:
    """Drafts formal consumer complaints under Section 35 Consumer Protection Act, 2019."""
    
    @staticmethod
    def draft_complaint(
        complainant_name: str,
        complainant_address: str,
        complainant_mobile: str,
        respondent_name: str,
        respondent_address: str,
        dispute_category: str = "ECOMMERCE",
        transaction_amount: float = 15000.0,
        transaction_date: str = "10-08-2026",
        order_or_ref_id: str = "OD9928172910",
        grievance_details: str = "Product delivered was counterfeit/defective, refund refused.",
        compensation_demanded: float = 25000.0
    ) -> Dict[str, Any]:
        today_str = datetime.now().strftime("%d day of %B, %Y")
        total_claim = transaction_amount + compensation_demanded
        
        # Determine Commission Jurisdiction (CPA 2019 Pecuniary Limits)
        if total_claim <= 5000000.0:  # Up to 50 Lakhs
            forum = "District Consumer Disputes Redressal Commission"
            fee_inr = 0 if total_claim <= 500000 else (500 if total_claim <= 1000000 else 1000)
        elif total_claim <= 20000000.0:  # 50 Lakhs to 2 Crores
            forum = "State Consumer Disputes Redressal Commission"
            fee_inr = 2500
        else:
            forum = "National Consumer Disputes Redressal Commission (New Delhi)"
            fee_inr = 5000

        docket_no = f"NS-CPA-{datetime.now().strftime('%Y%m')}-{int(transaction_amount) % 9000 + 1000}"

        petition_text = f"""BEFORE THE HON'BLE {forum.upper()}
AT DISTRICT / STATE COMMISSION JURISDICTION

CONSUMER COMPLAINT NO. ________ OF 2026

IN THE MATTER OF:
{complainant_name},
Residing at: {complainant_address},
Mobile: {complainant_mobile}
... COMPLAINANT / CONSUMER

VERSUS

{respondent_name},
Having office at: {respondent_address}
... OPPOSITE PARTY / RESPONDENT

---

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019
FOR DEFICIENCY IN SERVICE AND UNFAIR TRADE PRACTICE

MOST RESPECTFULLY SHOWETH:

1. That the Complainant is a 'Consumer' within the definition of Section 2(7) of the Consumer Protection Act, 2019, having purchased goods / availed services for personal consideration.

2. That the Opposite Party is engaged in commercial trade / e-commerce / service provision under the jurisdiction of this Hon'ble Commission.

3. BRIEF FACTS OF THE DISPUTE:
   a. On {transaction_date}, the Complainant transacted with the Opposite Party vide Order/Ref No. {order_or_ref_id} for a paid sum of Rs. {transaction_amount:,.2f}.
   b. Category of Deficiency: {dispute_category.upper()}.
   c. Specific Grievance: {grievance_details}.
   d. Despite repeated written notices and communications, the Opposite Party failed, neglected, and refused to remedy the grievance or issue full refund, causing severe financial loss and mental harassment.

4. CAUSE OF ACTION:
   The cause of action arose on {transaction_date} when the transaction occurred, and continues to subsist de die in diem as the Opposite Party has unlawfully retained the Complainant's monies without resolving the deficiency.

5. PRAYER:
   In view of the above stated facts, the Complainant most respectfully prays that this Hon'ble Commission may be pleased to:
   a. Direct the Opposite Party to immediately refund the principal amount of Rs. {transaction_amount:,.2f} along with 9% per annum interest from {transaction_date} till realization;
   b. Direct the Opposite Party to pay Rs. {compensation_demanded:,.2f} towards damages for mental agony, distress, and deficiency in service;
   c. Direct payment of litigation expenses of Rs. 5,000/-;
   d. Pass any other or further order(s) deemed just and proper in the interest of justice.

DATED: {today_str}
PLACE: {complainant_address.split(',')[-1].strip() if ',' in complainant_address else 'India'}

COMPLAINANT:
Signature: __________________________
Name: {complainant_name}

VERIFICATION:
I, {complainant_name}, do hereby verify on solemn affirmation that the contents of paras 1 to 5 above are true and correct to my knowledge and belief. Nothing material has been concealed therefrom.
Verified at ________ on this {today_str}.

DEPONENT: __________________________
"""
        return {
            "success": True,
            "docket_number": docket_no,
            "forum": forum,
            "total_claim_inr": total_claim,
            "statutory_filing_fee_inr": fee_inr,
            "live_portal_url": "https://edaakhil.nic.in",
            "nch_helpline": "1915 (National Consumer Helpline)",
            "petition_text": petition_text
        }


class RTIApplicationEngine:
    """Drafts formal RTI Applications under Section 6(1) of RTI Act, 2005."""

    @staticmethod
    def draft_rti(
        applicant_name: str,
        applicant_address: str,
        applicant_mobile: str,
        public_authority_name: str,
        public_authority_address: str,
        subject_matter: str,
        information_points: List[str],
        is_bpl: bool = False,
        bpl_card_no: str = ""
    ) -> Dict[str, Any]:
        today_str = datetime.now().strftime("%d-%m-%Y")
        docket_no = f"NS-RTI-{datetime.now().strftime('%Y%m')}-{len(subject_matter) * 31 % 9000 + 1000}"

        formatted_points = "\n".join([f"   {i+1}. {pt}" for i, pt in enumerate(information_points) if pt.strip()])

        fee_note = "Below Poverty Line (BPL) - Card No. " + bpl_card_no + " (Fee Exempt under Sec 7(5))" if is_bpl else "Statutory Application Fee of Rs. 10/- attached via IPO / Court Fee Stamp / Online Payment."

        rti_text = f"""FORM 'A'
[See Rule 3(1)]
APPLICATION FOR SEEKING INFORMATION UNDER SECTION 6(1) OF
THE RIGHT TO INFORMATION ACT, 2005

To,
The Public Information Officer (PIO) / Central Public Information Officer (CPIO),
{public_authority_name},
{public_authority_address}.

---

1. FULL NAME OF APPLICANT:
   {applicant_name}

2. ADDRESS FOR CORRESPONDENCE:
   {applicant_address}
   Mobile: {applicant_mobile}

3. CITIZENSHIP:
   Citizen of India (Under Section 3 of RTI Act 2005)

4. PARTICULARS OF INFORMATION SOUGHT:
   a. Subject Matter of Information:
      {subject_matter}

   b. Specific Period to which information relates:
      Current / Relevant Financial & Administrative Years

   c. Specific Information Requested:
{formatted_points}

5. STATUTORY TIME LIMIT:
   As provided under Section 7(1) of the RTI Act, 2005, the requested information must be supplied within 30 (thirty) days from the date of receipt of this application. If it concerns life and liberty, within 48 hours.

6. APPLICATION FEE PARTICULARS:
   {fee_note}

7. DECLARATION:
   I hereby declare that I am a citizen of India and the information sought does not fall under the exemptions contained in Section 8 or 9 of the RTI Act, 2005.

Date: {today_str}
Place: {applicant_address.split(',')[-1].strip() if ',' in applicant_address else 'India'}

SIGNATURE OF APPLICANT:
_________________________________
({applicant_name})
"""
        return {
            "success": True,
            "docket_number": docket_no,
            "statutory_response_days": 30,
            "statutory_fee_inr": 0 if is_bpl else 10,
            "public_authority": public_authority_name,
            "live_portal_url": "https://rtionline.gov.in",
            "rti_text": rti_text
        }


class CyberCrimeEngine:
    """Generates statutory cyber fraud complaints under Section 66D IT Act & 1930 protocol."""

    @staticmethod
    def draft_cyber_complaint(
        victim_name: str,
        victim_mobile: str,
        victim_email: str,
        victim_address: str,
        incident_category: str = "UPI_FRAUD",
        total_loss_inr: float = 45000.0,
        transaction_utr_or_ref: str = "UTR-482910294102",
        suspect_identifier: str = "fraudster@ybl / +91-9876501234",
        incident_date: str = "15-09-2026 14:30 IST",
        incident_summary: str = "Received fraudulent payment link under pretext of electricity bill update; funds debited unauthorizedly."
    ) -> Dict[str, Any]:
        today_str = datetime.now().strftime("%d-%m-%Y")
        docket_no = f"NS-CYBER-{datetime.now().strftime('%Y%m')}-{int(total_loss_inr) % 9000 + 1000}"

        complaint_text = f"""FORMAL POLICE COMPLAINT UNDER SECTION 66D OF THE INFORMATION TECHNOLOGY ACT, 2000
AND SECTION 318(4) OF BHARATIYA NYAYA SANHITA (BNS) / SECTION 420 IPC

TO:
The Station House Officer / Inspector In-Charge,
Cyber Crime Police Station / National Cyber Crime Reporting Portal (NCRP),
Government of India.

---

SUBJECT: REPORTING OF FINANCIAL CYBER FRAUD / CHEATING BY PERSONATION
CATEGORY: {incident_category.upper()} | TOTAL FRAUDULENT DEBIT: RS. {total_loss_inr:,.2f}

RESPECTED SIR / MA'AM,

I, the undersigned victim, wish to report a serious cognizable cyber crime executed against me:

1. VICTIM PARTICULARS:
   - Full Name: {victim_name}
   - Contact Mobile: {victim_mobile}
   - Email ID: {victim_email}
   - Residential Address: {victim_address}

2. INCIDENT & FRAUD PARTICULARS:
   - Date & Time of Incident: {incident_date}
   - Nature of Crime: {incident_category.replace('_', ' ').title()}
   - Fraudulent Amount Debited: Rs. {total_loss_inr:,.2f}
   - Bank Reference / UTR Number: {transaction_utr_or_ref}
   - Suspect UPI ID / Mobile / Bank Account: {suspect_identifier}

3. CHRONOLOGY OF EVENTS:
   {incident_summary}

4. IMMEDIATE ACTION TAKEN:
   - Reported to National Cyber Crime Helpline '1930' for Citizen Financial Cyber Fraud Reporting System (CFCFRMS) lien marking.
   - Bank notified for unauthorized debit dispute under RBI Circular RBI/2017-18/15 (Zero Liability of Customers in Unauthorized Electronic Banking Transactions).

5. PRAYER / REQUEST:
   In view of the above facts, it is prayed that:
   a. An FIR be registered under Section 66D IT Act, 2000 & relevant sections of BNS/IPC;
   b. Direct the beneficiary bank / payment aggregator to freeze and reverse the sum of Rs. {total_loss_inr:,.2f};
   c. Trace the IP address, Call Detail Records (CDR), and device IMEI of the perpetrators;
   d. Issue acknowledgment copy for official submission to my bank.

Date: {today_str}
Place: {victim_address.split(',')[-1].strip() if ',' in victim_address else 'India'}

COMPLAINANT SIGNATURE:
_____________________________
({victim_name})
"""
        return {
            "success": True,
            "docket_number": docket_no,
            "helpline": "1930 (National Cyber Fraud Reporting)",
            "live_portal_url": "https://cybercrime.gov.in",
            "statutory_act": "Section 66D IT Act 2000 & BNS 318(4)",
            "complaint_text": complaint_text
        }


class AffidavitEngine:
    """Formats standard First-Class Magistrate / Notary Public sworn affidavits."""

    @staticmethod
    def generate_affidavit(
        deponent_name: str,
        deponent_parent_name: str,
        deponent_age: int,
        deponent_residence: str,
        affidavit_type: str = "NAME_CORRECTION",
        declaration_facts: List[str] = None,
        state_name: str = "Maharashtra"
    ) -> Dict[str, Any]:
        today_str = datetime.now().strftime("%d day of %B, %Y")
        docket_no = f"NS-AFF-{datetime.now().strftime('%Y%m')}-{deponent_age * 47 % 9000 + 1000}"

        if not declaration_facts:
            declaration_facts = [
                f"That my correct and lawful name is '{deponent_name}'.",
                "That in certain records, my name was erroneously recorded with minor spelling variance.",
                f"That '{deponent_name}' and the name appearing in disputed records refer to one and the same living person, namely myself.",
                "That I am making this affidavit to submit before the competent authorities for updating official records."
            ]

        facts_formatted = "\n".join([f"{i+1}. {fact}" for i, fact in enumerate(declaration_facts)])

        affidavit_text = f"""BEFORE THE NOTARY PUBLIC / EXECUTIVE MAGISTRATE
AT {state_name.upper()}, INDIA

AFFIDAVIT
(In the matter of: {affidavit_type.replace('_', ' ').title()})

I, {deponent_name}, son/daughter/spouse of {deponent_parent_name}, aged about {deponent_age} years, residing at {deponent_residence}, do hereby solemnly affirm and declare on oath as under:

{facts_formatted}

That the contents of this affidavit are true and correct to the best of my knowledge and belief, and no part of it is false and nothing material has been concealed therefrom.

SOLEMNLY AFFIRMED AT ________ ON THIS {today_str}.

DEPONENT:
Signature: __________________________
Name: {deponent_name}

---

VERIFICATION:
Verified at ________ on this {today_str} that the contents of the above affidavit are true and correct. No part of it is false.

DEPONENT: __________________________

ATTESTATION (FOR NOTARY PUBLIC USE ONLY):
Sworn before me by the Deponent who is personally identified by ________________________.

NOTARY PUBLIC / OATH COMMISSIONER:
Seal & Signature: __________________________
"""
        return {
            "success": True,
            "docket_number": docket_no,
            "recommended_stamp_paper_inr": 100,
            "affidavit_text": affidavit_text
        }


class TaxRectificationEngine:
    """Drafts Section 154 Income Tax Act applications for CPC Bengaluru."""

    @staticmethod
    def draft_rectification(
        taxpayer_name: str,
        pan: str,
        assessment_year: str = "2025-26",
        acknowledgement_no: str = "89102941029102",
        rectification_reason: str = "TDS_MISMATCH",
        claimed_refund_inr: float = 38500.0,
        error_details: str = "TDS deposited under Form 26AS/AIS by employer was not credited in intimation order under Section 143(1)."
    ) -> Dict[str, Any]:
        today_str = datetime.now().strftime("%d-%m-%Y")
        docket_no = f"NS-ITR154-{datetime.now().strftime('%Y%m')}-{len(pan) * 73 % 9000 + 1000}"

        rectification_text = f"""APPLICATION UNDER SECTION 154 OF THE INCOME TAX ACT, 1961
FOR RECTIFICATION OF MISTAKE APPARENT FROM RECORD

TO:
The Centralized Processing Centre (CPC),
Income Tax Department,
Bengaluru, Karnataka - 560500.

(Through Online e-Filing Portal: eportal.incometax.gov.in)

---

1. TAXPAYER PARTICULARS:
   - Name of Assessee: {taxpayer_name}
   - Permanent Account Number (PAN): {pan}
   - Assessment Year (AY): {assessment_year}
   - Original ITR Ack No: {acknowledgement_no}

2. NATURE OF MISTAKE APPARENT FROM RECORD:
   Reason Code: {rectification_reason}
   Claimed Refund Due: Rs. {claimed_refund_inr:,.2f}

3. STATEMENT OF FACTS & GROUNDS FOR RECTIFICATION:
   a. The Assessee filed the Return of Income for AY {assessment_year} claiming legitimate refund of Rs. {claimed_refund_inr:,.2f}.
   b. In the Intimation under Section 143(1), an erroneous tax demand was raised / refund was reduced due to:
      "{error_details}"
   c. The tax credit is duly reflected in the annual information statement (AIS) and Form 26AS verified under Section 203AA.
   d. The non-granting of this statutory tax credit constitutes a mistake apparent from record rectifiable under Section 154 of the Income Tax Act, 1961 within the statutory limit of 4 years.

4. PRAYER:
   It is most respectfully prayed that:
   a. The mistake apparent from record in Intimation u/s 143(1) be rectified under Section 154;
   b. Credit for genuine tax prepaid/deducted be granted;
   c. Refund of Rs. {claimed_refund_inr:,.2f} along with statutory interest under Section 244A be released directly to the pre-validated bank account.

Date: {today_str}
Place: India

ASSESSEE / TAXPAYER:
Signature: __________________________
Name: {taxpayer_name} (PAN: {pan})
"""
        return {
            "success": True,
            "docket_number": docket_no,
            "assessment_year": assessment_year,
            "pan": pan,
            "live_portal_url": "https://eportal.incometax.gov.in",
            "rectification_text": rectification_text
        }
