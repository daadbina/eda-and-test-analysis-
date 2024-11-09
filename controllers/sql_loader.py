import os

def load_sql_queries(filename=r"controllers\sql_queris.sql"):
    # Find the project base path and create the absolute file path
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_dir, filename)

    queries = {}
    try:
        # Open the SQL file and read its content
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            # Split the script into individual queries
            sql_statements = sql_script.split('-- Query name: ')
            for statement in sql_statements[1:]:
                lines = statement.strip().split('\n')
                query_name = lines[0].strip()  # Extract query name
                query = "\n".join(lines[1:]).strip()  # Extract query content
                queries[query_name] = query
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the path and ensure the file exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return queries
