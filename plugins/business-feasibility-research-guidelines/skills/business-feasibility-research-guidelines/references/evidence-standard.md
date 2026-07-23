# Evidence Standard

## Contents

1. Information types
2. Claim-evidence model
3. Evidence dimensions
4. Source classes
5. Independence and lineage
6. Ledger requirements

## 1. Label every material statement

Use one label:

- `FACT`: externally sourced fact directly supported by the cited source;
- `INTERNAL`: user-provided operating fact whose integrity has been checked;
- `CALC`: reproducible result linked to formula and inputs;
- `PROXY`: evidence transferred from another place, period, segment, or business;
- `USER_ASSUMPTION`: unverified assumption supplied by the user;
- `MODEL_ASSUMPTION`: explicit temporary input chosen for analysis;
- `JUDGMENT`: interpretation rather than measurement;
- `UNKNOWN`: material information not currently known;
- `PRO_CONFIRM`: item requiring a qualified professional.

Do not demand an external source for a calculation or assumption. Demand a type label, input provenance, and formula instead.

## 2. Model claims and evidence separately

Assign stable IDs. Allow one claim to have multiple evidence records and one evidence record to bear on multiple claims. Record whether each item supports, contradicts, or contextualizes the claim.

Evaluate evidence at the claim-metric level. A reliable organization can publish one metric that fits the decision and another that does not.

## 3. Use a profile, never a composite score

Rate each applicable dimension `high`, `medium`, `low`, or `unknown` and explain the rating:

| Dimension | Test |
|---|---|
| Authority | Is the publisher competent and accountable for this metric? |
| Directness | Does it measure the target outcome rather than a proxy? |
| Geographic fit | Does the geography match or transfer defensibly? |
| Time fit | Do period, season, and event window match? |
| Definition fit | Are person, visit, lead, order, unit, and revenue definitions aligned? |
| Accuracy | Are coverage, error, sampling, and missingness understood? |
| Method transparency | Can collection and calculation be inspected? |
| Interpretability | Are units, population, denominator, and metadata available? |
| Coherence | Can the figure be compared without hidden definition changes? |
| Independence | Is it independent of other corroborating evidence? |
| Reproducibility | Can the result or transformation be recreated? |
| Materiality | Could error change the decision? |

Do not average the dimensions. Report the weak dimensions that matter to the decision.

## 4. Treat source class as context, not rank

- **Internal operating evidence:** transactions, refunds, inquiries, footfall, conversion, inventory, capacity, acquisition, and seasonality. Verify completeness and definitions.
- **Official and administrative data:** statistics agencies, regulators, governments, transport, tourism, event organizers, registries, and permits.
- **Transparent research:** peer-reviewed work, research institutes, method-disclosed surveys, filings, and public financial documents.
- **Market signals:** competitor pages, prices, maps, reviews, hiring, news, property listings, and supplier sites.
- **Discovery-only material:** unattributed market-size pages, SEO farms, AI-generated pages, unsourced forecasts, social speculation, and copied articles.

Government origin can raise authority without improving local or metric fit. Internal origin can raise directness without guaranteeing accuracy.

## 5. Trace independence and lineage

Assign a `source_lineage_id` or dependency cluster. Treat articles quoting the same release, dataset, consultant, or model as one evidentiary chain. Record the original source when discoverable.

For multiple estimation methods, record shared inputs. Do not call two outputs triangulation when both depend on the same population count, conversion assumption, or vendor forecast.

## 6. Preserve a decision-grade ledger

Use `assets/templates/evidence-ledger.csv`. At minimum record:

- claim ID, evidence ID, stance, and information type;
- value or range, unit, currency and price basis;
- geography, population, and reference period;
- title, organization, URL or internal identifier, and page/table locator;
- publication date, access date, and last verification date;
- methodology, sample, missingness, and transformation formula ID;
- proxy rationale, assumptions, limitations, and confidentiality;
- all evidence-profile dimensions;
- source lineage ID and decision materiality.

Preserve a short supporting excerpt or locator when permitted, not an entire copyrighted source. Mark inaccessible, changed, or removed sources rather than silently substituting them.
