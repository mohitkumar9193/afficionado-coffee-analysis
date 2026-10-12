# Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters

Internship research paper | 12 October 2026

## Abstract

This study develops a reproducible framework for assessing product popularity, revenue contribution, category dependency, and menu concentration at Afficionado Coffee Roasters. Transaction revenue is calculated from purchased quantity and unit price, then summarized by product, product type, category, and store. A Streamlit dashboard provides filtered rankings, contribution charts, Pareto analysis, product drill-downs, and transparent recommendation rules. The analytical implementation has passed 18 calculation and application interaction tests. Empirical EDA and business findings remain pending receipt and validation of the transaction dataset; no product performance or financial outcome is asserted. The framework supports subsequent evidence-based menu decisions while distinguishing revenue from profit and observed sales from demonstrated customer preference.

## Background and context

The project brief identifies three specialty coffee retail concerns: products with high sales volume but modest revenue contribution, expensive products with limited sales, and crowded menus that can complicate service and customer choice. These concerns motivate product-level analysis rather than an analysis centered on purchase timing. They are business questions to investigate, not measured conditions established for this retailer.

## Problem statement and objectives

The brief describes limited visibility into product performance, category revenue dependency, and low-impact items. The primary objectives are to rank top- and least-selling products, quantify revenue contribution by product and category, and measure concentration across the observed menu. Secondary objectives are to identify hero product candidates and items requiring review or redesign, and to support menu simplification and merchandising decisions.

The study asks which products lead in units and revenue, how those rankings differ, which categories and product types drive revenue, how mix varies across stores, and what share of sold products is needed to generate 80% of revenue. Profitability and operational improvements require additional cost and service evidence.

## Dataset and analytical scope

The expected source is transaction-level CSV or Excel data. The brief specifies year 2025, but the actual observation period, row count, currency, provenance, and completeness must be established during ingestion. An observation may be a transaction line rather than an entire customer purchase; transaction_id uniqueness must be verified before transaction counts or duplicate removal are interpreted.

| Field | Expected meaning |
| --- | --- |
| transaction_id | Transaction identifier; granularity to be verified |
| year | Transaction year described as 2025 in the brief |
| transaction_time | Time in HH:MM:SS format |
| transaction_qty | Purchased units |
| unit_price | Price per unit; currency to be confirmed |
| store_id and store_location | Store identifier and physical location |
| Balance | Account balance in the brief; business meaning unverified |
| product_id | Product identifier used for aggregation |
| product_category | Broad product group |
| product_type | Variant within a category |
| product_detail | Product description such as blend or flavor |

The dashboard currently requires seven analytical fields: product_id, product_detail, product_category, product_type, store_location, transaction_qty, and unit_price. Other supplied columns are retained. The complete 12-column schema still requires source inspection. All eligible categories are included; Coffee, Tea, and Chocolate are examples rather than a fixed list.

## Cleaning and validation

The implementation trims and lowercases column names and trims key labels. It checks required analytical fields, accepts only finite positive prices and positive whole-number quantities, and records excluded rows with source-row numbers and reasons. Original uploads are not overwritten. Exclusions are eligibility rules rather than verified corrections to the retailer’s records; refunds, free items, and returns would require a separate agreed treatment.

Exact duplicate records are retained until transaction granularity is confirmed. Unusually high quantities and prices are not automatically removed. Product IDs with conflicting descriptions, types, or categories are flagged, and store_id to location mappings require review. Balance is not used as revenue. Missing-value counts, exclusion rates, duplicate counts, and outlier distributions have not yet been measured on real records.

## Revenue computation and KPI definitions

For eligible source row i, revenue r_i equals transaction_qty_i multiplied by unit_price_i. Product revenue R_p is the sum of r_i for product p, and product volume Q_p is the sum of its quantities. Total revenue R is summed across the active filter scope. Decimal arithmetic is used for transaction revenue and the Pareto threshold; display and chart outputs use numerical summaries.

