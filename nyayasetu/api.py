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

from nyayasetu.integrations.gazette_live_client import CentralGazetteLiveClient
from nyayasetu.integrations.iepf_mca_client import IEPFUnclaimedAssetClient, MCACryptoEngine
from nyayasetu.integrations.rta_client import RTADirectory, RTAUnclaimedRegisterEngine

from nyayasetu.channels.whatsapp_bot import WhatsAppBotEngine
from nyayasetu.channels.web_intake import WebIntakeEngine, WebLeadIntakePayload

STATIC_INDEX = Path(__file__).parent.parent / "static" / "index.html"

app = FastAPI(
    title="NyayaSetu & CardSmart Platform API",
    description="Legal, Compliance, Bureaucracy, Financial & Free Consumer Utilities Engine for India",
    version="1.6.0"
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
        "platform": "NyayaSetu & CardSmart Core API",
        "version": "1.6.0",
        "free_consumer_utilities": [
            "HRA Rent Receipt & Tax Exemption Generator (Section 10(13A))",
            "Hindu Succession Legal Heir Share Calculator (Class-I)",
            "Multi-State Vehicle Compliance & Virtual Court Challan Radar"
        ]
    }
