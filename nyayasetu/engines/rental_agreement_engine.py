"""
Model Tenancy Act (MTA) 2021 Rental Agreement & Compliance Diagnostic Engine
Zero-cost legal drafting and statutory audit for residential & commercial leases in India.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

STATE_STAMP_RULES = {
    "MH": {"name": "Maharashtra", "flat_e_stamp": 1000, "rate_pct": 0.25, "notes": "Bombay Stamp Act Art 36A: 0.25% of total rent + deposit, min Rs. 1,000"},
    "KA": {"name": "Karnataka", "flat_e_stamp": 200, "rate_pct": 0.5, "notes": "Karnataka Stamp Act: 0.5% of annual rent or min Rs. 200 e-stamp"},
    "DL": {"name": "Delhi NCR", "flat_e_stamp": 100, "rate_pct": 2.0, "notes": "Indian Stamp (Delhi) Act: 2% for <= 5 yrs, min Rs. 100 e-stamp"},
    "UP": {"name": "Uttar Pradesh", "flat_e_stamp": 100, "rate_pct": 2.0, "notes": "UP Stamp Act: 2% of avg annual rent for <= 11 months"},
    "TN": {"name": "Tamil Nadu", "flat_e_stamp": 100, "rate_pct": 1.0, "notes": "TN Regulation of Rights and Responsibilities Act 2017: 1% stamp duty"},
    "TS": {"name": "Telangana", "flat_e_stamp": 100, "rate_pct": 0.5, "notes": "TS Stamp Act: 0.5% of total rent payable"},
    "GJ": {"name": "Gujarat", "flat_e_stamp": 300, "rate_pct": 1.0, "notes": "Gujarat Stamp Act: 1% of annual rent value"},
    "WB": {"name": "West Bengal", "flat_e_stamp": 100, "rate_pct": 1.0, "notes": "WB Stamp Rules: 1% of total rent payable"},
    "OTHER": {"name": "Other States", "flat_e_stamp": 100, "rate_pct": 1.0, "notes": "Standard Indian Stamp Act model schedule"}
}

class RentalAgreementEngine:
    @staticmethod
    def audit_and_generate(
        landlord_name: str,
        landlord_address: str,
        tenant_name: str,
        tenant_address: str,
        property_address: str,
        monthly_rent: float,
        security_deposit: float,
        tenure_months: int = 11,
        property_type: str = "residential",
        state: str = "MH",
        notice_period_days: int = 30,
        inspection_notice_hrs: int = 24,
        annual_escalation_pct: float = 5.0,
        maintenance_charges: float = 0.0,
        maintenance_payer: str = "tenant"
    ) -> Dict[str, Any]:
        """
        Audits terms against Model Tenancy Act 2021 rules and drafts full compliant agreement.
        """
        state_code = state.upper() if state.upper() in STATE_STAMP_RULES else "OTHER"
        state_info = STATE_STAMP_RULES[state_code]

        violations: List[Dict[str, str]] = []

        # 1. MTA Section 11(1): Security Deposit Cap
        if property_type.lower() == "residential":
            max_legal_deposit = monthly_rent * 2.0
            if security_deposit > max_legal_deposit:
                violations.append({
                    "section": "Section 11(1), Model Tenancy Act 2021",
                    "severity": "HIGH",
                    "title": "Excess Security Deposit (Statutory Cap Breached)",
                    "detail": f"Demanded ?{security_deposit:,.0f}. MTA 2021 strictly caps residential security deposit at a maximum of 2 months' rent (?{max_legal_deposit:,.0f}). Excess ?{security_deposit - max_legal_deposit:,.0f} is illegal under MTA.",
                    "remedy": f"Reduce security deposit to ?{max_legal_deposit:,.0f} or refund difference upon agreement execution."
                })
        else:
            max_legal_deposit = monthly_rent * 6.0
            if security_deposit > max_legal_deposit:
                violations.append({
                    "section": "Section 11(2), Model Tenancy Act 2021",
                    "severity": "HIGH",
                    "title": "Commercial Security Deposit Cap Exceeded",
                    "detail": f"Demanded ?{security_deposit:,.0f}. MTA caps commercial security deposit at 6 months' rent (?{max_legal_deposit:,.0f}).",
                    "remedy": f"Cap deposit at ?{max_legal_deposit:,.0f}."
                })

        # 2. MTA Section 15: Inspection Notice
        if inspection_notice_hrs < 24:
            violations.append({
                "section": "Section 15, Model Tenancy Act 2021",
                "severity": "MEDIUM",
                "title": "Insufficient Inspection Notice Window",
                "detail": f"Proposed {inspection_notice_hrs} hours. MTA mandates landlord/property manager must give at least 24 hours advance written notice before entering premises.",
                "remedy": "Enforce minimum 24 hours prior written notice between 7:00 AM and 8:00 PM."
            })

        # 3. Notice Period Audit
        if notice_period_days < 30:
            violations.append({
                "section": "Section 21 & Transfer of Property Act Sec 106",
                "severity": "MEDIUM",
                "title": "Sub-Statutory Eviction / Termination Notice",
                "detail": f"Proposed {notice_period_days} days. Indian tenancy jurisprudence requires minimum 30 days statutory written notice for termination without cause.",
                "remedy": "Amend termination notice period to at least 30 days."
            })

        # 4. Stamp Duty & Registration Calculation
        total_rent_period = monthly_rent * tenure_months
        calc_base = total_rent_period + (security_deposit * 0.10)
        stamp_duty_est = max(state_info["flat_e_stamp"], calc_base * (state_info["rate_pct"] / 100.0))
        reg_fee_est = 1000.0 if tenure_months <= 11 else 2000.0

        is_mta_compliant = len([v for v in violations if v["severity"] == "HIGH"]) == 0
        score = max(0, 100 - (len(violations) * 25))

        agreement_text = RentalAgreementEngine._draft_deed_text(
            landlord_name=landlord_name,
            landlord_address=landlord_address,
            tenant_name=tenant_name,
            tenant_address=tenant_address,
            property_address=property_address,
            monthly_rent=monthly_rent,
            security_deposit=min(security_deposit, monthly_rent * 2.0) if property_type == "residential" else security_deposit,
            tenure_months=tenure_months,
            property_type=property_type,
            state_name=state_info["name"],
            notice_period_days=max(30, notice_period_days),
            inspection_notice_hrs=max(24, inspection_notice_hrs),
            annual_escalation_pct=annual_escalation_pct,
            maintenance_charges=maintenance_charges,
            maintenance_payer=maintenance_payer
        )

        return {
            "is_mta_compliant": is_mta_compliant,
            "compliance_score": score,
            "violations_count": len(violations),
            "violations": violations,
            "stamp_duty_estimate": {
                "state": state_info["name"],
                "stamp_duty": round(stamp_duty_est, 2),
                "registration_fee": round(reg_fee_est, 2),
                "total_statutory_cost": round(stamp_duty_est + reg_fee_est, 2),
                "legal_basis": state_info["notes"]
            },
            "mta_statutory_safeguards": [
                "Section 11: Security deposit strictly capped at maximum 2 months' rent for residential premises.",
                "Section 15: Mandatory minimum 24 hours prior written notice before landlord entry (between 7am and 8pm).",
                "Section 20: Essential services (water, electricity, lift) CANNOT be disconnected under any dispute.",
                "Section 23: Tenant overstaying without renewal liable to pay 2x rent for first 2 months, 4x rent thereafter.",
                "Schedule II: Clear division between structural repairs (Landlord) and consumable wear (Tenant)."
            ],
            "agreement_markdown": agreement_text
        }

    @staticmethod
    def _draft_deed_text(
        landlord_name: str,
        landlord_address: str,
        tenant_name: str,
        tenant_address: str,
        property_address: str,
        monthly_rent: float,
        security_deposit: float,
        tenure_months: int,
        property_type: str,
        state_name: str,
        notice_period_days: int,
        inspection_notice_hrs: int,
        annual_escalation_pct: float,
        maintenance_charges: float,
        maintenance_payer: str
    ) -> str:
        today_str = datetime.now().strftime("%d day of %B, %Y")
        monthly_rent_str = f"Rs. {monthly_rent:,.2f}"
        security_deposit_str = f"Rs. {security_deposit:,.2f}"
        maintenance_str = f"Rs. {maintenance_charges:,.2f}"

        return f"""# RESIDENTIAL / COMMERCIAL LEASE AGREEMENT
