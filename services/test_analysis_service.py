import sqlite3
from controllers.sql_loader import load_sql_queries
import logging
from config.settings import DB_PATH

class TestAnalysisService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)  # Initialize logger
        self.db_path = DB_PATH
        self.queries = load_sql_queries()

    def execute_query(self, query_name):
        """Execute and retrieve results for the specified query"""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(self.queries[query_name])
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def analyze_ui_and_desc_changes(self):
        """Analyze UI and Description changes and return structured data"""
        try:
            result = self.execute_query('avg_purchase_by_ui_and_desc')
            if result:
                analysis = [{"UI Change": row[0], "Description Change": row[1], "Average Purchase": row[2]} for row in result]
                self.logger.info("UI and Description changes analysis generated successfully.")
                return analysis
            else:
                self.logger.warning("No data available for UI and Description changes analysis.")
                return []
        except Exception as e:
            error_message = f"Error in analyze_ui_and_desc_changes: {e}"
            self.logger.error(error_message)
            return []

    def analyze_product_ui_desc_changes(self):
        """Analyze Product, UI, and Description changes and return structured data"""
        try:
            result = self.execute_query('avg_purchase_by_product_ui_desc')
            if result:
                analysis = [{"Product": row[0], "UI Change": row[1], "Description Change": row[2], "Average Purchase": row[3]} for row in result]
                self.logger.info("Product, UI, and Description changes analysis generated successfully.")
                return analysis
            else:
                self.logger.warning("No data available for Product, UI, and Description changes analysis.")
                return []
        except Exception as e:
            error_message = f"Error in analyze_product_ui_desc_changes: {e}"
            self.logger.error(error_message)
            return []

    def generate_report(self):
        """Generate full report as structured data"""
        return {
            "ui_desc_changes": self.analyze_ui_and_desc_changes(),
            "product_ui_desc_changes": self.analyze_product_ui_desc_changes()
        }