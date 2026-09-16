"""
Legal & Tax Intelligence Engine (AI Vakil & AI CA India)
Powers:
1. Statutory Legal Notice Generator (Rental Arrears, Section 138 Cheque Bounce, Consumer Protection, Unpaid Salary)
2. Contract & Agreement Clause Risk Analyzer (Non-compete, lock-in, termination traps)
3. New vs Old Income Tax Regime Comparator (Section 115BAC vs Old Regime with 80C/80D/24b)
4. Section 44ADA Presumptive Taxation Calculator for Tech Freelancers & Consultants
5. Income Tax Notice Explainer (Sections 143(1), 139(9), 148, 142(1), 156)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
import math

class LegalNoticeEngine:
    """
    Generates statutory, court-admissible Indian legal notices with IPC/BNS,
    Negotiable Instruments Act, and Consumer Protection Act citations.
    """

    NOTICE_TEMPLATES: Dict[str, Dict[str, Any]] = {
        "CHEQUE_BOUNCE_SEC138": {
            "title": "STATUTORY LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881",
            "statute": "Section 138 & 142 of Negotiable Instruments Act, 1881",
            "statutory_period_days": 15,
            "consequences": "Criminal prosecution under Section 138 NI Act punishable with imprisonment up to 2 years, or fine up to twice the cheque amount, or both."
        },
        "RENTAL_EVICTION_ARREARS": {
            "title": "LEGAL NOTICE FOR RECOVERY OF RENT ARREARS AND TERMINATION OF TENANCY UNDER SECTION 106 OF THE TRANSFER OF PROPERTY ACT, 1882",
            "statute": "Section 106 Transfer of Property Act, 1882 & State Rent Control Act",
            "statutory_period_days": 15,
            "consequences": "Civil suit for eviction, recovery of outstanding arrears with 18% p.a. interest, mesne profits, and litigation costs."
        },
        "CONSUMER_DEFICIENCY": {
            "title": "FORMAL LEGAL NOTICE UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019 FOR DEFICIENCY OF SERVICE",
            "statute": "Consumer Protection Act, 2019 (Sections 2(11), 35 & 38)",
            "statutory_period_days": 30,
            "consequences": "Institution of consumer complaint before the District Consumer Disputes Redressal Commission seeking 100% refund, punitive damages, and compensation for mental agony."
        },
        "UNPAID_SALARY_EMPLOYMENT": {
            "title": "LEGAL DEMAND NOTICE FOR RELEASE OF ILLEGALLY WITHHELD SALARY, FULL & FINAL SETTLEMENT DUES AND EXPERIENCE CERTIFICATE",
            "statute": "Payment of Wages Act, 1936 & Industrial Disputes Act, 1947",
            "statutory_period_days": 15,
            "consequences": "Complaint before the Labour Commissioner, recovery application under Section 33C(2), and civil recovery suit with 18% compound interest."
        }
    }

    @classmethod
    def generate_notice(
        cls,
        notice_type: str,
        sender_name: str,
        sender_address: str,
        sender_phone: str,
        recipient_name: str,
        recipient_address: str,
        claim_amount_inr: float,
        transaction_date: str,
        instrument_or_reference_no: str,
        dispute_summary: str,
        advocate_name: str = "Adv. Rajeshwari Sen & Associates",
        advocate_bar_council_no: str = "D/1482/2012"
    ) -> Dict[str, Any]:
        """
        Synthesizes a complete legal notice docket ready for dispatch via Registered Post AD / Speed Post.
        """
        template = cls.NOTICE_TEMPLATES.get(notice_type, cls.NOTICE_TEMPLATES["CHEQUE_BOUNCE_SEC138"])
        today_str = date.today().strftime("%d-%B-%Y")
        tracking_docket = f"NS-NOT-{datetime.now().strftime('%Y%m')}-{int(claim_amount_inr) % 9000 + 1000}"

        if notice_type == "CHEQUE_BOUNCE_SEC138":
            substantive_clauses = (
                f"1. That my Client is a law-abiding citizen and had extended financial consideration / goods / services to you.\n"
                f"2. That towards the discharge of your legally enforceable debt and liability, you had issued Cheque bearing No. {instrument_or_reference_no} "
                f"dated {transaction_date} for an amount of Rs. {claim_amount_inr:,.2f}.\n"
                f"3. That upon presentation by my Client through their banker, the said cheque was returned dishonoured with the Banker's Memo citing "
                f"'FUNDS INSUFFICIENT / EXCEEDS ARRANGEMENT'.\n"
                f"4. That you have committed an offence under Section 138 of the Negotiable Instruments Act, 1881 by issuing a cheque without maintaining sufficient funds."
            )
        elif notice_type == "RENTAL_EVICTION_ARREARS":
            substantive_clauses = (
                f"1. That my Client is the absolute owner and Landlord of premises situated at {sender_address}, which was let out to you on monthly tenancy.\n"
                f"2. That as per the tenancy agreement, you were obligated to pay monthly rent, but you have defaulted and accumulated total unpaid arrears of "
                f"Rs. {claim_amount_inr:,.2f} since {transaction_date}.\n"
                f"3. That despite multiple oral and written reminders, you have failed and neglected to clear the outstanding rent.\n"
                f"4. That through this notice, my Client hereby determines and terminates your tenancy in respect of the said demised premises."
            )
        elif notice_type == "UNPAID_SALARY_EMPLOYMENT":
            substantive_clauses = (
                f"1. That my Client was employed with your esteemed organization as per Appointment Letter reference {instrument_or_reference_no} dated {transaction_date}.\n"
                f"2. That my Client discharged all contractual duties with utmost diligence and fidelity until separation.\n"
                f"3. That you have unlawfully, arbitrarily, and willfully withheld my Client's earned salary, notice pay, PF, and Full & Final dues amounting to Rs. {claim_amount_inr:,.2f}.\n"
                f"4. That withholding earned salary of an employee is a gross violation of statutory labour laws and basic constitutional rights."
            )
        else: # CONSUMER_DEFICIENCY
            substantive_clauses = (
                f"1. That my Client availed services / purchased products from you vide Invoice / Order No. {instrument_or_reference_no} dated {transaction_date} for Rs. {claim_amount_inr:,.2f}.\n"
                f"2. That the services rendered / goods supplied suffered from gross deficiency, defects, and unfair trade practices: {dispute_summary}.\n"
                f"3. That my Client repeatedly brought these defects to your customer service attention, but you failed to resolve or refund the consideration.\n"
                f"4. That your acts constitute deficiency in service within the meaning of Section 2(11) of the Consumer Protection Act, 2019."
            )

        demand_clause = (
            f"NOW THEREFORE, through this statutory legal notice, my Client hereby calls upon you to pay the sum of "
            f"Rs. {claim_amount_inr:,.2f} (Rupees {claim_amount_inr:,.0f} only) along with interest @ 18% p.a., within a period of "
            f"{template['statutory_period_days']} days from the date of receipt of this notice, failing which my Client has given me "
            f"peremptory instructions to initiate appropriate legal proceedings against you in the competent Court of Law, holding you "
            f"solely liable for all costs, consequences, and damages arising therefrom."
        )

        full_text = (
            f"{advocate_name.upper()}\n"
            f"Advocates & Legal Consultants\n"
            f"Bar Council Registration No: {advocate_bar_council_no}\n"
            f"Office: Chamber 402, High Court Complex • Contact: legal-desk@nyayasetu.in\n\n"
            f"DATE: {today_str}\n"
            f"DISPATCH MODE: REGISTERED POST WITH ACKNOWLEDGEMENT DUE (RPAD) / SPEED POST\n\n"
            f"TO:\n"
            f"{recipient_name}\n"
            f"{recipient_address}\n\n"
            f"FROM:\n"
            f"Under instructions from our Client, {sender_name}, residing at {sender_address} (Phone: {sender_phone})\n\n"
            f"SUBJECT: {template['title']}\n\n"
            f"Sir/Madam,\n\n"
            f"Under instructions and authority from my Client named above, I do hereby serve upon you this Statutory Legal Notice as under:\n\n"
            f"{substantive_clauses}\n\n"
            f"{demand_clause}\n\n"
            f"Copy retained in my chamber records for future legal proceedings.\n\n"
            f"Yours faithfully,\n\n"
            f"[{advocate_name}]\n"
            f"Advocate for the Complainant / Claimant"
        )

        return {
            "tracking_docket": tracking_docket,
            "notice_type": notice_type,
            "title": template["title"],
            "statute": template["statute"],
            "statutory_period_days": template["statutory_period_days"],
            "claim_amount_inr": claim_amount_inr,
            "sender_name": sender_name,
            "recipient_name": recipient_name,
            "formatted_notice_text": full_text,
            "consequences_note": template["consequences"],
            "dispatch_instructions": [
                "1. Print 2 copies on clean A4 bond paper.",
                "2. Sender and Advocate sign on every page at the bottom right.",
                "3. Dispatch 1 copy via Indian Speed Post or Registered Post AD (RPAD) from any Post Office.",
                "4. Keep the postal tracking receipt and yellow delivery acknowledgment slip safely as Court Exhibit A."
            ]
        }


class AgreementRiskEngine:
    """
    Analyzes Indian employment contracts, rental agreements, and freelance SOWs
    for statutory legal traps, void non-compete clauses, and arbitrary forfeiture terms.
    """

    @classmethod
    def analyze_agreement(cls, agreement_type: str, agreement_text: str) -> Dict[str, Any]:
        """
        Inspects agreement text against Indian Contract Act, 1872 & statutory precedent.
        """
        text_lower = agreement_text.lower()
        findings: List[Dict[str, Any]] = []
        overall_risk_score = 15  # baseline

        # 1. Non-Compete Check (Section 27 Indian Contract Act 1872)
        if any(term in text_lower for term in ["non-compete", "shall not work", "restraint of trade", "competing business", "post-termination"]):
            findings.append({
                "clause_name": "Post-Employment Non-Compete Clause",
                "severity": "CRITICAL_STATUTORY_VOID",
                "risk_points": 35,
                "statutory_analysis": (
                    "VOID UNDER SECTION 27 OF INDIAN CONTRACT ACT, 1872. The Supreme Court of India "
                    "(Percept D'Mark v. Zaheer Khan, Niranjan Shankar Golikari) has repeatedly ruled that "
                    "any negative covenant restraining an individual's right to work after termination is void and unenforceable in India."
                ),
                "actionable_fix": "You can safely sign or push to replace with a standard confidentiality and IP assignment clause."
            })
            overall_risk_score += 35

        # 2. Lock-In & Liquidated Damages Check
        if any(term in text_lower for term in ["lock in", "lock-in", "training bond", "liquidated damages", "employment bond"]):
            findings.append({
                "clause_name": "Arbitrary Lock-in / Training Bond",
                "severity": "HIGH_FINANCIAL_TRAP",
                "risk_points": 25,
                "statutory_analysis": (
                    "Section 74 of Indian Contract Act limits damages to reasonable actual losses proven by employer. "
                    "Courts do not enforce one-sided employment bond penalties unless the employer proves actual foreign/specialized training expense."
                ),
                "actionable_fix": "Request cap on bond repayment strictly limited to verified third-party training invoices with pro-rata deduction."
            })
            overall_risk_score += 25

        # 3. Notice Period Asymmetry Check
        if any(term in text_lower for term in ["immediate termination", "without notice", "90 days notice", "3 months notice"]):
            findings.append({
                "clause_name": "Asymmetrical Notice Period",
                "severity": "MEDIUM_UNFAIR_TERM",
                "risk_points": 15,
                "statutory_analysis": (
                    "Agreements allowing the employer/landlord to terminate immediately while forcing 60-90 days on the counterparty "
                    "are deemed unconscionable under natural justice principles."
                ),
                "actionable_fix": "Ensure bilateral notice parity (e.g. 30 days mutual notice on both sides)."
            })
            overall_risk_score += 15

        # 4. Security Deposit Forfeiture Check (Rental)
        if agreement_type == "rental" and any(term in text_lower for term in ["forfeit", "non-refundable deposit", "painting charge"]):
            findings.append({
                "clause_name": "Arbitrary Deposit Forfeiture & Painting Deduction",
                "severity": "HIGH_FINANCIAL_TRAP",
                "risk_points": 20,
                "statutory_analysis": (
                    "Under Model Tenancy Act, security deposits for residential premises cannot exceed 2 months' rent. "
                    "Deductions for normal wear & tear are illegal without actual repair receipts."
                ),
                "actionable_fix": "Insist on clause: 'Security deposit refundable within 7 days of handover minus only tenant-caused structural damage supported by tax invoices.'"
            })
            overall_risk_score += 20

        # 5. Jurisdiction Trap Check
        if any(term in text_lower for term in ["exclusive jurisdiction of courts in", "exclusive jurisdiction"]):
            findings.append({
                "clause_name": "Exclusive Distant Court Jurisdiction",
                "severity": "LOW_PROCEDURAL_NUISANCE",
                "risk_points": 10,
                "statutory_analysis": (
                    "Sections 20 & 28 Code of Civil Procedure (CPC): Parties cannot confer jurisdiction on a court "
                    "where no cause of action arose."
                ),
                "actionable_fix": "Ensure jurisdiction is set to your resident city / where work or property is situated."
            })
            overall_risk_score += 10

        overall_risk_score = min(100, overall_risk_score)
        if overall_risk_score >= 60:
            risk_badge = "🔴 HIGH RISK — Contains Unfavourable / Trap Clauses"
        elif overall_risk_score >= 35:
            risk_badge = "🟠 MODERATE RISK — Negotiate Specific Clauses"
        else:
            risk_badge = "🟢 LOW RISK — Standard Balanced Commercial Contract"

        return {
            "agreement_type": agreement_type,
            "overall_risk_score": overall_risk_score,
            "risk_score": overall_risk_score,
            "overall_risk_level": "severe" if overall_risk_score >= 60 else ("moderate" if overall_risk_score >= 35 else "clean"),
            "risk_badge": risk_badge,
            "total_clauses_flagged": len(findings),
            "findings": findings,
            "safe_counter_draft": (
                "Suggested Safe Counter-Clause: 'The Employee acknowledges proprietary obligations of "
                "confidentiality and IP assignment during and after employment; provided however, that "
                "nothing herein shall restrict Employee's right to pursue lawful employment under Section 27 "
                "of Indian Contract Act 1872.'"
            ),
            "indian_statutory_precedents": [
                "Section 27 Indian Contract Act, 1872 (Restraint of Trade)",
                "Section 74 Indian Contract Act, 1872 (Reasonable Compensation for Breach)",
                "Section 20 & 28 Code of Civil Procedure, 1908 (Territorial Jurisdiction)",
                "Supreme Court: Percept D'Mark (India) Pvt. Ltd. v. Zaheer Khan (2006) 4 SCC 227"
            ]
        }


class TaxRegimeEngine:
    """
    Accurately computes Indian Personal Income Tax under:
    1. New Tax Regime (Section 115BAC) for FY 2026-27 (Default Regime)
    2. Old Tax Regime with all Chapter VI-A deductions (80C, 80D, 24(b), HRA 10(13A))
    """

    @classmethod
    def compare_tax_regimes(
        cls,
        gross_annual_income: float,
        deduction_80c: float = 150000.0,
        deduction_80d: float = 25000.0,
        home_loan_interest_24b: float = 0.0,
        hra_exemption_10_13a: float = 0.0,
        other_deductions_chapter_via: float = 0.0
    ) -> Dict[str, Any]:
        """
        Side-by-side comparison of New vs Old Tax Regime liability.
        """
        # ----------------- NEW TAX REGIME (Section 115BAC) -----------------
        # Standard deduction for salaried in New Regime is Rs. 75,000
        new_standard_deduction = 75000.0 if gross_annual_income > 75000.0 else gross_annual_income
        new_taxable_income = max(0.0, gross_annual_income - new_standard_deduction)

        # FY 2025-26 / FY 2026-27 New Slabs:
        # 0 to 3,00,000: Nil
        # 3,00,001 to 7,00,000: 5%
        # 7,00,001 to 10,00,000: 10%
        # 10,00,001 to 12,00,000: 15%
        # 12,00,001 to 15,00,000: 20%
        # Above 15,00,000: 30%
        new_tax = 0.0
        if new_taxable_income > 1500000.0:
            new_tax += (new_taxable_income - 1500000.0) * 0.30
            new_tax += 300000.0 * 0.20  # 12L to 15L
            new_tax += 200000.0 * 0.15  # 10L to 12L
            new_tax += 300000.0 * 0.10  # 7L to 10L
            new_tax += 400000.0 * 0.05  # 3L to 7L
        elif new_taxable_income > 1200000.0:
            new_tax += (new_taxable_income - 1200000.0) * 0.20
            new_tax += 200000.0 * 0.15
            new_tax += 300000.0 * 0.10
            new_tax += 400000.0 * 0.05
        elif new_taxable_income > 1000000.0:
            new_tax += (new_taxable_income - 1000000.0) * 0.15
            new_tax += 300000.0 * 0.10
            new_tax += 400000.0 * 0.05
        elif new_taxable_income > 700000.0:
            new_tax += (new_taxable_income - 700000.0) * 0.10
            new_tax += 400000.0 * 0.05
        elif new_taxable_income > 300000.0:
            new_tax += (new_taxable_income - 300000.0) * 0.05

        # Section 87A Rebate under New Regime: 100% tax rebate if taxable income <= 7,00,000
        if new_taxable_income <= 700000.0:
            new_tax = 0.0

        new_cess = round(new_tax * 0.04, 2)
        total_new_tax = round(new_tax + new_cess, 2)

        # ----------------- OLD TAX REGIME -----------------
        old_standard_deduction = 50000.0 if gross_annual_income > 50000.0 else gross_annual_income
        capped_80c = min(150000.0, deduction_80c)
        capped_80d = min(100000.0, deduction_80d)
        capped_24b = min(200000.0, home_loan_interest_24b)

        total_old_deductions = (
            old_standard_deduction + capped_80c + capped_80d +
            capped_24b + hra_exemption_10_13a + other_deductions_chapter_via
        )
        old_taxable_income = max(0.0, gross_annual_income - total_old_deductions)

        # Old Slabs:
        # 0 to 2,50,000: Nil
        # 2,50,001 to 5,00,000: 5%
        # 5,00,001 to 10,00,000: 20%
        # Above 10,00,000: 30%
        old_tax = 0.0
        if old_taxable_income > 1000000.0:
            old_tax += (old_taxable_income - 1000000.0) * 0.30
            old_tax += 500000.0 * 0.20
            old_tax += 250000.0 * 0.05
        elif old_taxable_income > 500000.0:
            old_tax += (old_taxable_income - 500000.0) * 0.20
            old_tax += 250000.0 * 0.05
        elif old_taxable_income > 250000.0:
            old_tax += (old_taxable_income - 250000.0) * 0.05

        # Section 87A Rebate under Old Regime: Tax rebate if taxable income <= 5,00,000
        if old_taxable_income <= 500000.0:
            old_tax = 0.0

        old_cess = round(old_tax * 0.04, 2)
        total_old_tax = round(old_tax + old_cess, 2)

        # Delta & Recommendation
        tax_saved = round(abs(total_new_tax - total_old_tax), 2)
        if total_new_tax < total_old_tax:
            better_regime = "NEW_REGIME"
            recommendation = (
                f"CHOOSE NEW REGIME (Section 115BAC): You save ₹{tax_saved:,.0f} in taxes! "
                f"No need to lock funds in tax-saving instruments or submit rent receipts."
            )
        elif total_old_tax < total_new_tax:
            better_regime = "OLD_REGIME"
            recommendation = (
                f"CHOOSE OLD REGIME: Your substantial deductions (80C, 80D, HRA, Home Loan) "
                f"save you ₹{tax_saved:,.0f} compared to the new regime."
            )
        else:
            better_regime = "EQUAL"
            recommendation = "Both regimes yield identical tax liability. The New Regime is simpler with zero paperwork."

        return {
            "recommended_regime": better_regime.lower(),
            "tax_savings": tax_saved,
            "gross_annual_income_inr": gross_annual_income,
            "new_regime": {
                "standard_deduction_inr": new_standard_deduction,
                "total_deductions_inr": new_standard_deduction,
                "net_taxable_income_inr": new_taxable_income,
                "base_tax_inr": round(new_tax, 2),
                "cess_inr": new_cess,
                "total_tax_payable_inr": total_new_tax,
                "effective_tax_rate_pct": round((total_new_tax / gross_annual_income * 100), 2) if gross_annual_income > 0 else 0.0
            },
            "old_regime": {
                "standard_deduction_inr": old_standard_deduction,
                "deduction_80c_inr": capped_80c,
                "deduction_80d_inr": capped_80d,
                "home_loan_24b_inr": capped_24b,
                "hra_exemption_inr": hra_exemption_10_13a,
                "other_chapter_via_inr": other_deductions_chapter_via,
                "total_deductions_inr": total_old_deductions,
                "net_taxable_income_inr": old_taxable_income,
                "base_tax_inr": round(old_tax, 2),
                "cess_inr": old_cess,
                "total_tax_payable_inr": total_old_tax,
                "effective_tax_rate_pct": round((total_old_tax / gross_annual_income * 100), 2) if gross_annual_income > 0 else 0.0
            },
            "comparison": {
                "recommended_regime": better_regime,
                "net_tax_saved_inr": tax_saved,
                "recommendation_verdict": recommendation
            }
        }


class PresumptiveTaxEngine:
    """
    Computes Section 44ADA Presumptive Taxation for specified professionals.
    """

    @classmethod
    def calculate_44ada(
        cls,
        gross_professional_receipts: float,
        actual_business_expenses: float = 0.0
    ) -> Dict[str, Any]:
        """
        Under Section 44ADA:
        - Eligible if gross receipts <= Rs. 75 Lakhs (with >= 95% digital receipts).
        - Deemed professional income is fixed at minimum 50% of gross receipts.
        - Zero requirement to maintain books of accounts (Section 44AA) or get audit (Section 44AB).
        """
        is_eligible = gross_professional_receipts <= 7500000.0
        deemed_taxable_profit = round(gross_professional_receipts * 0.50, 2)

        # Tax under Section 44ADA (using New Regime slabs)
        tax_res_44ada = TaxRegimeEngine.compare_tax_regimes(deemed_taxable_profit)
        presumptive_tax = tax_res_44ada["new_regime"]["total_tax_payable_inr"]

        # Tax under normal accounting (actual receipts minus actual expenses)
        actual_net_profit = max(0.0, gross_professional_receipts - actual_business_expenses)
        tax_res_normal = TaxRegimeEngine.compare_tax_regimes(actual_net_profit)
        normal_tax = tax_res_normal["new_regime"]["total_tax_payable_inr"]

        ca_audit_fee_saved = 25000.0  # approximate CA audit and accounting retainer fee
        net_compliance_benefit = round(ca_audit_fee_saved + max(0.0, normal_tax - presumptive_tax), 2)

        return {
            "eligible": is_eligible,
            "deemed_profit": deemed_taxable_profit,
            "tax_payable": presumptive_tax,
            "gross_receipts_inr": gross_professional_receipts,
            "is_eligible_under_75_lakhs": is_eligible,
            "deemed_taxable_profit_inr": deemed_taxable_profit,
            "presumptive_tax_payable_inr": presumptive_tax,
            "actual_expenses_inr": actual_business_expenses,
            "actual_profit_under_books_inr": actual_net_profit,
            "normal_tax_payable_inr": normal_tax,
            "ca_audit_fee_eliminated_inr": ca_audit_fee_saved,
            "net_annual_financial_benefit_inr": net_compliance_benefit,
            "compliance_advantages": [
                "1. Zero requirement to maintain formal books of accounts (Ledgers, Cash Books, Invoices) under Section 44AA.",
                "2. 100% exemption from mandatory Chartered Accountant Tax Audit under Section 44AB.",
                "3. Pay advance tax in a single annual installment by 15th March instead of quarterly installments.",
                "4. High scrutiny immunity: Department cannot question actual expenditure below the 50% deemed threshold."
            ]
        }


class NoticeExplainerEngine:
    """
    Decodes Income Tax notices and outlines statutory response timelines and penalty mitigation.
    """

    NOTICES: Dict[str, Dict[str, Any]] = {
        "143_1": {
            "section": "Section 143(1)",
            "title": "Intimation / Summary Assessment Notice",
            "statutory_meaning": "The Income Tax Department has processed your return and matched it against Form 26AS, AIS, and TIS.",
            "common_causes": [
                "Arithmetic errors in computation of total income",
                "Mismatch between TDS claimed in ITR and TDS deposited in Form 26AS / AIS",
                "Incorrect claim of Chapter VI-A deduction or standard deduction"
            ],
            "severity": "LOW_TO_MEDIUM",
            "deadline_days": 30,
            "resolution_action": "Verify if demand is correct. If correct, pay tax via e-Pay Tax. If mismatch, file Rectification Application under Section 154 within 30 days."
        },
        "139_9": {
            "section": "Section 139(9)",
            "title": "Defective Return Notice",
            "statutory_meaning": "Your filed ITR contains structural defects or omissions preventing full processing.",
            "common_causes": [
                "Gross receipts reported in Profit & Loss do not match AIS turnover",
                "Taxes paid but BSR code / Challan serial number entered incorrectly",
                "Mandatory Balance Sheet or Auditor details left blank in ITR-3/ITR-4"
            ],
            "severity": "HIGH_URGENCY",
            "deadline_days": 15,
            "resolution_action": "Log in to incometax.gov.in -> e-Proceedings -> Defective Notice. Submit response by selecting 'Agree' and uploading corrected JSON within 15 days."
        },
        "148": {
            "section": "Section 148 / 148A",
            "title": "Reopening of Assessment / Income Escaping Assessment",
            "statutory_meaning": "Assessing Officer has 'information suggesting income chargeable to tax has escaped assessment'.",
            "common_causes": [
                "High-value property purchase / cash deposit flagged in SFT report",
                "Stock trading or crypto transaction not declared in original return",
                "Mismatch between passport foreign remittance and reported income"
            ],
            "severity": "CRITICAL_LEGAL_PROCEEDING",
            "deadline_days": 30,
            "resolution_action": "Strictly review Section 148A(b) show-cause notice. Draft point-by-point factual reply with bank statements and source of funds to prevent reassessment order."
        },
        "156": {
            "section": "Section 156",
            "title": "Notice of Demand",
            "statutory_meaning": "Official formal order demanding payment of specified tax, interest, or penalty.",
            "common_causes": [
                "Post-assessment demand following Section 143(3) scrutiny or 143(1) adjustment"
            ],
            "severity": "HIGH_FINANCIAL",
            "deadline_days": 30,
            "resolution_action": "Pay demand within 30 days to avoid 1% per month interest under Section 220(2) and penalty under Section 221."
        }
    }

    @classmethod
    def explain_notice(cls, section_code: str) -> Dict[str, Any]:
        """Returns plain-English diagnosis and resolution checklist."""
        code = section_code.replace("(", "").replace(")", "").replace("/", "_").strip()
        notice_info = cls.NOTICES.get(code, cls.NOTICES["143_1"])
        return {
            "section_code": notice_info["section"],
            "title": notice_info["title"],
            "statutory_meaning": notice_info["statutory_meaning"],
            "severity": notice_info["severity"],
            "reply_deadline_days": notice_info["deadline_days"],
            "common_causes": notice_info["common_causes"],
            "resolution_action": notice_info["resolution_action"],
            "statutory_shield_advisory": (
                "Do not ignore this notice. Failure to respond within statutory deadlines empowers the "
                "Assessing Officer to finalize 'Best Judgment Assessment' under Section 144."
            )
        }
