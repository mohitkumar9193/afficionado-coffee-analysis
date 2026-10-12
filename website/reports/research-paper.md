# Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters

Public dataset case study using Maven Roasters educational records  
Prepared for Mohit's internship | 12 October 2026

## Abstract

This study applies the Afficionado Coffee Roasters project objectives to the publicly available Maven Roasters Coffee Shop Sales dataset. Maven Roasters is a fictional business, and the results are case-study findings rather than observations of Afficionado. The dataset comprises 149,116 sales records from three New York City stores between 1 January and 30 June 2023. Validated quantity and unit-price calculations produce revenue of 698,812.33 and 214,470 units across 80 products, nine categories and 29 product types. Coffee contributes 38.63% of revenue and Tea contributes 28.11%. The ten leading products contribute 25.38%; 43 products are needed to exceed 80%. Product volume and revenue rankings differ materially. The study combines transparent screening rules with an interactive Streamlit dashboard to support merchandising trials and menu review. Missing cost, availability and customer data prevent profit conclusions, causal claims or justified automatic product removal.

## Background and problem statement

Specialty coffee menus can contain frequently purchased low-price products, expensive items with limited sales, and a long tail of menu variants. Product-level evidence helps retailers distinguish customer purchase volume from revenue contribution. The supplied project brief identifies a need for clearer product rankings, category dependency measures and underperforming-item review at Afficionado Coffee Roasters. No company transaction file was available for this study. A public educational dataset was therefore selected to demonstrate the full workflow and produce reproducible findings with explicitly limited applicability.

## Objectives

The primary objectives are to identify highest- and lowest-selling observed products, quantify revenue shares by product and category, and measure revenue concentration. Secondary objectives are to identify hero product candidates, investigate pricing and promotion opportunities, and develop cautious review or redesign recommendations. These objectives concern sales performance. Profitability, service efficiency and financial improvement require additional evidence.

## Dataset, provenance and scope

