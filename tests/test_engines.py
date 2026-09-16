"""
Comprehensive Unit Tests for NyayaSetu Core USP Engines,
Revenue Optimizers, and CardSmart Credit Card Personalized ROI & Upgrade Engine.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nyayasetu.engines.credit_card_engine import CreditCardEngine
from nyayasetu.engines.revenue_optimizer import RevenueOptimizationEngine
from nyayasetu.engines.corporate_action_engine import CorporateActionEngine
from nyayasetu.engines.succession_noc_engine import SuccessionNOCEngine
from nyayasetu.engines.iepf_recovery import IEPFTransmissionEngine, UnclaimedAssetFolio
from nyayasetu.engines.free_tools_engine import HRARentReceiptEngine, InheritanceShareCalculator, VehicleComplianceRadar
from nyayasetu.engines.loan_mitra_engine import LoanMitraMatchEngine, BalanceTransferEngine, LoanMitraCRM
from nyayasetu.engines.lookup_rails_engine import LookupRailsEngine
from nyayasetu.engines.legal_tax_engine import (
    LegalNoticeEngine,
    AgreementRiskEngine,
    TaxRegimeEngine,
    PresumptiveTaxEngine,
    NoticeExplainerEngine
)

def test_hra_rent_receipt_and_exemption():
    calc = HRARentReceiptEngine.calculate_hra_exemption(
        basic_salary_annual=600000.0,
        dearness_allowance_annual=0.0,
        hra_received_annual=240000.0,
        rent_paid_annual=300000.0,
        is_metro_city=True
    )
    assert calc["exempt_hra_amount_inr"] == 240000.0
    assert calc["taxable_hra_amount_inr"] == 0.0
    assert calc["landlord_pan_mandatory"] is True

    manifest = HRARentReceiptEngine.generate_receipts_manifest(
        tenant_name="Aditya Verma",
        landlord_name="Rajesh Khanna",
        landlord_pan="ABCDE1234F",
        rental_property_address="Flat 402, Indiranagar, Bengaluru",
        monthly_rent=25000.0,
        financial_year="2026-27"
    )
    assert manifest["total_receipts_generated"] == 12
    assert manifest["receipts"][0]["revenue_stamp_required"] is True
    print(f"HRA Rent Receipt & Exemption test passed! Exemption: Rs. {calc['exempt_hra_amount_inr']:,.2f}")

def test_hindu_succession_share_calculator():
    # Male deceased leaving widow, mother, 1 son, 1 daughter and father
    res = InheritanceShareCalculator.calculate_hindu_succession_shares(
        deceased_gender="MALE",
        total_estate_value_inr=10000000.0, # 1 Crore
        surviving_spouse=True,
        surviving_mother=True,
        surviving_father=True,
        sons_count=1,
        daughters_count=1
    )
    heirs = res["statutory_heir_distribution"]
    assert len(heirs) == 4
    # Each heir gets 25% (1/4)
    for heir in heirs:
        assert heir["share_pct"] == 25.0
        if "share_value_inr" in heir:
            assert heir["share_value_inr"] == 2500000.0
    assert "Father is a Class-II heir" in res["father_statutory_exclusion_note"]
    print(f"Hindu Succession Share test passed! Class-I 4-way split of Rs. 1 Cr calculated accurately.")

def test_vehicle_compliance_radar():
    radar = VehicleComplianceRadar.audit_vehicle_health("KA-03-MG-5678")
    assert radar["jurisdiction_state"] == "Karnataka"
    assert radar["hypothecation_status"]["has_bank_lien"] is True
    assert radar["pending_challans_summary"]["total_pending_count"] > 0
    assert len(radar["upsell_bridges"]) >= 3
    print(f"Vehicle Compliance Radar test passed for {radar['registration_number']} in {radar['jurisdiction_state']}")

def test_credit_card_personalized_ranking():
    # User spending ₹80,000/month: Online ₹20k, Dining ₹10k, Travel ₹15k, Groceries ₹10k, Other ₹25k
    spends = {
        "online_shopping": 20000.0,
        "dining": 10000.0,
        "travel": 15000.0,
        "groceries": 10000.0,
        "fuel": 5000.0,
        "international": 0.0,
        "other": 20000.0
    }
    ranked = CreditCardEngine.rank_cards_for_user(spends)
    assert len(ranked) >= 5
    top_card = ranked[0]
    assert top_card["net_annual_value_inr"] > 10000.0
    print(f"CardSmart Ranking passed! Top card: {top_card['card_name']} (Net Annual Value: Rs. {top_card['net_annual_value_inr']:,.2f})")

def test_credit_card_upgrade_calculator():
    spends = {
        "online_shopping": 25000.0,
        "dining": 15000.0,
        "travel": 25000.0,
        "groceries": 10000.0,
        "fuel": 5000.0,
        "international": 5000.0,
        "other": 15000.0
    }
    upgrade_res = CreditCardEngine.compare_upgrade(
        current_card_id="hdfc-millennia",
        new_card_id="hdfc-regalia-gold",
        monthly_spends=spends
    )
    assert "current_card" in upgrade_res
    assert "new_card" in upgrade_res
    assert "annual_difference_inr" in upgrade_res
    assert upgrade_res["upgrade_recommended"] is True
    print(f"Should I Upgrade? passed! Delta: Rs. {upgrade_res['annual_difference_inr']:,.2f}/yr - {upgrade_res['verdict'][:45]}...")

def test_revenue_optimizer():
    tatkal = RevenueOptimizationEngine.calculate_tatkal_pricing(service_type="GAZETTE", base_price=3499.0, rush_days=7)
    assert tatkal["total_price_inr"] > 3499.0

def test_corporate_action_multiplier():
    res = CorporateActionEngine.calculate_legacy_holding("TATASTEEL", cert_shares=100, certificate_year=1995)
    assert res["current_effective_shares"] == 1500

def test_succession_noc():
    noc = SuccessionNOCEngine.generate_form_c_relinquishment_deed(
        deceased_name="Late Suresh Sharma",
        company_name="Tata Steel Limited",
        folio_number="S1R0028491",
        shares_count=1500,
        primary_claimant_name="Vikram Sharma",
        relinquishing_heir_name="Pooja Sharma",
        relationship_with_deceased="Daughter"
    )
    assert "FORM-C" in noc["document_title"].upper()

def test_loan_mitra_matching():
    res = LoanMitraMatchEngine.match_loans(
        loan_type="personal_loan",
        requested_amount=500000.0,
        monthly_income=75000.0,
        employment_type="salaried",
        tenure_months=36,
        existing_monthly_emi=8000.0,
        credit_score=760,
        sort_by="compatibility"
    )
    assert len(res["offers"]) > 0
    top_offer = res["offers"][0]
    assert "apr_pct" in top_offer
    assert "monthly_emi_inr" in top_offer
    assert "why_appears" in top_offer
    assert len(top_offer["why_appears"]) >= 3
    assert top_offer["compatibility_score"] > 60.0

    # Test sorting by lowest APR
    apr_res = LoanMitraMatchEngine.match_loans(
        loan_type="personal_loan",
        requested_amount=500000.0,
        monthly_income=75000.0,
        employment_type="salaried",
        tenure_months=36,
        existing_monthly_emi=8000.0,
        credit_score=760,
        sort_by="lowest_apr"
    )
    aprs = [o["apr_pct"] for o in apr_res["offers"]]
    assert aprs == sorted(aprs)
    print(f"Loan Mitra Matching test passed! {len(res['offers'])} compliant offers evaluated. Top offer APR: {top_offer['apr_pct']}%")

def test_loan_mitra_balance_transfer():
    bt = BalanceTransferEngine.calculate_balance_transfer(
        outstanding_principal_inr=800000.0,
        current_interest_rate_pct=14.5,
        remaining_tenure_months=48,
        new_interest_rate_pct=10.5,
        new_processing_fee_pct=1.0,
        existing_foreclosure_penalty_pct=0.0,
        monthly_prepay_booster_inr=2000.0
    )
    summary = bt["savings_summary"]
    assert summary["monthly_emi_reduction_inr"] > 1000.0
    assert summary["gross_interest_saved_inr"] > summary["total_switching_cost_inr"]
    assert summary["net_lifetime_savings_inr"] > 0.0
    assert summary["break_even_period_months"] < 12.0
    assert bt["prepayment_booster"]["tenure_reduction_months"] > 0
    print(f"Loan Mitra Balance Transfer test passed! Net Lifetime Savings: Rs. {summary['net_lifetime_savings_inr']:,.2f}, Break-Even: {summary['break_even_period_months']} months")

def test_loan_mitra_crm():
    crm = LoanMitraCRM.get_lead_pipeline_summary()
    assert crm["total_leads_count"] >= 4
    assert crm["total_pipeline_volume_inr"] > 5000000.0
    assert len(crm["leads"]) >= 4
    health = LoanMitraCRM.get_verification_health()
    assert len(health) >= 5
    print(f"Loan Mitra CRM & Verification Health passed! Pipeline Volume: Rs. {crm['total_pipeline_volume_inr']:,.2f}")

def test_lookup_rails():
    # 1. IFSC lookup
    ifsc = LookupRailsEngine.lookup_ifsc("HDFC0000060")
    assert ifsc["success"] is True
    assert "HDFC Bank" in ifsc["bank"]

    # 2. Pincode lookup
    pin = LookupRailsEngine.lookup_pincode("560038")
    assert pin["success"] is True
    assert pin["pincode"] == "560038"

    # 3. PAN validation
    pan = LookupRailsEngine.validate_pan("ABCPE1234F")
    assert pan["valid"] is True
    assert pan["entity_type"] == "Individual Citizen"

    # 4. GSTIN validation
    gst = LookupRailsEngine.validate_gstin("29ABCPE1234F1Z5")
    assert gst["valid"] is True
    assert gst["state_name"] == "Karnataka"
    print("Zero-Cost Public Lookup Rails (IFSC, Pincode, PAN, GSTIN) passed!")

def test_legal_notice_engine():
    notice = LegalNoticeEngine.generate_notice(
        notice_type="CHEQUE_BOUNCE_SEC138",
        sender_name="Sunil Mehra",
        sender_address="Flat 204, Koramangala, Bengaluru",
        sender_phone="9876543210",
        recipient_name="Amit Enterprises",
        recipient_address="MG Road, Bengaluru",
        claim_amount_inr=250000.0,
        transaction_date="15-Jan-2026",
        instrument_or_reference_no="CHQ-991204",
        dispute_summary="Cheque dishonoured due to funds insufficient"
    )
    assert "SECTION 138" in notice["title"]
    assert notice["statutory_period_days"] == 15
    assert "250,000" in notice["formatted_notice_text"]
    print(f"Legal Notice Engine passed! Docket: {notice['tracking_docket']}")

def test_agreement_risk_analyzer():
    sample_contract = """
    EMPLOYMENT AGREEMENT
    1. The employee shall not engage in any competing business anywhere in India for a period of 2 years post-termination.
    2. Employee shall be bound by a 36-month lock-in period with liquidated damages of Rs. 5,00,000.
    3. The employer may terminate immediately without notice, while employee must provide 90 days notice.
    """
    analysis = AgreementRiskEngine.analyze_agreement("employment", sample_contract)
    assert analysis["overall_risk_score"] >= 60
    assert analysis["total_clauses_flagged"] >= 2
    assert any("SECTION 27" in f["statutory_analysis"].upper() for f in analysis["findings"])
    print(f"Agreement Risk Analyzer passed! Risk score: {analysis['overall_risk_score']}")

def test_tax_regime_and_44ada():
    # 1. Tax Regime Comparison for ₹15 Lakh income
    tax = TaxRegimeEngine.compare_tax_regimes(
        gross_annual_income=1500000.0,
        deduction_80c=150000.0,
        deduction_80d=25000.0,
        home_loan_interest_24b=0.0
    )
    assert tax["new_regime"]["total_tax_payable_inr"] > 0
    assert tax["comparison"]["recommended_regime"] in ("NEW_REGIME", "OLD_REGIME")
    print(f"Tax Regime Comparator passed! Recommended: {tax['comparison']['recommended_regime']} (Savings: Rs. {tax['comparison']['net_tax_saved_inr']:,.2f})")

    # 2. Section 44ADA Presumptive Tax for ₹40 Lakh tech consultant
    pres = PresumptiveTaxEngine.calculate_44ada(gross_professional_receipts=4000000.0, actual_business_expenses=500000.0)
    assert pres["deemed_taxable_profit_inr"] == 2000000.0
    assert pres["is_eligible_under_75_lakhs"] is True
    print(f"Section 44ADA Presumptive Tax passed! Deemed Profit: Rs. {pres['deemed_taxable_profit_inr']:,.2f}")

if __name__ == "__main__":
    test_credit_card_personalized_ranking()
    test_credit_card_upgrade_calculator()
    test_revenue_optimizer()
    test_corporate_action_multiplier()
    test_succession_noc()
    test_hra_rent_receipt_and_exemption()
    test_hindu_succession_share_calculator()
    test_vehicle_compliance_radar()
    test_loan_mitra_matching()
    test_loan_mitra_balance_transfer()
    test_loan_mitra_crm()
    test_lookup_rails()
    test_legal_notice_engine()
    test_agreement_risk_analyzer()
    test_tax_regime_and_44ada()
    print("\nALL 15+ ENGINES (LOAN MITRA, CARDSMART, VAKIL & CA INDIA, PUBLIC RAILS) PASSED AUTOMATED TESTS SUCCESSFULLY!")

