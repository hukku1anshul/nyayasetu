"""
NyayaSetu Online Legal & CA Engine
High-Volume Citizen & MSME Online Statutory Services:
1. MSME Samadhaan Delayed Payment Petition & 3x RBI Interest Calculator (MSMED Act 2006)
2. Statutory Will & Testament / Codicil Drafter (Indian Succession Act 1925)
3. Gift Deed & Family Settlement with Sec 56(2)(x) Relative Tax Exemption (Transfer of Property Act 1882)
4. GST Revocation of Cancellation Application Form GST REG-21 (Rule 23 CGST Rules 2017)
5. Section 143A NI Act 20% Interim Compensation Calculator & Magistrate Application (NI Act 1881)
"""

import math
from datetime import datetime, date
from typing import Dict, Any, List, Optional


class MSMESamadhaanEngine:
    """
    Sections 15, 16, 17, 18 Micro, Small and Medium Enterprises Development (MSMED) Act, 2006.
    Statutory 45-day payment ceiling and compound interest at 3x RBI Bank Rate with monthly rests.
    """
    CURRENT_RBI_BANK_RATE = 6.75  # RBI Bank Rate as of 2025-2026
    STATUTORY_INTEREST_MULTIPLIER = 3  # Section 16: 3 times the RBI Bank Rate
    STATUTORY_MAX_PAYMENT_DAYS = 45   # Section 15: Maximum agreed period cannot exceed 45 days

    @classmethod
    def calculate_delayed_interest(
        cls,
        principal_amount_inr: float,
        invoice_date: str,
        agreed_credit_days: int = 30,
        calculation_date: Optional[str] = None
    ) -> Dict[str, Any]:
        credit_days = min(agreed_credit_days, cls.STATUTORY_MAX_PAYMENT_DAYS)
        inv_dt = datetime.strptime(invoice_date, "%Y-%m-%d").date()
        calc_dt = datetime.strptime(calculation_date, "%Y-%m-%d").date() if calculation_date else date.today()

        # Payment due date
        from datetime import timedelta
        due_date = inv_dt + timedelta(days=credit_days)
        delay_days = max(0, (calc_dt - due_date).days)

        statutory_annual_rate = cls.CURRENT_RBI_BANK_RATE * cls.STATUTORY_INTEREST_MULTIPLIER  # e.g., 20.25%
        monthly_rate = (statutory_annual_rate / 100.0) / 12.0

        # Section 16: Monthly compounding rests
        months_elapsed = delay_days / 30.4375
        compounded_amount = principal_amount_inr * math.pow(1 + monthly_rate, months_elapsed)
        compound_interest = max(0.0, compounded_amount - principal_amount_inr)
        total_claimable = principal_amount_inr + compound_interest

        return {
            "principal_inr": round(principal_amount_inr, 2),
            "invoice_date": str(inv_dt),
            "due_date": str(due_date),
            "delay_days": delay_days,
            "statutory_rate_annual_pct": round(statutory_annual_rate, 2),
            "rbi_base_rate_pct": cls.CURRENT_RBI_BANK_RATE,
            "interest_amount_inr": round(compound_interest, 2),
            "total_claimable_inr": round(total_claimable, 2),
            "is_actionable_under_sec18": delay_days > 0,
            "statutory_forum": "Micro and Small Enterprises Facilitation Council (MSEFC)",
            "official_portal_url": "https://samadhaan.msme.gov.in"
        }

    @classmethod
    def draft_msme_petition(
        cls,
        supplier_enterprise_name: str,
        supplier_udyam_reg: str,
        supplier_address: str,
        buyer_company_name: str,
        buyer_gstin: str,
        buyer_address: str,
        invoice_number: str,
        invoice_date: str,
        principal_amount_inr: float,
        agreed_credit_days: int = 30,
        goods_or_services_desc: str = "Supply of engineering components & IT consulting"
    ) -> Dict[str, Any]:
        calc = cls.calculate_delayed_interest(principal_amount_inr, invoice_date, agreed_credit_days)
        docket = f"NS-MSME-{datetime.now().strftime('%Y%m')}-{int(principal_amount_inr) % 9000 + 1000}"

        petition_text = f"""BEFORE THE MICRO & SMALL ENTERPRISES FACILITATION COUNCIL (MSEFC)
APPLICATION UNDER SECTION 18 OF THE MSMED ACT, 2006 READ WITH SECTION 15 & 16

IN THE MATTER OF:
{supplier_enterprise_name}
(Udyam Reg: {supplier_udyam_reg})
Address: {supplier_address}
... APPLICANT / SUPPLIER

VERSUS

{buyer_company_name}
(GSTIN: {buyer_gstin})
Address: {buyer_address}
... RESPONDENT / BUYER

MEMORANDUM OF CLAIM FOR UNPAID DUES WITH STATUTORY COMPOUND INTEREST

1. That the Applicant is a registered Micro/Small Enterprise holding valid Udyam Registration No. {supplier_udyam_reg} under the Micro, Small and Medium Enterprises Development Act, 2006.

2. That the Respondent Buyer placed orders for and duly accepted the supply of:
   {goods_or_services_desc}, against Invoice No. {invoice_number} dated {invoice_date} for a principal sum of Rs. {principal_amount_inr:,.2f}.

3. That under Section 15 of the MSMED Act, 2006, the Respondent was legally obligated to make payment within the statutory period not exceeding 45 days. The payment fell due on {calc['due_date']} and has remained unpaid for {calc['delay_days']} days.

4. That under Section 16 of the MSMED Act, 2006, the Respondent is statutorily liable to pay compound interest with monthly rests at three times the RBI Bank Rate (Statutory Rate: {calc['statutory_rate_annual_pct']}% p.a.), amounting to Rs. {calc['interest_amount_inr']:,.2f}.

5. STATEMENT OF CLAIM:
   a) Principal Outstanding: Rs. {calc['principal_inr']:,.2f}
   b) Statutory Compound Interest u/s 16: Rs. {calc['interest_amount_inr']:,.2f}
   c) TOTAL RECOVERY CLAIMED: Rs. {calc['total_claimable_inr']:,.2f}

PRAYER:
The Applicant prays that this Hon'ble Council be pleased to issue notice to the Respondent, conduct conciliation/arbitration u/s 18(2)/18(3), and pass an Award directing the Respondent to pay the total sum of Rs. {calc['total_claimable_inr']:,.2f} along with ongoing compound interest until realization.

Dated: {datetime.now().strftime('%d-%m-%Y')}
Place: {supplier_address.split(',')[-1].strip() if ',' in supplier_address else 'India'}

For {supplier_enterprise_name}
(Authorized Signatory)
"""
        return {
            "success": True,
            "docket_number": docket,
            "petition_text": petition_text,
            "financial_breakdown": calc,
            "filing_instructions": [
                "1. Log in with Udyam Registration on https://samadhaan.msme.gov.in.",
                "2. Upload copy of Invoice, Delivery Challan/Work Completion, and this Petition.",
                "3. Council mandates conciliation within 90 days of registration."
            ]
        }


