# Decision and Reporting Standard

## Contents

1. Evidence maturity matrix
2. Decision rule
3. Baseline diagnostics
4. Scenarios and sensitivity
5. Recommendation vocabulary
6. Report requirements

## 1. Rate maturity by material dimension

Use E0-E4 as an internal evidence-stage label, not a probability or score:

| Level | Evidence stage | Permitted use |
|---|---|---|
| E0 | Idea or unsupported assertion | Research plan only |
| E1 | Secondary or proxy evidence | Initial range and validation decision |
| E2 | Local primary signals without reliable paid behavior | Small reversible experiment |
| E3 | Paid transactions or representative pilot with measured costs | Limited staged commitment |
| E4 | Stable cross-period operations with understood data quality | Mature model, subject to transfer risk |

Rate demand, unit economics, operations/capacity, legal/regulatory, and execution separately. Add technical, supply-chain, or platform-liquidity dimensions when material. Do not average them. Treat the weakest decision-critical dimension as the binding gate.

Do not promote interviews, clicks, waitlists, or stated intent to E3 unless they involve meaningful payment behavior. Do not promote a pilot that excludes hard costs, cancellations, or the difficult customer segment.

## 2. Apply a declared decision rule

Tie every recommendation to:

- the user-defined success and failure thresholds;
- the maximum loss or at-risk budget supplied by the user;
- the binding evidence gate;
- expected cash and operational constraints;
- the reversibility and timing of the commitment;
- alternatives and the cost of delay.

If the user did not provide a loss constraint, omit a numeric risk recommendation. If a material dimension remains below the required gate, recommend validation, deferment, or stopping rather than averaging it away.

## 3. Use baseline multiples as diagnostics

When a verified baseline exists, report:

- baseline and forecast intervals;
- absolute change;
- minimum and maximum implied multiples;
- baseline exposure, stockouts, capacity, season, and data quality;
- mechanism and evidence that could produce the change.

Use default alerts:

- 2×: flag and explain the mechanism;
- 5×: require a relevant historical analogue or direct local signal;
- 10×: exclude from a central case unless direct behavioral evidence, mechanism evidence, and verified capacity all support it;
- 20×: treat as an exceptional claim and require the same conditions plus explicit adversarial review.

Treat these as diagnostic defaults, not universal natural laws. Do not calculate a ratio from a zero or structurally constrained baseline; use absolute thresholds and a corrected reference class instead.

## 4. Build coherent scenarios

At E0-E1, call numerical cases `illustrative` or `threshold` scenarios. Reserve `central case` for evidence sufficient to support one. Never imply that conservative, central, or upside labels are probabilities.

Change related inputs together. Examples:

- higher price may reduce conversion;
- higher volume may require step-fixed labor and equipment;
- bad weather may affect demand, transport, cancellations, and staffing together;
- platform growth may require subsidies on both sides;
- an event may add visitors while displacing regular customers.

Show which assumption flips the decision. Prefer break-even and threshold questions when probability estimates are not defensible.

## 5. Use bounded recommendations

Choose one:

- continue to the next declared gate;
- continue after specified changes;
- run a small reversible validation;
- defer material commitment;
- evidence insufficient;
- stop under the declared thresholds.

Do not write `viable`, `profitable`, or `safe` without stating the decision definition, period, constraints, and evidence gate. Do not guarantee success.

## 6. Match report depth to the decision

Use the templates in `assets/templates/`.

Every output must include:

- decision contract and exclusions;
- capability and data limitations;
- evidence maturity by material dimension;
- facts, calculations, proxies, assumptions, judgments, and unknowns;
- alternatives and counterfactual;
- binding risks and adversarial findings;
- recommendation tied to thresholds;
- next decision, validation action, success threshold, failure threshold, and stop condition.

Include market size, technical feasibility, public-economic impact, tax, financing, or detailed regulation only when they change the decision. Write unavailable tool, model, or interface metadata as `unavailable`; never infer it.
