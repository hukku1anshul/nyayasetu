"""
Payment of Gratuity Act 1972 & Retiring Employee Tax Shield Engine
Calculates:
1. Statutory Gratuity under Section 4(2) using 15/26 formula
2. Section 10(10) Income Tax Exemption (Capped at Rs. 20 Lakhs)
3. Section 10(10AA) Leave Encashment Exemption (Capped at Rs. 25 Lakhs per Budget 2023)
4. EPS 95 Monthly Pension Estimation under Employees' Pension Scheme 1995
"""

from typing import Dict, List, Any, Optional
import math

class GratuityEngine:
    """
    Statutory retirement benefits and tax exemption engine under
    the Payment of Gratuity Act, 1972, Income Tax Act, 1961, and EPS 95.
    """

    STATUTORY_GRATUITY_CAP_INR = 2000000.0  # Rs. 20 Lakhs
    STATUTORY_LEAVE_ENCASHMENT_CAP_INR = 2500000.0  # Rs. 25 Lakhs (Amended 2023)
    EPS_WAGE_CEILING_INR = 15000.0  # Rs. 15,000 statutory wage ceiling for EPS

    @classmethod
    def calculate_retirement_benefits(
        cls,
        last_drawn_basic_monthly: float,
        last_drawn_da_monthly: float = 0.0,
        years_of_service: float = 10.0,
        is_covered_under_act: bool = True,
        leave_encashment_received_inr: float = 0.0,
        actual_gratuity_received_inr: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates statutory gratuity, tax-exempt amount, taxable portion,
        leave encashment relief, and estimated monthly EPS 95 pension.
        """
        monthly_base = last_drawn_basic_monthly + last_drawn_da_monthly

        # Rounding rule: fraction over 6 months counts as 1 full year for covered establishments
        if is_covered_under_act:
            fraction = years_of_service - math.floor(years_of_service)
            completed_years = math.floor(years_of_service) + (1 if fraction >= 0.5 else 0)
            # 15 days wages for each completed year (15/26 formula)
            statutory_gratuity_calculated = (15.0 / 26.0) * monthly_base * completed_years
        else:
            completed_years = math.floor(years_of_service)
            # Non-covered establishment: half month wages for each year (15/30 = 0.5 month)
            statutory_gratuity_calculated = 0.5 * monthly_base * completed_years

        is_eligible_for_gratuity = years_of_service >= 5.0
        capped_statutory_gratuity = min(statutory_gratuity_calculated, cls.STATUTORY_GRATUITY_CAP_INR)

        gratuity_received = actual_gratuity_received_inr if actual_gratuity_received_inr is not None else capped_statutory_gratuity

        # Tax exemption under Section 10(10)
        exempt_gratuity = min(gratuity_received, capped_statutory_gratuity, cls.STATUTORY_GRATUITY_CAP_INR)
        taxable_gratuity = max(0.0, gratuity_received - exempt_gratuity)

        # Leave Encashment under Section 10(10AA)
        exempt_leave_encashment = min(leave_encashment_received_inr, cls.STATUTORY_LEAVE_ENCASHMENT_CAP_INR)
        taxable_leave_encashment = max(0.0, leave_encashment_received_inr - exempt_leave_encashment)

        # EPS 95 Monthly Pension Estimation: (Pensionable Service * Pensionable Salary) / 70
        # If service >= 20 years, 2 bonus years added under EPS 95 rules
        pensionable_years = completed_years + (2 if completed_years >= 20 else 0)
        pensionable_salary = min(monthly_base, cls.EPS_WAGE_CEILING_INR)
        if completed_years >= 10:
            estimated_monthly_eps_pension = max(1000.0, (pensionable_years * pensionable_salary) / 70.0)
            pension_status = f"Eligible for Life Monthly Pension (~Rs. {estimated_monthly_eps_pension:,.2f}/mo)"
        else:
            estimated_monthly_eps_pension = 0.0
            pension_status = "Service under 10 years; eligible for Scheme Certificate or one-time withdrawal benefit (Form 10C)"

        return {
            "monthly_basic_plus_da": monthly_base,
            "years_of_service_input": years_of_service,
            "completed_statutory_years": completed_years,
            "is_eligible_for_gratuity": is_eligible_for_gratuity,
            "statutory_gratuity_amount_inr": round(capped_statutory_gratuity, 2),
            "gratuity_received_inr": round(gratuity_received, 2),
            "exempt_gratuity_section_10_10_inr": round(exempt_gratuity, 2),
            "taxable_gratuity_inr": round(taxable_gratuity, 2),
            "gratuity_statutory_cap_inr": cls.STATUTORY_GRATUITY_CAP_INR,
            "leave_encashment_received_inr": round(leave_encashment_received_inr, 2),
            "exempt_leave_encashment_10_10aa_inr": round(exempt_leave_encashment, 2),
            "taxable_leave_encashment_inr": round(taxable_leave_encashment, 2),
            "estimated_monthly_eps_pension_inr": round(estimated_monthly_eps_pension, 2),
            "pension_eligibility_status": pension_status,
            "formula_applied": "15/26 * (Basic + DA) * Completed Years (Section 4(2) Payment of Gratuity Act)",
            "statutory_basis": "Payment of Gratuity Act 1972 & Section 10(10)/10(10AA) Income Tax Act 1961"
        }
