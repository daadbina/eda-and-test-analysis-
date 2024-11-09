import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def load_csv_to_db(self, csv_path, table_name):
        """Load CSV data into SQLite database"""
        # Read data from the CSV file
        df = pd.read_csv(csv_path)

        # Connect to the SQLite database
        connection = sqlite3.connect(self.db_path)
        df.to_sql(table_name, connection, if_exists='replace', index=False)
        connection.close()
        print(f"Data from {csv_path} loaded into table {table_name}.")

    def execute_query(self, query_name, queries):
        """Execute and fetch results for a specified query"""
        try:
            # Connect to the database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Execute the query
            print(f"Executing query: {query_name}")
            cursor.execute(queries[query_name])
            result = cursor.fetchall()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return result

        except sqlite3.Error as e:
            # Print error message if an issue occurs
            print(f"Error occurred while executing the query: {e}")
            return None
