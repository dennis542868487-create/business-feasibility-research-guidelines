from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_response import evaluate  # noqa: E402


class BehaviorEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads((ROOT / "evals" / "cases" / "steveston-bike-rental-2026.json").read_text(encoding="utf-8"))

    def test_good_fixture_passes_screen(self):
        response = (ROOT / "evals" / "fixtures" / "steveston-good-response.md").read_text(encoding="utf-8")
        result = evaluate(self.case, response)
        self.assertTrue(result["summary"]["automated_pass"], result)

    def test_bad_fixture_fails_screen(self):
        response = (ROOT / "evals" / "fixtures" / "steveston-bad-response.md").read_text(encoding="utf-8")
        result = evaluate(self.case, response)
        self.assertFalse(result["summary"]["automated_pass"])
        self.assertTrue(result["summary"]["critical_forbidden_triggered"])


if __name__ == "__main__":
    unittest.main()
