# from litestar import Litestar, Request, Response, post
# import csv
# import io
# import duckdb

# async def upload_csv(request: Request) -> Response:
#     form = await request.form()
#     uploaded_file = form['file']
    
#     content = await uploaded_file.read()
    
#     csv_content = io.StringIO(content.decode('utf-8'))
    
#     con = duckdb.connect('my_database.db')

#     reader = csv.reader(csv_content)
#     data = [row for row in reader]

#     # Convert CSV data to a DataFrame and load it into DuckDB
#     import pandas as pd
#     df = pd.DataFrame(data[1:], columns=data[0])  # Assume first row is the header
#     # df = con.from_csv_auto(content)
#     df_datatypes = df.dtypes.to_dict()
#     df_datatypes = {k: str(v) for k, v in df_datatypes.items()}

#     # Create a DuckDB connection and load the data
#     con.execute("CREATE TABLE IF NOT EXISTS my_table AS SELECT * FROM df LIMIT 0")  # Create table with appropriate schema
#     con.execute("INSERT INTO my_table SELECT * FROM df")
#     schema = con.execute("DESCRIBE my_table").fetchall()
#     result = con.execute("SELECT * FROM my_table").fetchall()

#     return Response({"message": "File uploaded successfully and data inserted into DuckDB", "data": data, "schema":df_datatypes}, media_type="application/json")

# # Define the route using the @post decorator
# @post("/upload")
# async def upload_csv_endpoint(request: Request) -> Response:
#     return await upload_csv(request)

# # Create the Litestar app
# app = Litestar(route_handlers=[upload_csv_endpoint])

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)



# from litestar import Litestar, Request, Response, post
# import csv
# import io

# def infer_type(value):
#     """Try to infer the type of a value."""
#     try:
#         int_val = int(value)
#         return int_val
#     except ValueError:
#         pass

#     try:
#         float_val = float(value)
#         return float_val
#     except ValueError:
#         pass

#     if value.lower() in {'true', 'false'}:
#         return value.lower() == 'true'

#     return value

# async def upload_csv(request: Request) -> Response:
#     form = await request.form()
#     uploaded_file = form['file']
    
#     content = await uploaded_file.read()
#     csv_content = io.StringIO(content.decode('utf-8'))
    
#     reader = csv.reader(csv_content)
#     headers = next(reader)  # Read the header row
#     rows = []
    
#     for row in reader:
#         decoded_row = [infer_type(value) for value in row]
#         rows.append(decoded_row)
#         print(decoded_row)
    
#     return Response({"message": "File uploaded successfully", "data": rows}, media_type="application/json")

# # Define the route using the @post decorator
# @post("/upload")
# async def upload_csv_endpoint(request: Request) -> Response:
#     return await upload_csv(request)

# # Create the Litestar app
# app = Litestar(route_handlers=[upload_csv_endpoint])

# if __name__ == "_main_":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


# from litestar import Litestar, Request, Response, post, get
# import csv
# import io
# import duckdb

# # Store for the CSV data
# csv_data_store = []

# def infer_type(value):
#     """Try to infer the type of a value."""
#     try:
#         int_val = int(value)
#         return int_val
#     except ValueError:
#         pass

#     try:
#         float_val = float(value)
#         return float_val
#     except ValueError:
#         pass

#     if value.lower() in {'true', 'false'}:
#         return value.lower() == 'true'

#     return value

# async def upload_csv(request: Request) -> Response:
#     form = await request.form()
#     uploaded_file = form['file']
    
#     content = await uploaded_file.read()
#     csv_content = io.StringIO(content.decode('utf-8'))

#     form = await request.form()
    
#     reader = csv.reader(csv_content)
#     headers = next(reader)  # Read the header row
#     rows = []
    
#     for row in reader:
#         decoded_row = [infer_type(value) for value in row]
#         rows.append(decoded_row)
    
#     # Store the data
#     global csv_data_store
#     csv_data_store = rows
    
#     return Response({"message": "File uploaded successfully", "data": rows}, media_type="application/json")

# @post("/upload")
# async def upload_csv_endpoint(request: Request) -> Response:
#     return await upload_csv(request)

# @get("/data")
# async def get_csv_data(request: Request) -> Response:
#     # Retrieve the data
#     global csv_data_store
#     return Response({"data": csv_data_store}, media_type="application/json")

# # Create the Litestar app
# app = Litestar(route_handlers=[upload_csv_endpoint, get_csv_data])

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


# from litestar import Litestar, Request, Response, post, get
# import csv
# import io
# import duckdb

# # Store for the CSV data
# csv_data_store = []

# def infer_type(value):
#     """Try to infer the type of a value."""
#     try:
#         int_val = int(value)
#         return int_val
#     except ValueError:
#         pass

