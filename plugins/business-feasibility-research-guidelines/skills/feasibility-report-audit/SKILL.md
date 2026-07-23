---
name: feasibility-report-audit
description: Adversarially review a business feasibility report, market study, forecast, or investment memo for unsupported claims, source-fit problems, unit errors, dependency, fake precision, capacity omissions, weak scenarios, overconfident recommendations, and missing validation gates. Use before relying on a report for a material business commitment.
---

# Feasibility Report Audit

Try to falsify the report's decision, not merely improve its presentation.

## Audit order

1. Restate the decision, thresholds, time horizon, and amount at risk. Flag any missing decision contract.
2. Identify the three claims most capable of changing the recommendation.
3. Check statement labels and trace every material fact, internal datum, proxy, calculation, and assumption.
4. Audit source authority, decision fit, lineage, and contrary evidence using [the evidence standard](../business-feasibility-research-guidelines/references/evidence-standard.md).
5. Recalculate material formulas. Check units, denominators, currency, period, tax basis, person/visit/order distinctions, conditional funnels, supply-demand matching, and capacity caps.
6. Compare forecast and baseline intervals using absolute change and multiples. Check stockouts, exposure, seasonality, and structural changes before interpreting the multiple.
7. Check whether supposedly independent estimates share data or assumptions.
8. Challenge scenario coherence, step-fixed costs, cash timing, cancellations, implementation, regulation, and transfer assumptions.
9. Rate evidence maturity by material dimension and identify the binding dimension. Reject averaging.
10. Verify that the recommendation follows the declared thresholds and user-supplied risk constraint.
11. Identify what evidence would reverse the conclusion and the lowest-cost next test.
12. Run the bundled report validator when a local Markdown report is available.

Follow [the decision and reporting standard](../business-feasibility-research-guidelines/references/decision-and-reporting.md) and [security rules](../business-feasibility-research-guidelines/references/security-and-privacy.md).

## Output severity

- **Blocker:** could reverse the decision, violates units, fabricates evidence, or recommends material risk without a decision rule.
- **Major:** materially weakens confidence or reproducibility.
- **Minor:** improves clarity without changing the decision.

Lead with blockers. If none exist, state that explicitly and list residual uncertainty.
