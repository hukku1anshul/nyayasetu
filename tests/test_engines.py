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

if __name__ == "__main__":
    test_credit_card_personalized_ranking()
    test_credit_card_upgrade_calculator()
    test_revenue_optimizer()
    test_corporate_action_multiplier()
    test_succession_noc()
    test_hra_rent_receipt_and_exemption()
    test_hindu_succession_share_calculator()
    test_vehicle_compliance_radar()
    print("\nALL FREE VIRAL TOOLS, CARDSMART & NYAYASETU ENGINE TESTS PASSED SUCCESSFULLY!")
