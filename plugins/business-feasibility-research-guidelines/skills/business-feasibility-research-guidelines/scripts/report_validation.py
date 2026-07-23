#!/usr/bin/env python3
"""Validate structural and language guardrails in a Markdown feasibility report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


VERSION = "0.1.0"
MATURITY = {"E0", "E1", "E2", "E3", "E4"}
REQUIRED_HEADING_GROUPS = {
    "decision": ("decision summary", "decision contract"),
    "method": ("capability and methodology", "methodology and scope"),
    "maturity": ("evidence maturity",),
    "evidence": ("material claims and evidence", "evidence ledger"),
    "options": ("options and counterfactual", "alternatives"),
    "adversarial": ("adversarial audit",),
    "gaps": ("data gaps",),
    "recommendation": ("recommendation",),
    "next_gate": ("next gate", "validation plan"),
}
PROMOTIONAL_PATTERNS = {
    "guaranteed success": r"\bguarantee(?:d|s)?\s+(?:business\s+)?success\b",
    "certain profit": r"\b(?:certain|sure|guaranteed)\s+profit\b",
    "traffic tsunami": r"\btraffic tsunami\b|流量海[嘯啸]",
    "inevitable explosion": r"必然爆[發发]",
    "instant sellout": r"庫存一定秒空|库存一定秒空",
    "epic catalyst": r"史[詩诗]級催化[劑剂]",
}
STATEMENT_MARKER = re.compile(
    r"\[(?:FACT|INTERNAL|CALC|PROXY|ASSUMPTION|USER_ASSUMPTION|MODEL_ASSUMPTION|JUDGMENT|UNKNOWN|PRO_CONFIRM):[A-Z][A-Z0-9-]*\]",
    re.IGNORECASE,
)
NUMERIC_SIGNAL = re.compile(r"(?:\b(?:CAD|USD|EUR|GBP)\b|[$€£]|\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\s*[x×]\b)")


def headings(text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", match.group(1).strip().lower())
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    ]


def has_heading(all_headings: list[str], alternatives: tuple[str, ...]) -> bool:
    return any(any(name in heading for name in alternatives) for heading in all_headings)


def field_value(text: str, label_pattern: str) -> str | None:
    match = re.search(rf"^\s*[-*]?\s*{label_pattern}\s*:\s*(.*?)\s*$", text, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_report_text(text: str, maturity: str | None = None) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    all_headings = headings(text)
    for group, alternatives in REQUIRED_HEADING_GROUPS.items():
        if not has_heading(all_headings, alternatives):
            errors.append({"code": f"missing_{group}", "message": f"Missing heading for {group}."})

    for label in ("Data cutoff", "Source verification date", "Generated date"):
        value = field_value(text, re.escape(label))
        if value is None or value == "":
            errors.append({"code": "missing_metadata", "message": f"Missing value for {label}."})

    success = field_value(text, r"Success threshold")
    failure = field_value(text, r"Failure threshold")
    stop = field_value(text, r"Stop condition(?:s)?")
    for name, value in (("success threshold", success), ("failure threshold", failure), ("stop condition", stop)):
        if value is None or value == "":
            errors.append({"code": "missing_decision_rule", "message": f"Missing {name}."})

    for name, pattern in PROMOTIONAL_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            errors.append({"code": "promotional_language", "message": f"Unsupported promotional language: {name}."})

    if re.search(r"overall\s+(?:evidence\s+)?score|[總总]體[證证]據[评分分]", text, re.IGNORECASE):
        warnings.append({"code": "composite_score", "message": "Do not replace the evidence profile with a composite score."})

    if maturity in {"E0", "E1"}:
        prose = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith(("#", "|")))
        if re.search(r"\bbase case\b|基準情景|基准情景", prose, re.IGNORECASE):
            errors.append({"code": "low_maturity_base_case", "message": "E0-E1 numerical cases must be labelled illustrative or threshold scenarios."})
        if re.search(r"(?:recommend(?:ed)?|建[議议]).{0,30}(?:invest|investment|投入).{0,20}(?:[$€£]|\b\d)", prose, re.IGNORECASE):
            errors.append({"code": "low_maturity_investment", "message": "E0-E1 reports must not recommend a numeric material investment."})

    numeric_unmarked = []
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "|", "```")):
            continue
        if NUMERIC_SIGNAL.search(stripped) and not STATEMENT_MARKER.search(stripped):
            numeric_unmarked.append(number)
    if numeric_unmarked:
        preview = ", ".join(str(item) for item in numeric_unmarked[:10])
        warnings.append(
            {
                "code": "unmarked_numeric_claim",
                "message": f"Review numeric statements without an information-type marker on lines: {preview}.",
            }
        )

    marker_count = len(STATEMENT_MARKER.findall(text))
    if marker_count == 0:
        warnings.append({"code": "no_statement_markers", "message": "No FACT/INTERNAL/CALC/PROXY/ASSUMPTION/UNKNOWN markers found."})

    return {
        "validator_version": VERSION,
        "maturity": maturity,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "passed": not errors,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "statement_marker_count": marker_count,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a Markdown feasibility report.")
    parser.add_argument("report", help="Path to the Markdown report.")
    parser.add_argument("--maturity", choices=sorted(MATURITY))
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--version", action="version", version=VERSION)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = Path(args.report).read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"error": f"Cannot read report: {exc}"}))
        return 2
    result = validate_report_text(text, args.maturity)
    print(json.dumps(result, indent=None if args.compact else 2, sort_keys=True))
    return 0 if result["summary"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