class StatutoryWillEngine:
    """
    Sections 59-63 Indian Succession Act, 1925.
    Court-admissible simple testamentary will with executor appointment and 2-witness declaration.
    Does NOT require mandatory stamp paper or registration under Indian law.
    """
    @classmethod
    def draft_will(
        cls,
        testator_name: str,
        testator_age: int,
        testator_parent_or_spouse: str,
        testator_address: str,
        executor_name: str,
        executor_address: str,
        bequests: List[Dict[str, str]],
        witness_1_name: str = "Witness 1",
        witness_2_name: str = "Witness 2"
    ) -> Dict[str, Any]:
        docket = f"NS-WILL-{datetime.now().strftime('%Y%m')}-{testator_age}89"

        bequest_lines = ""
        for i, b in enumerate(bequests, 1):
            bequest_lines += f"\n   {i}. Property/Asset: {b.get('asset_description', 'Asset')}\n      Bequeathed Beneficiary: {b.get('beneficiary_name', 'Beneficiary')} (Relation: {b.get('relationship', 'Family')})\n      Share: {b.get('share_percentage', '100%')}"

        will_text = f"""LAST WILL AND TESTAMENT

I, {testator_name}, aged about {testator_age} years, resident of {testator_address}, Son/Daughter/Spouse of {testator_parent_or_spouse}, of sound mind, memory, and understanding, and without any coercion, undue influence, or fraud, do hereby make, publish, and declare this as my LAST WILL AND TESTAMENT, revoking all former Wills and Codicils made by me at any time heretofore.

1. APPOINTMENT OF EXECUTOR:
I hereby nominate, constitute, and appoint {executor_name}, residing at {executor_address}, to be the Sole Executor of this my Will. In the event of their inability or refusal to act, the court of competent jurisdiction may appoint an administrator.

2. FAMILY AND BENEFICIARY DECLARATION:
I am the absolute and exclusive owner of the movable and immovable properties set forth in the Schedule hereunder, with full legal power of alienation.

3. DISPOSITION AND BEQUEST OF ASSETS:
Upon my demise, my estate shall be transferred, assigned, and bequeathed absolutely and forever to the following beneficiaries:
{bequest_lines}

4. RESIDUARY ESTATE:
Any other property, whether movable or immovable, tangible or intangible (including bank accounts, fixed deposits, demat shares, PF accumulations, and insurance proceeds) not specifically disposed of herein shall devolve upon my Executor to be distributed equally among my legal heirs.

5. FREE WILL AND TESTAMENTARY CAPACITY:
I declare that I am executing this Will in good physical health and sound testamentary disposing state of mind, fully understanding the nature and consequences of this disposition.

IN WITNESS WHEREOF, I, {testator_name}, the Testator, have set my hand to this my Last Will and Testament on this {datetime.now().strftime('%d day of %B, %Y')}.

________________________________
TESTATOR / SIGNATURE
({testator_name})

ATTESTATION CLAUSE UNDER SECTION 63(c) OF THE INDIAN SUCCESSION ACT, 1925:
Signed and declared by the above-named Testator, {testator_name}, as and for their Last Will and Testament, in the presence of us, who in their presence and at their request, and in the presence of each other, have hereunto subscribed our names as attesting witnesses:

WITNESS 1:
Name: {witness_1_name}
Address: _______________________
Signature: ____________________

WITNESS 2:
Name: {witness_2_name}
Address: _______________________
Signature: ____________________
"""
        return {
            "success": True,
            "docket_number": docket,
            "will_text": will_text,
            "statutory_guidance": [
                "Under Indian Law (Section 18 Registration Act 1908), registration of a Will is purely OPTIONAL.",
                "A Will is legally valid when executed on plain white paper, signed by the Testator, and attested by TWO independent witnesses who are NOT beneficiaries.",
                "Witnesses must witness the Testator signing in person."
            ]
        }


