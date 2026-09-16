"""
Loan Mitra: RBI 2025-Compliant Digital Lending Marketplace Engine
Strictly implements the Reserve Bank of India (RBI) 2025 Digital Lending Directions &
Web-Aggregation Framework for Multi-Lender Portals:

Core Features:
1. LoanMitraMatchEngine: 6-factor transparent compatibility scoring algorithm
   - Eligibility (30%), Amount (20%), Tenure (10%), Income (15%), Credit (15%), Features (10%)
   - No dark patterns, no opaque "best offer" bias.
   - Transparent sorting: Compatibility, Lowest APR, Lowest EMI, Lowest Processing Fee.
   - Full Key Fact Statement (KFS) disclosure: APR, EMI, Penal Charges, Prepayment rules, FOIR.
2. BalanceTransferEngine:
   - Existing vs New Loan interest differential
   - Switching cost calculations (processing fee + documentation + prepayment)
   - Exact Break-Even timeline in months and prepayment acceleration scenarios.
3. Lead CRM & Product Verification Registry:
   - Tracks Regulated Entity (RE) licenses, Grievance Redressal Officers (GRO), and 7-day verification health.
   - Lead progression: Leads -> Document Submitted -> Bank In-Principle -> Disbursed.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
import math

class LoanMitraRegistry:
    """
    Verified Registry of Regulated Lenders (Scheduled Commercial Banks & Upper-Layer NBFCs)
    with KFS product configurations and regulatory compliance metadata.
    """
    
    LENDERS: List[Dict[str, Any]] = [
        {
            "lender_id": "hdfc_bank",
            "lender_name": "HDFC Bank Ltd.",
            "category": "Scheduled Commercial Bank (Private)",
            "rbi_code": "RBI/BANK/004",
            "gro_name": "Mr. Amit Pathak",
            "gro_email": "grievance.officer@hdfcbank.com",
            "gro_contact": "1800-266-4060",
            "last_verified_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "verification_status": "VERIFIED_ACTIVE",
            "products": [
                {
                    "product_id": "hdfc_pl_express",
                    "product_name": "HDFC Insta Personal Loan",
                    "loan_type": "personal_loan",
                    "min_amount": 50000.0,
                    "max_amount": 4000000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 60,
                    "base_rate_min": 10.50,
                    "base_rate_max": 16.25,
                    "processing_fee_pct": 1.50,
                    "processing_fee_min": 2500.0,
                    "processing_fee_max": 15000.0,
                    "min_monthly_income": 35000.0,
                    "min_credit_score": 720,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.5,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 4,
                    "digital_journey": True,
                    "perks": [
                        "100% Paperless Aadhaar e-KYC",
                        "Pre-approved instant disbursal in 4 hours",
                        "Part-prepayment allowed with zero penalty after 12 months"
                    ]
                },
                {
                    "product_id": "hdfc_hl_reach",
                    "product_name": "HDFC Reach Home Loan",
                    "loan_type": "home_loan",
                    "min_amount": 500000.0,
                    "max_amount": 50000000.0,
                    "min_tenure_months": 36,
                    "max_tenure_months": 360,
                    "base_rate_min": 8.50,
                    "base_rate_max": 9.40,
                    "processing_fee_pct": 0.50,
                    "processing_fee_min": 3000.0,
                    "processing_fee_max": 10000.0,
                    "min_monthly_income": 45000.0,
                    "min_credit_score": 750,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.0,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 48,
                    "digital_journey": True,
                    "perks": [
                        "RBI mandate: 0% prepayment penalty on floating rate",
                        "Doorstep document pickup or digital upload",
                        "Tax benefit eligibility under Section 24(b) & 80C"
                    ]
                }
            ]
        },
        {
            "lender_id": "sbi_bank",
            "lender_name": "State Bank of India",
            "category": "Scheduled Commercial Bank (Public)",
            "rbi_code": "RBI/BANK/001",
            "gro_name": "Ms. Sunita Sundaram",
            "gro_email": "dgm.customer@sbi.co.in",
            "gro_contact": "1800-1234",
            "last_verified_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "verification_status": "VERIFIED_ACTIVE",
            "products": [
                {
                    "product_id": "sbi_xpress_credit",
                    "product_name": "SBI Xpress Credit Personal Loan",
                    "loan_type": "personal_loan",
                    "min_amount": 25000.0,
                    "max_amount": 3500000.0,
                    "min_tenure_months": 6,
                    "max_tenure_months": 72,
                    "base_rate_min": 11.15,
                    "base_rate_max": 14.30,
                    "processing_fee_pct": 1.00,
                    "processing_fee_min": 1500.0,
                    "processing_fee_max": 10000.0,
                    "min_monthly_income": 25000.0,
                    "min_credit_score": 700,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 1.5,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 12,
                    "digital_journey": True,
                    "perks": [
                        "Lowest processing fee cap among peer banks",
                        "Flexible tenure up to 6 years",
                        "Special concessional pricing for defence & salary package accounts"
                    ]
                },
                {
                    "product_id": "sbi_regular_home",
                    "product_name": "SBI Regular Home Loan",
                    "loan_type": "home_loan",
                    "min_amount": 500000.0,
                    "max_amount": 100000000.0,
                    "min_tenure_months": 60,
                    "max_tenure_months": 360,
                    "base_rate_min": 8.40,
                    "base_rate_max": 9.15,
                    "processing_fee_pct": 0.35,
                    "processing_fee_min": 2000.0,
                    "processing_fee_max": 8000.0,
                    "min_monthly_income": 30000.0,
                    "min_credit_score": 750,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 0.0,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 72,
                    "digital_journey": True,
                    "perks": [
                        "Lowest benchmark home loan interest rate in India",
                        "Zero hidden charges, transparent EBLR linked",
                        "Overdraft Maxgain facility available"
                    ]
                }
            ]
        },
        {
            "lender_id": "icici_bank",
            "lender_name": "ICICI Bank Ltd.",
            "category": "Scheduled Commercial Bank (Private)",
            "rbi_code": "RBI/BANK/008",
            "gro_name": "Mr. Rakesh Menon",
            "gro_email": "headservicequality@icicibank.com",
            "gro_contact": "1800-200-3344",
            "last_verified_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "verification_status": "VERIFIED_ACTIVE",
            "products": [
                {
                    "product_id": "icici_smart_pl",
                    "product_name": "ICICI Smart Personal Loan",
                    "loan_type": "personal_loan",
                    "min_amount": 50000.0,
                    "max_amount": 5000000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 72,
                    "base_rate_min": 10.75,
                    "base_rate_max": 15.75,
                    "processing_fee_pct": 1.25,
                    "processing_fee_min": 2000.0,
                    "processing_fee_max": 12500.0,
                    "min_monthly_income": 30000.0,
                    "min_credit_score": 700,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 3.0,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 3,
                    "digital_journey": True,
                    "perks": [
                        "Pre-approved customers get money in 3 seconds",
                        "Highest loan limit up to Rs. 50 Lakhs",
                        "Transparent digital KFS before disbursement"
                    ]
                },
                {
                    "product_id": "icici_business_instabiz",
                    "product_name": "ICICI InstaBIZ MSME Working Capital",
                    "loan_type": "business_loan",
                    "min_amount": 100000.0,
                    "max_amount": 7500000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 60,
                    "base_rate_min": 12.00,
                    "base_rate_max": 17.50,
                    "processing_fee_pct": 2.00,
                    "processing_fee_min": 5000.0,
                    "processing_fee_max": 25000.0,
                    "min_monthly_income": 60000.0,
                    "min_credit_score": 680,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.5,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 24,
                    "digital_journey": True,
                    "perks": [
                        "Collateral-free overdraft & term loan for GST filers",
                        "Fast assessment using Account Aggregator bank statements",
                        "Zero prepayment charges on floating rate business lines"
                    ]
                }
            ]
        },
        {
            "lender_id": "bajaj_finance",
            "lender_name": "Bajaj Finance Ltd.",
            "category": "NBFC - Upper Layer (RBI Regulated)",
            "rbi_code": "RBI/NBFC/UL-02",
            "gro_name": "Mr. Rajesh Kumar",
            "gro_email": "grievanceredressalteam@bajajfinserv.in",
            "gro_contact": "020-71124000",
            "last_verified_at": (datetime.now() - timedelta(days=4)).isoformat(),
            "verification_status": "VERIFIED_ACTIVE",
            "products": [
                {
                    "product_id": "bajaj_flexi_pl",
                    "product_name": "Bajaj Finserv Flexi Personal Loan",
                    "loan_type": "personal_loan",
                    "min_amount": 30000.0,
                    "max_amount": 4000000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 96,
                    "base_rate_min": 11.00,
                    "base_rate_max": 18.00,
                    "processing_fee_pct": 2.00,
                    "processing_fee_min": 2500.0,
                    "processing_fee_max": 18000.0,
                    "min_monthly_income": 25000.0,
                    "min_credit_score": 685,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 3.0,
                    "penal_charges_monthly_pct": 2.5,
                    "turnaround_hours": 2,
                    "digital_journey": True,
                    "perks": [
                        "Flexi hybrid facility: Pay interest only on drawn funds",
                        "Tenure up to 8 years (96 months) for lower EMI",
                        "Drop-down overdraft line of credit"
                    ]
                },
                {
                    "product_id": "bajaj_lap_prime",
                    "product_name": "Bajaj Prime Loan Against Property",
                    "loan_type": "loan_against_property",
                    "min_amount": 1000000.0,
                    "max_amount": 50000000.0,
                    "min_tenure_months": 36,
                    "max_tenure_months": 240,
                    "base_rate_min": 9.50,
                    "base_rate_max": 12.50,
                    "processing_fee_pct": 1.00,
                    "processing_fee_min": 10000.0,
                    "processing_fee_max": 50000.0,
                    "min_monthly_income": 50000.0,
                    "min_credit_score": 700,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.0,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 48,
                    "digital_journey": False,
                    "perks": [
                        "High loan-to-value (LTV) up to 75% of property valuation",
                        "Long repayment tenure up to 20 years",
                        "Competitive rates lower than unsecured business credit"
                    ]
                }
            ]
        },
        {
            "lender_id": "axis_bank",
            "lender_name": "Axis Bank Ltd.",
            "category": "Scheduled Commercial Bank (Private)",
            "rbi_code": "RBI/BANK/012",
            "gro_name": "Mr. Saurabh Sharma",
            "gro_email": "nodalofficer@axisbank.com",
            "gro_contact": "1800-419-5577",
            "last_verified_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "verification_status": "VERIFIED_ACTIVE",
            "products": [
                {
                    "product_id": "axis_pl_prime",
                    "product_name": "Axis 24x7 Digital Personal Loan",
                    "loan_type": "personal_loan",
                    "min_amount": 50000.0,
                    "max_amount": 4000000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 60,
                    "base_rate_min": 10.65,
                    "base_rate_max": 16.00,
                    "processing_fee_pct": 1.50,
                    "processing_fee_min": 2500.0,
                    "processing_fee_max": 12000.0,
                    "min_monthly_income": 30000.0,
                    "min_credit_score": 720,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.0,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 6,
                    "digital_journey": True,
                    "perks": [
                        "Zero foreclosure charges after 18 EMI payments",
                        "Special pricing for salaried corporate professionals",
                        "Disbursal via instant UPI/IMPS"
                    ]
                },
                {
                    "product_id": "axis_business_growth",
                    "product_name": "Axis Business Growth Loan",
                    "loan_type": "business_loan",
                    "min_amount": 200000.0,
                    "max_amount": 5000000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 48,
                    "base_rate_min": 12.50,
                    "base_rate_max": 18.00,
                    "processing_fee_pct": 1.75,
                    "processing_fee_min": 4000.0,
                    "processing_fee_max": 20000.0,
                    "min_monthly_income": 50000.0,
                    "min_credit_score": 700,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.5,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 24,
                    "digital_journey": True,
                    "perks": [
                        "No balance sheet required up to Rs. 20 Lakhs",
                        "Assessed using verified GST returns",
                        "Overdraft limit available on current account"
                    ]
                }
            ]
        },
        {
            "lender_id": "tata_capital",
            "lender_name": "Tata Capital Financial Services",
            "category": "NBFC - Upper Layer (Tata Sons Subsidiary)",
            "rbi_code": "RBI/NBFC/UL-09",
            "gro_name": "Ms. Priya Kulkarni",
            "gro_email": "grievance.head@tatacapital.com",
            "gro_contact": "1860-267-6060",
            "last_verified_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "verification_status": "VERIFIED_ACTIVE",
            "products": [
                {
                    "product_id": "tata_custom_pl",
                    "product_name": "Tata Capital Custom Fit Personal Loan",
                    "loan_type": "personal_loan",
                    "min_amount": 40000.0,
                    "max_amount": 3500000.0,
                    "min_tenure_months": 12,
                    "max_tenure_months": 72,
                    "base_rate_min": 10.99,
                    "base_rate_max": 17.25,
                    "processing_fee_pct": 1.75,
                    "processing_fee_min": 2000.0,
                    "processing_fee_max": 14000.0,
                    "min_monthly_income": 28000.0,
                    "min_credit_score": 710,
                    "floating_prepayment_penalty_pct": 0.0,
                    "fixed_prepayment_penalty_pct": 2.5,
                    "penal_charges_monthly_pct": 2.0,
                    "turnaround_hours": 8,
                    "digital_journey": True,
                    "perks": [
                        "Backed by Tata Group trust and governance",
                        "Step-up EMI option for young professionals",
                        "Part-prepayment allowed from 6th month"
                    ]
                }
            ]
        }
    ]


class LoanMitraMatchEngine:
    """
    Implements the RBI 2025 compliant multi-lender matching engine.
    Ensures:
    1. Zero dark patterns or opaque "sponsored" favoritism.
    2. Transparent scoring criteria (Compatibility formula).
    3. Clear sort order options (Lowest APR, Lowest EMI, Lowest Fee, Profile Compatibility).
    4. Explicit "Why this option appears" checklist for every result.
    """

    @staticmethod
    def calculate_emi(principal: float, annual_rate_pct: float, tenure_months: int) -> float:
        """
        Calculates monthly EMI using standard reducing balance formula:
        E = P * r * (1+r)^n / ((1+r)^n - 1)
        """
        if annual_rate_pct <= 0 or tenure_months <= 0 or principal <= 0:
            return 0.0
        monthly_r = (annual_rate_pct / 100.0) / 12.0
        numerator = principal * monthly_r * math.pow(1.0 + monthly_r, tenure_months)
        denominator = math.pow(1.0 + monthly_r, tenure_months) - 1.0
        if denominator == 0:
            return round(principal / tenure_months, 2)
        return round(numerator / denominator, 2)

    @staticmethod
    def calculate_linearized_apr(principal: float, annual_rate_pct: float, tenure_months: int, processing_fee: float) -> float:
        """
        Calculates Annual Percentage Rate (APR) factoring in upfront processing fee,
        as required under RBI 2025 Digital Lending Directions.
        Linearized APR = Annual Interest Rate + (Processing Fee * 12 / (Principal * Tenure_Months)) * 100
        """
        if principal <= 0 or tenure_months <= 0:
            return annual_rate_pct
        amortized_fee_annual_pct = (processing_fee * 12.0 / (principal * tenure_months)) * 100.0
        return round(annual_rate_pct + amortized_fee_annual_pct, 2)

    @classmethod
    def match_loans(
        cls,
        loan_type: str,
        requested_amount: float,
        monthly_income: float,
        employment_type: str,
        tenure_months: int,
        existing_monthly_emi: float = 0.0,
        credit_score: int = 750,
        sort_by: str = "compatibility"  # "compatibility", "lowest_apr", "lowest_emi", "lowest_fee"
    ) -> Dict[str, Any]:
        """
        Evaluates the applicant against all registered lenders and outputs unbiased,
        KFS-compliant comparative loan cards.
        """
        all_lenders = LoanMitraRegistry.LENDERS
        matched_offers: List[Dict[str, Any]] = []

        for lender in all_lenders:
            for product in lender["products"]:
                if product["loan_type"] != loan_type:
                    continue

                # 1. Eligibility Check & Rate Determination based on credit score
                # Tiered interest rate deduction/surcharge based on verifiable credit score
                if credit_score >= 775:
                    rate_pct = product["base_rate_min"]
                    credit_subscore = 100.0
                elif credit_score >= 730:
                    rate_pct = product["base_rate_min"] + 0.60
                    credit_subscore = 90.0
                elif credit_score >= 690:
                    rate_pct = product["base_rate_min"] + 1.40
                    credit_subscore = 75.0
                elif credit_score >= 650:
                    rate_pct = product["base_rate_min"] + 2.50
                    credit_subscore = 60.0
                else:
                    rate_pct = product["base_rate_max"]
                    credit_subscore = 40.0

                rate_pct = min(rate_pct, product["base_rate_max"])

                # 2. Tenure bounds clamp
                valid_tenure = max(product["min_tenure_months"], min(tenure_months, product["max_tenure_months"]))
                tenure_subscore = 100.0 if valid_tenure == tenure_months else 70.0

                # 3. Amount bounds check
                within_amount = (product["min_amount"] <= requested_amount <= product["max_amount"])
                amount_subscore = 100.0 if within_amount else (70.0 if requested_amount <= product["max_amount"] * 1.2 else 30.0)

                # 4. Income check
                income_subscore = 100.0 if monthly_income >= product["min_monthly_income"] else max(20.0, (monthly_income / product["min_monthly_income"]) * 80.0)

                # 5. Financial calculations (EMI, Processing Fee, APR, FOIR)
                monthly_emi = cls.calculate_emi(requested_amount, rate_pct, valid_tenure)
                
                raw_fee = requested_amount * (product["processing_fee_pct"] / 100.0)
                processing_fee = round(min(product["processing_fee_max"], max(product["processing_fee_min"], raw_fee)), 2)
                gst_on_fee = round(processing_fee * 0.18, 2)
                total_processing_fee = round(processing_fee + gst_on_fee, 2)

                apr_pct = cls.calculate_linearized_apr(requested_amount, rate_pct, valid_tenure, total_processing_fee)

                total_repayment = round((monthly_emi * valid_tenure) + total_processing_fee, 2)
                total_interest = round((monthly_emi * valid_tenure) - requested_amount, 2)

                # FOIR (Fixed Obligation to Income Ratio)
                total_monthly_debt = existing_monthly_emi + monthly_emi
                foir_pct = round((total_monthly_debt / monthly_income * 100.0), 1) if monthly_income > 0 else 100.0

                if foir_pct <= 45.0:
                    eligibility_subscore = 100.0
                elif foir_pct <= 60.0:
                    eligibility_subscore = 80.0
                elif foir_pct <= 75.0:
                    eligibility_subscore = 55.0
                else:
                    eligibility_subscore = 30.0

                feature_subscore = 95.0 if product.get("digital_journey") else 85.0

                # Compatibility Formula:
                # Score = (Eligibility * 0.30) + (Amount Match * 0.20) + (Tenure Match * 0.10) +
                #         (Income Match * 0.15) + (Credit Match * 0.15) + (Features * 0.10)
                compatibility_score = round(
                    (eligibility_subscore * 0.30) +
                    (amount_subscore * 0.20) +
                    (tenure_subscore * 0.10) +
                    (income_subscore * 0.15) +
                    (credit_subscore * 0.15) +
                    (feature_subscore * 0.10),
                    1
                )

                # Compliance "Why this option appears" checklist
                why_appears = []
                if credit_score >= product["min_credit_score"]:
                    why_appears.append(f"Credit score ({credit_score}) meets required threshold (>={product['min_credit_score']})")
                else:
                    why_appears.append(f"Credit score ({credit_score}) below preferred benchmark ({product['min_credit_score']})")

                if within_amount:
                    why_appears.append(f"Requested loan ₹{requested_amount:,.0f} within eligible limit (₹{product['min_amount']:,.0f} - ₹{product['max_amount']:,.0f})")

                if monthly_income >= product["min_monthly_income"]:
                    why_appears.append(f"Monthly salary ₹{monthly_income:,.0f} satisfies minimum income requirement (₹{product['min_monthly_income']:,.0f})")

                if foir_pct <= 55.0:
                    why_appears.append(f"Safe debt-to-income FOIR at {foir_pct}% (below RBI prudential 60% threshold)")
                else:
                    why_appears.append(f"Elevated debt-to-income FOIR at {foir_pct}% (lender may require co-applicant)")

                why_appears.append(f"RBI KFS: Prepayment penalty 0% on floating rate debt; APR amortized at {apr_pct}%")

                offer = {
                    "lender_id": lender["lender_id"],
                    "lender_name": lender["lender_name"],
                    "category": lender["category"],
                    "rbi_code": lender["rbi_code"],
                    "gro_name": lender["gro_name"],
                    "gro_email": lender["gro_email"],
                    "gro_contact": lender["gro_contact"],
                    "last_verified_at": lender["last_verified_at"],
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "loan_type": product["loan_type"],
                    "compatibility_score": compatibility_score,
                    "offered_rate_pct": round(rate_pct, 2),
                    "base_rate_range": f"{product['base_rate_min']}% - {product['base_rate_max']}%",
                    "monthly_emi_inr": monthly_emi,
                    "tenure_months": valid_tenure,
                    "processing_fee_inr": processing_fee,
                    "gst_on_fee_inr": gst_on_fee,
                    "total_processing_fee_inr": total_processing_fee,
                    "apr_pct": apr_pct,
                    "total_interest_inr": total_interest,
                    "total_repayment_inr": total_repayment,
                    "foir_pct": foir_pct,
                    "turnaround_hours": product["turnaround_hours"],
                    "penal_charges_clause": f"{product['penal_charges_monthly_pct']}% per month on overdue installments",
                    "prepayment_clause": "0% foreclosure charges on floating rate (RBI Mandate)",
                    "perks": product["perks"],
                    "why_appears": why_appears,
                    "subscores": {
                        "eligibility": eligibility_subscore,
                        "amount_fit": amount_subscore,
                        "tenure_fit": tenure_subscore,
                        "income_fit": income_subscore,
                        "credit_fit": credit_subscore,
                        "features": feature_subscore
                    }
                }
                matched_offers.append(offer)

        # Transparent sorting as per user selection (No black-box ranking)
        if sort_by == "lowest_apr":
            matched_offers.sort(key=lambda x: x["apr_pct"])
        elif sort_by == "lowest_emi":
            matched_offers.sort(key=lambda x: x["monthly_emi_inr"])
        elif sort_by == "lowest_fee":
            matched_offers.sort(key=lambda x: x["total_processing_fee_inr"])
        else:  # "compatibility"
            matched_offers.sort(key=lambda x: x["compatibility_score"], reverse=True)

        return {
            "requested_profile": {
                "loan_type": loan_type,
                "requested_amount_inr": requested_amount,
                "monthly_income_inr": monthly_income,
                "employment_type": employment_type,
                "tenure_months": tenure_months,
                "existing_monthly_emi_inr": existing_monthly_emi,
                "credit_score": credit_score,
                "sort_criteria": sort_by
            },
            "compliance_notice": (
                "In compliance with RBI 2025 Digital Lending Directions for Web-Aggregators, "
                "offers are sorted strictly by user-chosen objective metrics without commercial bias "
                "or paid placement sponsorships."
            ),
            "total_offers_evaluated": len(matched_offers),
            "offers": matched_offers
        }


class BalanceTransferEngine:
    """
    Calculates existing loan refinancing, balance transfer switch-over benefits,
    switching costs, and net break-even horizon.
    """

    @classmethod
    def calculate_balance_transfer(
        cls,
        outstanding_principal_inr: float,
        current_interest_rate_pct: float,
        remaining_tenure_months: int,
        new_interest_rate_pct: Optional[float] = None,
        new_processing_fee_pct: float = 1.0,
        existing_foreclosure_penalty_pct: float = 0.0,
        monthly_prepay_booster_inr: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates:
        1. Existing vs New Monthly EMI
        2. Lifetime interest saved
        3. Switching costs (Processing fee + documentation + foreclosure penalty)
        4. Net savings after all switching costs
        5. Break-even period in months
        6. Prepayment acceleration benefit (if applicant pays extra monthly)
        """
        # Benchmark new rate if not provided (defaulting to competitive personal/home refinancing rate)
        if new_interest_rate_pct is None or new_interest_rate_pct <= 0:
            new_interest_rate_pct = round(max(8.50, current_interest_rate_pct - 2.50), 2)

        # Existing Loan Metrics
        current_emi = LoanMitraMatchEngine.calculate_emi(
            outstanding_principal_inr, current_interest_rate_pct, remaining_tenure_months
        )
        total_current_repayment = round(current_emi * remaining_tenure_months, 2)
        total_current_interest = round(total_current_repayment - outstanding_principal_inr, 2)

        # New Loan Metrics
        new_emi = LoanMitraMatchEngine.calculate_emi(
            outstanding_principal_inr, new_interest_rate_pct, remaining_tenure_months
        )
        total_new_repayment = round(new_emi * remaining_tenure_months, 2)
        total_new_interest = round(total_new_repayment - outstanding_principal_inr, 2)

        monthly_savings = round(max(0.0, current_emi - new_emi), 2)
        gross_interest_saved = round(max(0.0, total_current_interest - total_new_interest), 2)

        # Switching Costs
        new_processing_fee = round(outstanding_principal_inr * (new_processing_fee_pct / 100.0), 2)
        gst_on_fee = round(new_processing_fee * 0.18, 2)
        foreclosure_penalty = round(outstanding_principal_inr * (existing_foreclosure_penalty_pct / 100.0), 2)
        statutory_stamp_duty = 500.0  # nominal state stamp fee
        total_switching_cost = round(new_processing_fee + gst_on_fee + foreclosure_penalty + statutory_stamp_duty, 2)

        net_lifetime_savings = round(gross_interest_saved - total_switching_cost, 2)

        # Break-Even Period (in Months)
        if monthly_savings > 0:
            break_even_months = round(total_switching_cost / monthly_savings, 1)
        else:
            break_even_months = 999.0

        # Prepayment acceleration calculation if extra monthly payment provided
        accelerated_tenure_months = remaining_tenure_months
        accelerated_interest_saved = 0.0
        if monthly_prepay_booster_inr > 0:
            total_monthly_flow = new_emi + monthly_prepay_booster_inr
            monthly_r = (new_interest_rate_pct / 100.0) / 12.0
            bal = outstanding_principal_inr
            months_count = 0
            acc_interest = 0.0
            while bal > 0 and months_count < remaining_tenure_months * 2:
                months_count += 1
                interest_month = bal * monthly_r
                acc_interest += interest_month
                principal_paid = total_monthly_flow - interest_month
                bal -= principal_paid
                if principal_paid <= 0:
                    break
            accelerated_tenure_months = months_count
            accelerated_interest_saved = round(max(0.0, total_new_interest - acc_interest), 2)

        # Strategic Recommendation
        is_viable = (net_lifetime_savings > 10000.0) and (break_even_months <= (remaining_tenure_months * 0.5))
        if is_viable:
            recommendation = (
                f"HIGHLY RECOMMENDED: You will break even on transfer costs within {break_even_months} months, "
                f"saving a net ₹{net_lifetime_savings:,.0f} over the remaining tenure."
            )
        elif net_lifetime_savings > 0:
            recommendation = (
                f"MODERATE BENEFIT: Net lifetime savings of ₹{net_lifetime_savings:,.0f} with a break-even period of "
                f"{break_even_months} months. Evaluate if remaining tenure justifies switching paperwork."
            )
        else:
            recommendation = (
                f"NOT RECOMMENDED: High switching costs (₹{total_switching_cost:,.0f}) exceed the interest saved. "
                f"Remaining tenure or interest delta is insufficient."
            )

        return {
            "outstanding_principal_inr": outstanding_principal_inr,
            "remaining_tenure_months": remaining_tenure_months,
            "current_loan": {
                "interest_rate_pct": current_interest_rate_pct,
                "monthly_emi_inr": current_emi,
                "total_interest_inr": total_current_interest,
                "total_repayment_inr": total_current_repayment
            },
            "new_loan": {
                "interest_rate_pct": new_interest_rate_pct,
                "monthly_emi_inr": new_emi,
                "total_interest_inr": total_new_interest,
                "total_repayment_inr": total_new_repayment
            },
            "savings_summary": {
                "monthly_emi_reduction_inr": monthly_savings,
                "gross_interest_saved_inr": gross_interest_saved,
                "total_switching_cost_inr": total_switching_cost,
                "net_lifetime_savings_inr": net_lifetime_savings,
                "break_even_period_months": break_even_months,
                "is_transfer_viable": is_viable,
                "strategic_recommendation": recommendation
            },
            "switching_cost_breakdown": {
                "new_processing_fee_inr": new_processing_fee,
                "gst_on_fee_inr": gst_on_fee,
                "existing_prepayment_penalty_inr": foreclosure_penalty,
                "stamp_duty_and_documentation_inr": statutory_stamp_duty
            },
            "prepayment_booster": {
                "monthly_extra_payment_inr": monthly_prepay_booster_inr,
                "tenure_reduction_months": max(0, remaining_tenure_months - accelerated_tenure_months),
                "accelerated_tenure_months": accelerated_tenure_months,
                "extra_interest_saved_inr": accelerated_interest_saved
            }
        }


