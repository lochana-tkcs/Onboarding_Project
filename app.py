from litestar import Litestar, Request, Response, post, get
import csv
import io
import os
import pandas as pd
from tasks import store_csv_data
import duckdb
from litestar.config.cors import CORSConfig
import aiofiles

cors_config = CORSConfig(allow_origins=["http://localhost:8080"])

async def upload_csv(request: Request) -> Response:
    file_path = 'C:/m3/temp.csv'

    # with open(file_path, 'wb') as file:
    #     async for chunk in request.stream():
    #         file.write(chunk)

    # async with aiofiles.open(file_path, 'w', encoding='utf-8', newline='') as file:
    #     async for chunk in request.stream():
    #         lines = chunk.decode('utf-8').splitlines()
    #         for line in lines:
    #             # Split the line into columns
    #             columns = line.split(',')
    #             # Create a CSV formatted string
    #             output = io.StringIO()
    #             csv_writer = csv.writer(output)
    #             csv_writer.writerow(columns)
    #             # Write the CSV formatted string to the file
    #             await file.write(output.getvalue())
    #             output.close()

    form = await request.form()
    uploaded_file = form['file']

    # Read the uploaded file directly into a DataFrame
    df = pd.read_csv(io.StringIO((await uploaded_file.read()).decode('utf-8')), header=None)

    # Save DataFrame to CSV
    df.to_csv(file_path, index=False)

    # Celery Task
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