class GiftDeedEngine:
    """
    Section 122 Transfer of Property Act, 1882.
    Section 56(2)(x) Income Tax Act 1961 relative exemption audit.
    """
    EXEMPT_RELATIVES = [
        "SPOUSE", "BROTHER", "SISTER", "BROTHER_OF_SPOUSE", "SISTER_OF_SPOUSE",
        "LINEAL_ASCENDANT", "LINEAL_DESCENDANT", "LINEAL_ASCENDANT_OF_SPOUSE",
        "LINEAL_DESCENDANT_OF_SPOUSE", "SPOUSE_OF_BROTHER", "SPOUSE_OF_SISTER"
    ]

    @classmethod
    def audit_and_generate_gift_deed(
        cls,
        donor_name: str,
        donor_pan: str,
        donor_address: str,
        donee_name: str,
        donee_pan: str,
        donee_address: str,
        relationship: str,
        gift_type: str = "MOVABLE_CASH_OR_SECURITIES",
        asset_description: str = "Rs. 5,00,000 via RTGS / 500 Equity Shares",
        estimated_value_inr: float = 500000.0
    ) -> Dict[str, Any]:
        rel_key = relationship.upper().replace(" ", "_")
        is_exempt_relative = any(r in rel_key for r in cls.EXEMPT_RELATIVES) or rel_key in cls.EXEMPT_RELATIVES
        docket = f"NS-GIFT-{datetime.now().strftime('%Y%m')}-{int(estimated_value_inr) % 8000 + 1000}"

        deed_text = f"""DEED OF GIFT

THIS DEED OF GIFT is made and executed on this {datetime.now().strftime('%d day of %B, %Y')} at {donor_address.split(',')[-1].strip() if ',' in donor_address else 'India'}

BETWEEN:
{donor_name}, PAN: {donor_pan}, residing at {donor_address}
(hereinafter called the "DONOR", which expression shall include their legal heirs, executors, and assigns) ... OF THE FIRST PART

AND:
{donee_name}, PAN: {donee_pan}, residing at {donee_address}
(hereinafter called the "DONEE", which expression shall include their legal heirs, executors, and assigns) ... OF THE SECOND PART

WHEREAS:
1. The Donor and Donee are related to each other as {relationship}.
2. Out of natural love and affection towards the Donee, the Donor is desirous of gifting the property/assets described below, without any monetary consideration.
3. The Donor has full and unencumbered title and ownership over the gifted asset.

NOW THIS DEED WITNESSETH AS FOLLOWS:
1. VOLUNTARY TRANSFER:
In consideration of natural love and affection, the Donor hereby voluntarily, irrevocably, and absolutely transfers and assigns unto the Donee:
{asset_description} (Estimated Value: Rs. {estimated_value_inr:,.2f})

2. COVENANT OF ABSOLUTE TITLE:
The Donor covenants that the said property is free from all encumbrances, liens, attachments, or claims of any third party.

3. TAX COMPLIANCE UNDER SECTION 56(2)(x) OF THE INCOME TAX ACT, 1961:
The Donor and Donee affirm that as per Section 56(2)(x) proviso (I) of the Income Tax Act, 1961, gifts received from a "Relative" are completely exempt from Income Tax in the hands of the Donee.

4. ACCEPTANCE BY DONEE (SECTION 122 TRANSFER OF PROPERTY ACT):
The Donee hereby gratefully accepts the gift of the said property during the lifetime of the Donor.

IN WITNESS WHEREOF the Donor and Donee have set their hands on the day and year first above written.

___________________________         ___________________________
DONOR                               DONEE (In Acceptance)
({donor_name})                       ({donee_name})

WITNESS 1:                          WITNESS 2:
Signature: _________________        Signature: _________________
Name: ______________________        Name: ______________________
"""
        return {
            "success": True,
            "docket_number": docket,
            "is_tax_exempt_relative": is_exempt_relative,
            "section_56_2_x_compliant": is_exempt_relative,
            "tax_liability_donee_inr": 0.0 if is_exempt_relative else round(estimated_value_inr * 0.312, 2),
            "gift_deed_text": deed_text,
            "statutory_notes": [
                "Movable gifts (cash, cheque, shares, mutual funds) become legally complete upon delivery and acceptance.",
                "For immovable real estate, Section 123 of the Transfer of Property Act requires mandatory registration with local Sub-Registrar.",
                "No income tax applies to Donee when relationship falls within Section 56(2)(x) relative definitions."
            ]
        }


