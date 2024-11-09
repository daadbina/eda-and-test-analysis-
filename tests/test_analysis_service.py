import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from services.test_analysis_service import TestAnalysisService  # Assuming the service is located here
from controllers.sql_loader import load_sql_queries

class TestAnalysisServiceTestCase(unittest.TestCase):
    @patch('services.test_analysis_service.sqlite3.connect')  # Mocking the database connection
    @patch('controllers.sql_loader.load_sql_queries')  # Mocking the SQL query loading
    def setUp(self, mock_load_sql_queries, mock_connect):
        # Mocking SQL query loading
        mock_load_sql_queries.return_value = {
            'avg_purchase_by_ui_and_desc': 'SELECT * FROM dummy_table WHERE condition;',
            'avg_purchase_by_product_ui_desc': 'SELECT * FROM dummy_table WHERE product_condition;'
        }

        # Mocking database connection
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        mock_connect.return_value = self.mock_connection

        # Creating an instance of the service
        self.db_path = 'dummy_db_path.db'
        self.service = TestAnalysisService(self.db_path)

    def test_execute_query(self):
        # Mocking query result
        self.mock_cursor.fetchall.return_value = [(1, 'UI Change', 'Desc Change', 100)]

        result = self.service.execute_query('avg_purchase_by_ui_and_desc')
        
        # Checking if execute_query returns the correct result
        self.assertEqual(result, [(1, 'UI Change', 'Desc Change', 100)])
        self.mock_cursor.execute.assert_called_once_with('SELECT * FROM dummy_table WHERE condition;')

    @patch('builtins.print')  # Mocking print outputs
    def test_analyze_ui_and_desc_changes(self, mock_print):
        # Mocking output for analyze_ui_and_desc_changes method
        self.mock_cursor.fetchall.return_value = [(1, 'UI Change', 'Desc Change', 100)]

        self.service.analyze_ui_and_desc_changes()

        # Checking if the correct output is printed
        mock_print.assert_called_with("\nAverage Purchase Amount by UI and Description Change:")
        mock_print.assert_any_call("UI Change: UI Change, Description Change: Desc Change, Average Purchase: 100")

    @patch('builtins.print')  # Mocking print outputs
    def test_analyze_product_ui_desc_changes(self, mock_print):
        # Mocking output for analyze_product_ui_desc_changes method
        self.mock_cursor.fetchall.return_value = [(1, 'Product 1', 'UI Change', 'Desc Change', 200)]

        self.service.analyze_product_ui_desc_changes()

        # Checking if the correct output is printed
        mock_print.assert_called_with("\nAverage Purchase Amount by Product, UI, and Description Change:")
        mock_print.assert_any_call("Product: Product 1, UI Change: UI Change, Description Change: Desc Change, Average Purchase: 200")

    def test_generate_report(self):
        # Testing the generate_report method, which includes both analyses
        with patch('builtins.print') as mock_print:
            self.service.generate_report()

            # Checking that both analysis methods were called
            mock_print.assert_any_call("\nAverage Purchase Amount by UI and Description Change:")
            mock_print.assert_any_call("\nAverage Purchase Amount by Product, UI, and Description Change:")

if __name__ == '__main__':
    unittest.main()
