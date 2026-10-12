# Streamlit dashboard guide

## Local launch

Open PowerShell in the afficionado-coffee-analysis project folder. Install Python 3.12 if needed, then:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501. Upload the actual CSV or XLSX file in the sidebar; choose a worksheet for Excel.

## Dashboard views

- Products: KPI cards, highest and lowest product rankings, popularity/revenue scatter, full product summary, and exploratory review tables.
- Categories & stores: category revenue distribution, nested product-type contribution, store mix charts and heatmap.
- Pareto & menu balance: cumulative revenue curve, 80% threshold, revenue anchor set, long tail, and Top-N concentration ratio.
- Recommendations: all five KPI formulas, revenue per SKU, evidence-backed product action screens, and removal limitations.
- Product drill-down: product-specific units, revenue, overall contribution, selling price, ranks, store performance, action suggestion, and source rows.

Store, category, and product-type filters cascade. Empty selections show a message rather than zero-valued business conclusions. Top-N changes ranking length and concentration ratio, while revenue shares retain the full filtered scope denominator. Single-product selections remain supported.

## Data handling

Accepts CSV/XLSX up to 50 MB. Analysis requires product_id, product_detail, product_category, product_type, store_location, transaction_qty, and unit_price. Other expected brief columns are retained when supplied. Invalid rows have a reason log; original uploads are not overwritten. No dataset is bundled and no fictional business results are presented.

CSV exports are available for product, category, type, store, Pareto, recommendation, validation, and drill-down summaries. Currency must be verified from source documentation. Costs and menu completeness remain necessary for profitability or removal decisions.

## Hosting

Streamlit Community Cloud entrypoint: dashboard/app.py. Repository-root .streamlit/config.toml supplies the theme and upload limit. Vercel remains the companion submission page, to be built/published in the final deployment step.

## Validation completed

Installed and pinned Streamlit 1.65.0, pandas 3.0.6, Plotly 6.9.0, and openpyxl 3.1.5 in a local Python 3.12 environment. All 16 tests pass: 13 calculation tests plus three Streamlit AppTest checks covering all five views, CSV input, filtered totals, invalid schema, and empty states. The local server starts and responds with HTTP 200. Visual browser QA and real-data validation remain for the final verification step; Excel worksheet ingestion is implemented but not yet covered by an end-to-end test.
