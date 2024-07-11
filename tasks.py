from celery import Celery
import duckdb
import pandas as pd
import os
import csv

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def store_csv_data(file_path):
    con = None
    try:
        con = duckdb.connect('my_database.db')

        # Drop the table if it exists, and then create the table and load the CSV data directly
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
