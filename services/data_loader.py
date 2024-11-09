import pandas as pd
from config.settings import INVOICES_FILE, PRODUCTS_FILE, TEST_FILE
import logging

class DataLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)  # Initialize logger
        self.invoices_file = INVOICES_FILE
        self.products_file = PRODUCTS_FILE
        self.test_file = TEST_FILE

    def load_data(self):
        """Load data from CSV files and check for file contents"""
        try:
            self.logger.info("Starting to load data from CSV files.")
            
            # Attempt to load data from each CSV file
            invoices_data = pd.read_csv(self.invoices_file)
            self.logger.info(f"Invoices data loaded successfully from {self.invoices_file}.")

            products_data = pd.read_csv(self.products_file)
            self.logger.info(f"Products data loaded successfully from {self.products_file}.")

            test_data = pd.read_csv(self.test_file)
            self.logger.info(f"Test data loaded successfully from {self.test_file}.")
            
            # Return the loaded data in a dictionary
            return {
                "invoices": invoices_data,
                "products": products_data,
                "test": test_data
            }

        except FileNotFoundError as e:
            error_message = f"File not found: {e.filename}. Please check the file path."
            self.logger.error(error_message)
            raise FileNotFoundError(error_message)
        
        except pd.errors.EmptyDataError as e:
            error_message = f"File is empty: {e}. Please check the contents of the file."
            self.logger.error(error_message)
            raise pd.errors.EmptyDataError(error_message)
        
        except Exception as e:
            error_message = f"An unexpected error occurred while loading data: {e}"
            self.logger.error(error_message)
            raise Exception(error_message)