| KPI | Formula and interpretation |
| --- | --- |
| Product revenue contribution | 100 × R_p / R; percentage of filtered revenue |
| Product sales volume | Q_p; purchased units for each observed product |
| Category revenue share | 100 × category revenue / R |
| Revenue concentration ratio | 100 × top N product revenue / R; N is user selected |
| Product Efficiency Score | R / distinct sold product IDs; revenue per SKU in dataset currency |

Revenue per SKU is the brief’s definition of Product Efficiency Score. It measures average revenue across observed sold products, not profit or preparation efficiency. Product and category percentages use total filtered revenue. Type contribution within a category uses that category’s revenue, and store mix uses each store’s revenue or units. Top-N limits rankings and changes CR-N without changing the underlying percentage denominator.

## Popularity and revenue analysis

Products are grouped by product_id and ranked separately by purchased units and revenue. Equal values share competition ranks. The rank gap is revenue rank minus volume rank, so a positive gap indicates a stronger volume position. Weighted average selling price equals product revenue divided by product units. Sales-row counts are available, but they cannot be treated as customer purchase frequency until transaction structure is confirmed.

## Category and store comparisons

Category totals measure revenue dependency. Product types are grouped jointly with their categories so identically named types in different categories remain distinct. Store revenue and unit shares provide absolute scale and normalized sales mix. A store-category heatmap displays observed mix, while product drill-downs show store-level performance. Differences may reflect availability, pricing, traffic, or coverage as well as demand; they do not establish customer preference by themselves.

## Pareto analysis and menu balance

Products are sorted in descending revenue order, with product ID used as a deterministic tie-breaker. Cumulative contribution is calculated over all products in the filtered scope. The minimum set reaching at least 80% includes the first product crossing the threshold. Its size and percentage of observed products are reported. A tie warning appears if equal-revenue products straddle the boundary.

Revenue anchors are this minimum set; the long tail comprises the remaining observed products. These labels describe relative concentration. The app also calculates the revenue share generated by the top 20% of products, rounding the count upward. It does not assume that 20% actually generates 80% of revenue. A narrow filter can mechanically increase concentration, and a long-tail label alone does not establish that an item should be removed.

## Exploratory data analysis and findings status

Empirical EDA is pending. The intended sequence is to establish dataset coverage and quality, inspect quantity and price distributions, reconcile transaction revenue with all grouped summaries, examine product volume and revenue rankings, compare category and store mix, and evaluate the cumulative revenue curve. Observed zero sales cannot be identified from transaction data alone without a complete menu catalog.

| Analysis output | Current evidence status |
| --- | --- |
| Coverage and data quality | Source dataset pending; no observed counts or exclusion rates |
| Top and bottom products | Analysis implemented; no identified business leaders |
| Category and store performance | Analysis implemented; no measured dependency findings |
| Revenue concentration | Analysis implemented; no empirical 80% product count |
| Recommended products | Rules implemented; actual product classifications pending |

Once data is supplied, findings must report the filter scope, currency, coverage, and eligible population alongside each total, rank, and percentage. Tables and charts should be exported from the verified dashboard or shared analytics modules. Product, category, type, and store revenue totals must reconcile; contribution shares must total 100% within their stated denominators.

## Implementation verification

Eighteen tests pass: thirteen analytical checks and five Streamlit application checks. The checks cover revenue reconciliation, invalid numeric values, product metadata conflicts, category and store denominators, Pareto boundaries and ties, recommendation rules, dashboard navigation, invalid uploads, empty selections, and filtered totals. A local server responds with HTTP 200. Synthetic test fixtures verify software behavior and are not business observations. Visual browser QA with populated data and real-data validation remain outstanding. Excel ingestion and single-product selections pass application tests.

## Recommendations and decision rules

Recommendation rules are exploratory screens evaluated against product medians within the active scope. Metadata conflicts receive data review before business action. Fewer than three observed products produce an insufficient-comparison label. Other products are classified in priority order so each receives one label, supporting evidence, and an action suggestion.

