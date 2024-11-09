import unittest
from unittest.mock import patch, MagicMock
from services.test_analysis_service import TestAnalysisService

class TestTestAnalysisService(unittest.TestCase):

    def setUp(self):
        # Initialize TestAnalysisService instance
        self.service = TestAnalysisService()

    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_execute_query_success(self, mock_load_sql_queries, mock_connect):
        # Mocking the query result
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'UI Change 1', 'Description 1', 10)]
        
        # Call the method
        result = self.service.execute_query('avg_purchase_by_ui_and_desc')

        # Assertions
        mock_connect.assert_called_once_with(self.service.db_path)
        mock_cursor.execute.assert_called_once_with('SELECT * FROM ui_desc_changes')
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result, [(1, 'UI Change 1', 'Description 1', 10)])  # Verify the result

    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_execute_query_empty_result(self, mock_load_sql_queries, mock_connect):
        # Mock empty result from query
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        # Call the method
        result = self.service.execute_query('avg_purchase_by_ui_and_desc')

        # Assertions
        self.assertEqual(result, [])  # Verify that the result is empty
        mock_cursor.fetchall.assert_called_once()

    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_execute_query_error(self, mock_load_sql_queries, mock_connect):
        # Simulate an error in database execution
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connect.return_value = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = sqlite3.DatabaseError("Database error")

        # Call the method and handle the error
        with self.assertRaises(sqlite3.DatabaseError):
            self.service.execute_query('avg_purchase_by_ui_and_desc')

        mock_cursor.execute.assert_called_once_with('SELECT * FROM ui_desc_changes')

    @patch('services.test_analysis_service.logging.getLogger')
    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_analyze_ui_and_desc_changes_success(self, mock_load_sql_queries, mock_connect, mock_logger):
        # Mocking query result and logger
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'UI Change 1', 'Description 1', 10)]
        
        analysis_result = self.service.analyze_ui_and_desc_changes()

        # Check if the analysis result is structured correctly
        self.assertEqual(analysis_result, [{"UI Change": 1, "Description Change": 'UI Change 1', "Average Purchase": 10}])

        # Check logger info
        mock_logger.info.assert_called_once_with("UI and Description changes analysis generated successfully.")

    @patch('services.test_analysis_service.logging.getLogger')
    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_analyze_ui_and_desc_changes_empty_result(self, mock_load_sql_queries, mock_connect, mock_logger):
        # Mocking empty result for analysis
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        analysis_result = self.service.analyze_ui_and_desc_changes()

        # Check if empty analysis is returned
        self.assertEqual(analysis_result, [])

        # Check warning in the logger
        mock_logger.warning.assert_called_once_with("No data available for UI and Description changes analysis.")

    @patch('services.test_analysis_service.logging.getLogger')
    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_analyze_ui_and_desc_changes_error(self, mock_load_sql_queries, mock_connect, mock_logger):
        # Mocking error scenario in query execution
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")

        analysis_result = self.service.analyze_ui_and_desc_changes()

        # Check if empty analysis is returned due to error
        self.assertEqual(analysis_result, [])

        # Check that the error was logged
        mock_logger.error.assert_called_once_with("Error in analyze_ui_and_desc_changes: Database error")

    @patch('services.test_analysis_service.logging.getLogger')
    @patch('services.test_analysis_service.sqlite3.connect')
    @patch('services.test_analysis_service.load_sql_queries')
    def test_generate_report(self, mock_load_sql_queries, mock_connect, mock_logger):
        # Mocking queries and results
        mock_queries = {'avg_purchase_by_ui_and_desc': 'SELECT * FROM ui_desc_changes', 'avg_purchase_by_product_ui_desc': 'SELECT * FROM product_ui_desc_changes'}
        mock_load_sql_queries.return_value = mock_queries
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'UI Change 1', 'Description 1', 10)]

        report = self.service.generate_report()

        # Check the report structure
        self.assertIn("ui_desc_changes", report)
        self.assertIn("product_ui_desc_changes", report)
        self.assertIsInstance(report["ui_desc_changes"], list)

if __name__ == '__main__':
    unittest.main()