class GSTRevocationEngine:
    """
    Section 30 CGST Act, 2017 read with Rule 23 CGST Rules, 2017.
    Drafts Form GST REG-21 Application for Revocation of Suo-Motu Cancellation.
    """
    @classmethod
    def draft_revocation_application(
        cls,
        taxpayer_trade_name: str,
        gstin: str,
        principal_place_address: str,
        cancellation_order_number: str,
        cancellation_order_date: str,
        reason_category: str = "NON_FILING_OVERCOME",
        justification_details: str = "Pending returns filed with late fees; operations paused due to medical emergency."
    ) -> Dict[str, Any]:
        docket = f"NS-GST-REV-{datetime.now().strftime('%Y%m')}-{gstin[:4]}"

        # Calculate 30-day and condonation limits
        order_dt = datetime.strptime(cancellation_order_date, "%Y-%m-%d").date()
        from datetime import timedelta
        statutory_30_days = order_dt + timedelta(days=30)
        condonation_90_days = order_dt + timedelta(days=90)

        app_text = f"""FORM GST REG-21
[See Rule 23(1) of the Central Goods and Services Tax Rules, 2017]
APPLICATION FOR REVOCATION OF CANCELLATION OF REGISTRATION

1. GSTIN (Cancelled): {gstin}
2. Legal Name / Trade Name: {taxpayer_trade_name}
3. Address of Principal Place of Business: {principal_place_address}
4. Cancellation Order Reference No.: {cancellation_order_number}
5. Date of Cancellation Order: {cancellation_order_date}

6. REASONS FOR SEEKING REVOCATION:
The registration of the Applicant was cancelled under Section 29(2)(c) on ground of continuous non-filing of returns.

The Applicant respectfully submits:
a) The failure to file returns was neither intentional nor deliberate, but caused by:
   {justification_details}
b) The Applicant has now filed all pending returns up to date along with requisite late fees, interest, and taxes under Section 39.
c) Cancellation of GSTIN causes irreparable hardship to business operations, freezes input tax credit (ITC) for buyers, and hinders livelihoods.

7. UNDERTAKING UNDER RULE 23(1):
The Applicant hereby undertakes to comply strictly with all provisions of the CGST Act, 2017 and file all future monthly/quarterly returns within statutory deadlines.

PRAYER:
In view of the above facts, it is prayed that the Proper Officer be pleased to revoke the cancellation of GSTIN {gstin} under Section 30(2) of the CGST Act, 2017 and restore the GST registration.

Date: {datetime.now().strftime('%d-%m-%Y')}
Place: {principal_place_address.split(',')[-1].strip() if ',' in principal_place_address else 'India'}

For {taxpayer_trade_name}
(Authorized Signatory / Proprietor)
"""
        return {
            "success": True,
            "docket_number": docket,
            "application_text": app_text,
            "statutory_timeline": {
                "order_date": str(order_dt),
                "normal_window_30_days": str(statutory_30_days),
                "condonation_window_90_days": str(condonation_90_days),
                "is_within_standard_window": date.today() <= statutory_30_days
            },
            "official_portal_url": "https://services.gst.gov.in"
        }


