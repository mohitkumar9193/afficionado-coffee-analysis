"""Transparent revenue-based KPI and product review rules."""
from decimal import Decimal
from statistics import median
from src.products import summarize
from src.categories import category_performance
from src.concentration import concentration

FORMULAS = [
    {'KPI': 'Product Revenue Contribution (%)', 'Formula': 'Product revenue / total filtered revenue × 100', 'Scope': 'Each observed product'},
    {'KPI': 'Product Sales Volume', 'Formula': 'Sum of transaction_qty for the product', 'Scope': 'Each observed product'},
    {'KPI': 'Category Revenue Share (%)', 'Formula': 'Category revenue / total filtered revenue × 100', 'Scope': 'Each observed category'},
    {'KPI': 'Revenue Concentration Ratio (CR-N %)', 'Formula': 'Revenue of top N products / total filtered revenue × 100', 'Scope': 'Full filtered observed menu; N from slider'},
    {'KPI': 'Product Efficiency Score (revenue per SKU)', 'Formula': 'Total filtered revenue / distinct sold product IDs', 'Scope': 'Filtered observed menu; currency per SKU, not profit or operating efficiency'},
]


def evaluate(rows, top_n=10):
    products = summarize(rows)
    concentration_result = concentration(rows, top_n)
    revenue = sum((r['revenue'] for r in rows), Decimal(0))
    if not products:
        return {'kpis': {}, 'recommendations': [], 'formulas': FORMULAS}
    categories = category_performance(rows)['categories']
    kpis = {
        'total_revenue': float(revenue),
        'total_units': sum(r['units'] for r in rows),
        'revenue_per_sku': float(revenue / len(products)),
        'largest_category_share_pct': categories[0]['revenue_share_pct'],
        'concentration_ratio_pct': concentration_result['metrics']['top_n_revenue_pct'],
    }
    median_units = median(p['units_sold'] for p in products)
    median_revenue = median(p['revenue'] for p in products)
    median_price = median(p['average_selling_price'] for p in products)
    anchors = {p['product_id'] for p in concentration_result['products'] if p['segment'] == 'Revenue anchor'}
    result = []
    for product in products:
        units, sales = product['units_sold'], product['revenue']
        if product['metadata_conflict']:
            label, action = 'Data review', 'Resolve conflicting product labels before merchandising decisions.'
        elif len(products) < 3:
            label, action = 'Insufficient comparison scope', 'Broaden the selection before applying comparative product rules.'
        elif product['product_id'] in anchors and units > median_units and sales > median_revenue:
            label, action = 'Hero candidate', 'Prioritize availability and menu visibility; check margin and capacity before expansion.'
        elif units < median_units and product['average_selling_price'] > median_price and sales >= median_revenue:
            label, action = 'Promotion candidate', 'Trial focused merchandising or sampling; measure unit lift and margin before scaling.'
        elif units > median_units and product['rank_gap'] > 0:
            label, action = 'Revenue yield review', 'Review pricing, mix, and complementary purchases; preserve the product’s demonstrated popularity.'
        elif product['product_id'] not in anchors and units < median_units and sales < median_revenue:
            label, action = 'Review or redesign candidate', 'Check availability, menu role, cost, and customer feedback; trial redesign before any removal decision.'
        else:
            label, action = 'Monitor', 'Track performance; current screening rules do not support a targeted action.'
        result.append({**product, 'recommendation': label, 'suggested_action': action,
                       'evidence': f"Units {units}; revenue {sales:.2f}; share {product['revenue_share_pct']:.2f}%; volume rank {product['volume_rank']}; revenue rank {product['revenue_rank']}",
                       'median_product_units': median_units, 'median_product_revenue': median_revenue,
                       'median_product_selling_price': median_price,
                       'revenue_anchor': product['product_id'] in anchors})
    return {'kpis': kpis, 'recommendations': result, 'formulas': FORMULAS}
