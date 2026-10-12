# Executive summary

Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters  
Public dataset case study | Prepared for government stakeholders | 12 October 2026

## Purpose and evidence

Retailers need to understand which products sell frequently, which contribute most revenue, and whether a small part of the menu carries the business. This project provides an interactive dashboard and a reproducible analysis to support those decisions.

No actual Afficionado transaction records were available. The completed study uses the public Maven Analytics dataset for Maven Roasters, a fictional coffee business. It contains 149,116 records from three New York City stores covering January–June 2023. These findings illustrate the analytical method and must not be presented as actual Afficionado sales or 2025 results.

## Key findings

The dataset records 214,470 units and 698,812.33 in computed sales revenue across 80 products. Currency is not explicitly specified in the worksheet. All records passed the defined validation rules; no missing cells, duplicate rows or invalid prices/quantities were found.

Coffee supplies 38.63% of revenue and Tea 28.11%, together 66.74%. Maintaining availability in these categories deserves attention. Revenue is spread evenly across the three stores, with each contributing roughly one-third.

The leading revenue product, Sustainably Grown Organic Lg, generates 21,151.75, or 3.03% of total revenue. Earl Grey Rg leads sales volume at 4,708 units but ranks 26th in revenue, showing why volume and revenue should be examined together. Packaged Dark chocolate has the lowest recorded volume, at 118 units, and revenue of 755.20. Similar product names refer to different IDs and formats.

The top ten products generate 25.38% of revenue. Reaching 80% requires 43 of the 80 products. The top fifth of the menu generates 37.10%, so this case does not follow an 80/20 pattern. The remaining 37 products still contribute 19.48%, making broad menu cuts premature.

## Recommended actions

Protect availability and clear menu visibility for a small selection of proven high-volume, high-revenue products. Check margins, supply reliability and preparation capacity before expanding them.

Review popular lower-price products in the context of customer choice and complementary purchases. Use small promotion trials for appropriate premium products rather than assuming higher price means higher profitability.

Investigate low-volume products by checking stock availability, shelf life, costs and customer feedback. Trial better placement or redesign before removal. Compare store product mix using consistent periods and normalized shares.

For use at Afficionado, obtain its actual transactions, full menu and cost data. Measure trial outcomes against a baseline or comparison store. Track units, revenue, margin, stockouts and service time.

## Expected benefits and limits

The approach can help managers make more transparent merchandising decisions and prioritize further investigation. It also provides a practical example of data skills for small-business support programmes. Revenue uplift, profit improvement, reduced waste and faster service remain potential benefits, not measured outcomes.

The dataset has no costs, customer identifiers, availability measures or service times. It cannot support funding decisions, a forecast of financial gains or claims about actual Afficionado performance. Government stakeholders should evaluate evidence and local applicability before supporting an operational rollout.

## Deliverables

The project includes a research paper, this summary, reproducible analysis and a Streamlit dashboard with filters, rankings, category comparisons and revenue concentration charts. The public case study is clearly labelled, and supplied CSV/Excel data can replace it.

Source: [Maven Analytics Coffee Shop Sales](https://mavenanalytics.io/data-playground/coffee-shop-sales), Public Domain.

Dashboard: https://myrmbqv6kjne4hjr2m9vcx.streamlit.app/  
Repository: https://github.com/mohitkumar9193/afficionado-coffee-analysis

