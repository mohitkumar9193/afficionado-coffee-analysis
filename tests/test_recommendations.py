import unittest
from src.products import prepare
from src.recommendations import evaluate


def fixture():
    specs = [('hero',100,10), ('yield',90,1), ('premium',5,30), ('tail',1,1), ('middle',20,5)]
    rows = [dict(product_id=pid, product_detail=pid, product_category='Coffee', product_type='Brew',
                 store_location='A', transaction_qty=str(q), unit_price=str(p)) for pid,q,p in specs]
    return prepare(rows)[0]


class RecommendationTests(unittest.TestCase):
    def test_rules_and_kpis(self):
        result = evaluate(fixture(), 1)
        labels = {p['product_id']: p['recommendation'] for p in result['recommendations']}
        self.assertEqual(labels['hero'], 'Hero candidate')
        self.assertEqual(labels['premium'], 'Promotion candidate')
        self.assertEqual(labels['yield'], 'Revenue yield review')
        self.assertEqual(labels['tail'], 'Review or redesign candidate')
        self.assertEqual(labels['middle'], 'Monitor')
        self.assertEqual(result['kpis']['total_revenue'], 1341)
        self.assertEqual(result['kpis']['revenue_per_sku'], 1341/5)
        self.assertAlmostEqual(result['kpis']['concentration_ratio_pct'], 1000/1341*100)
        self.assertEqual(len(result['formulas']), 5)

    def test_equal_products_and_small_scope_do_not_create_heroes(self):
        one = fixture()[:1]
        self.assertEqual(evaluate(one)['recommendations'][0]['recommendation'], 'Insufficient comparison scope')
        equal = [dict(one[0], product_id=str(i)) for i in range(4)]
        self.assertTrue(all(p['recommendation'] == 'Monitor' for p in evaluate(equal)['recommendations']))

    def test_metadata_review_overrides_action(self):
        rows = fixture()
        rows.append(dict(rows[0], product_detail='Conflicting label'))
        hero = next(p for p in evaluate(rows)['recommendations'] if p['product_id'] == 'hero')
        self.assertEqual(hero['recommendation'], 'Data review')
        self.assertEqual(evaluate([])['kpis'], {})


if __name__ == '__main__':
    unittest.main()
