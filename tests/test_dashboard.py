"""UI checks with synthetic upload fixtures, never business findings."""
import io
import unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest

CSV = '''product_id,product_detail,product_category,product_type,store_location,transaction_qty,unit_price
1,House brew,Coffee,Brew,A,20,3
2,Espresso,Coffee,Espresso,B,10,4
3,Green tea,Tea,Green,A,5,5
4,Black tea,Tea,Black,B,1,6
'''


class DashboardTests(unittest.TestCase):
    def run_upload(self, content=CSV):
        uploaded = io.BytesIO(content.encode())
        uploaded.name = 'test.csv'
        return patch('streamlit.delta_generator.DeltaGenerator.file_uploader', return_value=uploaded)

    def test_empty_state(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'dashboard/app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(app.info)

    def test_all_views_and_filters(self):
        with self.run_upload():
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'dashboard/app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '131.00')
        for view in ['Categories & stores', 'Pareto & menu balance', 'Recommendations', 'Product drill-down']:
            with self.run_upload():
                app.sidebar.radio[1].set_value(view).run(timeout=30)
            self.assertFalse(app.exception, view)
        with self.run_upload():
            app.sidebar.multiselect[0].set_value(['A']).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '85.00')
        with self.run_upload():
            app.sidebar.multiselect[0].set_value([]).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(app.info)

    def test_invalid_upload(self):
        with self.run_upload('bad,column\n1,2\n'):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'dashboard/app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(app.error)

    def test_excel_single_product_and_filter_reset(self):
        from openpyxl import Workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Transactions'
        sheet.append(['product_id','product_detail','product_category','product_type','store_location','transaction_qty','unit_price'])
        sheet.append(['001','House brew','Coffee','Brew','A',2,3.50])
        uploaded = io.BytesIO()
        workbook.save(uploaded)
        uploaded.seek(0)
        uploaded.name = 'fixture.xlsx'
        with patch('streamlit.delta_generator.DeltaGenerator.file_uploader', return_value=uploaded):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'dashboard/app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '7.00')
        self.assertEqual(app.metric[2].value, '1')
        for view in ['Categories & stores','Pareto & menu balance','Recommendations','Product drill-down']:
            uploaded.seek(0)
            with patch('streamlit.delta_generator.DeltaGenerator.file_uploader', return_value=uploaded):
                app.sidebar.radio[1].set_value(view).run(timeout=30)
            self.assertFalse(app.exception)
        uploaded.seek(0)
        with patch('streamlit.delta_generator.DeltaGenerator.file_uploader', return_value=uploaded):
            app.sidebar.button[0].click().run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.sidebar.multiselect[0].value, ['A'])


if __name__ == '__main__':
    unittest.main()