#     try:
#         float_val = float(value)
#         return float_val
#     except ValueError:
#         pass

#     if value.lower() in {'true', 'false'}:
#         return value.lower() == 'true'

#     return value

# async def upload_csv(request: Request) -> Response:
#     form = await request.form()
#     uploaded_file = form['file']
    
#     content = await uploaded_file.read()
#     csv_content = io.StringIO(content.decode('utf-8'))

#     reader = csv.reader(csv_content)
#     headers = next(reader)  # Read the header row
#     rows = []
#     inferred_types = []

#     # Infer types and collect rows
#     for row in reader:
#         decoded_row = [infer_type(value) for value in row]
#         if not inferred_types:
#             inferred_types = [type(value).__name__ for value in decoded_row]
#         rows.append(decoded_row)

#     # Prepare the schema
#     schema = ", ".join([f"{header} {dtype}" for header, dtype in zip(headers, inferred_types)])
#     table_name = "uploaded_csv"

#     # Connect to DuckDB and create table
#     con = duckdb.connect('my_database.db')
#     con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")

#     # Insert data into table
#     for row in rows:
#         placeholders = ", ".join(["?" for _ in row])
#         con.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

#     # Fetch the data from the table
#     result = con.execute(f"SELECT * FROM {table_name}").fetchall()

#     # Store the data in the global store
#     global csv_data_store
#     csv_data_store = result

#     return Response({"message": "File uploaded successfully and data stored in DuckDB", "data": result}, media_type="application/json")

# @post("/upload")
# async def upload_csv_endpoint(request: Request) -> Response:
#     return await upload_csv(request)

# # @get("/data")
# # async def get_csv_data(request: Request) -> Response:
# #     # Retrieve the data from DuckDB
# #     con = duckdb.connect('my_database.db')
# #     result = con.execute("SELECT * FROM uploaded_csv").fetchall()
# #     return Response({"data": result}, media_type="application/json")

# # Create the Litestar app
# app = Litestar(route_handlers=[upload_csv_endpoint])

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


# from litestar import Litestar, Request, Response, post, get
# from litestar.config.cors import CORSConfig
# import csv
# import io
# import duckdb
# import pandas as pd

# # Configure CORS
# cors_config = CORSConfig(allow_origins=["http://localhost:8080"])

# async def upload_csv(request: Request) -> Response:
#     form = await request.form()
#     uploaded_file = form['file']
    
#     content = await uploaded_file.read()
#     csv_content = io.StringIO(content.decode('utf-8'))

#     reader = csv.reader(csv_content)
#     data = [row for row in reader]

#     # Convert CSV data to a DataFrame and load it into DuckDB
#     df = pd.DataFrame(data[1:], columns=data[0])  # Assume first row is the header

#     # Create a DuckDB connection and load the data
#     con = duckdb.connect('my_database.db')
#     con.execute("DROP TABLE IF EXISTS my_table")  # Drop the existing table if it exists
#     con.execute("CREATE TABLE my_table AS SELECT * FROM df LIMIT 0")  # Create table with appropriate schema
#     con.execute("INSERT INTO my_table SELECT * FROM df")
    
#     schema = con.execute("DESCRIBE my_table").fetchall()
#     result = con.execute("SELECT * FROM my_table").fetchall()

#     return Response({"message": "File uploaded successfully and data inserted into DuckDB", "data": result, "schema": schema}, media_type="application/json")

# @post("/upload")
# async def upload_csv_endpoint(request: Request) -> Response:
#     return await upload_csv(request)

# @get("/data")
# async def get_csv_data(request: Request) -> Response:
#     # Retrieve the data from DuckDB
#     con = duckdb.connect('my_database.db')
#     result = con.execute("SELECT * FROM my_table").fetchall()
#     return Response({"data": result}, media_type="application/json")

# # Create the Litestar app
# app = Litestar(route_handlers=[upload_csv_endpoint, get_csv_data], cors_config=cors_config)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

from litestar import Litestar, Request, Response, post, get
import csv
import io
from tasks import store_csv_data
import duckdb
from litestar.config.cors import CORSConfig

cors_config = CORSConfig(allow_origins=["http://localhost:8080"])

async def upload_csv(request: Request) -> Response:
    form = await request.form()
    uploaded_file = form['file']

    content = await uploaded_file.read()
    csv_content = io.StringIO(content.decode('utf-8'))

    reader = csv.reader(csv_content)
    data = [row for row in reader]

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
    result = con.execute("SELECT * FROM my_table").fetchall()
    return Response({"data": result}, media_type="application/json")

# Create the Litestar app with CORS middleware
app = Litestar(route_handlers=[upload_csv_endpoint, get_csv_data], cors_config=cors_config)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