*(Drafted in compliance with Model Tenancy Act, 2021 & Indian Contract Act, 1872)*

This LEASE AGREEMENT is executed on this **{today_str}** at **{state_name}**, India:

### BETWEEN:
**{landlord_name}**, residing at {landlord_address} (hereinafter referred to as the **"LESSOR / LANDLORD"**, which expression shall include legal heirs, executors, and assigns) of the **FIRST PART**;

### AND:
**{tenant_name}**, residing at {tenant_address} (hereinafter referred to as the **"LESSEE / TENANT"**, which expression shall include legal heirs and assigns) of the **SECOND PART**.

---

### WHEREAS:
1. The Lessor is the absolute lawful owner in possession of the premises situated at:
   **{property_address}** (hereinafter referred to as the **"DEMISED PREMISES"**).
2. The Lessee has approached the Lessor to take on lease the Demised Premises for **{property_type.upper()}** use for a period of **{tenure_months} months**.

---

### NOW THIS AGREEMENT WITNESSETH AND PARTIES AGREE AS FOLLOWS:

#### 1. TENURE & COMMENCEMENT
The lease shall be in force for an agreed term of **{tenure_months} months** commencing from the date of handover of possession.

#### 2. MONTHLY RENT & ESCALATION
- The Lessee shall pay to the Lessor a monthly rent of **{monthly_rent_str}**.
- Rent is payable on or before the 5th day of every English calendar month via electronic NEFT/RTGS/UPI.
- An annual escalation rate of **{annual_escalation_pct}%** shall apply upon renewal beyond 11 months as mutually consented in writing.

