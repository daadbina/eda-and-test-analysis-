import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from services.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    
    @patch("pandas.read_csv")  # Mocking pd.read_csv
    def test_load_data_success(self, mock_read_csv):
        # Mocking the loaded data
        mock_invoices = MagicMock(spec=pd.DataFrame)
        mock_products = MagicMock(spec=pd.DataFrame)
        mock_test = MagicMock(spec=pd.DataFrame)
        
        # Define what the mock will return
        mock_read_csv.side_effect = [mock_invoices, mock_products, mock_test]

        # Creating DataLoader instance
        data_loader = DataLoader()

        # Calling the load_data method
        result = data_loader.load_data()

        # Ensure the correct files are being read
        mock_read_csv.assert_any_call(data_loader.invoices_file)
        mock_read_csv.assert_any_call(data_loader.products_file)
        mock_read_csv.assert_any_call(data_loader.test_file)

        # Ensure the method returns the correct results
        self.assertEqual(result["invoices"], mock_invoices)
        self.assertEqual(result["products"], mock_products)
        self.assertEqual(result["test"], mock_test)
    
    @patch("pandas.read_csv")
    def test_load_data_file_not_found(self, mock_read_csv):
        # Mocking a FileNotFoundError
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        # Creating DataLoader instance
        data_loader = DataLoader()

        # Ensuring the exception is raised when FileNotFoundError occurs
        with self.assertRaises(FileNotFoundError):
            data_loader.load_data()

    @patch("pandas.read_csv")
    def test_load_data_empty_file(self, mock_read_csv):
        # Mocking an EmptyDataError
        mock_read_csv.side_effect = pd.errors.EmptyDataError("File is empty")

        # Creating DataLoader instance
        data_loader = DataLoader()

        # Ensuring the exception is raised when EmptyDataError occurs
        with self.assertRaises(pd.errors.EmptyDataError):
            data_loader.load_data()

if __name__ == "__main__":
    unittest.main()
