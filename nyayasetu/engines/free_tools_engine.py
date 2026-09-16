"""
Free Viral Consumer Utilities & Calculators Engine
High-Traffic, Zero-CAC Lead Magnets for the Indian Market:
1. HRA Rent Receipt & Tax Exemption Engine (Section 10(13A))
2. Statutory Legal Heir Inheritance Share Calculator (Hindu Succession Act)
3. Multi-State Vehicle Compliance & Challan Radar
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date
import math

class HRARentReceiptEngine:
    """
    Generates statutory monthly rent receipts with revenue stamp formatting,
    landlord PAN verification, and Section 10(13A) Income Tax HRA exemption calculation.
    """

    @staticmethod
    def calculate_hra_exemption(
        basic_salary_annual: float,
        dearness_allowance_annual: float,
        hra_received_annual: float,
        rent_paid_annual: float,
        is_metro_city: bool = True
    ) -> Dict[str, Any]:
        """
        Calculates statutory HRA exemption under Section 10(13A) Rule 2A:
        Least of the following 3 amounts is exempt from Income Tax:
        1. Actual HRA received
        2. 50% of (Basic + DA) for Metro cities (40% for Non-Metro)
        3. Excess of Rent Paid over 10% of (Basic + DA)
        """
        salary_base = basic_salary_annual + dearness_allowance_annual
        ten_pct_salary = 0.10 * salary_base

        clause_1_actual_hra = hra_received_annual
        clause_2_metro_pct = (0.50 if is_metro_city else 0.40) * salary_base
        clause_3_rent_excess = max(0.0, rent_paid_annual - ten_pct_salary)

        exempt_hra = min(clause_1_actual_hra, clause_2_metro_pct, clause_3_rent_excess)
        taxable_hra = max(0.0, hra_received_annual - exempt_hra)

        # Mandatory Landlord PAN check under Section 139A (if rent > ₹1 Lakh/year or > ₹8,333/month)
        landlord_pan_mandatory = rent_paid_annual > 100000.0

        return {
            "basic_plus_da_annual": salary_base,
            "rent_paid_annual": rent_paid_annual,
            "hra_received_annual": hra_received_annual,
            "is_metro_city": is_metro_city,
            "clause_1_actual_hra": clause_1_actual_hra,
            "clause_2_salary_pct": clause_2_metro_pct,
            "clause_3_rent_excess": clause_3_rent_excess,
            "exempt_hra_amount_inr": round(exempt_hra, 2),
            "taxable_hra_amount_inr": round(taxable_hra, 2),
            "landlord_pan_mandatory": landlord_pan_mandatory,
            "pan_compliance_note": (
                "Mandatory to furnish Landlord PAN to employer since annual rent exceeds Rs. 1,00,000 (Section 139A)"
                if landlord_pan_mandatory else
                "Landlord PAN is optional as annual rent is below Rs. 1,00,000"
            )
        }

    @staticmethod
    def generate_receipts_manifest(
        tenant_name: str,
        landlord_name: str,
        landlord_pan: str,
        rental_property_address: str,
        monthly_rent: float,
        financial_year: str = "2026-27"
    ) -> Dict[str, Any]:
        """
        Generates 12 monthly receipts payload ready for printing or instant PDF generation.
        """
        months = [
            "April", "May", "June", "July", "August", "September",
            "October", "November", "December", "January", "February", "March"
        ]
        start_year = int(financial_year.split("-")[0])

        receipts = []
        for idx, month in enumerate(months):
            curr_year = start_year if idx < 9 else start_year + 1
            receipt_id = f"REC-{curr_year}-{idx+1:02d}"
            receipts.append({
                "receipt_no": receipt_id,
                "month": f"{month} {curr_year}",
                "tenant": tenant_name,
                "landlord": landlord_name,
                "landlord_pan": landlord_pan if landlord_pan else "NOT APPLICABLE",
                "property_address": rental_property_address,
                "amount_inr": monthly_rent,
                "revenue_stamp_required": monthly_rent > 5000.0,
                "signature_placeholder": f"Signed by {landlord_name}"
            })

        return {
            "tenant_name": tenant_name,
            "landlord_name": landlord_name,
            "annual_rent_paid": monthly_rent * 12,
            "financial_year": financial_year,
            "total_receipts_generated": len(receipts),
            "receipts": receipts
        }


class InheritanceShareCalculator:
    """
    Computes statutory percentage and fractional inheritance shares under the
    Hindu Succession Act, 1956 (as amended by 2005 Amendment Act for equal coparcenary daughter rights).
    """

    @staticmethod
    def calculate_hindu_succession_shares(
        deceased_gender: str,  # 'MALE' or 'FEMALE'
        total_estate_value_inr: float,
        surviving_spouse: bool,
        surviving_mother: bool,
        surviving_father: bool,
        sons_count: int,
        daughters_count: int
    ) -> Dict[str, Any]:
        """
        Applies Class-I legal heir statutory distribution:
        - For a Deceased Male: Class-I heirs inherit equal simultaneous shares.
          Class-I heirs include: Widow, Mother, Sons, and Daughters.
          (Father is a Class-II heir and receives nothing if any Class-I heir exists).
        """
        gender = deceased_gender.upper().strip()
        heir_breakdown = []

        if gender == "MALE":
            # Count total eligible Class-I heads
            class_1_heads = 0
            if surviving_spouse:
                class_1_heads += 1
            if surviving_mother:
                class_1_heads += 1
            class_1_heads += (sons_count + daughters_count)

            if class_1_heads == 0:
                # Class II fallback (Father, siblings)
                if surviving_father:
                    return {
                        "statutory_act": "Hindu Succession Act, 1956 (Section 8, Class-II)",
                        "notes": "No Class-I heirs exist; Father inherits 100% as Entry-I of Class-II.",
                        "heirs": [{"category": "Father", "share_pct": 100.0, "value_inr": total_estate_value_inr}]
                    }
                return {"error": "No immediate Class-I or Class-II Entry-I heirs specified"}

            equal_share_pct = 100.0 / class_1_heads
            equal_share_val = total_estate_value_inr / class_1_heads

            if surviving_spouse:
                heir_breakdown.append({
                    "relationship": "Surviving Widow (Wife)",
                    "count": 1,
                    "fractional_share": f"1/{class_1_heads}",
                    "share_pct": round(equal_share_pct, 2),
                    "share_value_inr": round(equal_share_val, 2),
                    "statutory_tier": "Class-I Statutory Heir"
                })

            if surviving_mother:
                heir_breakdown.append({
                    "relationship": "Mother of Deceased",
                    "count": 1,
                    "fractional_share": f"1/{class_1_heads}",
                    "share_pct": round(equal_share_pct, 2),
                    "share_value_inr": round(equal_share_val, 2),
                    "statutory_tier": "Class-I Statutory Heir"
                })

            if sons_count > 0:
                total_sons_pct = equal_share_pct * sons_count
                total_sons_val = equal_share_val * sons_count
                heir_breakdown.append({
                    "relationship": f"Sons ({sons_count})",
                    "count": sons_count,
                    "per_person_fractional_share": f"1/{class_1_heads}",
                    "per_person_share_pct": round(equal_share_pct, 2),
                    "total_category_share_pct": round(total_sons_pct, 2),
                    "share_pct": round(total_sons_pct, 2),
                    "total_category_value_inr": round(total_sons_val, 2),
                    "share_value_inr": round(total_sons_val, 2),
                    "statutory_tier": "Class-I Statutory Heir"
                })

            if daughters_count > 0:
                total_dtr_pct = equal_share_pct * daughters_count
                total_dtr_val = equal_share_val * daughters_count
                heir_breakdown.append({
                    "relationship": f"Daughters ({daughters_count})",
                    "count": daughters_count,
                    "per_person_fractional_share": f"1/{class_1_heads}",
                    "per_person_share_pct": round(equal_share_pct, 2),
                    "total_category_share_pct": round(total_dtr_pct, 2),
                    "share_pct": round(total_dtr_pct, 2),
                    "total_category_value_inr": round(total_dtr_val, 2),
                    "share_value_inr": round(total_dtr_val, 2),
                    "statutory_tier": "Class-I Statutory Heir (Equal Rights via 2005 Amendment)"
                })

            father_note = (
                "Father is a Class-II heir and is statutorily excluded because Class-I heirs exist."
                if surviving_father else None
            )

        else:
            # Deceased Female (Section 15)
            # Property devolves: 1st on sons and daughters (including children of predeceased) and husband
            heads = (sons_count + daughters_count) + (1 if surviving_spouse else 0)
            equal_share_pct = 100.0 / max(1, heads)
            equal_share_val = total_estate_value_inr / max(1, heads)

            if surviving_spouse:
                heir_breakdown.append({
                    "relationship": "Surviving Husband",
                    "count": 1,
                    "share_pct": round(equal_share_pct, 2),
                    "share_value_inr": round(equal_share_val, 2),
                    "statutory_tier": "Section 15(1)(a) Heir"
                })
            if (sons_count + daughters_count) > 0:
                tot_children_cnt = sons_count + daughters_count
                tot_children_pct = equal_share_pct * tot_children_cnt
                tot_children_val = equal_share_val * tot_children_cnt
                heir_breakdown.append({
                    "relationship": f"Children ({sons_count} Sons, {daughters_count} Daughters)",
                    "count": tot_children_cnt,
                    "per_child_share_pct": round(equal_share_pct, 2),
                    "share_pct": round(tot_children_pct, 2),
                    "total_category_value_inr": round(tot_children_val, 2),
                    "share_value_inr": round(tot_children_val, 2),
                    "statutory_tier": "Section 15(1)(a) Heirs"
                })
            father_note = None

        return {
            "deceased_gender": gender,
            "total_estate_valuation_inr": total_estate_value_inr,
            "governing_law": "Hindu Succession Act, 1956 (Amended 2005)",
            "statutory_heir_distribution": heir_breakdown,
            "father_statutory_exclusion_note": father_note,
            "next_step_recommendation": (
                "Generate Form-C Relinquishment Deeds or initiate IEPF / Probate Transmission claim"
            )
        }


class VehicleComplianceRadar:
    """
    Aggregates simulated multi-state e-Challan, PUCC pollution validity,
    and bank loan hypothecation (HP) status without captcha friction.
    """

    @staticmethod
    def audit_vehicle_health(registration_number: str) -> Dict[str, Any]:
        clean_reg = registration_number.upper().replace(" ", "").replace("-", "")

        # State code extraction
        state_code = clean_reg[:2]
        state_names = {
            "DL": "Delhi-NCR",
            "KA": "Karnataka",
            "MH": "Maharashtra",
            "UP": "Uttar Pradesh",
            "TS": "Telangana",
            "TN": "Tamil Nadu",
            "HR": "Haryana"
        }
        state_name = state_names.get(state_code, "All India / State RTO")

        # Mock comprehensive radar report
        return {
            "registration_number": clean_reg,
            "jurisdiction_state": state_name,
            "fitness_validity": "15-Aug-2032 (Active)",
            "insurance_status": {
                "policy_active": True,
                "insurer": "HDFC ERGO General Insurance",
                "expiry_date": "24-Oct-2026",
                "days_to_expiry": 38
            },
            "pucc_emission_status": {
                "valid": True,
                "expiry_date": "10-Nov-2026",
                "tested_zone": f"{state_name} Transport Auth"
            },
            "hypothecation_status": {
                "has_bank_lien": True,
                "lender_bank": "HDFC Bank Limited",
                "hp_removal_required": True,
                "form_35_status": "Lien active on RC smartcard"
            },
            "pending_challans_summary": {
                "total_pending_count": 2,
                "total_fine_amount_inr": 2000.0,
                "challans": [
                    {
                        "challan_no": f"CH-{clean_reg}-992",
                        "offense": "Violation of Mandatory Traffic Sign (Over-speeding)",
                        "location": f"{state_name} Outer Ring Road",
                        "fine_inr": 1000.0,
                        "status": "SENT TO VIRTUAL COURT"
                    },
                    {
                        "challan_no": f"CH-{clean_reg}-884",
                        "offense": "Improper / Unauthorized Parking",
                        "location": "Commercial Street",
                        "fine_inr": 1000.0,
                        "status": "PENDING AT TRAFFIC POLICE"
                    }
                ]
            },
            "upsell_bridges": [
                {"service": "Virtual Court Challan Settlement", "price_inr": 499.0},
                {"service": "RTO Form 35 Bank HP Removal Concierge", "price_inr": 2999.0},
                {"service": "Interstate Vehicle NOC (Form 28)", "price_inr": 3499.0}
            ]
        }
