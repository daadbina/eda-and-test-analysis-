import sqlite3
from controllers.sql_loader import load_sql_queries
from config.settings import DB_PATH
import logging

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

    def generate_report(self):
        """Generate full report as structured data"""
        return {
            "product_sales_summary": self.product_sales_summary(),
            "event_sales_summary": self.event_sales_summary()
        }