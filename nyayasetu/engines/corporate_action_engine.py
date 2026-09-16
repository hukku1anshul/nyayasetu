"""
Historical Corporate Action & Certificate Valuation Engine
Calculates modern share counts from legacy physical share certificates by factoring in
historical stock splits, bonus share issuances, and demergers.
"""

from typing import Dict, List, Any, Optional

class CorporateActionEngine:
    """
    Historical corporate actions database for top Indian bluechips.
    Converts legacy paper certificate share counts into current holding quantities.
    """
    CORPORATE_ACTIONS_HISTORY = {
        "TATASTEEL": {
            "name": "Tata Steel Limited (formerly TISCO)",
            "cmp": 150.0,
            "actions": [
                {"year": 2004, "type": "bonus", "ratio": "1:2", "multiplier": 1.5, "notes": "1 bonus share for every 2 shares held"},
                {"year": 2022, "type": "split", "ratio": "10:1", "multiplier": 10.0, "notes": "Sub-division of face value from Rs 10 to Rs 1"}
            ],
            "dividend_per_share_last_7_years": 85.0
        },
        "RELIANCE": {
            "name": "Reliance Industries Limited",
            "cmp": 2950.0,
            "actions": [
                {"year": 1997, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2009, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2017, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2024, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"}
            ],
            "dividend_per_share_last_7_years": 95.0
        },
        "INFY": {
            "name": "Infosys Limited",
            "cmp": 1850.0,
            "actions": [
                {"year": 1999, "type": "split", "ratio": "2:1", "multiplier": 2.0, "notes": "Face value split from Rs 10 to Rs 5"},
                {"year": 2004, "type": "bonus", "ratio": "3:1", "multiplier": 4.0, "notes": "3:1 Bonus Issue"},
                {"year": 2006, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2014, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2015, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2018, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"}
            ],
            "dividend_per_share_last_7_years": 160.0
        },
        "ITC": {
            "name": "ITC Limited",
            "cmp": 490.0,
            "actions": [
                {"year": 2005, "type": "split", "ratio": "10:1", "multiplier": 10.0, "notes": "Face value split from Rs 10 to Rs 1"},
                {"year": 2005, "type": "bonus", "ratio": "1:2", "multiplier": 1.5, "notes": "1:2 Bonus Issue"},
                {"year": 2010, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus Issue"},
                {"year": 2016, "type": "bonus", "ratio": "1:2", "multiplier": 1.5, "notes": "1:2 Bonus Issue"}
            ],
            "dividend_per_share_last_7_years": 75.0
        },
        "WIPRO": {
            "name": "Wipro Limited",
            "cmp": 540.0,
            "actions": [
                {"year": 1995, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus"},
                {"year": 1997, "type": "bonus", "ratio": "2:1", "multiplier": 3.0, "notes": "2:1 Bonus"},
                {"year": 1999, "type": "split", "ratio": "5:1", "multiplier": 5.0, "notes": "Split from Rs 10 to Rs 2"},
                {"year": 2004, "type": "bonus", "ratio": "2:1", "multiplier": 3.0, "notes": "2:1 Bonus"},
                {"year": 2005, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus"},
                {"year": 2010, "type": "bonus", "ratio": "2:3", "multiplier": 1.667, "notes": "2:3 Bonus"},
                {"year": 2017, "type": "bonus", "ratio": "1:1", "multiplier": 2.0, "notes": "1:1 Bonus"},
                {"year": 2019, "type": "bonus", "ratio": "1:3", "multiplier": 1.333, "notes": "1:3 Bonus"}
            ],
            "dividend_per_share_last_7_years": 25.0
        }
    }

    @classmethod
    def calculate_legacy_holding(cls, symbol: str, cert_shares: int, certificate_year: int) -> Dict[str, Any]:
        sym = symbol.upper().strip()
        data = cls.CORPORATE_ACTIONS_HISTORY.get(sym)
        if not data:
            return {
                "symbol": sym,
                "recognized": False,
                "current_shares": cert_shares,
                "current_market_value_inr": cert_shares * 500.0,
                "unpaid_dividends_estimate_inr": 0.0,
                "message": "Company corporate actions not in benchmark index; standard 1:1 holding assumed."
            }

        cumulative_multiplier = 1.0
        applied_actions = []

        for action in data["actions"]:
            if action["year"] >= certificate_year:
                cumulative_multiplier *= action["multiplier"]
                applied_actions.append(action)

        current_shares = int(round(cert_shares * cumulative_multiplier))
        current_market_val = round(current_shares * data["cmp"], 2)
        unpaid_div = round(current_shares * data["dividend_per_share_last_7_years"], 2)
        total_wealth = current_market_val + unpaid_div

        return {
            "symbol": sym,
            "recognized": True,
            "company_name": data["name"],
            "original_certificate_shares": cert_shares,
            "certificate_issue_year": certificate_year,
            "multiplication_factor": round(cumulative_multiplier, 2),
            "current_effective_shares": current_shares,
            "current_market_price": data["cmp"],
            "current_shares_market_value_inr": current_market_val,
            "estimated_unclaimed_dividends_inr": unpaid_div,
            "total_recoverable_portfolio_wealth_inr": total_wealth,
            "applied_corporate_actions": applied_actions,
            "dopamine_insight": (
                f"Your original {cert_shares} shares from {certificate_year} have grown into "
                f"{current_shares} shares worth Rs. {current_market_val:,.2f}, plus Rs. {unpaid_div:,.2f} in unpaid dividends!"
            )
        }
