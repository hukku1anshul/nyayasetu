"""
Revenue Optimization & Monetization Engine
Implements high-margin upsells, Tatkal speed pricing, NRI FEMA repatriation calculators,
FinTech demat liquidation commissions, and micro-paid lead unlock modules.
"""

from typing import Dict, List, Any, Optional

class RevenueOptimizationEngine:
    """
    Maximizes Average Revenue Per User (ARPU), Customer Lifetime Value (LTV),
    and cross-sell margins across all NyayaSetu rails.
    """

    # ---------------- 1. TATKAL / FAST-TRACK RUSH PRICING ----------------
    @staticmethod
    def calculate_tatkal_pricing(service_type: str, base_price: float, rush_days: int) -> Dict[str, Any]:
        """
        Monetizes urgency. Customers needing urgent Gazette notifications (for passport/visa)
        or urgent Apostille pay a premium for priority processing.
        """
        # Standard SLAs
        default_sla_days = 30 if service_type == "GAZETTE" else 15
        
        # Rush multiplier: 2.0x for 7-day rush, 1.5x for 14-day rush
        if rush_days <= 7:
            speed_multiplier = 2.25
            tier_name = "VIP Super-Tatkal (Dedicated Legal Runner)"
            extra_perks = [
                "Same-day newspaper ad placement",
                "Priority physical Delhi Gazette press filing within 48h",
                "Dedicated WhatsApp Paralegal on 24/7 hotline",
                "Speedpost delivery of Gazette Hardcopy"
            ]
        elif rush_days <= 14:
            speed_multiplier = 1.60
            tier_name = "Express Tatkal"
            extra_perks = [
                "Guaranteed 48h newspaper ad placement",
                "Next-batch Gazette press dispatch",
                "Daily SMS & WhatsApp milestone alerts"
            ]
        else:
            speed_multiplier = 1.0
            tier_name = "Standard Regular"
            extra_perks = ["Standard 30-day processing"]

        total_price = round(base_price * speed_multiplier, 2)
        incremental_revenue = round(total_price - base_price, 2)

        return {
            "service_type": service_type,
            "selected_sla_days": rush_days,
            "standard_sla_days": default_sla_days,
            "tier": tier_name,
            "base_price_inr": base_price,
            "total_price_inr": total_price,
            "incremental_revenue_inr": incremental_revenue,
            "gross_margin_pct": 72.0 if speed_multiplier > 1.0 else 60.0,
            "included_perks": extra_perks
        }

    # ---------------- 2. FINTECH DEMAT LIQUIDATION & BROKERAGE UPSELL ----------------
    @staticmethod
    def calculate_liquidation_upsell(portfolio_value: float) -> Dict[str, Any]:
        """
        80% of heirs recovering ancestral shares want to sell them for immediate cash.
        We capture Demat account opening bounty (partner fee) + 0.35% liquidation fee.
        """
        demat_bounty_inr = 1200.0  # From Zerodha / Upstox / ICICI Direct partnership
        brokerage_advisory_fee = round(portfolio_value * 0.0035, 2)  # 0.35% secondary share sale advisory cut
        total_fintech_revenue = round(demat_bounty_inr + brokerage_advisory_fee, 2)

        return {
            "portfolio_value_inr": portfolio_value,
            "demat_partner_bounty_inr": demat_bounty_inr,
            "liquidation_advisory_fee_inr": brokerage_advisory_fee,
            "total_additional_fintech_revenue_inr": total_fintech_revenue,
            "partner_brokers": ["Zerodha", "Upstox", "ICICI Direct", "HDFC Securities"],
            "value_prop_to_client": "1-Click automated demat opening + block sale liquidation into bank account"
        }

    # ---------------- 3. NRI 15CA / 15CB FEMA REPATRIATION MODULE ----------------
    @staticmethod
    def calculate_nri_repatriation_package(remittance_amount_inr: float) -> Dict[str, Any]:
        """
        NRIs inheriting Indian shares/property must file Form 15CA (online tax declaration)
        and Form 15CB (Chartered Accountant certified tax certificate) under RBI/FEMA rules.
        """
        base_ca_fee = 18999.0
        if remittance_amount_inr > 5000000:  # > 50 Lakhs
            base_ca_fee = 34999.0

        return {
            "remittance_amount_inr": remittance_amount_inr,
            "turnkey_fema_fee_inr": base_ca_fee,
            "statutory_deliverables": [
                "Form 15CB Certification by Senior Empanelled CA",
                "Form 15CA Part-C Electronic Filing on Income Tax Portal",
                "FEMA NRO-to-NRE Repatriation Bank A2 Form Documentation",
                "Direct liaison with Authorized Dealer (AD) Category-I Bank"
            ],
            "gross_margin_pct": 55.0
        }

    # ---------------- 4. MICRO-PAID HERITAGE REPORT UNLOCK (LEAD MAGNET) ----------------
    @staticmethod
    def generate_micro_report_pricing(found_shares_value: float) -> Dict[str, Any]:
        """
        Freemium funnel: User searches father's name for free, sees that Rs. 2.5 Lakhs
        is waiting. They pay a micro-fee (Rs. 499) to unlock the full Folio & RTA Dossier,
        which is 100% credited back if they sign up for our 15% recovery service.
        """
        unlock_fee = 499.0 if found_shares_value < 500000 else 999.0
        return {
            "found_asset_value_inr": found_shares_value,
            "micro_unlock_fee_inr": unlock_fee,
            "conversion_hook": "100% refunded / adjusted against recovery success fee",
            "unlocks": [
                "Full Folio Number and Certificate Distinctive Numbers",
                "Designated RTA and Nodal Officer Direct Contact",
                "Pre-filled Form ISR-1 and ISR-4 ready to sign"
            ]
        }
