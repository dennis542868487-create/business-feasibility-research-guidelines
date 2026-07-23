from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "plugins" / "business-feasibility-research-guidelines" / "skills" / "business-feasibility-research-guidelines" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import feasibility_math as fm  # noqa: E402


class FunnelTests(unittest.TestCase):
    def test_capacity_caps_latent_orders(self):
        result = fm.calculate_funnel(
            {
                "starting_count": "1000",
                "stages": [
                    {"name": "in_area", "rate": "0.2"},
                    {"name": "pays", "rate": "0.5"},
                ],
                "orders_per_buyer": "1",
                "capacity": "60",
            }
        )
        self.assertEqual(result["result"]["latent_orders"], Decimal("100.0"))
        self.assertEqual(result["result"]["fulfilled_orders"], Decimal("60"))
        self.assertEqual(result["result"]["unmet_demand"], Decimal("40.0"))

    def test_invalid_rate_is_rejected(self):
        with self.assertRaises(fm.InputError):
            fm.calculate_funnel(
                {
                    "starting_count": 10,
                    "stages": [{"name": "bad", "rate": 1.1}],
                    "orders_per_buyer": 1,
                    "capacity": 10,
                }
            )


class MarketplaceTests(unittest.TestCase):
    def test_matches_supply_and_demand_with_minimum(self):
        result = fm.calculate_marketplace(
            {
                "supply": {
                    "reachable_suppliers": "100",
                    "contact_rate": "0.5",
                    "onboarding_rate": "0.4",
                    "average_available_units_per_supplier": "2",
                    "availability_rate": "0.5",
                    "time_match_rate": "0.5",
                },
                "demand": {
                    "reachable_customers": "1000",
                    "stages": [
                        {"name": "visits", "rate": "0.1"},
                        {"name": "pays", "rate": "0.5"},
                    ],
                    "orders_per_buyer": "1",
                },
                "matching": {
                    "supply_stages": [{"name": "right_product", "rate": "0.8"}],
                    "demand_stages": [{"name": "right_time", "rate": "0.5"}],
                },
            }
        )
        self.assertEqual(result["steps"]["available_units"], Decimal("10.0000"))
        self.assertEqual(result["result"]["matched_supply_units"], Decimal("8.00000"))
        self.assertEqual(result["result"]["matched_demand_orders"], Decimal("25.000"))
        self.assertEqual(result["result"]["completed_transactions"], Decimal("8.00000"))


class FinancialTests(unittest.TestCase):
    def test_unit_economics_and_ceiling_break_even(self):
        result = fm.calculate_unit_economics(
            {
                "currency": "CAD",
                "period": "month",
                "price": "100",
                "refund_rate": "0.10",
                "payment_fee_rate": "0.02",
                "fixed_payment_fee": "1",
                "variable_costs": {"materials": "40", "labor": "10"},
                "fixed_period_costs": "370",
            }
        )
        self.assertEqual(result["result"]["contribution_per_unit"], Decimal("37.00"))
        self.assertEqual(result["result"]["break_even_units"], Decimal("10"))

    def test_nonpositive_contribution_has_no_break_even(self):
        result = fm.calculate_unit_economics(
            {
                "currency": "CAD",
                "period": "month",
                "price": "20",
                "refund_rate": "0",
                "payment_fee_rate": "0",
                "fixed_payment_fee": "0",
                "variable_costs": {"service": "25"},
                "fixed_period_costs": "100",
            }
        )
        self.assertIsNone(result["result"]["break_even_units"])
        self.assertTrue(result["warnings"])

    def test_cash_runway_stops_at_observed_horizon(self):
        result = fm.calculate_cash_runway(
            {
                "currency": "CAD",
                "opening_cash": "100",
                "net_cash_flows": [
                    {"period": "M1", "net_cash_flow": "-40"},
                    {"period": "M2", "net_cash_flow": "-70"},
                ],
            }
        )
        self.assertEqual(result["result"]["first_period_below_zero"], "M2")
        self.assertEqual(result["result"]["ending_cash"], Decimal("-10"))

    def test_scenarios_are_deterministic(self):
        result = fm.calculate_scenarios(
            {
                "currency": "CAD",
                "period": "month",
                "scenarios": [
                    {"name": "threshold", "volume": "100", "price": "10", "variable_cost_per_unit": "4", "fixed_costs": "500"}
                ],
            }
        )
        self.assertEqual(result["result"][0]["operating_result"], Decimal("100"))


class BaselineAndEvidenceTests(unittest.TestCase):
    def baseline_input(self, **flags):
        evidence = {
            "direct_behavioral": False,
            "mechanism": False,
            "capacity_validated": False,
            "exceptional_adversarial_review": False,
        }
        evidence.update(flags)
        return {
            "baseline_low": "1",
            "baseline_high": "5",
            "forecast_low": "50",
            "forecast_high": "80",
            "evidence": evidence,
        }

    def test_steveston_interval_is_10_to_80_and_blocked(self):
        result = fm.calculate_baseline(self.baseline_input())
        self.assertEqual(result["result"]["multiple_interval"]["minimum"], Decimal("10"))
        self.assertEqual(result["result"]["multiple_interval"]["maximum"], Decimal("80"))
        self.assertFalse(result["result"]["central_case_eligible"])

    def test_exceptional_case_requires_all_evidence(self):
        result = fm.calculate_baseline(
            self.baseline_input(
                direct_behavioral=True,
                mechanism=True,
                capacity_validated=True,
                exceptional_adversarial_review=True,
            )
        )
        self.assertTrue(result["result"]["central_case_eligible"])

    def test_zero_baseline_does_not_create_ratio(self):
        data = self.baseline_input()
        data["baseline_low"] = "0"
        result = fm.calculate_baseline(data)
        self.assertIsNone(result["result"]["multiple_interval"])
        self.assertFalse(result["result"]["central_case_eligible"])

    def test_evidence_profile_has_no_total_score(self):
        dimensions = {name: "high" for name in fm.EVIDENCE_DIMENSIONS}
        dimensions["geographic_fit"] = {"rating": "low", "explanation": "National proxy"}
        result = fm.calculate_evidence_profile({"claim_id": "C1", "dimensions": dimensions})
        self.assertIn("geographic_fit", result["result"]["weak_dimensions"])
        self.assertNotIn("score", result["result"])


if __name__ == "__main__":
    unittest.main()
