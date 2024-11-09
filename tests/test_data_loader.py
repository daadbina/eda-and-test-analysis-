import unittest
from unittest.mock import patch, MagicMock
from services.data_loader import DataLoader
import pandas as pd
import logging

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Initialize DataLoader instance
        self.data_loader = DataLoader()

    @patch('services.data_loader.pd.read_csv')
    @patch('services.data_loader.logging.getLogger')
    def test_load_data_success(self, mock_logger, mock_read_csv):
        # Mocking successful CSV file loading
        mock_invoices_data = MagicMock(spec=pd.DataFrame)
        mock_products_data = MagicMock(spec=pd.DataFrame)
        mock_test_data = MagicMock(spec=pd.DataFrame)
        
        mock_read_csv.side_effect = [mock_invoices_data, mock_products_data, mock_test_data]
        
        # Call the load_data method
        loaded_data = self.data_loader.load_data()

        # Assertions
        self.assertEqual(loaded_data["invoices"], mock_invoices_data)
        self.assertEqual(loaded_data["products"], mock_products_data)
        self.assertEqual(loaded_data["test"], mock_test_data)
        
        # Check logger info calls
        mock_logger.info.assert_any_call("Starting to load data from CSV files.")
        mock_logger.info.assert_any_call(f"Invoices data loaded successfully from {self.data_loader.invoices_file}.")
        mock_logger.info.assert_any_call(f"Products data loaded successfully from {self.data_loader.products_file}.")
        mock_logger.info.assert_any_call(f"Test data loaded successfully from {self.data_loader.test_file}.")

    @patch('services.data_loader.pd.read_csv')
    @patch('services.data_loader.logging.getLogger')
    def test_load_data_file_not_found(self, mock_logger, mock_read_csv):
        # Simulate FileNotFoundError when reading CSV
        mock_read_csv.side_effect = FileNotFoundError("File not found: invoices.csv")
        
        with self.assertRaises(FileNotFoundError):
            self.data_loader.load_data()
        
        # Check that the error was logged
        mock_logger.error.assert_called_once_with("File not found: invoices.csv. Please check the file path.")

    @patch('services.data_loader.pd.read_csv')
    @patch('services.data_loader.logging.getLogger')
    def test_load_data_empty_file(self, mock_logger, mock_read_csv):
        # Simulate EmptyDataError when reading a CSV file
        mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse from file")
        
        with self.assertRaises(pd.errors.EmptyDataError):
            self.data_loader.load_data()
        
        # Check that the error was logged
        mock_logger.error.assert_called_once_with("File is empty: No columns to parse from file. Please check the contents of the file.")

    @patch('services.data_loader.pd.read_csv')
    @patch('services.data_loader.logging.getLogger')
    def test_load_data_unexpected_error(self, mock_logger, mock_read_csv):
        # Simulate a general exception during CSV reading
        mock_read_csv.side_effect = Exception("An unexpected error occurred")
        
        with self.assertRaises(Exception):
            self.data_loader.load_data()
        
        # Check that the error was logged
        mock_logger.error.assert_called_once_with("An unexpected error occurred while loading data: An unexpected error occurred")

    @patch('services.data_loader.pd.read_csv')
    @patch('services.data_loader.logging.getLogger')
    def test_load_data_logger_info_called(self, mock_logger, mock_read_csv):
        # Mock successful file loading
        mock_invoices_data = MagicMock(spec=pd.DataFrame)
        mock_products_data = MagicMock(spec=pd.DataFrame)
        mock_test_data = MagicMock(spec=pd.DataFrame)
        
        mock_read_csv.side_effect = [mock_invoices_data, mock_products_data, mock_test_data]
        
        # Call the load_data method
        self.data_loader.load_data()

        # Check that the logger.info is called the correct number of times
        self.assertEqual(mock_logger.info.call_count, 4)

if __name__ == '__main__':
    unittest.main()
