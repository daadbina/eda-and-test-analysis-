import unittest
from unittest.mock import patch, MagicMock
from services.eda_service import EDAService
import sqlite3
import numpy as np
import logging

class TestEDAService(unittest.TestCase):

    def setUp(self):
        # Initialize EDAService instance
        self.eda_service = EDAService()

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_execute_query_success(self, mock_logger, mock_connect):
        # Mock the database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Product A', 100), ('Product B', 150)]
        
        result = self.eda_service.execute_query('product_sales_summary')

        # Assertions
        self.assertEqual(result, [('Product A', 100), ('Product B', 150)])
        mock_logger.info.assert_any_call("Executing query: product_sales_summary")
        mock_logger.info.assert_any_call("Query 'product_sales_summary' executed successfully.")
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT product, SUM(sales) FROM sales GROUP BY product")
        mock_cursor.fetchall.assert_called_once()

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_execute_query_query_not_found(self, mock_logger, mock_connect):
        # Simulate a missing query in the loaded queries
        self.eda_service.queries = {}  # Empty queries dictionary
        with self.assertRaises(ValueError):
            self.eda_service.execute_query('non_existent_query')
        
        # Check that the correct error was logged
        mock_logger.error.assert_called_once_with("Query 'non_existent_query' not found in loaded queries.")

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_execute_query_database_error(self, mock_logger, mock_connect):
        # Simulate a database error during query execution
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        
        result = self.eda_service.execute_query('product_sales_summary')
        
        # Assertions
        self.assertIsNone(result)
        mock_logger.error.assert_called_once_with("Database error occurred while executing query 'product_sales_summary': Database error")

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_execute_query_unexpected_error(self, mock_logger, mock_connect):
        # Simulate an unexpected error during query execution
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Unexpected error")
        
        result = self.eda_service.execute_query('product_sales_summary')
        
        # Assertions
        self.assertIsNone(result)
        mock_logger.error.assert_called_once_with("Unexpected error occurred in 'execute_query': Unexpected error")

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_product_sales_summary_success(self, mock_logger, mock_connect):
        # Mock execute_query to return a sample result
        self.eda_service.execute_query = MagicMock(return_value=[('Product A', 100), ('Product B', 150)])
        
        summary = self.eda_service.product_sales_summary()
        
        # Assertions
        self.assertEqual(summary, [{'Product': 'Product A', 'Total Sales': 100}, {'Product': 'Product B', 'Total Sales': 150}])
        mock_logger.info.assert_called_with("Product sales summary generated successfully.")

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_product_sales_summary_no_data(self, mock_logger, mock_connect):
        # Mock execute_query to return an empty result
        self.eda_service.execute_query = MagicMock(return_value=[])
        
        summary = self.eda_service.product_sales_summary()
        
        # Assertions
        self.assertEqual(summary, [])
        mock_logger.warning.assert_called_once_with("No data available for product sales summary.")

    def test_calculate_statistics_success(self):
        sales_data = [{"Product": "Product A", "Total Sales": 100}, {"Product": "Product B", "Total Sales": 200}]
        
        stats = self.eda_service.calculate_statistics(sales_data)
        
        # Assertions
        self.assertEqual(stats['mean'], 150.0)
        self.assertEqual(stats['std'], 70.71067811865476)  # sqrt(((100-150)^2 + (200-150)^2) / 2)
        self.assertEqual(stats['min'], 100)
        self.assertEqual(stats['max'], 200)

    def test_calculate_statistics_empty_data(self):
        stats = self.eda_service.calculate_statistics([])
        self.assertEqual(stats, {})

    def test_calculate_percentage_change(self):
        percentage_change = self.eda_service.calculate_percentage_change(100, 150)
        self.assertEqual(percentage_change, 50.0)

    def test_calculate_percentage_change_zero_division(self):
        percentage_change = self.eda_service.calculate_percentage_change(0, 150)
        self.assertIsNone(percentage_change)

    @patch('services.eda_service.sqlite3.connect')
    @patch('services.eda_service.logging.getLogger')
    def test_generate_report(self, mock_logger, mock_connect):
        # Mock all necessary methods
        self.eda_service.product_sales_summary = MagicMock(return_value=[{'Product': 'Product A', 'Total Sales': 100}])
        self.eda_service.event_sales_summary = MagicMock(return_value=[{'Event ID': 1, 'Total Sales': 50}])
        self.eda_service.calculate_statistics = MagicMock(return_value={'mean': 100, 'std': 20, 'min': 80, 'max': 120})
        self.eda_service.execute_query = MagicMock(return_value=[(None, None, 100), (None, None, 150), (None, None, 200), (None, None, 250)])
        
        report = self.eda_service.generate_report()
        
        # Assertions
        self.assertIn("product_sales_summary", report)
        self.assertIn("event_sales_summary", report)
        self.assertIn("product_sales_statistics", report)
        self.assertIn("percentage_changes", report)
        
        mock_logger.info.assert_called_with("Full report generated successfully.")

if __name__ == '__main__':
    unittest.main()
