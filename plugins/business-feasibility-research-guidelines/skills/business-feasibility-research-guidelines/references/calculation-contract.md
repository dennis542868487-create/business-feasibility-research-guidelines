# Calculation Contract

## Principles

- Use decimal arithmetic for money and user-supplied rates.
- Require explicit units, currency, tax basis, period, and price basis where applicable.
- Reject missing, negative, non-finite, or out-of-range inputs instead of silently defaulting them.
- Emit formulas, normalized inputs, intermediate steps, warnings, and outputs.
- Preserve inputs and JSON output with the report.
- Treat JSON as the canonical calculation interchange format. Use CSV for ledgers and tabular source data.
- Do not use randomness for decision outputs.

## Run the engine

Use:

```text
python3 scripts/feasibility_math.py COMMAND --input INPUT.json
```

Pass `-` as the input path to read JSON from standard input. Run `--help` for the complete schema.

## Commands

### `funnel`

Require `starting_count`, ordered `stages` with `name` and conditional `rate`, `orders_per_buyer`, and `capacity`. Return every stage, latent orders, fulfilled orders, and unmet demand.

### `marketplace`

Require supply inputs, demand funnel inputs, and explicit matching filters. Calculate activated suppliers, available units, qualified demand, and transactions as the minimum of matched supply and demand.

### `unit-economics`

Require price, named variable costs, refund rate, payment fee rate, fixed payment fee, and fixed period costs. Return expected net revenue, contribution per unit, contribution margin, and ceiling break-even units. Reject non-positive contribution for break-even.

### `cash-runway`

Require opening cash and an explicit ordered list of period net cash flows. Return each closing balance and the first period below zero. Do not extrapolate beyond the provided horizon.

### `scenarios`

Require named scenarios with volume, price, variable cost per unit, and fixed costs. Return revenue, contribution, and operating result. Treat names as scenarios, not probabilities.

### `baseline`

Require baseline and forecast intervals plus evidence flags. Return absolute changes, interval multiples when defined, diagnostic level, and central-case eligibility. Do not calculate a multiple from a zero baseline.

### `evidence-profile`

Require claim ID and all evidence dimensions. Validate the profile and echo weaknesses without calculating a total score.

## Interpret outputs conservatively

Do not turn a mathematically valid result into an evidence claim. A result is only as decision-useful as its inputs, definitions, dependencies, and maturity. Preserve `CALC` labels and link every material output to the corresponding input and formula IDs.
