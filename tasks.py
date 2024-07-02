from celery import Celery
import duckdb
import pandas as pd

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def store_csv_data(data, columns):
    # Convert data to a DataFrame and load it into DuckDB
    df = pd.DataFrame(data, columns=columns)

    # Create a DuckDB connection and load the data
    con = duckdb.connect('my_database.db')
    con.execute("DROP TABLE IF EXISTS my_table")  # Drop the existing table if it exists
    con.execute("CREATE TABLE my_table AS SELECT * FROM df LIMIT 0")  # Create table with appropriate schema
    con.execute("INSERT INTO my_table SELECT * FROM df")
    return "Data inserted into DuckDB"
