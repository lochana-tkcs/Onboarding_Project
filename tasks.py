from celery import Celery
import duckdb
import pandas as pd
import io
import csv

app = Celery('tasks')
app.config_from_object('celeryconfig')

# @app.task
# def store_csv_data(content):
#     csv_content = io.StringIO(content)
#     reader = csv.reader(csv_content)
#     data = [row for row in reader]

#     # Convert CSV data to a DataFrame and load it into DuckDB
#     columns = data[0]
#     rows = data[1:]
#     df = pd.DataFrame(rows, columns=columns)

#     # Create a DuckDB connection and load the data
#     con = duckdb.connect('my_database.db')
#     con.execute("DROP TABLE IF EXISTS my_table")  # Drop the existing table if it exists
#     con.execute("CREATE TABLE my_table AS SELECT * FROM df LIMIT 0")  # Create table with appropriate schema
#     con.execute("INSERT INTO my_table SELECT * FROM df")
#     return "Data inserted into DuckDB"


@app.task
def store_csv_data(data, columns):
    df = pd.DataFrame(data, columns=columns)

    # Set the first row as the header
    df.columns = df.iloc[0]
    df = df[1:]  # Remove the first row which is now the header

    # Connect to DuckDB
    con = duckdb.connect('my_database.db')

    # Ensuring the database operations are safe and managed
    try:
        con.execute("BEGIN TRANSACTION;")
        con.execute("DROP TABLE IF EXISTS my_table")
        # Create table with the schema from the DataFrame
        con.execute("CREATE TABLE my_table AS SELECT * FROM df LIMIT 0")
        # Populate table with data
        con.execute("INSERT INTO my_table SELECT * FROM df")
        con.execute("COMMIT;")
    except Exception as e:
        con.execute("ROLLBACK;")
        raise e
    finally:
        con.close()

    return "Data inserted into DuckDB successfully with headers set."

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

    # return "Data inserted into DuckDB successfully with headers set."