Source: [Maven Analytics Coffee Shop Sales](https://mavenanalytics.io/data-playground/coffee-shop-sales), labelled Public Domain by its publisher. The downloaded ZIP contains the Transactions worksheet of Coffee Shop Sales.xlsx. It has 149,116 rows and 11 source columns. All transaction_id values are unique in this file. Each row records one product and its quantity at a store and time. It should not be assumed to capture a complete multi-item basket, a distinct customer or customer purchase frequency.

Coverage is 2023-01-01 through 2023-06-30, across Astoria, Hell's Kitchen and Lower Manhattan. There are 80 observed product IDs, nine categories and 29 category/type combinations. The source contains transaction_date rather than year, and has no Balance column. Year is derived from the source date without altering 2023 to match the brief's expected 2025. Balance remains unavailable and is unnecessary for sales revenue. Monetary results are expressed in source price units; a currency symbol is omitted because the worksheet does not explicitly declare currency.

| Source field | Interpretation and treatment |
| --- | --- |
| transaction_id | Unique source record identifier; retained |
| transaction_date | Actual source date; preserved, year derived |
| transaction_time | Source time; retained |
| transaction_qty | Positive purchased whole units |
| unit_price | Positive source price per unit |
| store_id, store_location | Store identifiers and labels |
| product_id | SKU identifier retained as text for grouping |
| product_category | Source category preserved |
| product_type | Product grouping within category |
| product_detail | Source product description preserved |

Archive SHA-256: `be13c59c4cfdc0d1b08ceab514aea50a0cd329c916e4c3585eeef92a5b4c3a2c`. The dashboard checks this fingerprint before loading the public source. A changed download requires revalidation. The original workbook is preserved, and the prepared CSV is a separate derivative with the additional year column.

## Cleaning and validation

Column names are trimmed and normalized to lowercase, identifiers are retained as strings, and key text labels are trimmed. Quantity must be finite, positive and whole-number; price must be finite and positive. Required analytical fields must be populated. Invalid records would be logged by source row and excluded, with the original retained. Exact duplicates are inspected before deletion, because repeated sales can be legitimate.

The inspected file contains zero missing cells, zero exact duplicate rows, zero duplicate transaction IDs, zero excluded rows and zero conflicting product descriptions/categories/types for a product ID. Quantities range from 1 to 8; prices range from 0.80 to 45.00. No arbitrary upper-price cutoff is applied, since packaged beans and drinks have different price ranges. No product or store labels are renamed. No corrections or exclusions were necessary beyond formatting normalization and the derived year.

## Methodology and KPI definitions

Revenue for each record equals transaction_qty multiplied by unit_price. Decimal arithmetic computes transaction and grouped revenue. Units and revenue are grouped by product_id, category, category/type and store. Weighted average selling price equals revenue divided by units. Competition ranks give equal values the same rank. Rank gap equals revenue rank minus volume rank; a positive value identifies a stronger volume position than revenue position.

| Required KPI | Formula and scope |
| --- | --- |
| Product Revenue Contribution (%) | Product revenue / total selected revenue × 100 |
| Product Sales Volume | Sum of product transaction quantities |
| Category Revenue Share (%) | Category revenue / total selected revenue × 100 |
| Revenue Concentration Ratio | Revenue of top N products / total selected revenue × 100 |
| Product Efficiency Score | Total selected revenue / distinct sold product IDs |

Revenue per SKU is 8,735.15 for the full case study. This is a revenue allocation measure, not margin or operating efficiency. Full-scope shares use all eligible rows; type-within-category shares use the corresponding category denominator, and store mix uses that store's denominator. Top-N changes displayed rankings and CR-N, not the denominator of ordinary product shares.

Pareto analysis sorts products by decreasing revenue and accumulates their shares. The product crossing the 80% threshold is included. The minimum set reaching 80% is termed the revenue-anchor set; the remainder is the long tail. These are analytical segments, not proof that tail items are unnecessary.

## Exploratory data analysis and findings

### Sales scale and product rankings

Total revenue is 698,812.33 and total units are 214,470. Average realized revenue per unit is 3.26. The highest-revenue products are:

| ID | Product | Units | Revenue | Share (%) | Volume rank | Revenue rank |
| --- | --- | --- | --- | --- | --- | --- |
| 61 | Sustainably Grown Organic Lg | 4,453 | 21,151.75 | 3.03 | 11 | 1 |
| 59 | Dark chocolate Lg | 4,668 | 21,006.00 | 3.01 | 2 | 2 |
| 39 | Latte Rg | 4,497 | 19,112.25 | 2.73 | 8 | 3 |
| 41 | Cappuccino Lg | 4,151 | 17,641.75 | 2.52 | 35 | 4 |
| 55 | Morning Sunrise Chai Lg | 4,346 | 17,384.00 | 2.49 | 19 | 5 |
| 38 | Latte | 4,602 | 17,257.50 | 2.47 | 4 | 6 |
| 36 | Jamaican Coffee River Lg | 4,395 | 16,481.25 | 2.36 | 15 | 7 |
| 60 | Sustainably Grown Organic Rg | 4,329 | 16,233.75 | 2.32 | 20 | 8 |
| 40 | Cappuccino | 4,266 | 15,997.50 | 2.29 | 25 | 9 |
| 27 | Brazilian Lg | 4,317 | 15,109.50 | 2.16 | 22 | 10 |

Sustainably Grown Organic Lg (ID 61) leads revenue at 21,151.75, contributing 3.03%, while ranking eleventh in volume. Dark chocolate Lg (ID 59) ranks second in both measures. Products are identified by ID and full detail because similar names can describe different sizes or retail formats.

The strongest volume products include:

| ID | Product | Units | Revenue | Share (%) | Volume rank | Revenue rank |
| --- | --- | --- | --- | --- | --- | --- |
| 50 | Earl Grey Rg | 4,708 | 11,770.00 | 1.68 | 1 | 26 |
| 59 | Dark chocolate Lg | 4,668 | 21,006.00 | 3.01 | 2 | 2 |
| 54 | Morning Sunrise Chai Rg | 4,643 | 11,607.50 | 1.66 | 3 | 29 |
| 38 | Latte | 4,602 | 17,257.50 | 2.47 | 4 | 6 |
| 44 | Peppermint Rg | 4,564 | 11,410.00 | 1.63 | 5 | 30 |

Earl Grey Rg (ID 50) leads units at 4,708 but ranks 26th in revenue. Morning Sunrise Chai Rg ranks third in units and 29th in revenue. These gaps show the effect of selling price and product mix; they do not establish weak margins. High unit sales can support footfall, customer choice and complementary purchases, so revenue rank alone is insufficient grounds for removal.

The least-selling observed products are:

| ID | Product | Units | Revenue | Share (%) | Volume rank | Revenue rank |
| --- | --- | --- | --- | --- | --- | --- |
| 19 | Dark chocolate | 118 | 755.20 | 0.11 | 80 | 80 |
| 18 | Spicy Eye Opener Chai | 122 | 1,335.90 | 0.19 | 79 | 78 |
| 10 | Guatemalan Sustainably Grown | 134 | 1,340.00 | 0.19 | 78 | 77 |
| 14 | Earl Grey | 142 | 1,270.90 | 0.18 | 77 | 79 |
| 7 | Jamacian Coffee River | 146 | 2,883.50 | 0.41 | 76 | 62 |

Packaged Dark chocolate (ID 19) records 118 units and 755.20 revenue, the lowest observed figures. The dataset contains only sold products; it cannot identify items with zero sales without a complete menu catalog. Low sales might reflect restricted availability or a specialized menu role.

### Category and product-type performance

| Category | Units | Revenue | Share (%) |
| --- | --- | --- | --- |
| Coffee | 89,250 | 269,952.45 | 38.63 |
| Tea | 69,737 | 196,405.95 | 28.11 |
| Bakery | 23,214 | 82,315.64 | 11.78 |
| Drinking Chocolate | 17,457 | 72,416.00 | 10.36 |
| Coffee beans | 1,828 | 40,085.25 | 5.74 |
| Branded | 776 | 13,607.00 | 1.95 |
| Loose Tea | 1,210 | 11,213.60 | 1.60 |
| Flavours | 10,511 | 8,408.80 | 1.20 |
| Packaged Chocolate | 487 | 4,407.64 | 0.63 |

Coffee and Tea together contribute 66.74% of revenue. This indicates dependency on the two main beverage categories. Bakery and Drinking Chocolate add meaningful revenue diversity. Coffee beans are treated separately from prepared Coffee, and Packaged Chocolate separately from Drinking Chocolate, preserving the source taxonomy.

The leading category/type combinations by revenue are:

| Category | Type | Revenue | Within category (%) |
| --- | --- | --- | --- |
| Coffee | Barista Espresso | 91,406.20 | 33.86 |
| Tea | Brewed Chai tea | 77,081.95 | 39.25 |
| Drinking Chocolate | Hot chocolate | 72,416.00 | 100.00 |
| Coffee | Gourmet brewed coffee | 70,034.60 | 25.94 |
| Tea | Brewed Black tea | 47,932.00 | 24.40 |
| Tea | Brewed herbal tea | 47,539.50 | 24.20 |
| Coffee | Premium brewed coffee | 38,781.15 | 14.37 |
| Coffee | Organic brewed coffee | 37,746.50 | 13.98 |

Type contribution is measured within its category. A product type's category share should not be confused with its share of the entire business.

### Store comparisons

| Store | Units | Revenue | Share (%) |
| --- | --- | --- | --- |
| Hell's Kitchen | 71,737 | 236,511.17 | 33.84 |
| Astoria | 70,991 | 232,243.91 | 33.23 |
| Lower Manhattan | 71,742 | 230,057.25 | 32.92 |

Revenue is distributed fairly evenly across the three stores, with shares from 32.92% to 33.84%. Hell's Kitchen leads revenue, while Lower Manhattan leads units by a narrow margin. Different revenue and unit rankings support examining realized prices and sales mix. These data do not measure traffic, store size, stockouts or operating hours, so a store ranking does not establish relative managerial effectiveness or customer preference.

### Revenue concentration and menu balance

The top ten products contribute 25.38% of revenue. The top 16 products, exactly 20% of the observed menu, contribute 37.10%. It takes 43 products, or 53.75% of the menu, to reach 80.52% of revenue. The other 37 products contribute 19.48%. There is no equal-revenue tie at the 80% boundary.

The classic 80/20 pattern does not hold in this dataset. A broad group contributes material revenue, and no single product exceeds approximately 3.03%. Simplifying the menu to a small handful of best sellers would therefore expose substantial recorded revenue. The tail has lower collective impact per SKU, but its 19.48% share still warrants careful product-by-product review.

## Recommendations

The dashboard applies explicitly documented, exclusive median-based rules. An anchor with units and revenue strictly above their product medians is a hero candidate. A below-median volume product with above-median average price and at-least-median revenue is a promotion candidate. A popular product with a weaker revenue rank receives a yield review. A tail item below both volume and revenue medians receives a review or redesign flag. Other products are monitored. These rules flag 38 hero candidates, 2 promotion candidates, 2 yield reviews, 36 review/redesign candidates and 2 monitor items in the full scope. The number of hero candidates reflects the rule's broad screening purpose; it is not a recommendation to promote all of them simultaneously.

Prioritize availability and visibility for a short list of strong products, including Dark chocolate Lg and Sustainably Grown Organic Lg. Validate costs and service capacity before expanding them. Review highly popular regular-size teas as entry-price or complementary-purchase products rather than treating rank gaps as failure. Test a small, measured merchandising trial for the promotion-screened Civet Cat and Chocolate Croissant, subject to stock availability, customer suitability and margins. A high price alone does not justify promotion.

For packaged Dark chocolate and other low-volume items, check stock availability, days on menu, sourcing cost, shelf life, customer feedback and cross-sell role. Trial revised visibility, assortment or portioning before considering removal. Protect Coffee and Tea availability while testing complementary category opportunities. Compare stores using normalized mix and consistent periods rather than total revenue alone.

Measure a trial against a comparable baseline or control store, recording units, revenue, contribution margin, stockouts and service time. Forecasted revenue uplift, cost savings and stipend eligibility are not established by this analysis.

## Dashboard and reproducibility

The Streamlit app includes KPI cards, volume/revenue ranking, category and type distribution, popularity/revenue scatter plots, Pareto charts, recommendation tables and product drill-downs. Store, category and type filters and a Top-N slider update the selected scope. It loads the credited public case study by default and accepts user CSV/XLSX uploads. A separate synthetic demonstration mode remains explicitly labelled.

The repository includes an analysis runner, source checksum, pinned dependencies and tests. Run `python analysis/run_case_study.py archive.zip` to reproduce summaries in data/processed. Independent pandas integer-cent controls reconcile the overall Decimal revenue, total units and each of the 80 product totals. Category, type, store and nested summary revenues reconcile to the same overall total. Application tests cover all views and filtering behavior; public-data browser checks verify populated charts and disclosure.

## Limitations

These published records describe a fictional Maven business in 2023. They cannot substantiate actual Afficionado performance or a 2025 reporting period. No Balance, costs, discounts, taxes, returns policy, customer IDs, stock availability, complete menu, service time or marketing exposure are supplied. Gross computed sales are therefore distinguished from net revenue and profit. Six months cannot establish full-year seasonality. An observed sale does not reveal availability-adjusted demand. Ranking and median thresholds summarize the selected population and change with filters. Recommendations support further investigation and controlled trials, not causal conclusions or automatic menu deletion.

## Conclusion

The completed case study demonstrates product-centric analytics with reproducible revenue computations and consistent reporting. Coffee and Tea account for two-thirds of revenue, product popularity differs from revenue ranking, and 43 of 80 products are needed to reach 80% of revenue. These findings support protecting proven products and reviewing the long tail carefully. Applying the recommendations to Afficionado requires its own transaction and operating data.

## References and live deliverables

Maven Analytics. Coffee Shop Sales. Public-domain educational dataset. Downloaded 12 October 2026. https://mavenanalytics.io/data-playground/coffee-shop-sales

GitHub: https://github.com/mohitkumar9193/afficionado-coffee-analysis  
Dashboard: https://myrmbqv6kjne4hjr2m9vcx.streamlit.app/  
Submission page: https://afficionado-coffee-analysis.vercel.app/

