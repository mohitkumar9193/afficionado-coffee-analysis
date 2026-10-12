# Confirmed project requirements

## Business objectives

Identify top- and least-selling products, quantify product and category revenue contributions, and measure menu revenue concentration. Support menu simplification, identify hero products, and flag low-performing products for review or redesign.

## Expected columns

transaction_id, year, transaction_time, transaction_qty, unit_price, store_id, store_location, Balance, product_id, product_category, product_type, product_detail.

The brief describes year as 2025. Actual coverage must be checked. Validate whether transaction_id identifies a transaction or a line item before counting transactions or removing duplicates.

## Analytical workflow

Validate data; compute revenue; aggregate by product, type, category, and store; compare units and revenue rankings; evaluate category dependency; calculate cumulative revenue and Pareto concentration; develop evidence-based recommendations.

## KPI definitions for implementation

- Product revenue contribution: product revenue / revenue in the selected scope × 100.
- Product sales volume: sum of transaction_qty by product.
- Category revenue share: category revenue / revenue in the selected scope × 100.
- Revenue concentration ratio (CR-N): revenue of top N products / revenue in the selected scope × 100.
- Revenue per SKU (brief's Product Efficiency Score): revenue / distinct product IDs in the selected scope. This is revenue productivity, not an operational efficiency or profit measure.

Specify denominator scope in chart labels and handle empty or zero-revenue selections. Top-N changes rankings and CR-N, not the underlying filter-scope revenue denominator. For Pareto analysis, include the first product crossing 80%; do not assume 20% of products achieve that threshold.

## Dashboard requirements

Product rankings by volume and revenue; category distribution; popularity versus revenue scatter plot; product drill-down tables; category and product-type filters; store location selector; Top-N slider. Include concentration analysis and the required KPIs.

## Deliverables

Research paper (EDA, insights, recommendations), Streamlit dashboard, executive summary for government stakeholders. GitHub and Vercel submission presence requested by the user.

## Questions to resolve when data arrives

Currency; Balance meaning; dataset coverage and completeness; transaction granularity; product ID consistency; dataset publishing permissions; any cost or margin fields. Products absent from transactions cannot be identified as zero-selling without a complete menu catalog.
