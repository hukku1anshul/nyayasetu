"""
NyayaSetu & CardSmart Unified FastAPI Application
Exposes REST endpoints across:
- Free Viral Consumer Utilities (HRA Rent Receipts, Hindu Succession Share Calculator, Vehicle Radar)
- CardSmart: Credit Card Personalized ROI & Upgrade Marketplace
- National High-Volume & High-Ticket USPs (Gazette, IEPF, RTO, Municipal)
- 100% Free Government Direct Rails (e-Gazette, MCA IEPF Crypto)
- Multi-Channel Lead Intake (WhatsApp + Web)
- Revenue Optimization & FinTech Upsell Engine
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from pathlib import Path

from nyayasetu.engines.free_tools_engine import HRARentReceiptEngine, InheritanceShareCalculator, VehicleComplianceRadar
from nyayasetu.engines.credit_card_engine import CreditCardEngine
from nyayasetu.engines.iepf_recovery import IEPFTransmissionEngine, UnclaimedAssetFolio
from nyayasetu.engines.gazette_engine import GazetteEngine
from nyayasetu.engines.corporate_action_engine import CorporateActionEngine
from nyayasetu.engines.succession_noc_engine import SuccessionNOCEngine
from nyayasetu.engines.revenue_optimizer import RevenueOptimizationEngine
from nyayasetu.engines.loan_mitra_engine import (
    LoanMitraRegistry,
    LoanMitraMatchEngine,
    BalanceTransferEngine,
    LoanMitraCRM
)
from nyayasetu.engines.lookup_rails_engine import LookupRailsEngine
from nyayasetu.engines.legal_tax_engine import (
    LegalNoticeEngine,
    AgreementRiskEngine,
    TaxRegimeEngine,
    PresumptiveTaxEngine,
    NoticeExplainerEngine
)

from nyayasetu.integrations.gazette_live_client import CentralGazetteLiveClient
from nyayasetu.integrations.iepf_mca_client import IEPFUnclaimedAssetClient, MCACryptoEngine
from nyayasetu.integrations.rta_client import RTADirectory, RTAUnclaimedRegisterEngine

from nyayasetu.channels.whatsapp_bot import WhatsAppBotEngine
from nyayasetu.channels.web_intake import WebIntakeEngine, WebLeadIntakePayload

STATIC_INDEX = Path(__file__).parent.parent / "static" / "index.html"

app = FastAPI(
    title="NyayaSetu, Loan Mitra & CardSmart Unified Platform API",
    description="RBI 2025 Digital Lending Marketplace, Card ROI Engine, AI Vakil & CA India Suite, and Public Rails",
    version="1.8.0"
)

# Enable CORS for web and mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def serve_index():
    if STATIC_INDEX.exists():
        return FileResponse(STATIC_INDEX)
    return HTMLResponse("<h1>NyayaSetu & CardSmart Running</h1><p><a href='/docs'>Swagger API Docs</a></p>")

gazette_client = CentralGazetteLiveClient()
iepf_client = IEPFUnclaimedAssetClient()

# ----------------- FREE VIRAL UTILITY 1: HRA RENT RECEIPTS & EXEMPTION -----------------
class HRACalculateRequest(BaseModel):
    basic_salary_annual: float = Field(..., ge=0, description="Annual Basic Salary")
    dearness_allowance_annual: float = Field(0.0, ge=0, description="Annual Dearness Allowance")
    hra_received_annual: float = Field(..., ge=0, description="Annual HRA received from employer")
    rent_paid_annual: float = Field(..., ge=0, description="Total annual rent paid to landlord")
    is_metro_city: bool = Field(True, description="True if residing in Delhi, Mumbai, Kolkata, Chennai")

@app.post("/api/v1/tools/calculate-hra-exemption")
def calculate_hra_exemption(req: HRACalculateRequest):
    """
    Computes statutory Section 10(13A) Income Tax HRA Exemption and checks Landlord PAN mandatory status.
    """
    return HRARentReceiptEngine.calculate_hra_exemption(
        basic_salary_annual=req.basic_salary_annual,
        dearness_allowance_annual=req.dearness_allowance_annual,
        hra_received_annual=req.hra_received_annual,
        rent_paid_annual=req.rent_paid_annual,
        is_metro_city=req.is_metro_city
    )

class RentReceiptGenerateRequest(BaseModel):
    tenant_name: str
    landlord_name: str
    landlord_pan: Optional[str] = "ABCDE1234F"
    rental_property_address: str
    monthly_rent: float = Field(..., ge=1000)
    financial_year: str = "2026-27"

@app.post("/api/v1/tools/generate-rent-receipts")
def generate_rent_receipts(req: RentReceiptGenerateRequest):
    """
    Generates full 12-month stamped rent receipts payload compliant with Income Tax rules.
    """
    return HRARentReceiptEngine.generate_receipts_manifest(
        tenant_name=req.tenant_name,
        landlord_name=req.landlord_name,
        landlord_pan=req.landlord_pan or "",
        rental_property_address=req.rental_property_address,
        monthly_rent=req.monthly_rent,
        financial_year=req.financial_year
    )

# ----------------- FREE VIRAL UTILITY 2: HINDU SUCCESSION SHARE CALCULATOR -----------------
class InheritanceShareRequest(BaseModel):
    deceased_gender: str = Field("MALE", description="'MALE' or 'FEMALE'")
    total_estate_value_inr: float = Field(1000000.0, ge=1000)
    surviving_spouse: bool = True
    surviving_mother: bool = True
    surviving_father: bool = False
    sons_count: int = Field(1, ge=0)
    daughters_count: int = Field(1, ge=0)

@app.post("/api/v1/tools/calculate-inheritance-shares")
def calculate_inheritance_shares(req: InheritanceShareRequest):
    """
    Computes statutory legal heir ownership percentage and rupee breakdown under the Hindu Succession Act (Class-I).
    """
    return InheritanceShareCalculator.calculate_hindu_succession_shares(
        deceased_gender=req.deceased_gender,
        total_estate_value_inr=req.total_estate_value_inr,
        surviving_spouse=req.surviving_spouse,
        surviving_mother=req.surviving_mother,
        surviving_father=req.surviving_father,
        sons_count=req.sons_count,
        daughters_count=req.daughters_count
    )

# ----------------- FREE VIRAL UTILITY 3: VEHICLE COMPLIANCE RADAR -----------------
@app.get("/api/v1/tools/vehicle-radar/{reg_number}")
def audit_vehicle_compliance(reg_number: str):
    """
    Simulates multi-state vehicle audit: Pending e-Challans, PUCC expiry, bank hypothecation lien, virtual court status.
    """
    return VehicleComplianceRadar.audit_vehicle_health(reg_number)

# ----------------- CARDSMART & REVENUE -----------------
class MonthlySpendsPayload(BaseModel):
    online_shopping: float = 15000.0
    dining: float = 7000.0
    travel: float = 15000.0
    groceries: float = 8000.0
    fuel: float = 5000.0
    international: float = 0.0
    other: float = 20000.0
    preferred_bank: Optional[str] = None

@app.post("/api/v1/cards/recommend")
def recommend_cards(payload: MonthlySpendsPayload):
    spends = payload.model_dump()
    bank = spends.pop("preferred_bank", None)
    return {"recommendations_ranked": CreditCardEngine.rank_cards_for_user(spends, bank)}

@app.get("/api/v1/revenue/tatkal-quote")
def get_tatkal_pricing(service_type: str = "GAZETTE", base_price: float = 3499.0, rush_days: int = 7):
    return RevenueOptimizationEngine.calculate_tatkal_pricing(service_type, base_price, rush_days)

# ----------------- LOAN MITRA (RBI 2025 COMPLIANT MARKETPLACE) -----------------
class LoanMatchRequest(BaseModel):
    loan_type: str = Field("personal_loan", description="'personal_loan', 'home_loan', 'business_loan', 'loan_against_property'")
    requested_amount: float = Field(500000.0, ge=10000)
    monthly_income: float = Field(60000.0, ge=10000)
    employment_type: str = Field("salaried", description="'salaried' or 'self_employed'")
    tenure_months: int = Field(36, ge=6, le=360)
    existing_monthly_emi: float = Field(0.0, ge=0)
    credit_score: int = Field(750, ge=300, le=900)
    sort_by: str = Field("compatibility", description="'compatibility', 'lowest_apr', 'lowest_emi', 'lowest_fee'")

@app.post("/api/v1/loans/match")
def match_loans(req: LoanMatchRequest):
    """
    Evaluates applicant profile across all regulated lenders and returns unbiased comparative cards
    with complete Key Fact Statement (KFS) disclosures, APR, and 'Why this appears' compliance details.
    """
    return LoanMitraMatchEngine.match_loans(
        loan_type=req.loan_type,
        requested_amount=req.requested_amount,
        monthly_income=req.monthly_income,
        employment_type=req.employment_type,
        tenure_months=req.tenure_months,
        existing_monthly_emi=req.existing_monthly_emi,
        credit_score=req.credit_score,
        sort_by=req.sort_by
    )

class BalanceTransferRequest(BaseModel):
    outstanding_principal_inr: float = Field(800000.0, ge=10000)
    current_interest_rate_pct: float = Field(14.5, ge=5.0, le=45.0)
    remaining_tenure_months: int = Field(48, ge=6, le=360)
    new_interest_rate_pct: Optional[float] = None
    new_processing_fee_pct: float = Field(1.0, ge=0.0, le=5.0)
    existing_foreclosure_penalty_pct: float = Field(0.0, ge=0.0, le=5.0)
    monthly_prepay_booster_inr: float = Field(0.0, ge=0.0)

@app.post("/api/v1/loans/balance-transfer-optimize")
def optimize_balance_transfer(req: BalanceTransferRequest):
    """
    Calculates existing vs refinancing rate savings, switching fees, and exact break-even timeline in months.
    """
    return BalanceTransferEngine.calculate_balance_transfer(
        outstanding_principal_inr=req.outstanding_principal_inr,
        current_interest_rate_pct=req.current_interest_rate_pct,
        remaining_tenure_months=req.remaining_tenure_months,
        new_interest_rate_pct=req.new_interest_rate_pct,
        new_processing_fee_pct=req.new_processing_fee_pct,
        existing_foreclosure_penalty_pct=req.existing_foreclosure_penalty_pct,
        monthly_prepay_booster_inr=req.monthly_prepay_booster_inr
    )

@app.get("/api/v1/loans/products")
def list_loan_products():
    """Returns verified catalog of registered lenders, products, and 7-day compliance verification audits."""
    return {
        "framework": "RBI 2025 Digital Lending Web-Aggregation Framework",
        "registered_lenders": LoanMitraRegistry.LENDERS,
        "verification_audit": LoanMitraCRM.get_verification_health()
    }

@app.get("/api/v1/loans/crm-pipeline")
def get_loan_crm_pipeline():
    """Returns pipeline metrics: Leads, Approved Sanctions, Disbursals, and Aggregator Commission payouts."""
    return LoanMitraCRM.get_lead_pipeline_summary()

# ----------------- REAL OPEN PUBLIC RAILS LOOKUP -----------------
@app.get("/api/v1/lookup/ifsc/{ifsc_code}")
def lookup_ifsc(ifsc_code: str):
    """Real-time bank branch lookup via Razorpay Open IFSC Rail."""
    return LookupRailsEngine.lookup_ifsc(ifsc_code)

@app.get("/api/v1/lookup/pincode/{pincode}")
def lookup_pincode(pincode: str):
    """Real-time postal district, state, and RTO circle lookup via India Post Open API."""
    return LookupRailsEngine.lookup_pincode(pincode)

class PanValidateRequest(BaseModel):
    pan_number: Optional[str] = None
    pan: Optional[str] = None

@app.post("/api/v1/lookup/validate-pan")
def validate_pan(req: PanValidateRequest):
    """Validates 10-digit statutory PAN under Section 139A and extracts entity classification."""
    target_pan = req.pan_number or req.pan or ""
    return LookupRailsEngine.validate_pan(target_pan)

class GstinValidateRequest(BaseModel):
    gstin: Optional[str] = None
    gstin_number: Optional[str] = None

@app.post("/api/v1/lookup/validate-gstin")
def validate_gstin(req: GstinValidateRequest):
    """Validates 15-digit GSTIN and decodes State, PAN component, and entity sequence."""
    target_gstin = req.gstin or req.gstin_number or ""
    return LookupRailsEngine.validate_gstin(target_gstin)

# ----------------- AI VAKIL & LEGAL INTELLIGENCE -----------------
class LegalNoticeRequest(BaseModel):
    notice_type: str = "CHEQUE_BOUNCE_SEC138"
    sender_name: str = "Claimant Citizen"
    sender_address: str = "India"
    sender_phone: str = "+91 98200 11223"
    recipient_name: str = "Respondent"
    recipient_address: str = "India"
    claim_amount_inr: Optional[float] = None
    amount: Optional[float] = None
    transaction_date: str = "2026-08-01"
    instrument_or_reference_no: Optional[str] = None
    reference_no: Optional[str] = None
    dispute_summary: str = ""
    reason_description: str = ""

@app.post("/api/v1/legal/generate-notice")
def generate_legal_notice(req: LegalNoticeRequest):
    """Generates statutory legal notice docket ready for dispatch via Registered Post AD / Speed Post."""
    eff_amount = req.claim_amount_inr if req.claim_amount_inr is not None else (req.amount or 0.0)
    eff_ref = req.instrument_or_reference_no or req.reference_no or "N/A"
    eff_desc = req.dispute_summary or req.reason_description or eff_ref
    return LegalNoticeEngine.generate_notice(
        notice_type=req.notice_type,
        sender_name=req.sender_name,
        sender_address=req.sender_address,
        sender_phone=req.sender_phone,
        recipient_name=req.recipient_name,
        recipient_address=req.recipient_address,
        claim_amount_inr=eff_amount,
        transaction_date=req.transaction_date,
        instrument_or_reference_no=eff_ref,
        dispute_summary=eff_desc
    )

class AgreementAnalysisRequest(BaseModel):
    agreement_type: str = Field("employment", description="'employment', 'rental', 'freelance_sow'")
    agreement_text: str

@app.post("/api/v1/legal/analyze-agreement")
def analyze_agreement(req: AgreementAnalysisRequest):
    """Inspects contract text for void non-compete clauses, arbitrary bonds, and statutory legal traps."""
    return AgreementRiskEngine.analyze_agreement(
        agreement_type=req.agreement_type,
        agreement_text=req.agreement_text
    )

# ----------------- AI CA & TAX INTELLIGENCE -----------------
class TaxRegimeCompareRequest(BaseModel):
    gross_annual_income: Optional[float] = None
    gross_income: Optional[float] = None
    deduction_80c: float = 150000.0
    deduction_80d: float = 25000.0
    home_loan_interest_24b: float = 0.0
    hra_exemption_10_13a: Optional[float] = None
    hra_exemption: Optional[float] = None
    other_deductions_chapter_via: Optional[float] = 0.0
    other_deductions: Optional[float] = 0.0

@app.post("/api/v1/tax/compare-regimes")
def compare_tax_regimes(req: TaxRegimeCompareRequest):
    """Side-by-side comparison of New (Section 115BAC) vs Old Tax Regime liability."""
    gross = req.gross_annual_income if req.gross_annual_income is not None else (req.gross_income or 0.0)
    hra = req.hra_exemption_10_13a if req.hra_exemption_10_13a is not None else (req.hra_exemption or 0.0)
    other = req.other_deductions_chapter_via or req.other_deductions or 0.0
    return TaxRegimeEngine.compare_tax_regimes(
        gross_annual_income=gross,
        deduction_80c=req.deduction_80c,
        deduction_80d=req.deduction_80d,
        home_loan_interest_24b=req.home_loan_interest_24b,
        hra_exemption_10_13a=hra,
        other_deductions_chapter_via=other
    )

class PresumptiveTaxRequest(BaseModel):
    gross_professional_receipts: Optional[float] = None
    gross_receipts: Optional[float] = None
    actual_business_expenses: float = 0.0
    digital_receipts_percentage: float = 95.0
    other_income: float = 0.0

@app.post("/api/v1/tax/presumptive-44ada")
def calculate_44ada(req: PresumptiveTaxRequest):
    """Calculates Section 44ADA 50% deemed profit and tax savings for notified professionals."""
    receipts = req.gross_professional_receipts if req.gross_professional_receipts is not None else (req.gross_receipts or 0.0)
    return PresumptiveTaxEngine.calculate_44ada(
        gross_professional_receipts=receipts,
        actual_business_expenses=req.actual_business_expenses
    )

@app.get("/api/v1/tax/explain-notice/{section_code}")
def explain_tax_notice(section_code: str):
    """Provides plain-English diagnosis and statutory response strategy for IT notices."""
    return NoticeExplainerEngine.explain_notice(section_code)

# ----------------- PERSISTENT USER HISTORY & DOCKET AUDIT -----------------
USER_HISTORY_STORE: List[Dict[str, Any]] = [
    {
        "id": "ACT-2026-901",
        "category": "LOAN_MITRA",
        "title": "Personal Loan Multi-Lender Match",
        "summary": "Evaluated ₹5,00,000 for 36 months across 6 lenders (HDFC Insta PL top match at 10.50%)",
        "timestamp": "Today, 11:15 AM",
        "data": {"amount": 500000, "tenure": 36, "rate": 10.5}
    },
    {
        "id": "ACT-2026-902",
        "category": "BALANCE_TRANSFER",
        "title": "Refinancing Break-Even Simulation",
        "summary": "Outstanding ₹8,00,000 switched from 14.50% to 10.50% (Net savings ₹65,884, break-even 6.3 mos)",
        "timestamp": "Today, 10:45 AM",
        "data": {"balance": 800000, "saved": 65884}
    },
    {
        "id": "ACT-2026-903",
        "category": "HRA_RECEIPT",
        "title": "12-Month Section 10(13A) Stamped Receipts",
        "summary": "Generated ₹2,40,000 annual exemption manifest for Landlord Rajesh Khanna (PAN: ABCDE1234F)",
        "timestamp": "Yesterday, 04:20 PM",
        "data": {"annual_rent": 300000, "exemption": 240000}
    },
    {
        "id": "ACT-2026-904",
        "category": "LEGAL_NOTICE",
        "title": "Section 138 Cheque Bounce Demand Notice",
        "summary": "Statutory notice drafted for dishonoured Cheque #449102 (₹1,50,000) under NI Act 1881",
        "timestamp": "14 Sep 2026, 02:10 PM",
        "data": {"amount": 150000, "section": "138 NI Act"}
    }
]

class UserActivityPayload(BaseModel):
    category: Optional[str] = None
    action_type: Optional[str] = None
    title: Optional[str] = None
    tool_name: Optional[str] = None
    summary: Optional[str] = None
    output_summary: Optional[Any] = None
    data: Optional[Dict[str, Any]] = None
    input_payload: Optional[Dict[str, Any]] = None

@app.get("/api/v1/user/history")
def get_user_history():
    """Returns chronological activity history and generated dockets."""
    return {"success": True, "history": USER_HISTORY_STORE, "history_records": USER_HISTORY_STORE}

@app.post("/api/v1/user/history")
def add_user_history(payload: UserActivityPayload):
    """Logs user calculation or generated docket."""
    eff_cat = payload.category or payload.action_type or "GENERAL"
    eff_title = payload.title or payload.tool_name or "User Action"
    eff_summary = payload.summary or (payload.output_summary.get("summary") if isinstance(payload.output_summary, dict) else str(payload.output_summary or ""))
    eff_data = payload.data or payload.input_payload or {}
    record = {
        "id": f"ACT-2026-{len(USER_HISTORY_STORE) + 901}",
        "category": eff_cat,
        "title": eff_title,
        "summary": eff_summary,
        "timestamp": "Just now",
        "data": eff_data
    }
    USER_HISTORY_STORE.insert(0, record)
    return {"success": True, "record": record}

# ----------------- CHANNELS -----------------
class WhatsAppIncomingPayload(BaseModel):
    From: str
    Body: str
    MediaUrl0: Optional[str] = None

@app.post("/webhook/whatsapp")
def handle_whatsapp(payload: WhatsAppIncomingPayload):
    clean = payload.From.replace("whatsapp:", "").strip()
    return WhatsAppBotEngine.handle_incoming_message(clean, payload.Body, payload.MediaUrl0)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "platform": "NyayaSetu, CardSmart, Loan Mitra & Vakil-CA India Unified Engine",
        "version": "1.8.0",
        "core_modules": [
            "Loan Mitra: RBI 2025 Digital Lending Multi-Lender Aggregator & Balance Transfer Optimizer",
            "CardSmart: Credit Card Personalized ROI & Upgrade Marketplace",
            "AI Vakil & CA India: Legal Notices, Contract Risk Analysis, New vs Old Tax Regime, 44ADA",
            "Real Public Rails: Razorpay Open IFSC API, India Post Pincode API, PAN/GSTIN Validators",
            "NyayaSetu: Central Gazette, MCA IEPF Recovery, RTO Registry, Relinquishment Deeds",
            "Free Viral Utilities: HRA Rent Exemption (10(13A)), Hindu Succession, Vehicle Radar"
        ]
    }
