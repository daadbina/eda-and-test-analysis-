import logging

class DataCleaner:
    def __init__(self, data):
        # Ensure data is in dictionary format
        self.data = data
        self.logger = logging.getLogger(__name__)  # Initialize logger

    def clean_invoices(self):
        """Clean invoice data"""
        try:
            invoices = self.data["invoices"]
            self.logger.info("Cleaning invoice data.")
            # Perform cleaning operations on invoices, e.g., removing missing values
            cleaned_invoices = invoices.dropna()  # Example: removing rows with missing values
            self.logger.info("Invoice data cleaned successfully.")
            return cleaned_invoices
        except KeyError:
            self.logger.error("Error: 'invoices' data not found in provided data dictionary.")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while cleaning invoices: {e}")
            return None

    def clean_test_data(self):
        """Clean test data"""
        try:
            test_data = self.data["test"]
            self.logger.info("Cleaning test data.")
            # Perform cleaning operations on test data, e.g., removing missing values
            cleaned_test_data = test_data.dropna()  # Example: removing rows with missing values
            self.logger.info("Test data cleaned successfully.")
            return cleaned_test_data
        except KeyError:
            self.logger.error("Error: 'test' data not found in provided data dictionary.")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while cleaning test data: {e}")
            return None

    def clean_products_data(self):
        """Clean products data"""
        try:
            products_data = self.data["products"]
            self.logger.info("Cleaning products data.")
            # Perform cleaning operations on products data if needed
            cleaned_products_data = products_data.dropna()
            self.logger.info("Products data cleaned successfully.")
            return cleaned_products_data
        except KeyError:
            self.logger.error("Error: 'products' data not found in provided data dictionary.")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while cleaning products data: {e}")
            return None

    def clean_all(self):
        """Run all cleaning functions and return cleaned data"""
        try:
            self.logger.info("Starting to clean all data.")
            cleaned_data = {
                "invoices": self.clean_invoices(),
                "test": self.clean_test_data(),
                "products": self.clean_products_data()
            }
            self.logger.info("All data cleaned successfully.")
            return cleaned_data
        except Exception as e:
            self.logger.error(f"An error occurred while running all cleaning functions: {e}")
            return None
