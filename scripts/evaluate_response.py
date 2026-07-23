#!/usr/bin/env python3
"""Screen a saved model response against one behavioral Eval case."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


VERSION = "0.1.0"


def load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Case must be a JSON object")
    return data


def matches(text: str, pattern: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE | re.MULTILINE) is not None


def evaluate(case: dict[str, Any], response: str) -> dict[str, Any]:
    required_results = []
    for item in case.get("required_concepts", []):
        patterns = item.get("patterns", [])
        passed = any(matches(response, pattern) for pattern in patterns)
        required_results.append(
            {"id": item.get("id"), "passed": passed, "patterns": patterns}
        )

    forbidden_results = []
    for item in case.get("forbidden_patterns", []):
        triggered = matches(response, item.get("pattern", r"(?!)"))
        forbidden_results.append(
            {
                "id": item.get("id"),
                "triggered": triggered,
                "critical": bool(item.get("critical", True)),
                "pattern": item.get("pattern"),
            }
        )

    required_total = len(required_results)
    required_passed = sum(1 for item in required_results if item["passed"])
    coverage = required_passed / required_total if required_total else 1.0
    threshold = float(case.get("automated_pass_threshold", 0.75))
    critical_triggered = any(
        item["triggered"] and item["critical"] for item in forbidden_results
    )
    automated_pass = coverage >= threshold and not critical_triggered
    return {
        "grader_version": VERSION,
        "case_id": case.get("id"),
        "case_type": case.get("type"),
        "required": required_results,
        "forbidden": forbidden_results,
        "summary": {
            "automated_pass": automated_pass,
            "required_coverage": round(coverage, 4),
            "required_passed": required_passed,
            "required_total": required_total,
            "critical_forbidden_triggered": critical_triggered,
            "human_review_required": True,
        },
        "critical_failures_for_human_review": case.get("critical_failures", []),
        "human_rubric": case.get("human_rubric", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Screen a saved response against an Eval case.")
    parser.add_argument("--case", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    try:
        case = load_json(args.case)
        response = Path(args.response).read_text(encoding="utf-8")
        result = evaluate(case, response)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(result, indent=None if args.compact else 2, sort_keys=True))
    return 0 if result["summary"]["automated_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
