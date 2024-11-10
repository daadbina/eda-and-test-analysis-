import sqlite3
from controllers.sql_loader import load_sql_queries
from config.settings import DB_PATH
import logging
import numpy as np  # برای محاسبات آماری
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        
    def product_sales_by_group(self):
        """Summarize product sales and return as structured data based on user groups"""
        try:
            # Execute the query to fetch sales based on user groups (A, B, C, D) and total_sales from invoices
            result = self.execute_query('product_sales_by_group')  # Ensure this query is added in the SQL queries
            
            if result:
                # Parse the results and return them in the expected format
                summary = [{"Group": row[0], "Total Sales": row[1]} for row in result if row[0] != 'Unknown']
                self.logger.info("Product sales summary generated successfully for groups A, B, C, D.")
                return summary
            else:
                self.logger.warning("No data available for product sales summary.")
                return []
        except Exception as e:
            error_message = f"Error in product_sales_by_group: {e}"
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

    def calculate_z_score(self):
        """Calculate Z-Score for the sales data from the invoices table"""
        try:
            # 1. Fetch sales data (amount) from the 'invoices' table
            sales_data = self.execute_query('z_score')

            if not sales_data:
                self.logger.error("No sales data found in the 'invoices' table.")
                return {'z_scores': []}

            # 2. Convert the result into a pandas DataFrame for easier manipulation
            sales_df = pd.DataFrame(sales_data, columns=['amount'])

            # 3. Calculate Z-Score for the 'amount' column
            mean = sales_df['amount'].mean()
            std = sales_df['amount'].std()

            # 4. Handle case where std is 0 (division by zero)
            if std == 0:
                self.logger.warning("Standard deviation is 0. Cannot calculate Z-Score.")
                sales_df['z_score'] = None
            else:
                sales_df['z_score'] = (sales_df['amount'] - mean) / std
            z_scores_list = sales_df['z_score'].tolist()
            # 5. Return the results (z_scores) as a dictionary or list
            return {'z_scores': z_scores_list, 'mean':np.mean(z_scores_list), 'std_dev': np.std(z_scores_list), 'min': np.min(z_scores_list), 'max': np.max(z_scores_list) }

        except Exception as e:
            self.logger.error(f"Error calculating Z-Score: {e}")
            return {'z_scores': []}


    def calculate_percentage_change(self, old_value, new_value):
        """Calculate percentage change between old and new values"""
        try:
            if old_value == 0 or old_value is None or new_value is None:
                self.logger.warning(f"Invalid values for percentage change calculation: old_value={old_value}, new_value={new_value}")
                return None
            
            percentage_change = ((new_value - old_value) / old_value) * 100
            return round(percentage_change, 2)  # Round the result to two decimal places for consistency
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
            group_sales = self.product_sales_by_group()
            # Calculating statistics for product sales
            if product_sales:
                product_statistics = self.calculate_statistics(product_sales)
            else:
                product_statistics = {}

            # Calculating Z-Scores for sales data
            if product_sales:
                z_scores = self.calculate_z_score()
            else:
                z_scores = {}

            # Calculate percentage changes between product sales
            percentage_changes = {}
            if len(group_sales) >= 2:
                percentage_changes['B_A'] = self.calculate_percentage_change(group_sales[0]['Total Sales'], group_sales[0]['Total Sales'])
            if len(group_sales) >= 3:
                percentage_changes['C_A'] = self.calculate_percentage_change(group_sales[0]['Total Sales'], group_sales[2]['Total Sales'])
            if len(group_sales) >= 4:
                percentage_changes['D_A'] = self.calculate_percentage_change(group_sales[0]['Total Sales'], group_sales[3]['Total Sales'])

            # Generating report
            report = {
                "product_sales_summary": product_sales,
                "event_sales_summary": event_sales,
                "product_sales_statistics": product_statistics,
                "z_scores": z_scores,
                "z_score_mean": z_scores['mean'],
                "z_score_std_dev" : z_scores['std_dev'],
                "z_score_max" :z_scores['max'] ,
                "z_score_min" : z_scores['min'],
                "percentage_changes": percentage_changes,
                "group_sales_summary":group_sales

            }

            self.logger.info("Full report generated successfully.")
            return report
        
        except Exception as e:
            error_message = f"Unexpected error while generating report: {e}"
            self.logger.error(error_message)
            return {}
