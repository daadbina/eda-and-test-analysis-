import unittest
from unittest.mock import patch, MagicMock
from services.eda_service import EDAService
import sqlite3


class TestEDAService(unittest.TestCase):

    @patch('sqlite3.connect')
    @patch('controllers.sql_loader.load_sql_queries')
    def test_execute_query_success(self, mock_load_sql_queries, mock_sqlite_connect):
        # Mock queries to return a known query for testing
        mock_load_sql_queries.return_value = {
            'product_sales_summary': "SELECT * FROM product_sales_summary",
            'event_sales_summary': "SELECT * FROM event_sales_summary"
        }

        # Mock sqlite3 connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Product A', 1000), ('Product B', 2000)]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_sqlite_connect.return_value = mock_connection

        # Create instance of EDAService
        service = EDAService(db_path='test_db.sqlite')

        # Call the method
        result = service.execute_query('product_sales_summary')

        # Assertions
        mock_sqlite_connect.assert_called_once_with('test_db.sqlite')
        mock_cursor.execute.assert_called_once_with("SELECT * FROM product_sales_summary")
        self.assertEqual(result, [('Product A', 1000), ('Product B', 2000)])

    @patch('sqlite3.connect')
    @patch('controllers.sql_loader.load_sql_queries')
    def test_execute_query_failure(self, mock_load_sql_queries, mock_sqlite_connect):
        # Mock queries to return a known query for testing
        mock_load_sql_queries.return_value = {
            'product_sales_summary': "SELECT * FROM product_sales_summary"
        }

        # Mock sqlite3 connection and cursor
        mock_connection = MagicMock()
        mock_sqlite_connect.return_value = mock_connection
        mock_connection.cursor.side_effect = sqlite3.Error("Database error")

        # Create instance of EDAService
        service = EDAService(db_path='test_db.sqlite')

        # Call the method and check the result
        result = service.execute_query('product_sales_summary')

        # Assertions
        mock_sqlite_connect.assert_called_once_with('test_db.sqlite')
        self.assertIsNone(result)

    @patch('sqlite3.connect')
    @patch('controllers.sql_loader.load_sql_queries')
    def test_product_sales_summary(self, mock_load_sql_queries, mock_sqlite_connect):
        # Mock queries to return a known query for testing
        mock_load_sql_queries.return_value = {
            'product_sales_summary': "SELECT * FROM product_sales_summary"
        }

        # Mock sqlite3 connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Product A', 1000), ('Product B', 2000)]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_sqlite_connect.return_value = mock_connection

        # Create instance of EDAService
        service = EDAService(db_path='test_db.sqlite')

        # Call the method
        service.product_sales_summary()

        # Assertions
        mock_cursor.execute.assert_called_once_with("SELECT * FROM product_sales_summary")
        mock_cursor.fetchall.assert_called_once()

    @patch('sqlite3.connect')
    @patch('controllers.sql_loader.load_sql_queries')
    def test_event_sales_summary(self, mock_load_sql_queries, mock_sqlite_connect):
        # Mock queries to return a known query for testing
        mock_load_sql_queries.return_value = {
            'event_sales_summary': "SELECT * FROM event_sales_summary"
        }

        # Mock sqlite3 connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, 5000), (2, 10000)]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_sqlite_connect.return_value = mock_connection

        # Create instance of EDAService
        service = EDAService(db_path='test_db.sqlite')

        # Call the method
        service.event_sales_summary()

        # Assertions
        mock_cursor.execute.assert_called_once_with("SELECT * FROM event_sales_summary")
        mock_cursor.fetchall.assert_called_once()

    @patch('sqlite3.connect')
    @patch('controllers.sql_loader.load_sql_queries')
    def test_generate_report(self, mock_load_sql_queries, mock_sqlite_connect):
        # Mock queries to return a known query for testing
        mock_load_sql_queries.return_value = {
            'product_sales_summary': "SELECT * FROM product_sales_summary",
            'event_sales_summary': "SELECT * FROM event_sales_summary"
        }

        # Mock sqlite3 connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Product A', 1000), ('Product B', 2000)]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_sqlite_connect.return_value = mock_connection

        # Create instance of EDAService
        service = EDAService(db_path='test_db.sqlite')

        # Call the method
        service.generate_report()

        # Assertions
        mock_cursor.execute.assert_any_call("SELECT * FROM product_sales_summary")
        mock_cursor.execute.assert_any_call("SELECT * FROM event_sales_summary")
        mock_cursor.fetchall.assert_any_call()

if __name__ == '__main__':
    unittest.main()
