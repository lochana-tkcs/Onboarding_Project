from celery import Celery
import duckdb
import pandas as pd
import os
import csv

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def store_csv_data(file_path):
    file_path = 'C:/m3/temp.csv'
    con = None
    try:
        con = duckdb.connect('my_database.db')
        
        # Drop the table if it exists and then create the table and load the CSV data directly
        con.execute("DROP TABLE IF EXISTS my_table")
        con.execute(f"""
            CREATE TABLE my_table AS
            SELECT * FROM read_csv_auto('{file_path}')
        """)
        result = con.execute("SELECT * FROM my_table").fetchall()
        
        return result
    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred: {e}")
        raise e
    finally:
        if con is not None:
            con.close()
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

# @app.task
# def store_csv_data(file_path):
#     con = None
#     try:
#         con = duckdb.connect('my_database.db')
        
#         # Drop the table if it exists and then create the table and load the CSV data directly
#         con.execute("DROP TABLE IF EXISTS my_table")
#         con.execute(f"""
#             CREATE TABLE my_table AS
#             SELECT * FROM read_csv_auto('{file_path}')
#         """)
        
#         return "Data inserted into DuckDB successfully."
#     except Exception as e:
#         # Handle exceptions appropriately
#         print(f"An error occurred: {e}")
#         raise e
#     finally:
#         if con is not None:
#             con.close()
#         # Clean up the temporary file
#         if os.path.exists(file_path):
#             os.remove(file_path)

# @app.task
# def store_csv_data(data, columns):
#     df = pd.DataFrame(data, columns=columns)

#     # Set the first row as the header
#     df.columns = df.iloc[0]
#     df = df[1:]  # Remove the first row which is now the header

#     # Connect to DuckDB
#     con = duckdb.connect('C:/m3/my_database.db')

#     # Ensuring the database operations are safe and managed
#     try:
#         con.execute("BEGIN TRANSACTION;")
#         con.execute("DROP TABLE IF EXISTS my_table")
#         # Create table with the schema from the DataFrame
#         con.execute("CREATE TABLE my_table AS SELECT * FROM df LIMIT 0")
#         # Populate table with data
#         con.execute("INSERT INTO my_table SELECT * FROM df")
#         con.execute("COMMIT;")
#     except Exception as e:
#         con.execute("ROLLBACK;")
#         raise e
#     finally:
#         con.close()

#     return "Data inserted into DuckDB successfully with headers set."

    # # Connect to DuckDB
    # con = duckdb.connect('my_database.db')

    # # Ensuring the database operations are safe and managed
    # try:
    #     con.execute("BEGIN TRANSACTION;")
    #     con.execute("DROP TABLE IF EXISTS my_table")
    #     con.execute("CREATE TABLE my_table AS SELECT * FROM df LIMIT 0")  # Create empty table with schema from DataFrame
    #     con.execute("INSERT INTO my_table SELECT * FROM df")  # Populate table with data
    #     con.execute("COMMIT;")
    # except Exception as e:
    #     con.execute("ROLLBACK;")
    #     raise e
    # finally:
    #     con.close()
