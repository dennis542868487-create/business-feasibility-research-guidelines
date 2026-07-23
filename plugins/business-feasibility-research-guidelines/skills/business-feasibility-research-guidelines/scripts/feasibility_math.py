#!/usr/bin/env python3
"""Deterministic, dependency-free calculations for feasibility research.

All material numeric inputs are parsed as Decimal. JSON outputs encode Decimal
values as strings so a report can reproduce exact arithmetic without binary
floating-point drift.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path
from typing import Any


VERSION = "0.1.0"
RATINGS = {"high", "medium", "low", "unknown"}
EVIDENCE_DIMENSIONS = (
    "authority",
    "directness",
    "geographic_fit",
    "time_fit",
    "definition_fit",
    "accuracy",
    "method_transparency",
    "interpretability",
    "coherence",
    "independence",
    "reproducibility",
    "materiality",
)


class InputError(ValueError):
    """Raised when a required or dimensionally valid input is missing."""


def require(mapping: dict[str, Any], key: str, context: str = "input") -> Any:
    if key not in mapping:
        raise InputError(f"Missing required field: {context}.{key}")
    return mapping[key]


def decimal_value(value: Any, name: str, *, allow_negative: bool = False) -> Decimal:
    if value is None or isinstance(value, bool):
        raise InputError(f"{name} must be a finite decimal number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise InputError(f"{name} must be a finite decimal number") from None
    if not result.is_finite():
        raise InputError(f"{name} must be finite")
    if not allow_negative and result < 0:
        raise InputError(f"{name} must be non-negative")
    return result


def rate_value(value: Any, name: str) -> Decimal:
    result = decimal_value(value, name)
    if result > 1:
        raise InputError(f"{name} must be between 0 and 1 inclusive")
    return result


def boolean_value(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise InputError(f"{name} must be true or false")
    return value


def nonempty_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{name} must be a non-empty string")
    return value.strip()


def conditional_funnel(
    starting_count: Decimal, stages: Any, context: str = "stages"
) -> tuple[Decimal, list[dict[str, Any]]]:
    if not isinstance(stages, list):
        raise InputError(f"{context} must be an ordered list")
    current = starting_count
    seen: set[str] = set()
    steps: list[dict[str, Any]] = []
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            raise InputError(f"{context}[{index}] must be an object")
        name = nonempty_text(require(stage, "name", f"{context}[{index}]"), f"{context}[{index}].name")
        if name in seen:
            raise InputError(f"Duplicate stage name in {context}: {name}")
        seen.add(name)
        rate = rate_value(require(stage, "rate", f"{context}[{index}]"), f"{context}[{index}].rate")
        output = current * rate
        steps.append(
            {
                "stage": name,
                "input_count": current,
                "conditional_rate": rate,
                "output_count": output,
                "formula": f"{name} = prior_stage × P({name} | prior_stage)",
            }
        )
        current = output
    return current, steps


def calculate_funnel(data: dict[str, Any]) -> dict[str, Any]:
    start = decimal_value(require(data, "starting_count"), "starting_count")
    orders_per_buyer = decimal_value(require(data, "orders_per_buyer"), "orders_per_buyer")
    capacity = decimal_value(require(data, "capacity"), "capacity")
    qualified, steps = conditional_funnel(start, require(data, "stages"))
    latent = qualified * orders_per_buyer
    fulfilled = min(latent, capacity)
    return {
        "formula": {
            "funnel": "stage_n = stage_(n-1) × P(stage_n | stage_(n-1))",
            "latent_orders": "qualified_buyers × average_orders_per_buyer",
            "fulfilled_orders": "min(latent_orders, capacity)",
        },
        "steps": steps,
        "result": {
            "qualified_buyers": qualified,
            "latent_orders": latent,
            "capacity": capacity,
            "fulfilled_orders": fulfilled,
            "unmet_demand": max(Decimal("0"), latent - fulfilled),
        },
        "warnings": [
            "Rates must be conditional on the preceding stage; this engine cannot detect overlapping populations."
        ],
    }


def calculate_marketplace(data: dict[str, Any]) -> dict[str, Any]:
    supply = require(data, "supply")
    demand = require(data, "demand")
    matching = require(data, "matching")
    if not all(isinstance(item, dict) for item in (supply, demand, matching)):
        raise InputError("supply, demand, and matching must be objects")

    reachable_suppliers = decimal_value(
        require(supply, "reachable_suppliers", "supply"), "supply.reachable_suppliers"
    )
    contact_rate = rate_value(require(supply, "contact_rate", "supply"), "supply.contact_rate")
    onboarding_rate = rate_value(
        require(supply, "onboarding_rate", "supply"), "supply.onboarding_rate"
    )
    average_units = decimal_value(
        require(supply, "average_available_units_per_supplier", "supply"),
        "supply.average_available_units_per_supplier",
    )
    availability_rate = rate_value(
        require(supply, "availability_rate", "supply"), "supply.availability_rate"
    )
    time_match_rate = rate_value(
        require(supply, "time_match_rate", "supply"), "supply.time_match_rate"
    )
    activated = reachable_suppliers * contact_rate * onboarding_rate
    available_units = activated * average_units * availability_rate * time_match_rate

    reachable_customers = decimal_value(
        require(demand, "reachable_customers", "demand"), "demand.reachable_customers"
    )
    qualified_buyers, demand_steps = conditional_funnel(
        reachable_customers, require(demand, "stages", "demand"), "demand.stages"
    )
    orders_per_buyer = decimal_value(
        require(demand, "orders_per_buyer", "demand"), "demand.orders_per_buyer"
    )
    qualified_orders = qualified_buyers * orders_per_buyer

    matched_supply, supply_match_steps = conditional_funnel(
        available_units,
        require(matching, "supply_stages", "matching"),
        "matching.supply_stages",
    )
    matched_demand, demand_match_steps = conditional_funnel(
        qualified_orders,
        require(matching, "demand_stages", "matching"),
        "matching.demand_stages",
    )
    transactions = min(matched_supply, matched_demand)
    return {
        "formula": {
            "activated_suppliers": "reachable_suppliers × contact_rate × onboarding_rate",
            "available_units": "activated_suppliers × average_available_units_per_supplier × availability_rate × time_match_rate",
            "completed_transactions": "min(matched_supply_units, matched_demand_orders)",
        },
        "steps": {
            "activated_suppliers": activated,
            "available_units": available_units,
            "demand_funnel": demand_steps,
            "supply_matching": supply_match_steps,
            "demand_matching": demand_match_steps,
        },
        "result": {
            "matched_supply_units": matched_supply,
            "matched_demand_orders": matched_demand,
            "completed_transactions": transactions,
            "unmatched_supply_units": max(Decimal("0"), matched_supply - transactions),
            "unmatched_demand_orders": max(Decimal("0"), matched_demand - transactions),
        },
        "warnings": [
            "Matching-stage rates must use comparable geography, time, product, price, trust, and quality definitions."
        ],
    }


def calculate_unit_economics(data: dict[str, Any]) -> dict[str, Any]:
    currency = nonempty_text(require(data, "currency"), "currency")
    period = nonempty_text(require(data, "period"), "period")
    price = decimal_value(require(data, "price"), "price")
    refund_rate = rate_value(require(data, "refund_rate"), "refund_rate")
    payment_fee_rate = rate_value(require(data, "payment_fee_rate"), "payment_fee_rate")
    fixed_payment_fee = decimal_value(require(data, "fixed_payment_fee"), "fixed_payment_fee")
    fixed_period_costs = decimal_value(require(data, "fixed_period_costs"), "fixed_period_costs")
    raw_costs = require(data, "variable_costs")
    if not isinstance(raw_costs, dict) or not raw_costs:
        raise InputError("variable_costs must be a non-empty object of named costs")
    costs = {
        nonempty_text(name, "variable_costs key"): decimal_value(value, f"variable_costs.{name}")
        for name, value in raw_costs.items()
    }
    expected_net_revenue = price * (Decimal("1") - refund_rate)
    payment_fees = (price * payment_fee_rate) + fixed_payment_fee
    variable_cost_total = sum(costs.values(), Decimal("0"))
    contribution = expected_net_revenue - payment_fees - variable_cost_total
    margin = contribution / expected_net_revenue if expected_net_revenue > 0 else None
    break_even = None
    warnings: list[str] = []
    if contribution > 0:
        break_even = (fixed_period_costs / contribution).to_integral_value(rounding=ROUND_CEILING)
    else:
        warnings.append("Contribution per unit is non-positive; break-even units are undefined.")
    return {
        "formula": {
            "expected_net_revenue": "price × (1 - refund_rate)",
            "payment_fees": "price × payment_fee_rate + fixed_payment_fee",
            "contribution_per_unit": "expected_net_revenue - payment_fees - variable_cost_total",
            "break_even_units": "ceiling(fixed_period_costs / contribution_per_unit), only when contribution > 0",
        },
        "inputs": {"currency": currency, "period": period, "variable_costs": costs},
        "result": {
            "expected_net_revenue_per_unit": expected_net_revenue,
            "payment_fees_per_unit": payment_fees,
            "variable_cost_total_per_unit": variable_cost_total,
            "contribution_per_unit": contribution,
            "contribution_margin": margin,
            "fixed_period_costs": fixed_period_costs,
            "break_even_units": break_even,
        },
        "warnings": warnings,
    }


def calculate_cash_runway(data: dict[str, Any]) -> dict[str, Any]:
    currency = nonempty_text(require(data, "currency"), "currency")
    opening = decimal_value(require(data, "opening_cash"), "opening_cash")
    flows = require(data, "net_cash_flows")
    if not isinstance(flows, list) or not flows:
        raise InputError("net_cash_flows must be a non-empty ordered list")
    balance = opening
    first_negative = None
    rows = []
    seen: set[str] = set()
    for index, item in enumerate(flows):
        if not isinstance(item, dict):
            raise InputError(f"net_cash_flows[{index}] must be an object")
        period = nonempty_text(require(item, "period", f"net_cash_flows[{index}]"), f"net_cash_flows[{index}].period")
        if period in seen:
            raise InputError(f"Duplicate cash-flow period: {period}")
        seen.add(period)
        flow = decimal_value(
            require(item, "net_cash_flow", f"net_cash_flows[{index}]"),
            f"net_cash_flows[{index}].net_cash_flow",
            allow_negative=True,
        )
        opening_balance = balance
        balance += flow
        if balance < 0 and first_negative is None:
            first_negative = period
        rows.append(
            {
                "period": period,
                "opening_balance": opening_balance,
                "net_cash_flow": flow,
                "closing_balance": balance,
            }
        )
    return {
        "formula": "closing_cash_t = closing_cash_(t-1) + net_cash_flow_t",
        "inputs": {"currency": currency, "opening_cash": opening},
        "steps": rows,
        "result": {"first_period_below_zero": first_negative, "ending_cash": balance},
        "warnings": ["No cash flows are extrapolated beyond the explicit input horizon."],
    }


def calculate_scenarios(data: dict[str, Any]) -> dict[str, Any]:
    currency = nonempty_text(require(data, "currency"), "currency")
    period = nonempty_text(require(data, "period"), "period")
    scenarios = require(data, "scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise InputError("scenarios must be a non-empty list")
    results = []
    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            raise InputError(f"scenarios[{index}] must be an object")
        name = nonempty_text(require(scenario, "name", f"scenarios[{index}]"), f"scenarios[{index}].name")
        if name in seen:
            raise InputError(f"Duplicate scenario name: {name}")
        seen.add(name)
        volume = decimal_value(require(scenario, "volume", name), f"{name}.volume")
        price = decimal_value(require(scenario, "price", name), f"{name}.price")
        variable = decimal_value(
            require(scenario, "variable_cost_per_unit", name), f"{name}.variable_cost_per_unit"
        )
        fixed = decimal_value(require(scenario, "fixed_costs", name), f"{name}.fixed_costs")
        revenue = volume * price
        contribution = volume * (price - variable)
        result = contribution - fixed
        results.append(
            {
                "name": name,
                "volume": volume,
                "revenue": revenue,
                "contribution": contribution,
                "fixed_costs": fixed,
                "operating_result": result,
            }
        )
    return {
        "formula": {
            "revenue": "volume × price",
            "contribution": "volume × (price - variable_cost_per_unit)",
            "operating_result": "contribution - fixed_costs",
        },
        "inputs": {"currency": currency, "period": period},
        "result": results,
        "warnings": [
            "Scenario names are not probabilities. Change dependent inputs together before interpreting results."
        ],
    }


def calculate_baseline(data: dict[str, Any]) -> dict[str, Any]:
    baseline_low = decimal_value(require(data, "baseline_low"), "baseline_low")
    baseline_high = decimal_value(require(data, "baseline_high"), "baseline_high")
    forecast_low = decimal_value(require(data, "forecast_low"), "forecast_low")
    forecast_high = decimal_value(require(data, "forecast_high"), "forecast_high")
    if baseline_low > baseline_high:
        raise InputError("baseline_low must not exceed baseline_high")
    if forecast_low > forecast_high:
        raise InputError("forecast_low must not exceed forecast_high")
    flags = require(data, "evidence")
    if not isinstance(flags, dict):
        raise InputError("evidence must be an object")
    direct = boolean_value(require(flags, "direct_behavioral", "evidence"), "evidence.direct_behavioral")
    mechanism = boolean_value(require(flags, "mechanism", "evidence"), "evidence.mechanism")
    capacity = boolean_value(require(flags, "capacity_validated", "evidence"), "evidence.capacity_validated")
    adversarial = boolean_value(
        require(flags, "exceptional_adversarial_review", "evidence"),
        "evidence.exceptional_adversarial_review",
    )
    absolute_change = {
        "minimum": forecast_low - baseline_high,
        "maximum": forecast_high - baseline_low,
    }
    warnings = []
    multiples = None
    level = "ratio unavailable"
    central_eligible = False
    if baseline_low == 0 or baseline_high == 0:
        warnings.append(
            "Baseline interval includes zero; ratio diagnostics are undefined. Use absolute change and a corrected reference class."
        )
    else:
        minimum = forecast_low / baseline_high
        maximum = forecast_high / baseline_low
        multiples = {"minimum": minimum, "maximum": maximum}
        if maximum >= 20:
            level = "20x exceptional-claim alert"
            central_eligible = direct and mechanism and capacity and adversarial
        elif maximum >= 10:
            level = "10x central-case gate"
            central_eligible = direct and mechanism and capacity
        elif maximum >= 5:
            level = "5x strong-evidence alert"
            central_eligible = True
        elif maximum >= 2:
            level = "2x mechanism alert"
            central_eligible = True
        else:
            level = "below default multiple alerts"
            central_eligible = True
        if maximum >= 5 and not (direct or mechanism):
            warnings.append("Large change lacks direct behavior or explicit mechanism evidence.")
        if maximum >= 10 and not central_eligible:
            warnings.append("A 10x or larger central case requires direct behavior, mechanism evidence, and validated capacity.")
        if maximum >= 20 and not adversarial:
            warnings.append("A 20x or larger claim also requires explicit exceptional-claim adversarial review.")
    return {
        "formula": {
            "absolute_change_interval": "[forecast_low - baseline_high, forecast_high - baseline_low]",
            "multiple_interval": "[forecast_low / baseline_high, forecast_high / baseline_low] when baseline excludes zero",
        },
        "result": {
            "absolute_change": absolute_change,
            "multiple_interval": multiples,
            "diagnostic_level": level,
            "central_case_eligible": central_eligible,
        },
        "warnings": warnings,
    }


def calculate_evidence_profile(data: dict[str, Any]) -> dict[str, Any]:
    claim_id = nonempty_text(require(data, "claim_id"), "claim_id")
    dimensions = require(data, "dimensions")
    if not isinstance(dimensions, dict):
        raise InputError("dimensions must be an object")
    normalized = {}
    weak = []
    for dimension in EVIDENCE_DIMENSIONS:
        raw = require(dimensions, dimension, "dimensions")
        if isinstance(raw, str):
            rating = raw.strip().lower()
            explanation = ""
        elif isinstance(raw, dict):
            rating = nonempty_text(require(raw, "rating", f"dimensions.{dimension}"), f"dimensions.{dimension}.rating").lower()
            explanation = str(raw.get("explanation", "")).strip()
        else:
            raise InputError(f"dimensions.{dimension} must be a rating or object")
        if rating not in RATINGS:
            raise InputError(f"dimensions.{dimension}.rating must be high, medium, low, or unknown")
        normalized[dimension] = {"rating": rating, "explanation": explanation}
        if rating in {"low", "unknown"}:
            weak.append(dimension)
    return {
        "formula": "No composite score is calculated.",
        "result": {"claim_id": claim_id, "dimensions": normalized, "weak_dimensions": weak},
        "warnings": ["Interpret weak dimensions in relation to decision materiality; do not average ratings."],
    }


COMMANDS = {
    "funnel": calculate_funnel,
    "marketplace": calculate_marketplace,
    "unit-economics": calculate_unit_economics,
    "cash-runway": calculate_cash_runway,
    "scenarios": calculate_scenarios,
    "baseline": calculate_baseline,
    "evidence-profile": calculate_evidence_profile,
}


def json_ready(value: Any) -> Any:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    return value


def read_input(path: str) -> dict[str, Any]:
    try:
        text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
        data = json.loads(text)
    except OSError as exc:
        raise InputError(f"Cannot read input: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(f"Invalid JSON input: {exc}") from exc
    if not isinstance(data, dict):
        raise InputError("Top-level JSON input must be an object")
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run deterministic, unit-aware feasibility calculations from JSON."
    )
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("--input", default="-", help="JSON input path, or - for stdin (default).")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    parser.add_argument("--version", action="version", version=VERSION)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = read_input(args.input)
        payload = {
            "engine_version": VERSION,
            "command": args.command,
            **COMMANDS[args.command](data),
        }
    except InputError as exc:
        print(json.dumps({"error": str(exc), "command": getattr(args, "command", None)}), file=sys.stderr)
        return 2
    separators = (",", ":") if args.compact else None
    print(json.dumps(json_ready(payload), indent=None if args.compact else 2, separators=separators, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
