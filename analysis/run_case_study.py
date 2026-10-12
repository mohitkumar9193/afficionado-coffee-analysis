"""Reproduce the public case study: python analysis/run_case_study.py archive.zip.

Outputs go to data/processed. Original workbook bytes remain unchanged.
"""
import sys
import json
import hashlib
from pathlib import Path
from decimal import Decimal
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.public_data import read_public_archive, SOURCE_URL, SOURCE_PAGE
from src.products import prepare, summarize
from src.categories import category_performance
from src.concentration import concentration
from src.recommendations import evaluate


def run(archive_path, destination):
    content = Path(archive_path).read_bytes()
    frame = read_public_archive(content)
    dates = pd.to_datetime(frame.transaction_date)
    frame['year'] = dates.dt.year.astype(str)
    frame['transaction_date'] = dates.dt.strftime('%Y-%m-%d')
    rows, issues = prepare(frame.to_dict('records'))
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination / 'maven-coffee-transactions.csv', index=False)
    products = summarize(rows)
    categories = category_performance(rows)
    pareto = concentration(rows)
    recommendations = evaluate(rows)
    # Independent integer-cent pandas controls, separate from Decimal analytics.
    cents = frame.unit_price.map(lambda x: int(Decimal(x) * 100))
    quantities = frame.transaction_qty.astype(int)
    independent = frame.assign(revenue_cents=cents * quantities, units=quantities)
    assert not issues, 'Inspect exclusions before publishing results'
    assert sum(r['revenue'] for r in rows) * 100 == int(independent.revenue_cents.sum())
    assert sum(r['units'] for r in rows) == int(quantities.sum())
    controls = independent.groupby('product_id').agg(revenue_cents=('revenue_cents','sum'),units=('units','sum'))
    for p in products:
        assert round(p['revenue'] * 100) == int(controls.loc[p['product_id'], 'revenue_cents'])
        assert p['units_sold'] == int(controls.loc[p['product_id'], 'units'])
    for key, summary in categories.items():
        assert round(sum(r['revenue'] for r in summary) * 100) == int(independent.revenue_cents.sum()), key
    assert not any(p['metadata_conflict'] for p in products)
    for name, values in {'products':products, **categories, 'pareto':pareto['products'],
                         'recommendations':recommendations['recommendations']}.items():
        pd.DataFrame(values).to_csv(destination / f'{name}.csv', index=False)
    result = {
        'source_page': SOURCE_PAGE, 'source_url': SOURCE_URL,
        'archive_sha256': hashlib.sha256(content).hexdigest(),
        'records':len(frame), 'source_columns':len(frame.columns)-1,
        'start':str(dates.min().date()), 'end':str(dates.max().date()),
        'missing_cells':int(frame.replace('',pd.NA).isna().sum().sum()),
        'duplicate_rows':int(frame.duplicated().sum()),
        'duplicate_transaction_ids':int(frame.transaction_id.duplicated().sum()),
        'excluded_rows':len(issues), 'quantity_range':[int(quantities.min()),int(quantities.max())],
        'price_range':[float(frame.unit_price.astype(float).min()),float(frame.unit_price.astype(float).max())],
        'product_count':len(products), 'category_count':len(categories['categories']),
        'type_count':len(categories['types']), 'store_count':len(categories['stores']),
        'kpis':recommendations['kpis'], 'concentration':pareto['metrics'],
        'top_revenue':products[:10],
        'top_volume':sorted(products,key=lambda p:(-p['units_sold'],p['product_id']))[:10],
        'bottom_volume':sorted(products,key=lambda p:(p['units_sold'],p['product_id']))[:10],
        'categories':categories['categories'], 'stores':categories['stores'],
        'types':categories['types'], 'store_categories':categories['store_categories'],
        'recommendations':recommendations['recommendations'],
        'verification':'Decimal totals and every product reconciled to independent integer-cent pandas controls; all dimension totals reconcile.'
    }
    (destination/'case-study-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


if __name__ == '__main__':
    result = run(sys.argv[1],Path(__file__).resolve().parents[1]/'data/processed')
    print(json.dumps({k:result[k] for k in ['records','start','end','product_count','category_count','type_count','kpis','concentration','quantity_range','price_range']},indent=2))

