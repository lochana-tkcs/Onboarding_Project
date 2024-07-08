from litestar import Litestar, Request, Response, post, get
import csv
import io
import psycopg2
from psycopg2 import sql
import tiktoken
from tasks import store_csv_data
import duckdb
from litestar.config.cors import CORSConfig
from pydantic import BaseModel

cors_config = CORSConfig(allow_origins=["http://localhost:8080"])

async def upload_csv(request: Request) -> Response:
    form = await request.form()
    uploaded_file = form['file']

    content = await uploaded_file.read()
    csv_content = io.StringIO(content.decode('utf-8'))

    reader = csv.reader(csv_content)
    data = [row for row in reader]

    if not data:
        return Response({"message": "Empty CSV file"}, media_type="application/json", status_code=400)

    # Convert CSV data to a DataFrame and load it into DuckDB
    columns = data[0]
    rows = data[1:]

    # Send task to Celery worker
    store_csv_data.delay(rows, columns)

    return Response({"message": "File uploaded successfully and data insertion task sent to Celery", "data":data}, media_type="application/json")

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
