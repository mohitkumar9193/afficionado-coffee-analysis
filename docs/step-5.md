# Step 5: product popularity and revenue contribution

Implemented reusable validation and product aggregation in src/products.py, with an upload-driven Streamlit interface in dashboard/app.py.

## Run locally

From the project folder, with Python 3.12 or another dependency-supported version:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

Dependencies use bounded ranges pending full runtime validation and a reproducible lock during deployment preparation.

Upload CSV or XLSX data. For Excel, choose the worksheet. Currency is intentionally unspecified until confirmed from source documentation.

## Implemented analysis

Products are grouped by product_id. Units and transaction revenue are summed, and product revenue is divided by the full filtered scope revenue. Volume and revenue use competition ranks, so ties share ranks. Positive rank gap = revenue rank minus volume rank, indicating better volume than revenue position.

High popularity / weaker revenue ranking uses units at or above the product median and a positive rank gap. Premium low-volume screening uses weighted average selling price above the median and units below the median. These screens are exploratory, not evidence of profitability or grounds for immediate menu removal.

Invalid rows are excluded with a downloadable reason log. Duplicate records are retained pending transaction granularity review. Product metadata conflicts are flagged. Original uploaded files are not modified or written to disk. Sales-row counts are not transaction frequency. Absent products cannot be described as zero-selling without a menu catalog.

## Verification and limitations

Core tests use synthetic fixtures exclusively to verify exact revenue arithmetic, aggregation, ties, denominator reconciliation, invalid numeric values, empty input, and metadata conflict handling. Fixture values are not business findings. Real-data conclusions remain pending the supplied dataset. UI runtime checks require the Streamlit and chart dependencies.

