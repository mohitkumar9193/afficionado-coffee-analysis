# Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters

An internship project examining product popularity, revenue contribution, category dependency, and menu concentration.

## Status

Project structure, analytics modules, and the Streamlit dashboard are implemented. All 18 calculation and Streamlit interaction tests pass. Real-data validation and findings, final real-data visual QA is pending. Streamlit and Vercel are deployed. Research paper and executive summary are included. See docs/step-9.md for launch instructions.

## Project structure

```text
data/raw/              Original dataset (kept unchanged and excluded from Git)
data/processed/        Cleaned data and aggregates (excluded from Git)
analysis/              EDA scripts or notebooks
src/                   Shared validation, metrics, and aggregation logic
dashboard/             Streamlit application; entrypoint: dashboard/app.py
reports/figures/       Verified charts for written deliverables
reports/research/      Research paper source
reports/executive/     Executive summary source
website/               Vercel companion submission page
docs/                  Requirements, methodology, and deployment guidance
tests/                 Meaningful calculation and interaction checks
```

## Delivery approach

- GitHub: one repository named `afficionado-coffee-analysis` for code and documentation.
- Streamlit Community Cloud: required interactive dashboard, deployed from the same repository.
- Vercel: companion submission page with dashboard and report links. Its root directory will be `website`.

The Vercel page is a companion to the Streamlit app. It does not replace the required analytics dashboard. See `docs/deployment.md`.

## Planned analytics stack

Python 3.12, pandas, Streamlit, Plotly, and openpyxl for Excel ingestion. Tested direct dependency versions are pinned in requirements.txt. See docs/step-9.md for local setup and launch commands.

## Data and interpretation

Revenue = transaction_qty × unit_price. Profitability cannot be calculated without cost or margin data. The meaning of `Balance`, currency, dataset coverage, and transaction granularity must be verified during inspection.

Raw and processed transaction files are excluded from Git by default. A deployable data strategy will be selected after inspecting the supplied dataset and its sharing permissions.

## Required deliverables

1. Research paper covering EDA, insights, recommendations, and limitations.
2. Interactive Streamlit dashboard.
3. Executive summary for government stakeholders.
4. GitHub repository and Vercel companion page for the requested submission workflow.

## Next step

Supply the actual CSV or Excel dataset and begin Step 2: dataset inspection.

## Run the dashboard

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

Upload CSV or XLSX data. The app starts with an empty state until a file is uploaded. Required analysis fields are product_id, product_detail, product_category, product_type, store_location, transaction_qty, and unit_price. Keep product IDs as text, including leading zeros.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests use synthetic fixtures solely for verification. Actual business findings require the transaction dataset. Automated GitHub Actions checks are configured for Python 3.12.

## Submission documents

- [Research paper](reports/research/research-paper.md)
- [Executive summary](reports/executive/executive-summary.md)
- [Deployment plan](docs/deployment.md)
- [Dashboard guide](docs/step-9.md)

## Cloud setup

Streamlit Community Cloud: select this repository, main branch, and dashboard/app.py; choose Python 3.12.
Vercel: import this repository, set Root Directory to website, choose Other framework, and leave the build command empty. Serve website directly as the static output.

Reports currently document methods and verified implementation progress. Empirical findings, profitability claims, and quantitative benefit estimates are pending source data.

## Demonstration mode

Select Explore synthetic demonstration data to preview populated charts without a file. All demo records and results are visibly labelled synthetic and are not retailer findings. Turn it off to analyze uploaded transaction data.

## Live dashboard

https://myrmbqv6kjne4hjr2m9vcx.streamlit.app/

The app is deployed and accepts uploads. Synthetic demonstration mode is optional and visibly labelled. Actual retailer findings remain pending the transaction dataset.

## Live submission page

https://afficionado-coffee-analysis.vercel.app/