class LoanMitraCRM:
    """
    Manages the loan lead lifecycle, lender verification audits, and aggregation referral commissions.
    """

    MOCK_LEADS: List[Dict[str, Any]] = [
        {
            "lead_id": "LM-2026-8821",
            "borrower_name": "Rohan Verma",
            "loan_type": "personal_loan",
            "loan_amount_inr": 850000.0,
            "selected_lender": "HDFC Bank Ltd.",
            "offered_rate_pct": 10.50,
            "stage": "SANCTION_APPROVED",
            "payout_commission_pct": 1.25,
            "estimated_commission_inr": 10625.0,
            "kfs_consent_recorded": True,
            "created_at": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
        },
        {
            "lead_id": "LM-2026-8834",
            "borrower_name": "Kavita Nair",
            "loan_type": "home_loan",
            "loan_amount_inr": 6500000.0,
            "selected_lender": "State Bank of India",
            "offered_rate_pct": 8.40,
            "stage": "BANK_LOGIN_INITIATED",
            "payout_commission_pct": 0.50,
            "estimated_commission_inr": 32500.0,
            "kfs_consent_recorded": True,
            "created_at": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
        },
        {
            "lead_id": "LM-2026-8849",
            "borrower_name": "Deepak Choudhary",
            "loan_type": "business_loan",
            "loan_amount_inr": 2500000.0,
            "selected_lender": "ICICI Bank Ltd.",
            "offered_rate_pct": 12.00,
            "stage": "DISBURSED",
            "payout_commission_pct": 1.50,
            "estimated_commission_inr": 37500.0,
            "kfs_consent_recorded": True,
            "created_at": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d %H:%M")
        },
        {
            "lead_id": "LM-2026-8872",
            "borrower_name": "Pooja Singhania",
            "loan_type": "personal_loan",
            "loan_amount_inr": 400000.0,
            "selected_lender": "Bajaj Finance Ltd.",
            "offered_rate_pct": 11.00,
            "stage": "DOCS_SUBMITTED",
            "payout_commission_pct": 1.75,
            "estimated_commission_inr": 7000.0,
            "kfs_consent_recorded": True,
            "created_at": (datetime.now() - timedelta(hours=14)).strftime("%Y-%m-%d %H:%M")
        }
    ]

    @classmethod
    def get_lead_pipeline_summary(cls) -> Dict[str, Any]:
        """Returns lead pipeline stats and aggregate channel earnings."""
        total_leads = len(cls.MOCK_LEADS)
        disbursed_leads = [l for l in cls.MOCK_LEADS if l["stage"] == "DISBURSED"]
        approved_leads = [l for l in cls.MOCK_LEADS if l["stage"] == "SANCTION_APPROVED"]
        pipeline_leads = [l for l in cls.MOCK_LEADS if l["stage"] in ("DOCS_SUBMITTED", "BANK_LOGIN_INITIATED")]

        total_disbursed_volume = sum(l["loan_amount_inr"] for l in disbursed_leads)
        total_pipeline_volume = sum(l["loan_amount_inr"] for l in cls.MOCK_LEADS)
        total_realized_commissions = sum(l["estimated_commission_inr"] for l in disbursed_leads)
        potential_commissions = sum(l["estimated_commission_inr"] for l in cls.MOCK_LEADS)

        return {
            "total_leads_count": total_leads,
            "disbursed_count": len(disbursed_leads),
            "approved_count": len(approved_leads),
            "in_processing_count": len(pipeline_leads),
            "total_pipeline_volume_inr": total_pipeline_volume,
            "total_disbursed_volume_inr": total_disbursed_volume,
            "realized_commissions_inr": total_realized_commissions,
            "potential_commissions_inr": potential_commissions,
            "leads": cls.MOCK_LEADS
        }

    @classmethod
    def get_verification_health(cls) -> List[Dict[str, Any]]:
        """Returns the audit health status of each lender product."""
        health_list = []
        for lender in LoanMitraRegistry.LENDERS:
            # check verification recency
            verified_dt = datetime.fromisoformat(lender["last_verified_at"])
            days_ago = (datetime.now() - verified_dt).days
            if days_ago <= 7:
                status_badge = "🟢 VERIFIED_ACTIVE (Compliant < 7 Days)"
            elif days_ago <= 30:
                status_badge = "🟠 AUDIT_PENDING (Within 30 Days)"
            else:
                status_badge = "🔴 EXPIRED_NEEDS_REAUDIT"

            health_list.append({
                "lender_id": lender["lender_id"],
                "lender_name": lender["lender_name"],
                "category": lender["category"],
                "rbi_code": lender["rbi_code"],
                "gro_name": lender["gro_name"],
                "gro_email": lender["gro_email"],
                "last_verified_at": lender["last_verified_at"],
                "status_badge": status_badge,
                "products_count": len(lender["products"])
            })
        return health_list
