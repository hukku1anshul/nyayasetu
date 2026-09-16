"""
Hyper-Local Municipal Commercial Launchpad Engine
State / City Level B2B High-Ticket Service (₹15,000 - ₹50,000 / Outlet)
"""

from typing import Dict, List, Any

class MunicipalLaunchpadEngine:
    """
    Automates municipal clearances across major Indian metropolitan corporations.
    Solves the 'last-mile inspector friction' that pure software players abandon.
    """

    MUNICIPAL_BODIES = {
        "bengaluru": {
            "name": "Bruhat Bengaluru Mahanagara Palike (BBMP)",
            "state": "Karnataka",
            "portal": "BBMP e-Aasthi & Trade License Portal",
            "zonal_wards": 198
        },
        "mumbai": {
            "name": "Brihanmumbai Municipal Corporation (BMC)",
            "state": "Maharashtra",
            "portal": "BMC Citizen Portal / Aaple Sarkar",
            "zonal_wards": 24
        },
        "delhi": {
            "name": "Municipal Corporation of Delhi (MCD)",
            "state": "Delhi-NCR",
            "portal": "MCD Online Services (mcdonline.nic.in)",
            "zonal_wards": 12
        },
        "hyderabad": {
            "name": "Greater Hyderabad Municipal Corporation (GHMC)",
            "state": "Telangana",
            "portal": "GHMC Citizen Trade Portal",
            "zonal_wards": 30
        }
    }

    @classmethod
    def get_compliance_bundle(cls, city: str, establishment_type: str, floor_area_sqft: int) -> Dict[str, Any]:
        city_key = city.lower()
        muni = cls.MUNICIPAL_BODIES.get(city_key, cls.MUNICIPAL_BODIES["bengaluru"])

        licenses: List[Dict[str, Any]] = []
        base_fee = 14999

        # Universal Trade License
        licenses.append({
            "license_name": f"{muni['name']} Commercial Trade License",
            "issuing_authority": "Health & Revenue Department",
            "statutory_act": "State Municipal Corporation Act",
            "expected_sla_days": 14,
            "offline_inspection_mandate": True
        })

        # Shop & Establishment
        licenses.append({
            "license_name": "Shop & Commercial Establishment Registration",
            "issuing_authority": f"{muni['state']} Department of Labour",
            "statutory_act": f"{muni['state']} Shops & Commercial Establishments Act",
            "expected_sla_days": 3,
            "offline_inspection_mandate": False
        })

        if establishment_type in ["restaurant", "cloudkitchen"]:
            base_fee = 34999 if establishment_type == "restaurant" else 19999
            licenses.append({
                "license_name": "FSSAI State Food Safety License (Form B)",
                "issuing_authority": "Food Safety and Standards Authority of India (FoSCoS)",
                "statutory_act": "Food Safety and Standards Act, 2006",
                "expected_sla_days": 15,
                "offline_inspection_mandate": True
            })

            if establishment_type == "restaurant" and floor_area_sqft > 1000:
                licenses.append({
                    "license_name": "Fire Services Department No Objection Certificate (Fire NOC)",
                    "issuing_authority": f"{muni['state']} Fire & Emergency Services",
                    "statutory_act": "National Building Code & State Fire Prevention Act",
                    "expected_sla_days": 21,
                    "offline_inspection_mandate": True
                })
                licenses.append({
                    "license_name": "Eating House Registration / Police Permission",
                    "issuing_authority": "City Police Commissionerate (Licensing Unit)",
                    "statutory_act": "City Police Act",
                    "expected_sla_days": 30,
                    "offline_inspection_mandate": True
                })

        # Signboard / Exterior Display
        licenses.append({
            "license_name": "Commercial Advertisement & Signboard Sanction",
            "issuing_authority": f"{muni['name']} Advertisement Department",
            "statutory_act": "Municipal Advertisement By-Laws",
            "expected_sla_days": 7,
            "offline_inspection_mandate": False
        })

        return {
            "city": muni["name"],
            "state": muni["state"],
            "establishment_type": establishment_type,
            "floor_area_sqft": floor_area_sqft,
            "total_mandatory_clearances": len(licenses),
            "licenses_breakdown": licenses,
            "turnkey_pricing_inr": base_fee,
            "ward_paralegal_included": True,
            "inspector_scrutiny_guarantee": "Empanelled local paralegal represents client at zonal ward"
        }
