"""Synthetic demonstration records, never empirical project evidence."""


def demo_records():
    specs = [
        ('DEMO-01', 'Example house coffee', 'Coffee', 'Brewed', 'Example store A', 100, 3),
        ('DEMO-01', 'Example house coffee', 'Coffee', 'Brewed', 'Example store B', 80, 3),
        ('DEMO-02', 'Example latte', 'Coffee', 'Espresso drink', 'Example store A', 65, 5),
        ('DEMO-02', 'Example latte', 'Coffee', 'Espresso drink', 'Example store B', 70, 5),
        ('DEMO-03', 'Example green tea', 'Tea', 'Green', 'Example store A', 30, 4),
        ('DEMO-03', 'Example green tea', 'Tea', 'Green', 'Example store B', 15, 4),
        ('DEMO-04', 'Example premium beans', 'Coffee', 'Packaged beans', 'Example store A', 8, 25),
        ('DEMO-05', 'Example cocoa', 'Chocolate', 'Hot chocolate', 'Example store B', 12, 5),
        ('DEMO-06', 'Example specialty tea', 'Tea', 'Specialty', 'Example store A', 2, 6),
    ]
    return [dict(product_id=pid, product_detail=detail, product_category=category,
                 product_type=kind, store_location=store, transaction_qty=str(qty), unit_price=str(price))
            for pid, detail, category, kind, store, qty, price in specs]

