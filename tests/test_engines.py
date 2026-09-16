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
from nyayasetu.engines.epfo_engine import EPFOEngine
from nyayasetu.engines.stamp_duty_engine import StampDutyEngine
from nyayasetu.engines.cibil_dispute_engine import CIBILDisputeEngine
from nyayasetu.engines.gratuity_engine import GratuityEngine
from nyayasetu.engines.rental_agreement_engine import RentalAgreementEngine
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

    # 5. MCA Corporate CIN validation
    cin = LookupRailsEngine.validate_cin("U72200KA2020PTC134567")
    assert cin["valid"] is True
    assert "Software" in cin["industry_sector"]
    assert "Karnataka" in cin["roc_jurisdiction"]

    # 6. NPCI UPI VPA validation
    upi = LookupRailsEngine.validate_upi_vpa("merchant@okhdfcbank")
    assert upi["valid"] is True
    assert "HDFC Bank" in upi["sponsor_bank"]

    # 7. RBI Card BIN intelligence
    bin_info = LookupRailsEngine.lookup_card_bin("405520")
    assert bin_info["valid"] is True
    assert "HDFC Bank" in bin_info["bank"]
    assert bin_info["network"] == "Visa"

    # 8. eCourts CNR case decoder
    cnr = LookupRailsEngine.decode_ecourts_cnr("MHAU010012342026")
    assert cnr["valid"] is True
    assert "Aurangabad" in cnr["court_name"]
    print("All 8 Zero-Cost Public Rails (IFSC, Pincode, PAN, GSTIN, CIN, UPI, BIN, CNR) passed!")

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


def test_epfo_passbook_and_joint_declaration():
    # 1. Passbook diagnosis
    diag = EPFOEngine.diagnose_passbook(
        member_name_epfo="Aditya Verma",
        member_name_aadhaar="Aditya K Verma",
        father_name_epfo="R. K. Verma",
        father_name_id="Ram Kumar Verma",
        has_date_of_exit=False,
        is_aadhaar_seeded=True,
        is_pan_linked=True,
        service_years=4.5
    )
    assert diag["rejection_risk_score"] > 50
    assert "CRITICAL" in diag["risk_level"] or "HIGH" in diag["risk_level"]
    assert len(diag["findings"]) >= 2
    print(f"EPFO Passbook Diagnostic passed! Risk Score: {diag['rejection_risk_score']} ({diag['risk_level']})")

    # 2. Joint declaration generation
    jd = EPFOEngine.generate_joint_declaration(
        uan="101234567890",
        member_name_correct="Aditya K Verma",
        member_name_wrong="Aditya Verma",
        father_name_correct="Ram Kumar Verma",
        father_name_wrong="R. K. Verma",
        dob_correct="1992-05-15",
        dob_wrong="1992-05-18",
        doj_correct="2020-01-01",
        doe_correct="2024-01-01",
        establishment_name="Acme Infotech Ltd"
    )
    assert "JOINT DECLARATION" in jd["form_text"]
    assert "101234567890" in jd["form_text"]
    print("EPFO Joint Declaration Generator passed!")

def test_stamp_duty_calculator():
    res = StampDutyEngine.calculate_stamp_duty(
        state_code="MH",
        agreed_value_inr=10000000.0, # 1 Crore
        carpet_area_sqft=800.0,
        circle_rate_per_sqft=11000.0, # circle value = 88 Lakhs, taxable = 1 Crore
        buyer_gender="female",
        is_urban=True
    )
    assert "Maharashtra" in res["state_name"]
    assert res["statutory_taxable_value_inr"] == 10000000.0
    assert res["female_buyer_savings_inr"] > 0 # Female rebate 1%
    assert res["total_government_outflow_inr"] > 0
    print(f"Stamp Duty Calculator passed! Total Govt Charges: Rs. {res['total_government_outflow_inr']:,.2f}")

def test_cibil_dispute_and_notice():
    diag = CIBILDisputeEngine.diagnose_remark(
        remark_code="WRITTEN_OFF",
        bank_name="HDFC Bank",
        account_number="50100456789012",
        disputed_amount_inr=75000.0
    )
    assert diag["severity_level"] == "CRITICAL"
    assert abs(diag["estimated_score_penalty"]) >= 70
    print(f"CIBIL Remark Diagnostic passed! Severity: {diag['severity_level']} (Hit: {diag['estimated_score_penalty']} pts)")

    notice = CIBILDisputeEngine.generate_cicra_dispute_notice(
        complainant_name="Sunil Sharma",
        complainant_pan="ABCPS1234E",
        complainant_mobile="9876543210",
        complainant_address="B-402, Powai, Mumbai",
        lender_bank_name="HDFC Bank",
        account_number="50100456789012",
        remark_type="WRITTEN_OFF",
        disputed_amount_inr=75000.0
    )
    assert "SECTION 21" in notice["notice_text"]
    assert "HDFC Bank" in notice["notice_text"]
    print("CICRA 2005 Section 21 Dispute Notice Generator passed!")

def test_gratuity_and_pension():
    res = GratuityEngine.calculate_retirement_benefits(
        last_drawn_basic_monthly=100000.0,
        last_drawn_da_monthly=10000.0,
        years_of_service=12.6, # rounds to 13 years
        is_covered_under_act=True,
        leave_encashment_received_inr=800000.0
    )
    assert res["statutory_gratuity_amount_inr"] > 0
    assert res["exempt_gratuity_section_10_10_inr"] <= 2000000.0
    assert "Eligible" in res["pension_eligibility_status"]
    print(f"Gratuity & Pension Shield passed! Gratuity: Rs. {res['statutory_gratuity_amount_inr']:,.2f}, Taxable: Rs. {res['taxable_gratuity_inr']:,.2f}")

def test_rental_agreement_and_mta_audit():
    audit = RentalAgreementEngine.audit_and_generate(
        landlord_name="Ramesh Gupta",
        landlord_address="Flat 101, Bandra West, Mumbai",
        tenant_name="Priya Nair",
        tenant_address="A-203, Andheri East, Mumbai",
        property_address="Flat 402, Palm Heights, Bandra, Mumbai",
        monthly_rent=40000.0,
        security_deposit=150000.0, # Breaches 2 months cap
        tenure_months=11,
        property_type="residential",
        state="MH",
        notice_period_days=15 # Sub-statutory notice
    )
    assert audit["is_mta_compliant"] is False
    assert len(audit["violations"]) >= 2
    assert "LEASE AGREEMENT" in audit["agreement_markdown"]
    print(f"Model Tenancy Act Audit & Generator passed! Violations: {len(audit['violations'])}")

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
    test_epfo_passbook_and_joint_declaration()
    test_stamp_duty_calculator()
    test_cibil_dispute_and_notice()
    test_gratuity_and_pension()
    test_rental_agreement_and_mta_audit()
    print("\nALL 20+ ENGINES (LOAN MITRA, CARDSMART, VAKIL & CA INDIA, PUBLIC RAILS, AND 5 NEW MOATS) PASSED AUTOMATED TESTS SUCCESSFULLY!")
