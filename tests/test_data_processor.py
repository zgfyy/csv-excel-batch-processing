import unittest
import pandas as pd
from src.data_processor import load_data, clean_and_transform_with_rules, merge_dataframes

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        # 准备测试数据
        self.test_csv_file = 'tests/data/test.csv'
        self.test_excel_file = 'tests/data/test.xlsx'
        self.test_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'price': [100.5, 200.75, 300.0]
        })

    def test_load_data_csv(self):
        df = load_data(self.test_csv_file)
        self.assertEqual(len(df), 3)

    def test_load_data_excel(self):
        df = load_data(self.test_excel_file)
        self.assertEqual(len(df), 3)

    def test_clean_and_transform_with_rules(self):
        df = clean_and_transform_with_rules(self.test_df, custom_rules=[
            {'column': 'age', 'operation': 'dropna'},
            {'column': 'price', 'operation': 'convert_type', 'type': 'int'}
        ])
        self.assertEqual(len(df), 3)
        self.assertTrue(all(isinstance(x, int) for x in df['price']))

    def test_merge_dataframes(self):
        df1 = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
        df2 = pd.DataFrame({'id': [2, 3], 'age': [30, 35]})
        merged_df = merge_dataframes([df1, df2], key_columns=['id'])
        self.assertEqual(len(merged_df), 3)
        self.assertIn('name', merged_df.columns)
        self.assertIn('age', merged_df.columns)

if __name__ == '__main__':
    unittest.main()