# Step 8: KPI definitions and product recommendations

Implemented src/recommendations.py and added a KPI formula table, revenue-per-SKU metric, recommendation filters, evidence table, downloadable action plan, and menu review guidance to the dashboard.

## Five KPI formulas

| KPI | Formula |
| --- | --- |
| Product Revenue Contribution (%) | Product revenue / total filtered revenue × 100 |
| Product Sales Volume | Sum of product transaction quantities |
| Category Revenue Share (%) | Category revenue / total filtered revenue × 100 |
| Revenue Concentration Ratio (CR-N %) | Top-N product revenue / total filtered revenue × 100 |
| Product Efficiency Score | Total filtered revenue / distinct sold product IDs |

Product Efficiency Score is defined by the brief as revenue per SKU. It is a scope-level currency amount, not a profit metric or operational efficiency score. Individual SKU revenue is already in the product table. Top-N affects CR-N only.

## Recommendation rules, in priority order

1. Data review: conflicting product metadata; withhold product action until resolved.
2. Insufficient comparison scope: fewer than three observed products; broaden the filters.
3. Hero candidate: in the revenue anchor set and strictly above both product medians for units and revenue. Prioritize availability and visibility, subject to cost/capacity review.
4. Promotion candidate: below-median units, above-median weighted selling price, and revenue at or above the median. Trial merchandising and measure results.
5. Revenue yield review: above-median units and a positive revenue-minus-volume rank gap. Review pricing and mix while preserving demonstrated popularity.
6. Review/redesign candidate: in the long tail and strictly below both units and revenue medians. Investigate availability, customer feedback, and menu role before redesign.
7. Monitor: no preceding rule applies. Equal-median ties are not automatically classified as heroes or underperformers.

Each product receives one label and retains the measured revenue, contribution, ranks, anchor status, and median thresholds in its CSV export. Thresholds are transparent heuristics rather than validated causal models. Changing filters can change the medians and recommendations; changing Top-N does not change recommendation labels.

## Menu-removal limits

There is no automatic removal recommendation. Confirm margin and product cost, stock availability, sales exposure, completeness of the menu catalog, preparation effort, customer feedback, and strategic role. Pilot changes before making permanent decisions. Business findings remain pending real validated transaction data.

## Validation

Synthetic fixtures verify KPI totals, five formula definitions, hero/promotion/yield/review classifications, metadata override, equal products, small scopes, and empty data. All 13 calculation tests pass, and Python compilation passes. Interactive runtime validation remains pending dependency installation.

Launch instructions are in docs/step-5.md. Upload the actual CSV or XLSX dataset to populate the analysis.

