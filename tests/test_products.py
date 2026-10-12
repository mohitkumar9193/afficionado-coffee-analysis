import unittest
from decimal import Decimal
from src.products import prepare, summarize


def record(pid, quantity, price):
    return dict(product_id=pid, product_detail='Product '+pid, product_category='Coffee',
                product_type='Brew', store_location='A', transaction_qty=quantity, unit_price=price)


class ProductTests(unittest.TestCase):
    def test_revenue_units_rank_and_denominator(self):
        source = [record('A', '10', '1.10'), record('A', '5', '1.10'), record('B', '2', '20'), record('C', '2', '20')]
        clean, issues = prepare(source)
        self.assertEqual(issues, [])
        self.assertEqual(sum(r['revenue'] for r in clean), Decimal('96.50'))
        products = {r['product_id']: r for r in summarize(clean)}
        self.assertEqual(products['A']['units_sold'], 15)
        self.assertEqual(products['A']['rank_gap'], 2)
        self.assertEqual(products['B']['revenue_rank'], 1)
        self.assertEqual(products['C']['volume_rank'], 2)
        self.assertAlmostEqual(sum(p['revenue_share_pct'] for p in products.values()), 100)
        self.assertNotIn('revenue', source[0])

    def test_invalid_nonfinite_and_fractional_values(self):
        clean, issues = prepare([record('A', q, p) for q, p in [('0','2'), ('-1','2'), ('1.5','2'), ('NaN','2'), ('1','Infinity'), ('1','bad'), ('1','0')]])
        self.assertEqual(clean, [])
        self.assertEqual(len(issues), 7)

    def test_empty_and_conflicting_metadata(self):
        self.assertEqual(summarize([]), [])
        records = [record('A','1','2'), record('A','1','3')]
        records[1]['product_detail'] = 'Alternate'
        clean, _ = prepare(records)
        product = summarize(clean)[0]
        self.assertTrue(product['metadata_conflict'])
        self.assertEqual(product['average_selling_price'], 2.5)


if __name__ == '__main__':
    unittest.main()
