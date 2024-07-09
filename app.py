from litestar import Litestar, Request, Response, post, get
import csv
import io
import os
import pandas as pd
from tasks import store_csv_data
import duckdb
from litestar.config.cors import CORSConfig
from pydantic import BaseModel

cors_config = CORSConfig(allow_origins=["http://localhost:8080"])

# def store_csv_data():
#     file_path = 'C:/m3/temp.csv'
#     con = None
#     try:
#         con = duckdb.connect('my_database.db')
        
#         # Drop the table if it exists and then create the table and load the CSV data directly
#         con.execute("DROP TABLE IF EXISTS my_table")
#         con.execute(f"""
#             CREATE TABLE my_table AS
#             SELECT * FROM read_csv_auto('{file_path}')
#         """)
#         result = con.execute("SELECT * FROM my_table").fetchall()
        
#         return result
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

async def upload_csv(request: Request) -> Response:
    file_path = 'C:/m3/temp.csv'
    form = await request.form()
    uploaded_file = form['file']
    
    content = await uploaded_file.read()
    csv_content = io.StringIO(content.decode('utf-8'))

    reader = csv.reader(csv_content)
    data = [row for row in reader]

    # Convert CSV data to a DataFrame and load it into DuckDB
    df = pd.DataFrame(data[0:], columns=data[0])  # Assume first row is the header
    df.to_csv(file_path, index=False)
    result = store_csv_data(file_path)

    return Response({"message": "File uploaded successfully and data inserted into DuckDB", "data": result}, media_type="application/json")

@post("/upload")
async def upload_csv_endpoint(request: Request) -> Response:
    return await upload_csv(request)

@get("/data")
async def get_csv_data(request: Request) -> Response:
    # Retrieve the data from DuckDB
    con = duckdb.connect('my_database.db')
    try:
        # Fetch the table contents
        result = con.execute("SELECT * FROM my_table").fetchdf()
    finally:
        con.close()
    return Response({"data": result}, media_type="application/json")

# Create the Litestar app with CORS middleware
app = Litestar(route_handlers=[upload_csv_endpoint, get_csv_data], cors_config=cors_config)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)