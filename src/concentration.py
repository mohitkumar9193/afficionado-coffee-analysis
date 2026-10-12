"""Pareto concentration using exact Decimal transaction revenue."""
from collections import defaultdict
from decimal import Decimal
from math import ceil


def concentration(rows, top_n=10):
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
        raise ValueError('Top N must be a positive integer')
    revenue = defaultdict(lambda: Decimal(0))
    details = defaultdict(set)
    for row in rows:
        revenue[row['product_id']] += row['revenue']
        details[row['product_id']].add(row['product_detail'])
    ordered = sorted(revenue, key=lambda pid: (-revenue[pid], pid))
    total = sum(revenue.values(), Decimal(0))
    if not ordered or total <= 0:
        return {'products': [], 'metrics': {}}
    cumulative = Decimal(0)
    cutoff = None
    table = []
    for position, pid in enumerate(ordered, 1):
        cumulative += revenue[pid]
        if cutoff is None and cumulative >= total * Decimal('0.8'):
            cutoff = position
        table.append({'product_id': pid, 'product_detail': ' / '.join(sorted(details[pid])),
                      'revenue_order': position, 'revenue': float(revenue[pid]),
                      'revenue_share_pct': float(revenue[pid] / total * 100),
                      'cumulative_revenue_pct': float(cumulative / total * 100),
                      'cumulative_product_pct': position / len(ordered) * 100})
    cutoff = cutoff or len(ordered)
    for product in table:
        product['segment'] = 'Revenue anchor' if product['revenue_order'] <= cutoff else 'Long tail'
    anchor_revenue = sum((revenue[pid] for pid in ordered[:cutoff]), Decimal(0))
    twenty_count = ceil(len(ordered) * 0.2)
    effective_n = min(top_n, len(ordered))
    metrics = {
        'product_count': len(ordered), 'products_to_80': cutoff,
        'products_to_80_pct': cutoff / len(ordered) * 100,
        'anchor_revenue_pct': float(anchor_revenue / total * 100),
        'tail_product_count': len(ordered) - cutoff,
        'tail_revenue_pct': float((total - anchor_revenue) / total * 100),
        'top_n': effective_n,
        'top_n_revenue_pct': float(sum((revenue[p] for p in ordered[:effective_n]), Decimal(0)) / total * 100),
        'top_20_product_count': twenty_count,
        'top_20_revenue_pct': float(sum((revenue[p] for p in ordered[:twenty_count]), Decimal(0)) / total * 100),
        'boundary_tie': cutoff < len(ordered) and revenue[ordered[cutoff - 1]] == revenue[ordered[cutoff]],
    }
    return {'products': table, 'metrics': metrics}
