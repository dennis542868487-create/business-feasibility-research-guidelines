# Business-Model Modules

## Contents

1. Shared mathematical rules
2. Physical location and restaurant
3. Rental assets
4. Two-sided marketplace
5. SaaS and subscription
6. Ecommerce
7. Manufacturing and capital projects
8. Regulated business
9. Event-driven demand

## 1. Apply shared mathematical rules

Keep units explicit. A count multiplied by a conditional rate remains a count. A count multiplied by average units per entity becomes units. Capacity is a ceiling, not a conversion factor.

Use:

```text
stage_n = stage_(n-1) × P(stage_n | stage_(n-1))
latent_orders = qualified_buyers × average_orders_per_buyer
fulfilled_orders = min(latent_orders, service_capacity)
```

Flag funnel stages that overlap or depend on one another. Do not multiply unrelated point estimates merely because the units appear compatible.

## 2. Physical location and restaurant

Analyze trade area and travel time, location visibility, daypart, weekday/weekend, season, comparable capacity, price, channel, seats, table turns, takeout, food and labor cost, rent, waste, permits, safety, and opening ramp.

Use observed footfall only after separating passersby, entrants, purchasing parties, orders, and items. Cap restaurant orders by seats, service duration, kitchen throughput, staffing, opening hours, and channel constraints.

## 3. Rental assets

Analyze fleet or asset count, bookable hours, utilization, turnaround, cleaning, maintenance, damage, depreciation, insurance, deposits, cancellation, seasonality, and maximum orders per asset.

Calculate capacity as available assets multiplied by feasible turns in the period, adjusted for maintenance and blocked time. Do not multiply latent orders by capacity.

## 4. Two-sided marketplace

Model supply:

```text
activated_suppliers
  = reachable_suppliers
  × contact_rate
  × onboarding_rate

available_units
  = activated_suppliers
  × average_available_units_per_supplier
  × availability_rate
  × time_match_rate
```

Model demand:

```text
qualified_orders
  = reachable_customers
  × visit_rate
  × search_or_quote_rate
  × booking_rate
  × payment_rate
  × average_orders_per_buyer
```

Filter both sides for geography, time, product, price, trust, insurance, and quality before matching. Calculate:

```text
completed_transactions = min(matched_supply_units, matched_demand_orders)
```

Also test cold start, local density, cancellations, dispute rate, payment failure, subsidy, take rate, acquisition cost, repeat behavior, multi-homing, disintermediation, and regulatory responsibility.

## 5. SaaS and subscription

Analyze qualified traffic, activation, trial-to-paid conversion, cohort retention, gross and net revenue retention when relevant, revenue per account, variable infrastructure, support, acquisition cost, contribution, payback, implementation burden, security, privacy, and compliance.

Do not infer revenue from global TAM. Use cohorts and paid behavior. Ensure LTV assumptions are consistent with churn definition, margin, contract length, and observation window.

## 6. Ecommerce

Analyze qualified sessions, conversion, average order value, returns, refunds, discounts, payment fees, fulfillment, shipping, customer support, inventory, working capital, repeat orders, channel concentration, and acquisition incrementality.

Distinguish gross merchandise value, collected revenue, recognized revenue, and contribution.

## 7. Manufacturing and capital projects

Analyze technical readiness, inputs, suppliers, yield, scrap, quality, capacity, equipment, commissioning, ramp, safety, environmental constraints, permits, working capital, capital cost, schedule, financing, and downside recovery value.

Separate financial feasibility for the owner from broader economic or social appraisal. Apply public-sector appraisal methods only when the decision actually includes public value and distributional effects.

## 8. Regulated business

Identify jurisdictions, licenses, approvals, professional scope, insurance, reporting, data, safety, labor, consumer, and tax obligations. Mark each unresolved legal or regulatory conclusion `PRO_CONFIRM`.

Do not provide definitive legal, medical, financial, engineering, insurance, or regulatory conclusions. State the exact question and qualified professional required.

## 9. Event-driven demand

Establish incremental attendance versus the counterfactual. Use conditional stages:

```text
latent_incremental_orders
  = incremental_people
  × P(in_service_area)
  × P(has_relevant_free_time | in_service_area)
  × P(has_category_need | relevant_free_time)
  × P(exposed_to_business | category_need)
  × P(chooses_business | exposed)
  × P(pays | chooses)
  × average_orders_per_buyer

fulfilled_incremental_orders
  = min(latent_incremental_orders, incremental_service_capacity)
```

Test displacement of regular demand, event schedule, routes, road closures, weather, ticket rules, food or retail restrictions, accommodation location, trip purpose, historical comparable POS, cancellations, inventory, and staffing. Do not convert regional attendance into one store's orders without evidence for every material transition.
