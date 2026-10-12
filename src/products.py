"""Revenue and popularity analysis, independent of the dashboard runtime."""
from collections import defaultdict
from decimal import Decimal, InvalidOperation

REQUIRED = ('product_id', 'product_detail', 'product_category', 'product_type',
            'store_location', 'transaction_qty', 'unit_price')


def prepare(records):
    """Return valid rows and an exclusion log; never mutate the input."""
    valid, issues = [], []
    for line, original in enumerate(records, start=2):
        row = {str(k).strip().lower(): v for k, v in original.items()}
        reasons = []
        for field in REQUIRED:
            if row.get(field) is None or not str(row[field]).strip():
                reasons.append(f'Missing {field}')
        try:
            qty = Decimal(str(row.get('transaction_qty', '')).strip())
            price = Decimal(str(row.get('unit_price', '')).strip())
            if not qty.is_finite() or qty <= 0 or qty != qty.to_integral_value():
                reasons.append('Quantity must be a finite positive whole number')
            if not price.is_finite() or price <= 0:
                reasons.append('Price must be finite and positive')
        except InvalidOperation:
            reasons.append('Quantity or price is not numeric')
        if reasons:
            issues.append({'source_row': line, 'reason': '; '.join(reasons)})
            continue
        for field in REQUIRED[:5]:
            row[field] = str(row[field]).strip()
        row['units'] = int(qty)
        row['revenue'] = qty * price
        row['price'] = price
        valid.append(row)
    return valid, issues


def summarize(rows):
    """One row per product ID; tied values receive competition ranks."""
    groups = defaultdict(list)
    for row in rows:
        groups[row['product_id']].append(row)
    total = sum((r['revenue'] for r in rows), Decimal(0))
    result = []
    for product_id, items in groups.items():
        units = sum(r['units'] for r in items)
        revenue = sum((r['revenue'] for r in items), Decimal(0))
        labels = {field: sorted({r[field] for r in items}) for field in REQUIRED[1:4]}
        result.append({
            'product_id': product_id,
            **{field: ' / '.join(values) for field, values in labels.items()},
            'metadata_conflict': any(len(values) > 1 for values in labels.values()),
            'units_sold': units, 'revenue': float(revenue),
            'revenue_share_pct': float(revenue / total * 100) if total else 0.0,
            'average_selling_price': float(revenue / units),
            'sales_rows': len(items),
        })
    for row in result:
        row['volume_rank'] = 1 + sum(p['units_sold'] > row['units_sold'] for p in result)
        row['revenue_rank'] = 1 + sum(p['revenue'] > row['revenue'] for p in result)
        row['rank_gap'] = row['revenue_rank'] - row['volume_rank']
    return sorted(result, key=lambda p: (-p['revenue'], p['product_id']))
