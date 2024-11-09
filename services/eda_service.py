import sqlite3
from controllers.sql_loader import load_sql_queries
from config.settings import DB_PATH
import logging
import numpy as np  # برای محاسبات آماری

class EDAService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)  # Initialize logger
        self.db_path = DB_PATH
        self.queries = load_sql_queries()
        self.logger.info("EDAService initialized with database path and loaded queries.")

    def execute_query(self, query_name):
        """Execute and fetch results for a specified query"""
        try:
            # Check if query exists in loaded queries
            if query_name not in self.queries:
                error_message = f"Query '{query_name}' not found in loaded queries."
                self.logger.error(error_message)
                raise ValueError(error_message)
            
            self.logger.info(f"Executing query: {query_name}")

            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            
            # Execute the query
            cursor.execute(self.queries[query_name])
            result = cursor.fetchall()

            self.logger.info(f"Query '{query_name}' executed successfully.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
            self.logger.info("Database connection closed after query execution.")

            return result

        except sqlite3.Error as e:
            error_message = f"Database error occurred while executing query '{query_name}': {e}"
            self.logger.error(error_message)
            return None

        except Exception as e:
            error_message = f"Unexpected error occurred in 'execute_query': {e}"
            self.logger.error(error_message)
            return None

    def product_sales_summary(self):
        """Summarize product sales and return as structured data"""
        try:
            result = self.execute_query('product_sales_summary')
            if result:
                summary = [{"Product": row[0], "Total Sales": row[1]} for row in result]
                self.logger.info("Product sales summary generated successfully.")
                return summary
            else:
                self.logger.warning("No data available for product sales summary.")
                return []
        except Exception as e:
            error_message = f"Error in product_sales_summary: {e}"
            self.logger.error(error_message)
            return []

    def event_sales_summary(self):
        """Summarize event sales and return as structured data"""
        try:
            result = self.execute_query('event_sales_summary')
            if result:
                summary = [{"Event ID": row[0], "Total Sales": row[1]} for row in result]
                self.logger.info("Event sales summary generated successfully.")
                return summary
            else:
                self.logger.warning("No data available for event sales summary.")
                return []
        except Exception as e:
            error_message = f"Error in event_sales_summary: {e}"
            self.logger.error(error_message)
            return []

    def calculate_statistics(self, sales_data):
        """Calculate descriptive statistics (mean, std, min, max) for sales data"""
        try:
            # Extract sales values (Total Sales) from the sales_data
            sales_values = [row['Total Sales'] for row in sales_data]
            
            # Check if sales_values is not empty
            if not sales_values:
                self.logger.error("Sales data is empty. Cannot calculate statistics.")
                return {}

            mean = np.mean(sales_values)
            std = np.std(sales_values)
            min_sales = np.min(sales_values)
            max_sales = np.max(sales_values)

            return {
                "mean": mean,
                "std": std,
                "min": min_sales,
                "max": max_sales
            }

        except Exception as e:
            self.logger.error(f"Error calculating statistics: {e}")
            return {}

    def calculate_percentage_change(self, old_value, new_value):
        """Calculate percentage change between old and new values"""
        try:
            percentage_change = ((new_value - old_value) / old_value) * 100
            return percentage_change
        except ZeroDivisionError:
            self.logger.error("Division by zero encountered while calculating percentage change.")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error while calculating percentage change: {e}")
            return None

    def generate_report(self):
        """Generate full report as structured data"""
        try:
            # Fetching the sales summaries
            product_sales = self.product_sales_summary()
            event_sales = self.event_sales_summary()

            # Calculating statistics for product sales
            if product_sales:
                product_statistics = self.calculate_statistics(product_sales)
            else:
                product_statistics = {}

            # Calculating percentage changes between the different groups of UI and description changes
            ui_description_sales = self.execute_query('ui_description_sales_summary')  # فرض کنید که این query داده‌های مورد نظر رو میده
            if ui_description_sales:
                # Extracting sales values for each group
                group_A_sales = ui_description_sales[0][2]  # Group A: no, no
                group_B_sales = ui_description_sales[1][2]  # Group B: no, yes
                group_C_sales = ui_description_sales[2][2]  # Group C: yes, no
                group_D_sales = ui_description_sales[3][2]  # Group D: yes, yes

                # Calculate percentage changes
                percentage_change_B_A = self.calculate_percentage_change(group_A_sales, group_B_sales)
                percentage_change_C_A = self.calculate_percentage_change(group_A_sales, group_C_sales)
                percentage_change_D_A = self.calculate_percentage_change(group_A_sales, group_D_sales)

                # Add to the report
                report = {
                    "product_sales_summary": product_sales,
                    "event_sales_summary": event_sales,
                    "product_sales_statistics": product_statistics,
                    "percentage_changes": {
                        "B_A": percentage_change_B_A,
                        "C_A": percentage_change_C_A,
                        "D_A": percentage_change_D_A
                    }
                }
                self.logger.info("Full report generated successfully.")
                return report
            else:
                self.logger.warning("No data available for UI/Description sales summary.")
                return {}

        except Exception as e:
            error_message = f"Unexpected error while generating report: {e}"
            self.logger.error(error_message)
            return {}
