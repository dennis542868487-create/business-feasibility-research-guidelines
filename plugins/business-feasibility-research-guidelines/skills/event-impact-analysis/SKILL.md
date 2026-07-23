---
name: event-impact-analysis
description: Estimate whether an event, festival, concert, tournament, cruise schedule, policy change, or transport opening can materially affect a specific local business. Use when regional attendance, visitor, traffic, or economic-impact numbers are being converted into store footfall, orders, inventory, staffing, or revenue decisions.
---

# Event Impact Analysis

Translate incremental event exposure into capacity-capped orders without turning regional attendance into store demand.

## Procedure

1. Define the counterfactual: what demand would occur without the event in the same dates, weather, season, and operating conditions?
2. Use incremental unique people when available. Separate people, visits, ticket scans, visitor nights, footfall, entrants, purchasing parties, orders, and items.
3. Verify event dates, schedule, accommodation, transport routes, closures, entry and exit behavior, restrictions, and the business's actual service area and opening hours.
4. Build conditional stages for service-area presence, relevant free time, category need, business exposure, choice, payment, and orders per buyer.
5. Attach a source or explicit assumption to every material stage. Flag correlation and overlapping filters.
6. Calculate latent incremental orders, then use `fulfilled_incremental_orders = min(latent_incremental_orders, incremental_service_capacity)`.
7. Test displacement of regular customers, cancellations, weather, staffing, stock, turnaround, and service degradation.
8. Compare with historical events or POS only after aligning event type, scale, route, season, hours, and business category.
9. Apply interval baseline diagnostics. Treat large multiples as alerts requiring direct behavior, mechanism, and capacity evidence.
10. Recommend reservations, deposits, event-specific landing pages, small ads, manual counts, temporary inventory, or reversible staffing before irreversible commitments.

Read [the event module](../business-feasibility-research-guidelines/references/business-models.md) and [decision rules](../business-feasibility-research-guidelines/references/decision-and-reporting.md). Return `evidence insufficient` when a material transition lacks evidence.

In the answer, show the regional-to-store transition stages and the capacity ceiling formula explicitly. Do not leave either implicit in prose.
