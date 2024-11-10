# t_test.py
import sqlite3
from controllers.sql_loader import load_sql_queries
from config.settings import DB_PATH
import logging
import pandas as pd
from scipy.stats import ttest_ind

class TTestService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = DB_PATH
        self.queries = load_sql_queries()
        self.logger.info("TTestService initialized with database path and loaded queries.")

    def execute_query(self, query_name):
        """Execute and fetch results for a specified query."""
        try:
            if query_name not in self.queries:
                error_message = f"Query '{query_name}' not found in loaded queries."
                self.logger.error(error_message)
                raise ValueError(error_message)

            self.logger.info(f"Executing query: {query_name}")
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute(self.queries[query_name])
            result = cursor.fetchall()

            self.logger.info(f"Query '{query_name}' executed successfully.")
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

    def perform_t_test(self, group_a_data, group_b_data):
        """Perform t-test between two groups."""
        try:
            # Perform t-test
            t_stat, p_value = ttest_ind(group_a_data, group_b_data, equal_var=False)
            return t_stat, p_value

        except Exception as e:
            self.logger.error(f"Error performing t-test: {e}")
            return None, None

    def perform_t_tests_for_all_groups(self):
        """Perform t-tests for all combinations of groups (A, B, C, D)."""
        try:
            # Define group query names
            groups = {
                "A": "group_a_sales",
                "B": "group_b_sales",
                "C": "group_c_sales",
                "D": "group_d_sales"
            }

            # Load data for each group
            group_data = {}
            for group_name, query_name in groups.items():
                data = self.execute_query(query_name)
                if data:
                    group_data[group_name] = pd.DataFrame(data, columns=['amount'])['amount']
                else:
                    self.logger.error(f"No data found for group {group_name}.")
                    return None

            # Perform t-tests for each combination of groups
            t_test_results = {}
            for group1, data1 in group_data.items():
                for group2, data2 in group_data.items():
                    if group1 < group2:  # Avoid duplicate and self-comparisons (e.g., A-B, B-A)
                        t_stat, p_value = self.perform_t_test(data1, data2)
                        t_test_results[f"{group1}-{group2}"] = {
                            "t_statistic": t_stat,
                            "p_value": p_value
                        }

            self.logger.info("T-tests for all group combinations completed successfully.")
            return t_test_results

        except Exception as e:
            self.logger.error(f"Error performing t-tests for all groups: {e}")
            return None
