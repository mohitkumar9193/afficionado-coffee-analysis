import unittest
from decimal import Decimal
from src.concentration import concentration


def rows(values):
    return [{'product_id': str(i), 'product_detail': 'Item', 'revenue': Decimal(str(value))}
            for i, value in enumerate(values)]


class ConcentrationTests(unittest.TestCase):
    def test_exact_boundary_and_reconciliation(self):
        result = concentration(rows([60, 20, 10, 10]), 1)
        metrics = result['metrics']
        self.assertEqual(metrics['products_to_80'], 2)
        self.assertEqual(metrics['anchor_revenue_pct'], 80)
        self.assertEqual(metrics['tail_revenue_pct'], 20)
        self.assertEqual(metrics['top_n_revenue_pct'], 60)
        self.assertEqual(result['products'][-1]['cumulative_revenue_pct'], 100)

    def test_crossing_product_included(self):
        metrics = concentration(rows([70, 15, 10, 5]), 99)['metrics']
        self.assertEqual(metrics['products_to_80'], 2)
        self.assertEqual(metrics['anchor_revenue_pct'], 85)
        self.assertEqual(metrics['top_n'], 4)
        self.assertEqual(metrics['top_n_revenue_pct'], 100)

    def test_uniform_ties_and_small_population(self):
        metrics = concentration(rows([1]*6))['metrics']
        self.assertEqual(metrics['products_to_80'], 5)
        self.assertTrue(metrics['boundary_tie'])
        self.assertEqual(metrics['top_20_product_count'], 2)
        single = concentration(rows([Decimal('0.1')]))['metrics']
        self.assertEqual(single['products_to_80'], 1)
        self.assertEqual(single['tail_product_count'], 0)

    def test_empty_and_repeat_product(self):
        self.assertEqual(concentration([])['products'], [])
        repeated = rows([1, 2])
        repeated[1]['product_id'] = '0'
        self.assertEqual(concentration(repeated)['metrics']['product_count'], 1)
        with self.assertRaises(ValueError):
            concentration([], 0)


if __name__ == '__main__':
    unittest.main()
