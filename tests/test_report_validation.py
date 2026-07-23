from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "plugins" / "business-feasibility-research-guidelines" / "skills" / "business-feasibility-research-guidelines" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import report_validation as rv  # noqa: E402


VALID_REPORT = """# Decision Summary

- Generated date: 2026-07-22
- Data cutoff: 2026-07-20
- Source verification date: 2026-07-22
- Success threshold: 10 paid orders
- Failure threshold: fewer than 3 paid orders
- Stop condition: CAD 500 test budget exhausted

[FACT:E001] The local permit fee is CAD 100.

## Decision contract and scope
Defined.

## Capability and methodology
Defined.

## Evidence maturity
Demand E2; economics E1.

## Material claims and evidence
See ledger.

## Options and counterfactual
Defer, test, or stage.

## Adversarial audit
Demand may be overstated.

## Data gaps
Paid conversion.

## Recommendation
Run a reversible validation.

## Next gate
Review paid conversion.
"""


class ReportValidationTests(unittest.TestCase):
    def test_valid_report_passes(self):
        result = rv.validate_report_text(VALID_REPORT, "E2")
        self.assertTrue(result["summary"]["passed"], result)

    def test_missing_threshold_fails(self):
        result = rv.validate_report_text(VALID_REPORT.replace("- Failure threshold: fewer than 3 paid orders\n", ""), "E2")
        self.assertFalse(result["summary"]["passed"])
        self.assertIn("missing_decision_rule", {item["code"] for item in result["errors"]})

    def test_promotional_language_fails(self):
        result = rv.validate_report_text(VALID_REPORT + "\nThis creates a traffic tsunami.\n", "E2")
        self.assertFalse(result["summary"]["passed"])

    def test_low_maturity_base_case_fails(self):
        result = rv.validate_report_text(VALID_REPORT + "\nThe base case is 20 orders.\n", "E1")
        self.assertIn("low_maturity_base_case", {item["code"] for item in result["errors"]})


if __name__ == "__main__":
    unittest.main()