class InterimCompensation143AEngine:
    """
    Section 143A Negotiable Instruments Act, 1881.
    Statutory calculation of 20% interim compensation in Section 138 cheque bounce trials.
    """
    MAX_INTERIM_PERCENT = 20.0
    PAYMENT_TIMELINE_DAYS = 60
    EXTENSION_DAYS = 30

    @classmethod
    def calculate_and_draft_143a(
        cls,
        complainant_name: str,
        accused_name: str,
        court_name: str,
        case_cc_number: str,
        cheque_number: str,
        cheque_amount_inr: float,
        cheque_date: str,
        plea_date: str = "Date of framing of notice/charge"
    ) -> Dict[str, Any]:
        interim_relief = round(cheque_amount_inr * (cls.MAX_INTERIM_PERCENT / 100.0), 2)
        docket = f"NS-143A-{datetime.now().strftime('%Y%m')}-{int(cheque_amount_inr) % 9000 + 1000}"

        app_text = f"""IN THE COURT OF METROPOLITAN MAGISTRATE / JMFC, AT {court_name.upper()}
C.C. NO. {case_cc_number} OF 2026

IN THE MATTER OF:
{complainant_name} ... COMPLAINANT
VERSUS
{accused_name} ... ACCUSED

APPLICATION UNDER SECTION 143A OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 FOR GRANT OF 20% INTERIM COMPENSATION

MOST RESPECTFULLY SHOWETH:
1. That the Complainant has filed the present complaint under Section 138 of the Negotiable Instruments Act, 1881 against the Accused for dishonour of Cheque No. {cheque_number} dated {cheque_date} for an amount of Rs. {cheque_amount_inr:,.2f}.

2. That the Accused has pleaded not guilty to the notice/charge framed by this Hon'ble Court.

3. That Section 143A(1) of the Negotiable Instruments Act empowers this Hon'ble Court to order the drawer of the cheque to pay interim compensation to the Complainant in a summary trial or summons case where the accused pleads not guilty.

4. That under Section 143A(2), the interim compensation shall not exceed 20% of the amount of the cheque, which in the present case amounts to:
   Rs. {interim_relief:,.2f} (20% of Rs. {cheque_amount_inr:,.2f}).

5. That the Complainant undertakes to repay the said interim compensation with RBI Bank Rate interest if the Accused is acquitted after trial, as mandated under Section 143A(4).

PRAYER:
It is therefore respectfully prayed that this Hon'ble Court may be pleased to direct the Accused to deposit/pay 20% interim compensation amounting to Rs. {interim_relief:,.2f} within 60 days under Section 143A of the Negotiable Instruments Act, 1881.

Complainant / Through Counsel
Dated: {datetime.now().strftime('%d-%m-%Y')}
"""
        return {
            "success": True,
            "docket_number": docket,
            "cheque_amount_inr": cheque_amount_inr,
            "statutory_interim_pct": cls.MAX_INTERIM_PERCENT,
            "interim_compensation_inr": interim_relief,
            "statutory_compliance_deadline_days": cls.PAYMENT_TIMELINE_DAYS,
            "magistrate_application_text": app_text
        }
