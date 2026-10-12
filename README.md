# Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters

Completed public-data internship case study with an interactive dashboard, reproducible analysis, research paper and executive summary.

## Source and scope

No actual Afficionado dataset was supplied. Results use the public Maven Analytics Coffee Shop Sales dataset for **Maven Roasters, a fictional business**, covering January–June 2023. Findings are educational case-study results, not actual Afficionado or 2025 sales. The publisher labels the dataset Public Domain.

Source: https://mavenanalytics.io/data-playground/coffee-shop-sales

The original has 149,116 rows and 11 columns. The prepared data preserves all rows and adds year derived from transaction_date. Balance is absent and is not invented. No missing cells, duplicates, invalid quantities/prices or conflicting product metadata were found. See data/public/README.md for attribution and checksums.

## Verified findings

| Measure | Result |
| --- | --- |
| Computed revenue | 698,812.33 source price units |
| Units sold | 214,470 |
| Products / categories / types / stores | 80 / 9 / 29 / 3 |
| Coffee / Tea revenue share | 38.63% / 28.11% |
| Top ten product revenue share | 25.38% |
| Products needed for 80% revenue | 43 (53.75%) |
| Revenue per sold SKU | 8,735.15 |

Revenue equals quantity × price, not profit. The worksheet does not explicitly declare currency.

## Live deliverables

- Dashboard: https://myrmbqv6kjne4hjr2m9vcx.streamlit.app/
- Vercel page: https://afficionado-coffee-analysis.vercel.app/
- Research paper: reports/research/research-paper.md
- Executive summary: reports/executive/executive-summary.md

The dashboard defaults to the clearly credited public case study. It supports CSV/XLSX uploads, a separately disclosed synthetic demo, store/category/type filters, Top-N rankings, category comparisons, scatter plots, Pareto analysis, recommendations and product drill-downs. Vercel serves website/; Streamlit runs dashboard/app.py using Python 3.12.

## Setup and reproduction

```sh
pip install -r requirements.txt
python -m streamlit run dashboard/app.py
python analysis/run_case_study.py path/to/publisher-archive.zip
python -m unittest discover -s tests -v
```

Run from the repository root using Python 3.12. Direct dependencies are pinned. The analysis runner validates the source checksum, writes summaries to data/processed and reconciles Decimal revenue against independent integer-cent controls for the total and every product. Category, type, store and nested totals also reconcile. All 18 unit/application tests pass. An additional full-source application check verifies every view and the Astoria filter. Remote CI success is not assumed from local verification.

## Structure

analysis/ contains the reproducible runner. data/public/ contains the licensed bundled CSV gzip and attribution. src/ contains validation and analytical logic. dashboard/ contains Streamlit. reports/ contains finalized documents and verified result evidence. website/ contains the Vercel page and report downloads. docs/ contains methodology and submission guidance. tests/ contains analytical and application checks.

Private originals and regenerated data/processed outputs are excluded from Git. The public case study is bundled for fast startup and verified by checksum; the original publisher archive is a fallback. Private uploads are analyzed in the active session and are not saved to the repository.

## Limitations and submission

Costs, customer IDs, stock availability, complete unsold menu and service times are absent. Recommendation flags support investigation, not automatic removal. Actual Afficionado conclusions require its company data. Confirm internship acceptance of a public educational case study and the supplied Markdown report format. See docs/submission.md.

