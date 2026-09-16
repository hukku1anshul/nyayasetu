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

    print("\nSUCCESS: ALL 10 REST API ENDPOINTS VERIFIED & FULLY FUNCTIONAL!")

if __name__ == "__main__":
    run_tests()