#### 3. STATUTORY SECURITY DEPOSIT (SEC 11 MTA 2021)
- The Lessee has deposited with the Lessor an interest-free refundable security deposit of **{security_deposit_str}**.
- *(Strictly adhering to Section 11 of Model Tenancy Act 2021 cap of maximum 2 months rent for residential premises).*
- The full security deposit shall be refunded to the Lessee simultaneously upon handover of vacant possession, subject only to deductions for unpaid utility bills or actual physical damages beyond normal fair wear and tear.

#### 4. MAINTENANCE & OUTGOINGS (SCHEDULE II MTA 2021)
- Monthly society/maintenance charges of **{maintenance_str}** shall be borne by the **{maintenance_payer.upper()}**.
- **Lessor Responsibility**: Structural repairs, foundation, roof leakages, external wall dampness, and main electrical/plumbing distribution.
- **Lessee Responsibility**: Day-to-day internal cleaning, light bulbs, tap washers, minor geyser servicing, and routine drain clearing.

#### 5. RIGHT OF ENTRY & INSPECTION (SEC 15 MTA 2021)
The Lessor or their authorized agent shall have the right to inspect the Demised Premises only after giving at least **{inspection_notice_hrs} hours prior written notice** (SMS/WhatsApp/Email valid), and such inspection shall take place strictly between 7:00 AM and 8:00 PM.

#### 6. UNINTERRUPTED ESSENTIAL SERVICES (SEC 20 MTA 2021)
Under Section 20 of the Model Tenancy Act 2021, the Lessor covenants NOT to withhold, disconnect, or tamper with essential supplies and services including water, electricity, and lift access, even in the event of dispute over rent.

#### 7. TERMINATION & OVERSTAY PENALTY (SEC 23 MTA 2021)
- Either party may terminate this agreement by providing **{notice_period_days} days advance written notice** to the other party.
- If the Lessee fails to vacate upon lawful termination or expiry, under Section 23 of MTA 2021, the Lessee shall be liable to pay **double the monthly rent** for the first two months, and **four times the monthly rent** for every month thereafter until vacant possession is delivered.

#### 8. JURISDICTION & DISPUTE RESOLUTION
This agreement is governed by the laws of India and the competent Rent Tribunal / Civil Courts having jurisdiction over {state_name}.

---

**IN WITNESS WHEREOF**, the Lessor and Lessee have signed this Lease Deed on the date and year first above written.

**LESSOR / LANDLORD:**
Signature: __________________________   
Name: **{landlord_name}**
Date: __________________________

**LESSEE / TENANT:**
Signature: __________________________   
Name: **{tenant_name}**
Date: __________________________

**WITNESS 1:** __________________________      **WITNESS 2:** __________________________
"""
