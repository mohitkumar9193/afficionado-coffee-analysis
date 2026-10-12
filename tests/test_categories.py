import unittest
from src.products import prepare
from src.categories import category_performance


class CategoryTests(unittest.TestCase):
    def fixture(self):
        specs = [('A','Coffee','Brew',2,5), ('A','Tea','Brew',1,10),
                 ('B','Coffee','Brew',1,20), ('B','Coffee','Espresso',2,5)]
        rows = [dict(product_id=str(i), product_detail='Item', store_location=s,
                     product_category=c, product_type=t, transaction_qty=str(q), unit_price=str(p))
                for i,(s,c,t,q,p) in enumerate(specs)]
        return prepare(rows)[0]

    def test_reconciliation_and_category_denominators(self):
        result = category_performance(self.fixture())
        categories = {r['product_category']: r for r in result['categories']}
        self.assertEqual(categories['Coffee']['revenue'], 40)
        self.assertEqual(categories['Coffee']['revenue_share_pct'], 80)
        self.assertEqual(sum(r['units_sold'] for r in result['categories']), 6)
        self.assertAlmostEqual(sum(r['revenue_share_pct'] for r in result['categories']), 100)
        coffee_types = [r for r in result['types'] if r['product_category'] == 'Coffee']
        self.assertAlmostEqual(sum(r['parent_revenue_share_pct'] for r in coffee_types), 100)
        brew = next(r for r in coffee_types if r['product_type'] == 'Brew')
        self.assertEqual(brew['parent_revenue_share_pct'], 75)
        self.assertEqual(brew['revenue_share_pct'], 60)
        self.assertEqual(len(result['types']), 3)  # Same type name in separate categories stays separate.

    def test_store_mix_and_filtered_denominators(self):
        rows = self.fixture()
        result = category_performance(rows)
        for store in ('A', 'B'):
            mix = [r for r in result['store_categories'] if r['store_location'] == store]
            self.assertAlmostEqual(sum(r['parent_revenue_share_pct'] for r in mix), 100)
            self.assertAlmostEqual(sum(r['parent_unit_share_pct'] for r in mix), 100)
        filtered = category_performance([r for r in rows if r['store_location'] == 'A'])
        self.assertEqual(len(filtered['stores']), 1)
        self.assertTrue(all(r['revenue_share_pct'] == 50 for r in filtered['categories']))
        for store_type in result['store_types']:
            siblings = [r for r in result['store_types'] if (r['store_location'],r['product_category']) == (store_type['store_location'],store_type['product_category'])]
            self.assertAlmostEqual(sum(r['parent_revenue_share_pct'] for r in siblings), 100)

    def test_empty(self):
        self.assertTrue(all(not rows for rows in category_performance([]).values()))


if __name__ == '__main__':
    unittest.main()
