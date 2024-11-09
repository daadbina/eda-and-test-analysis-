import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from services.data_cleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        # Set up mock data for testing
        self.valid_data = {
            "invoices": pd.DataFrame({'invoice_id': [1, 2], 'amount': [100, 200]}),
            "test": pd.DataFrame({'test_id': [1, 2], 'result': [90, 85]}),
            "products": pd.DataFrame({'product_id': [1, 2], 'name': ['Product A', 'Product B']}),
        }
        self.invalid_data = {
            "invoices": "invalid_data",
            "test": pd.DataFrame({'test_id': [1, 2], 'result': [90, 85]}),
        }

    @patch('logging.getLogger')
    def test_clean_invoices_success(self, mock_logger):
        # Create instance of DataCleaner with valid data
        data_cleaner = DataCleaner(self.valid_data)
        
        # Mocking dropna function to return the data without changes
        self.valid_data["invoices"].dropna = MagicMock(return_value=self.valid_data["invoices"])

        cleaned_invoices = data_cleaner.clean_invoices()
        
        # Test if dropna was called
        self.valid_data["invoices"].dropna.assert_called_once()

        # Test that the returned cleaned data is correct
        self.assertEqual(cleaned_invoices.shape, (2, 2))  # Should be the same shape as input
        mock_logger.info.assert_any_call("Cleaning invoice data.")  # Check if logging happened

    @patch('logging.getLogger')
    def test_clean_invoices_key_error(self, mock_logger):
        # Data missing the 'invoices' key
        data_cleaner = DataCleaner({})
        
        cleaned_invoices = data_cleaner.clean_invoices()
        
        self.assertIsNone(cleaned_invoices)  # Should return None
        mock_logger.error.assert_called_once_with("Error: 'invoices' data not found in provided data dictionary.")

    @patch('logging.getLogger')
    def test_clean_test_data_success(self, mock_logger):
        # Create instance with valid data
        data_cleaner = DataCleaner(self.valid_data)
        
        # Mocking dropna for test data
        self.valid_data["test"].dropna = MagicMock(return_value=self.valid_data["test"])

        cleaned_test_data = data_cleaner.clean_test_data()
        
        # Assert dropna was called on test data
        self.valid_data["test"].dropna.assert_called_once()

        self.assertEqual(cleaned_test_data.shape, (2, 2))  # Should be the same shape as input
        mock_logger.info.assert_any_call("Cleaning test data.")  # Check if logging happened

    @patch('logging.getLogger')
    def test_clean_products_data_success(self, mock_logger):
        # Create instance with valid data
        data_cleaner = DataCleaner(self.valid_data)
        
        # Mocking dropna for products data
        self.valid_data["products"].dropna = MagicMock(return_value=self.valid_data["products"])

        cleaned_products_data = data_cleaner.clean_products_data()
        
        # Assert dropna was called on products data
        self.valid_data["products"].dropna.assert_called_once()

        self.assertEqual(cleaned_products_data.shape, (2, 2))  # Should be the same shape as input
        mock_logger.info.assert_any_call("Cleaning products data.")  # Check if logging happened

    @patch('logging.getLogger')
    def test_clean_all_success(self, mock_logger):
        # Create instance with valid data
        data_cleaner = DataCleaner(self.valid_data)
        
        # Mock dropna for all datasets
        for key in self.valid_data:
            self.valid_data[key].dropna = MagicMock(return_value=self.valid_data[key])
        
        cleaned_data = data_cleaner.clean_all()
        
        # Ensure each cleaning function was called and returned the cleaned data
        self.assertEqual(cleaned_data["invoices"].shape, (2, 2))
        self.assertEqual(cleaned_data["test"].shape, (2, 2))
        self.assertEqual(cleaned_data["products"].shape, (2, 2))
        mock_logger.info.assert_any_call("Starting to clean all data.")  # Check if logging happened

    @patch('logging.getLogger')
    def test_clean_all_missing_key(self, mock_logger):
        # Data missing a key (e.g., 'products')
        data_cleaner = DataCleaner({"invoices": pd.DataFrame(), "test": pd.DataFrame()})
        
        cleaned_data = data_cleaner.clean_all()
        
        # The cleaned data should be None because of the missing 'products' key
        self.assertIsNone(cleaned_data)
        mock_logger.error.assert_called_once_with("Error: 'products' data not found in provided data dictionary.")

    @patch('logging.getLogger')
    def test_invalid_data_type(self, mock_logger):
        # Passing invalid data type for cleaning
        data_cleaner = DataCleaner(self.invalid_data)
        
        # Test invalid type (non-DataFrame for 'invoices')
        cleaned_invoices = data_cleaner.clean_invoices()
        self.assertIsNone(cleaned_invoices)
        mock_logger.error.assert_called_once_with("An error occurred while cleaning invoices: 'invoices' data must be a DataFrame.")

if __name__ == '__main__':
    unittest.main()
