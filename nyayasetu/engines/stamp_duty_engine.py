"""
Multi-State Land Stamp Duty, Circle Rate & Registration Fee Engine
Covers the top 8 Indian property markets: Maharashtra, Karnataka, Delhi, Uttar Pradesh,
Tamil Nadu, Telangana, Gujarat, and West Bengal.
Calculates statutory Stamp Duty %, Women Buyer Concessions, Metro / Infra Cesses,
Registration Fee Caps, and Section 50C Income Tax circle rate floor comparison.
"""

from typing import Dict, List, Any, Optional
import math

class StampDutyEngine:
    """
    Statutory property stamp duty and government registration fee calculator
    for Indian state Inspector General of Registration (IGR) authorities.
    """

    STATE_RATES = {
        "MH": {
            "name": "Maharashtra (IGR Maharashtra)",
            "base_rate_male": 5.0,
            "base_rate_female": 4.0,
            "base_rate_joint": 4.5,
            "metro_cess_pct": 1.0,
            "local_body_cess_pct": 1.0,
            "registration_fee_pct": 1.0,
            "registration_cap_inr": 30000.0,
            "female_rebate_note": "1% concession for female buyers on residential purchases (conditions apply)",
            "metro_cess_applicable": True
        },
        "KA": {
            "name": "Karnataka (Kaveri 2.0)",
            "slabs": [
                {"max_val": 2000000, "rate": 2.0},
                {"max_val": 4500000, "rate": 3.0},
                {"max_val": float("inf"), "rate": 5.0}
            ],
            "cess_on_duty_pct": 10.0,
            "surcharge_on_duty_pct": 2.0,
            "registration_fee_pct": 1.0,
            "registration_cap_inr": None,
            "female_rebate_note": "Same rates apply across genders; lower slabs for affordable housing"
        },
        "DL": {
            "name": "Delhi (Revenue Dept / DORIS)",
            "base_rate_male": 6.0,
            "base_rate_female": 4.0,
            "base_rate_joint": 5.0,
            "registration_fee_pct": 1.0,
            "registration_cap_inr": None,
            "female_rebate_note": "Significant 2.0% statutory concession for female sole owners"
        },
        "UP": {
            "name": "Uttar Pradesh (IGRSUP)",
            "base_rate_male": 7.0,
            "base_rate_female": 6.0,
            "base_rate_joint": 6.5,
            "registration_fee_pct": 1.0,
            "registration_cap_inr": None,
            "female_rebate_note": "1.0% concession for female buyers up to Rs. 10 Lakhs of property value"
        },
        "TN": {
            "name": "Tamil Nadu (TNREGINET)",
            "base_rate_male": 7.0,
            "base_rate_female": 7.0,
            "base_rate_joint": 7.0,
            "registration_fee_pct": 4.0,
            "registration_cap_inr": None,
            "female_rebate_note": "Uniform 7% stamp duty and 4% registration charge"
        },
        "TS": {
            "name": "Telangana (Registration & Stamps Dept)",
            "base_rate_male": 4.0,
            "transfer_duty_pct": 1.5,
            "registration_fee_pct": 0.5,
            "registration_cap_inr": None,
            "female_rebate_note": "Combined 6.0% (4% Stamp Duty + 1.5% Transfer Duty + 0.5% Registration Fee)"
        },
        "GJ": {
            "name": "Gujarat (Garvi Gujarat)",
            "base_rate_male": 4.9,
            "base_rate_female": 3.9,
            "base_rate_joint": 4.4,
            "registration_fee_pct": 1.0,
            "female_registration_exempt": True,
            "female_rebate_note": "Women buyers receive 1% duty concession and are 100% EXEMPT from registration fees"
        },
        "WB": {
            "name": "West Bengal (WB e-District IGR)",
            "rate_below_1cr": 5.0,
            "rate_above_1cr": 6.0,
            "registration_fee_pct": 1.0,
            "registration_cap_inr": None,
            "female_rebate_note": "Progressive 5% below Rs. 1 Crore, 6% above Rs. 1 Crore"
        }
    }

    @classmethod
    def calculate_stamp_duty(
        cls,
        state_code: str,
        agreed_value_inr: float,
        carpet_area_sqft: float = 0.0,
        circle_rate_per_sqft: float = 0.0,
        buyer_gender: str = "male",
        is_urban: bool = True
    ) -> Dict[str, Any]:
        """
        Calculates exact stamp duty, registration fee, and statutory cesses.
        Enforces Section 50C Income Tax rule: stamp valuation floor = max(agreed, circle_valuation).
        """
        clean_state = state_code.strip().upper()
        if clean_state not in cls.STATE_RATES:
            clean_state = "MH"

        info = cls.STATE_RATES[clean_state]

        # Section 50C Circle Rate Valuation
        circle_valuation = (carpet_area_sqft * circle_rate_per_sqft) if (carpet_area_sqft > 0 and circle_rate_per_sqft > 0) else 0.0
        taxable_value = max(agreed_value_inr, circle_valuation)
        is_circle_rate_higher = circle_valuation > agreed_value_inr

        stamp_duty = 0.0
        metro_cess = 0.0
        registration_fee = 0.0
        female_savings = 0.0

        if clean_state == "MH":
            rate = info["base_rate_female"] if buyer_gender == "female" else (info["base_rate_joint"] if buyer_gender == "joint" else info["base_rate_male"])
            stamp_duty = (rate / 100.0) * taxable_value
            if is_urban:
                metro_cess = (info["metro_cess_pct"] / 100.0) * taxable_value
            reg_calc = (info["registration_fee_pct"] / 100.0) * taxable_value
            registration_fee = min(reg_calc, info["registration_cap_inr"])
            male_duty = (info["base_rate_male"] / 100.0) * taxable_value
            female_savings = max(0.0, male_duty - stamp_duty)

        elif clean_state == "KA":
            slab_rate = 5.0
            for slab in info["slabs"]:
                if taxable_value <= slab["max_val"]:
                    slab_rate = slab["rate"]
                    break
            base_duty = (slab_rate / 100.0) * taxable_value
            cess = base_duty * (info["cess_on_duty_pct"] / 100.0)
            surcharge = base_duty * (info["surcharge_on_duty_pct"] / 100.0)
            stamp_duty = base_duty + cess + surcharge
            registration_fee = (info["registration_fee_pct"] / 100.0) * taxable_value

        elif clean_state == "DL":
            rate = info["base_rate_female"] if buyer_gender == "female" else (info["base_rate_joint"] if buyer_gender == "joint" else info["base_rate_male"])
            stamp_duty = (rate / 100.0) * taxable_value
            registration_fee = (info["registration_fee_pct"] / 100.0) * taxable_value
            male_duty = (info["base_rate_male"] / 100.0) * taxable_value
            female_savings = max(0.0, male_duty - stamp_duty)

        elif clean_state == "UP":
            rate = info["base_rate_female"] if buyer_gender == "female" else (info["base_rate_joint"] if buyer_gender == "joint" else info["base_rate_male"])
            stamp_duty = (rate / 100.0) * taxable_value
            registration_fee = (info["registration_fee_pct"] / 100.0) * taxable_value
            male_duty = (info["base_rate_male"] / 100.0) * taxable_value
            female_savings = max(0.0, male_duty - stamp_duty)

        elif clean_state == "GJ":
            rate = info["base_rate_female"] if buyer_gender == "female" else (info["base_rate_joint"] if buyer_gender == "joint" else info["base_rate_male"])
            stamp_duty = (rate / 100.0) * taxable_value
            if buyer_gender == "female":
                registration_fee = 0.0
                female_savings = ((info["base_rate_male"] - info["base_rate_female"]) / 100.0) * taxable_value + ((info["registration_fee_pct"] / 100.0) * taxable_value)
            else:
                registration_fee = (info["registration_fee_pct"] / 100.0) * taxable_value

        elif clean_state == "TS":
            base_duty = (info["base_rate_male"] / 100.0) * taxable_value
            transfer_duty = (info["transfer_duty_pct"] / 100.0) * taxable_value
            stamp_duty = base_duty + transfer_duty
            registration_fee = (info["registration_fee_pct"] / 100.0) * taxable_value

        elif clean_state == "WB":
            rate = info["rate_above_1cr"] if taxable_value > 10000000 else info["rate_below_1cr"]
            stamp_duty = (rate / 100.0) * taxable_value
            registration_fee = (info["registration_fee_pct"] / 100.0) * taxable_value

        else: # Default (TN / others)
            stamp_duty = (info.get("base_rate_male", 7.0) / 100.0) * taxable_value
            registration_fee = (info.get("registration_fee_pct", 1.0) / 100.0) * taxable_value

        total_gov_outflow = stamp_duty + metro_cess + registration_fee

        return {
            "state_code": clean_state,
            "state_name": info["name"],
            "agreed_value_inr": agreed_value_inr,
            "circle_rate_valuation_inr": round(circle_valuation, 2),
            "statutory_taxable_value_inr": round(taxable_value, 2),
            "is_circle_rate_higher": is_circle_rate_higher,
            "buyer_gender": buyer_gender,
            "stamp_duty_inr": round(stamp_duty, 2),
            "metro_or_local_cess_inr": round(metro_cess, 2),
            "registration_fee_inr": round(registration_fee, 2),
            "total_government_outflow_inr": round(total_gov_outflow, 2),
            "effective_tax_pct": round((total_gov_outflow / taxable_value) * 100.0, 2) if taxable_value > 0 else 0.0,
            "female_buyer_savings_inr": round(female_savings, 2),
            "statutory_note": info.get("female_rebate_note", "Calculated under State Stamp Act & Indian Registration Act 1908")
        }
