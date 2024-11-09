import unittest
import pandas as pd
from services.data_cleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.sample_data = {
            "invoices": pd.DataFrame({
                "id": [1, 2, 3, None],
                "amount": [100, 200, None, 400]
            }),
            "test": pd.DataFrame({
                "test_id": [1, None, 3, 4],
                "score": [85, 90, None, 70]
            })
        }
        # Creating an instance of DataCleaner
        self.cleaner = DataCleaner(self.sample_data)

    def test_clean_invoices(self):
        # Cleaning invoice data
        cleaned_invoices = self.cleaner.clean_invoices()
        
        # Ensuring that invoices with missing data are removed
        self.assertEqual(len(cleaned_invoices), 3)  # 3 rows should remain
        self.assertTrue(cleaned_invoices.isnull().sum().sum() == 0)  # No null values should remain

    def test_clean_test_data(self):
        # Cleaning test data
        cleaned_test_data = self.cleaner.clean_test_data()
        
        # Ensuring that missing data is removed
        self.assertEqual(len(cleaned_test_data), 3)  # 3 rows should remain
        self.assertTrue(cleaned_test_data.isnull().sum().sum() == 0)  # No null values should remain

    def test_missing_invoices_key(self):
        # Data without the "invoices" key
        incomplete_data = {
            "test": pd.DataFrame({
                "test_id": [1, 2],
                "score": [90, 85]
            })
        }
        cleaner = DataCleaner(incomplete_data)
        
        # Ensuring KeyError is raised when "invoices" key is missing
        with self.assertRaises(KeyError):
            cleaner.clean_invoices()

    def test_missing_test_key(self):
        # Data without the "test" key
        incomplete_data = {
            "invoices": pd.DataFrame({
                "id": [1, 2],
                "amount": [100, 200]
            })
        }
        cleaner = DataCleaner(incomplete_data)
        
        # Ensuring KeyError is raised when "test" key is missing
        with self.assertRaises(KeyError):
            cleaner.clean_test_data()

if __name__ == "__main__":
    unittest.main()
