---
name: operational-financial-feasibility
description: Analyze operational capacity, process constraints, supply, staffing, unit economics, break-even, working capital, cash runway, and scenario risk for a business decision. Use for launches, hiring, inventory, equipment, locations, rental fleets, manufacturing, service capacity, pricing, contribution margin, or financial feasibility; do not replace qualified accounting, tax, financing, engineering, insurance, or regulatory advice.
---

# Operational and Financial Feasibility

Connect demand, capacity, contribution, cash, and implementation in one coherent model.

## Procedure

1. Define the decision period, currency, tax basis, price basis, units, and user-supplied loss constraint.
2. Map the operating process from acquisition through delivery, cancellation, refund, support, and rework.
3. Calculate capacity from assets, staff, opening hours, cycle time, downtime, yield, maintenance, and step-fixed constraints.
4. Calculate recognized or expected net revenue consistently. Separate gross sales, refunds, payment fees, variable costs, contribution, fixed costs, capital expenditure, financing flows, and working capital.
5. Reject break-even calculations when contribution per unit is non-positive or inputs are missing.
6. Build explicit period cash flows; do not substitute accounting profit for liquidity.
7. Construct coherent scenarios by changing dependent inputs together. Add step costs when volume exceeds capacity.
8. Test downside demand, lower conversion, higher acquisition cost, higher labor or supply cost, delays, cancellations, and unavailable capacity.
9. Compare do-nothing, minimal test, staged, proposed, and relevant alternative options.
10. Tie the recommendation to declared thresholds and the weakest material evidence dimension. Do not invent a safe investment ceiling.

Read [the calculation contract](../business-feasibility-research-guidelines/references/calculation-contract.md), [business-model modules](../business-feasibility-research-guidelines/references/business-models.md), and [decision standard](../business-feasibility-research-guidelines/references/decision-and-reporting.md). Run the bundled math engine when available and preserve its JSON output.

Mark tax, financing, legal, engineering, insurance, and regulatory conclusions requiring a qualified reviewer as `PRO_CONFIRM`.
