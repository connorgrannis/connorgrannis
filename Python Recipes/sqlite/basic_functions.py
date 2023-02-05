import pandas as pd
import sqlite3 as sq

# Connect to a SQLite database (will be created if it doesn't exist).
def connect_db(file_name):
    if not os.path.isfile(file_name):
        print('Database file does not exist and will be created.')
    try:
        conn = sq.connect(file_name)
        print("Database connection established.")
        return conn
    except Error:
        print(Error)
        return None

# Create a cursor to use to access the data.
def get_cursor(connection):
    try:
        cur = connection.cursor()
        print('Cursor created.')
        return cur
    except Error:
        print(Error)
        return None

# Run a SQLite query and return the result.
def run_query(conn_or_cur, query_string):
    """ wraps a query in a try/except block """
    try:
        result = conn_or_cur.execute(query_string)
    except:
        print("Query error")
        result = None
    return result

# Close the connection to the database.
def close_db(connection, cursor):
    # save all changes to file
    connection.commit()
    # close the cursor and db connection
    cursor.close()
    connection.close()