A hero candidate belongs to the 80% revenue anchor set and exceeds both median units and median revenue. The suggested action is to prioritize availability and visibility, subject to margin and capacity review. A promotion candidate has below-median units, above-median weighted price, and revenue at or above the median; a limited merchandising or sampling trial can test demand before expansion.

A revenue-yield review candidate has above-median units and a positive rank gap. Pricing, product mix, and complementary purchases can be investigated while preserving demonstrated popularity. A review or redesign candidate belongs to the long tail and falls below both unit and revenue medians. Availability, customer feedback, cost, and menu role should be reviewed before a redesign trial. Products meeting none of these rules remain under monitoring.

No specific item is recommended for removal at this stage. Permanent removal decisions require cost and margin data, stock availability, comparable sales exposure, preparation effort, customer feedback, a complete menu catalog, and strategic context. A pilot should measure revenue, units, margin where available, and substitution effects before wider changes. Expected gains cannot be quantified from the current evidence.

## Limitations

The absence of real transaction records prevents empirical findings. The expected schema lacks product cost, discount, tax, availability, service-time, and complete calendar-date information. Quantity multiplied by listed unit price should therefore be described as computed sales revenue until its accounting interpretation is confirmed. Whole-number and positive-value validation may exclude legitimate records if the business uses fractional sales, refunds, or complimentary items.

The framework describes sold products rather than the complete menu. Median thresholds depend on filter choices and are not externally validated decision models. Revenue concentration measures dependency, not a probability of business failure. Store comparisons require comparable coverage and do not prove preference or causality. Benefits to profitability and operational efficiency remain proposed outcomes rather than demonstrated effects.

## Conclusion

The project provides an implemented framework for product-centered revenue intelligence and a tested interactive dashboard. It connects popularity, contribution, category mix, and Pareto concentration to transparent product review rules. Completion of the empirical research requires source-data validation, reconciled EDA outputs, and evidence-based findings. The resulting analysis can then support menu and merchandising trials without overstating profit or service improvements.

## Reproducibility and references

The project folder afficionado-coffee-analysis contains shared modules in src, the Streamlit entrypoint dashboard/app.py, tests, dependency requirements, and methodology guides. The tested environment uses Python 3.12, Streamlit 1.65.0, pandas 3.0.6, Plotly 6.9.0, and openpyxl 3.1.5. Direct dependency versions are pinned. Run the dashboard from the repository root with python -m streamlit run dashboard/app.py, and run verification with python -m unittest discover -s tests -v.

CSV and XLSX uploads are analyzed without saving the uploaded file to the project. Exported summaries document values in the selected scope. Raw and processed local data are excluded from Git by default. Streamlit Community Cloud is the planned analytics host; Vercel is the planned companion page linking to the dashboard and reports. The project is published on GitHub, with a live Streamlit dashboard and Vercel companion page. Empirical findings remain pending the source dataset.

The project brief and implementation are the primary sources for this paper. Software documentation supports the application design; it does not constitute empirical evidence about Afficionado Coffee Roasters.

[1] Afficionado Coffee Roasters internship project brief supplied in this conversation. Background, objectives, expected schema, methodology, KPIs, and deliverables. Accessed 12 October 2026.

[2] Project implementation. src/products.py, src/categories.py, src/concentration.py, src/recommendations.py, dashboard/app.py, and tests. Local project version assessed 12 October 2026.

[3] Streamlit. Understanding Streamlit’s client-server architecture. https://docs.streamlit.io/develop/concepts/architecture/architecture. Accessed 12 October 2026. The documented architecture supports the Python server and browser client design used here.

[4] Streamlit. Deploy your app on Community Cloud. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy. Accessed 12 October 2026. The documented GitHub repository and entrypoint deployment flow informs the hosting plan.

## Completion requirements for empirical submission

The final empirical paper must add source provenance, dataset coverage, validation outcomes, actual product and category tables, store comparisons, the observed Pareto curve, and recommendations tied to those findings. Each published numerical conclusion must match a verified output. Author and institutional submission details should be added using confirmed information. This version supplies the methodology and implementation evidence, while empirical conclusions await the dataset.


