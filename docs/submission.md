# Submission package and verification

## Verified repository

https://github.com/mohitkumar9193/afficionado-coffee-analysis

The project code, dashboard, tests, methodology guides, research paper, executive summary, and Vercel companion page have been uploaded. No private transaction data or virtual environment is included.

## Deliverables

- Research paper: reports/research/research-paper.md
- Executive summary: reports/executive/executive-summary.md
- Streamlit dashboard: dashboard/app.py
- Vercel companion page: website/index.html

The Markdown reports are readable on GitHub and available for download from the companion page. The paper's empirical findings remain pending the transaction dataset; no invented sales results are included. Word/PDF layout conversion was unavailable and those formats are not included as verified deliverables.

## Verification

All 18 tests pass: 13 analytical checks and five Streamlit application checks. Checks cover CSV/XLSX ingestion, every dashboard view, filtered totals, invalid schema, empty scope, single-product views, reset filters, ranking ties, contribution reconciliation, nested category/store denominators, Pareto thresholds, and recommendation rules. Tests use synthetic data solely for verification. Direct dependencies are pinned and package compatibility is checked separately.

The local Streamlit server started successfully and returned HTTP 200. The empty state was inspected in the browser. Browser file chooser automation did not complete. A clearly labelled synthetic demo mode was added, and populated ranking, category, and Pareto charts were visually inspected. Remaining views passed automated interaction tests; real-data visual QA is pending. Automated application checks did exercise those views. GitHub Actions is configured; no successful remote workflow run is claimed.

## Hosting actions pending

Vercel's existing GitHub integration does not currently include this repository. Grant access specifically to afficionado-coffee-analysis, then import it with Root Directory website and framework Other. No build command is needed; serve the root of that directory.

Streamlit Community Cloud currently requires sign-in and acceptance of its terms. After signing in, deploy from the repository, branch main, app path dashboard/app.py, Python 3.12. No data needs to be publicly bundled because the app accepts uploads.

Live Vercel and Streamlit URLs are pending these account actions. A localhost address is not a public submission link.

## Before final internship submission

Supply and validate the actual dataset, update the reports with measured findings, complete visual QA on populated charts, verify the cloud URLs and report downloads, and confirm accepted document formats with the internship evaluator. The current package is an implemented analytics application and methodological report, not a completed empirical study.

