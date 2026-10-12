"""Category, nested product-type, and store performance from validated rows."""
from collections import defaultdict
from decimal import Decimal


def aggregate(rows, dimensions, parent_dimensions=()):
    """Shares use filtered scope and, separately, the specified parent scope."""
    groups = defaultdict(list)
    parents = defaultdict(lambda: {'revenue': Decimal(0), 'units': 0})
    total_revenue = sum((r['revenue'] for r in rows), Decimal(0))
    total_units = sum(r['units'] for r in rows)
    for row in rows:
        groups[tuple(row[d] for d in dimensions)].append(row)
        parent = parents[tuple(row[d] for d in parent_dimensions)]
        parent['revenue'] += row['revenue']
        parent['units'] += row['units']
    result = []
    for key, members in groups.items():
        labels = dict(zip(dimensions, key))
        revenue = sum((r['revenue'] for r in members), Decimal(0))
        units = sum(r['units'] for r in members)
        parent = parents[tuple(members[0][d] for d in parent_dimensions)]
        result.append({
            **labels, 'revenue': float(revenue), 'units_sold': units,
            'products_sold': len({r['product_id'] for r in members}),
            'revenue_share_pct': float(revenue / total_revenue * 100) if total_revenue else 0.0,
            'unit_share_pct': units / total_units * 100 if total_units else 0.0,
            'parent_revenue_share_pct': float(revenue / parent['revenue'] * 100) if parent['revenue'] else 0.0,
            'parent_unit_share_pct': units / parent['units'] * 100 if parent['units'] else 0.0,
            'average_selling_price': float(revenue / units) if units else 0.0,
        })
    return sorted(result, key=lambda r: (-r['revenue'], tuple(r[d] for d in dimensions)))


def category_performance(rows):
    return {
        'categories': aggregate(rows, ('product_category',)),
        'types': aggregate(rows, ('product_category', 'product_type'), ('product_category',)),
        'stores': aggregate(rows, ('store_location',)),
        'store_categories': aggregate(rows, ('store_location', 'product_category'), ('store_location',)),
        'store_types': aggregate(rows, ('store_location', 'product_category', 'product_type'), ('store_location', 'product_category')),
    }
