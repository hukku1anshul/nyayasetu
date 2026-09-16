"""
Automated Integration Tests for NyayaSetu & CardSmart FastAPI Endpoints
"""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8000"

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers={"User-Agent": "TestClient/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def post(path, body):
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "TestClient/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def run_tests():
    print("Testing NyayaSetu API Endpoints on localhost:8000...")

    # 1. Test IFSC
    code, res = get("/api/v1/lookup/ifsc/HDFC0000001")
    assert code == 200 and res.get("success") is True, f"IFSC Failed: {res}"
    print(f"PASS: /api/v1/lookup/ifsc/HDFC0000001 -> Bank: {res['bank']}, Branch: {res['branch']}")

    # 2. Test Pincode
    code, res = get("/api/v1/lookup/pincode/560038")
    assert code == 200 and res.get("success") is True, f"Pincode Failed: {res}"
    print(f"PASS: /api/v1/lookup/pincode/560038 -> District: {res['district']}, State: {res['state']}")

    # 3. Test PAN Validation
    code, res = post("/api/v1/lookup/validate-pan", {"pan_number": "ABCPE1234F"})
    assert code == 200 and res.get("valid") is True, f"PAN Failed: {res}"
    print(f"PASS: /api/v1/lookup/validate-pan -> Entity: {res['entity_type']}")

    # 4. Test GSTIN Validation
    code, res = post("/api/v1/lookup/validate-gstin", {"gstin": "27ABCPD9012H1Z5"})
    assert code == 200 and res.get("valid") is True, f"GSTIN Failed: {res}"
    print(f"PASS: /api/v1/lookup/validate-gstin -> State: {res['state_name']} ({res['state_code']})")

    # 5. Test Legal Notice Generator
    code, res = post("/api/v1/legal/generate-notice", {
        "notice_type": "CHEQUE_BOUNCE_SEC138",
        "sender_name": "Kunal Deshmukh",
        "sender_address": "Pune, Maharashtra",
        "recipient_name": "Vertex Logistics Pvt Ltd",
        "recipient_address": "Mumbai, Maharashtra",
        "claim_amount_inr": 250000,
        "transaction_date": "2026-08-15",
        "instrument_or_reference_no": "Cheque #440912",
        "dispute_summary": "Funds Insufficient"
    })
    assert code == 200 and res.get("tracking_docket"), f"Notice Gen Failed: {res}"
    print(f"PASS: /api/v1/legal/generate-notice -> Docket: {res['tracking_docket']}, Cure Days: {res['statutory_period_days']}")

    # 6. Test Agreement Risk Analyzer
    code, res = post("/api/v1/legal/analyze-agreement", {
        "agreement_type": "employment",
        "agreement_text": "Clause 14 (Non-Compete): Employee agrees to a non-compete covenant and shall not work in competing business for 24 months post-termination. Clause 17: Mandatory training bond of Rs 3,00,000."
    })
    assert code == 200 and res.get("risk_score") >= 60, f"Agreement Analysis Failed: {res}"
    print(f"PASS: /api/v1/legal/analyze-agreement -> Risk Score: {res['risk_score']}/100, Level: {res['overall_risk_level']}")

    # 7. Test Tax Regime Comparison
    code, res = post("/api/v1/tax/compare-regimes", {
        "gross_annual_income": 1800000,
        "deduction_80c": 150000,
        "deduction_80d": 25000,
        "home_loan_interest_24b": 200000,
        "hra_exemption_10_13a": 180000
    })
    assert code == 200 and "recommended_regime" in res, f"Tax Regime Failed: {res}"
    print(f"PASS: /api/v1/tax/compare-regimes -> Recommended: {res['recommended_regime']}, Savings: Rs. {res['tax_savings']}")

    # 8. Test Section 44ADA Presumptive Tax
    code, res = post("/api/v1/tax/presumptive-44ada", {
        "gross_professional_receipts": 3200000,
        "actual_business_expenses": 0.0
    })
    assert code == 200 and res.get("eligible") is True, f"44ADA Failed: {res}"
    print(f"PASS: /api/v1/tax/presumptive-44ada -> Deemed Profit: Rs. {res['deemed_profit']}, Net Tax: Rs. {res['tax_payable']}")

    # 9. Test Notice Explainer
    code, res = get("/api/v1/tax/explain-notice/143_1")
    assert code == 200 and res.get("section_code") == "Section 143(1)", f"Explainer Failed: {res}"
    print(f"PASS: /api/v1/tax/explain-notice/143_1 -> Section: {res['section_code']}, Severity: {res['severity']}")

    # 10. Test User Activity History
    code, post_res = post("/api/v1/user/history", {
        "category": "LEGAL_NOTICE",
        "title": "Section 138 Cheque Bounce Notice",
        "summary": "Served demand for Rs 250,000 to Vertex Logistics",
        "data": {"amount": 250000}
    })
    assert code == 200 and post_res.get("success") is True, f"History POST Failed: {post_res}"
    
    code, get_res = get("/api/v1/user/history")
    assert code == 200 and get_res.get("success") is True and len(get_res.get("history", [])) > 0, f"History GET Failed: {get_res}"
    print(f"PASS: /api/v1/user/history -> Persisted entries count: {len(get_res['history'])}")

    # 11. Test MCA Corporate CIN Validation
    code, res = post("/api/v1/lookup/validate-cin", {"cin_number": "U72200KA2020PTC134567"})
    assert code == 200 and res.get("valid") is True, f"CIN Failed: {res}"
    print(f"PASS: /api/v1/lookup/validate-cin -> Industry: {res['industry_sector']}, RoC: {res['roc_jurisdiction']}")

    # 12. Test NPCI UPI VPA Validation
    code, res = post("/api/v1/lookup/validate-upi", {"upi_id": "merchant@okhdfcbank"})
    assert code == 200 and res.get("valid") is True, f"UPI Failed: {res}"
    print(f"PASS: /api/v1/lookup/validate-upi -> Sponsor: {res['sponsor_bank']}, TPAP: {res['tpap_app']}")

    # 13. Test RBI Card BIN Intelligence
    code, res = post("/api/v1/lookup/card-bin", {"bin_number": "405520"})
    assert code == 200 and res.get("valid") is True, f"Card BIN Failed: {res}"
    print(f"PASS: /api/v1/lookup/card-bin -> Issuer: {res['bank']}, Network: {res['network']} ({res['tier']})")

    # 14. Test eCourts CNR Case Decoder
    code, res = post("/api/v1/lookup/decode-cnr", {"cnr_number": "MHAU010012342026"})
    assert code == 200 and res.get("valid") is True, f"CNR Failed: {res}"
    print(f"PASS: /api/v1/lookup/decode-cnr -> Court: {res['court_name']}, Identifier: {res['case_identifier']}")


    # 15. Test EPFO Passbook Diagnostic
    code, res = post("/api/v1/epfo/diagnose-passbook", {
        "member_name_epfo": "Rahul Sharma",
        "member_name_aadhaar": "Rahul K Sharma",
        "father_name_epfo": "S. P. Sharma",
        "father_name_id": "Surya Prakash Sharma",
        "has_date_of_exit": False,
        "is_aadhaar_seeded": True,
        "is_pan_linked": True,
        "service_years": 5.2
    })
    assert code == 200 and res.get("rejection_risk_score") > 50, f"EPFO Diagnose Failed: {res}"
    print(f"PASS: /api/v1/epfo/diagnose-passbook -> Risk Score: {res['rejection_risk_score']}, Level: {res['risk_level']}")

    # 16. Test EPFO Joint Declaration
    code, res = post("/api/v1/epfo/generate-joint-declaration", {
        "uan": "101234567890",
        "member_name_correct": "Rahul K Sharma",
        "member_name_wrong": "Rahul Sharma",
        "father_name_correct": "Surya Prakash Sharma",
        "father_name_wrong": "S. P. Sharma",
        "dob_correct": "1990-08-15",
        "establishment_name": "Tech Corp Pvt Ltd"
    })
    assert code == 200 and res.get("success") is True, f"EPFO JD Failed: {res}"
    print(f"PASS: /api/v1/epfo/generate-joint-declaration -> Docket: {res['docket_number']}")

    # 17. Test Stamp Duty Calculator
    code, res = post("/api/v1/property/calculate-stamp-duty", {
        "state_code": "MH",
        "agreed_value_inr": 8500000,
        "carpet_area_sqft": 750,
        "circle_rate_per_sqft": 9000,
        "buyer_gender": "female",
        "is_urban": True
    })
    assert code == 200 and res.get("total_government_outflow_inr") > 0, f"Stamp Duty Failed: {res}"
    print(f"PASS: /api/v1/property/calculate-stamp-duty -> State: {res['state_name']}, Outflow: Rs. {res['total_government_outflow_inr']}")

    # 18. Test CIBIL Remark Diagnostic
    code, res = post("/api/v1/credit/diagnose-cibil-remark", {
        "remark_code": "WRITTEN_OFF",
        "bank_name": "State Bank of India",
        "account_number": "33400192831",
        "disputed_amount_inr": 45000
    })
    assert code == 200 and res.get("severity_level") == "CRITICAL", f"CIBIL Diagnose Failed: {res}"
    print(f"PASS: /api/v1/credit/diagnose-cibil-remark -> Severity: {res['severity_level']}, RBI Penalty: Rs. {res['rbi_penalty_per_day_inr']}/day")

    # 19. Test CICRA Dispute Notice
    code, res = post("/api/v1/credit/generate-cicra-notice", {
        "complainant_name": "Aman Mehra",
        "complainant_pan": "ABCDE1234F",
        "complainant_mobile": "9876543210",
        "complainant_address": "Indiranagar, Bangalore",
        "lender_bank_name": "State Bank of India",
        "account_number": "33400192831",
        "remark_type": "WRITTEN_OFF",
        "disputed_amount_inr": 45000
    })
    assert code == 200 and res.get("success") is True, f"CICRA Notice Failed: {res}"
    print(f"PASS: /api/v1/credit/generate-cicra-notice -> Docket: {res['docket_number']}, Period: {res['statutory_period_days']} days")

    # 20. Test Gratuity & Retirement Shield
    code, res = post("/api/v1/tax/calculate-gratuity", {
        "last_drawn_basic_monthly": 80000,
        "last_drawn_da_monthly": 5000,
        "years_of_service": 8.5,
        "is_covered_under_act": True,
        "leave_encashment_received_inr": 400000
    })
    assert code == 200 and res.get("statutory_gratuity_amount_inr") > 0, f"Gratuity Failed: {res}"
    print(f"PASS: /api/v1/tax/calculate-gratuity -> Gratuity: Rs. {res['statutory_gratuity_amount_inr']}, Taxable: Rs. {res['taxable_gratuity_inr']}")

    # 21. Test Model Tenancy Act Rental Agreement
    code, res = post("/api/v1/legal/generate-rental-agreement", {
        "landlord_name": "Anil Kapoor",
        "landlord_address": "Juhu, Mumbai",
        "tenant_name": "Vikram Seth",
        "tenant_address": "Koramangala, Bengaluru",
        "property_address": "Flat 801, Sea View Apartments, Worli, Mumbai",
        "monthly_rent": 50000,
        "security_deposit": 100000,
        "tenure_months": 11,
        "property_type": "residential",
        "state": "MH"
    })
    assert code == 200 and "agreement_markdown" in res, f"Rental Agreement Failed: {res}"
    print(f"PASS: /api/v1/legal/generate-rental-agreement -> MTA Compliant: {res['is_mta_compliant']}, Score: {res['compliance_score']}")


    # 22. Test Consumer Forum Complaint (e-Daakhil)
    code, res = post("/api/v1/legal/draft-consumer-complaint", {
        "complainant_name": "Vikram Seth",
        "complainant_address": "Koramangala, Bangalore",
        "complainant_mobile": "9876543210",
        "respondent_name": "Flipkart India Pvt Ltd",
        "respondent_address": "Bellandur, Bangalore",
        "dispute_category": "ECOMMERCE",
        "transaction_amount": 28000,
        "compensation_demanded": 35000
    })
    assert code == 200 and res.get("success") is True, f"Consumer Complaint Failed: {res}"
    print(f"PASS: /api/v1/legal/draft-consumer-complaint -> Docket: {res['docket_number']}, Forum: {res['forum']}")

    # 23. Test RTI Application
    code, res = post("/api/v1/legal/draft-rti-application", {
        "applicant_name": "Deepak Joshi",
        "applicant_address": "Civil Lines, Jaipur",
        "applicant_mobile": "9876543210",
        "public_authority_name": "Regional Passport Office",
        "public_authority_address": "Jaipur",
        "subject_matter": "Passport Delay #JP10829102",
        "information_points": ["Reason for delay", "Date police verification received"]
    })
    assert code == 200 and res.get("success") is True, f"RTI Failed: {res}"
    print(f"PASS: /api/v1/legal/draft-rti-application -> Docket: {res['docket_number']}, Authority: {res['public_authority']}")

    # 24. Test Cyber Crime Complaint (1930)
    code, res = post("/api/v1/legal/draft-cybercrime-complaint", {
        "victim_name": "Pooja Hegde",
        "victim_mobile": "9876543210",
        "victim_email": "pooja@gmail.com",
        "victim_address": "Andheri West, Mumbai",
        "incident_category": "UPI_FRAUD",
        "total_loss_inr": 52000
    })
    assert code == 200 and res.get("success") is True, f"Cyber Complaint Failed: {res}"
    print(f"PASS: /api/v1/legal/draft-cybercrime-complaint -> Docket: {res['docket_number']}, Helpline: {res['helpline']}")

    # 25. Test General Sworn Affidavit
    code, res = post("/api/v1/legal/generate-affidavit", {
        "deponent_name": "Rohan Mehra",
        "deponent_parent_name": "Sanjay Mehra",
        "deponent_age": 28,
        "deponent_residence": "Bandra West, Mumbai",
        "affidavit_type": "NAME_CORRECTION",
        "state_name": "Maharashtra"
    })
    assert code == 200 and res.get("success") is True, f"Affidavit Failed: {res}"
    print(f"PASS: /api/v1/legal/generate-affidavit -> Docket: {res['docket_number']}, Stamp: Rs. {res['recommended_stamp_paper_inr']}")

    # 26. Test Tax Rectification 154
    code, res = post("/api/v1/tax/draft-rectification-154", {
        "taxpayer_name": "Ananya Roy",
        "pan": "ABCDE1234F",
        "assessment_year": "2025-26",
        "acknowledgement_no": "89102941029102",
        "rectification_reason": "TDS_MISMATCH",
        "claimed_refund_inr": 42000
    })
    assert code == 200 and res.get("success") is True, f"Tax Rectification Failed: {res}"
    print(f"PASS: /api/v1/tax/draft-rectification-154 -> Docket: {res['docket_number']}, AY: {res['assessment_year']}")

    print("\nSUCCESS: ALL 26 REST API ENDPOINTS VERIFIED & FULLY FUNCTIONAL!")



if __name__ == "__main__":
    run_tests()
