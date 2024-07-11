import pytest
from httpx import AsyncClient, ASGITransport
import pandas as pd
import duckdb
import os
from unittest.mock import patch, MagicMock
import duckdb

# Ensure the app is imported correctly from the right path
import sys
sys.path.insert(0, 'C:/m3')
from app import app
from tasks import store_csv_data  # Import the store_csv_data task from tasks module

@pytest.fixture(scope='module')
def setup_duckdb():
    # Setup: create the DuckDB database
    con = duckdb.connect('my_database.db')
    # Prepare by ensuring any prior table does not exist
    con.execute("DROP TABLE IF EXISTS my_table")
    con.close()
    yield
    # Teardown: remove the database file after tests
    os.remove('my_database.db')

@pytest.mark.asyncio
async def test_upload_csv(setup_duckdb):
    # Prepare a CSV file for testing
    csv_content = "column1,column2,column3\nvalue1,value2,value3\nvalue4,value5,value6"
    files = {'file': ('test.csv', csv_content)}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/upload", files=files)
    
    assert response.status_code == 201  # Adjusted to expect 201 Created
    assert response.json()["message"] == "File uploaded successfully and data inserted into DuckDB"

    # Verify the data in DuckDB
    con = duckdb.connect('my_database.db')
    result = con.execute("SELECT * FROM my_table").fetchall()
    con.close()

    expected_data = [('value1', 'value2', 'value3'), ('value4', 'value5', 'value6')]
    assert result[1:] == expected_data  # Skip the header row

def test_store_csv_data(setup_duckdb):
    file_path = 'test.csv'
    # Mocking the database connection and os.remove to avoid actual file and DB operations
    with patch('duckdb.connect') as mock_connect, patch('os.remove') as mock_remove:
        mock_con = MagicMock()
        mock_connect.return_value = mock_con
        mock_con.execute.return_value = mock_con
        mock_con.fetchall.return_value = [("value1", "value2", "value3"), ("value4", "value5", "value6")]

        # Run the task
        result = store_csv_data(file_path)

        # Assert that the result matches expected data
        expected_result = [("value1", "value2", "value3"), ("value4", "value5", "value6")]
        assert result == expected_result

        # Assert that the database commands were executed
        mock_con.execute.assert_any_call("DROP TABLE IF EXISTS my_table")
        
        # Normalize the SQL command before asserting
        sql_command_expected = "CREATE TABLE my_table AS SELECT * FROM read_csv_auto('test.csv')"
        sql_calls = [call.args[0].replace('\n', '').replace(' ', '') for call in mock_con.execute.call_args_list]
        assert any(sql_command_expected.replace(' ', '') in sql_call for sql_call in sql_calls)

if __name__ == "__main__":
    pytest.main()
