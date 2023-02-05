import pandas as pd
import sqlite3 as sq

# Create a Pandas DataFrame from a SQLite cursor.
def create_dataframe_from_cursor(cursor):
    """ creates a pandas dataframe from the result of a query """
    cols = [column[0] for column in cursor.description]
    return pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)

# Create a Pandas DataFrame from a SQLite table (or view).
def create_dataframe_from_table(connection, table_name):
    """ turns a table into a dataframe """
    cursor = run_query(connection,'SELECT * FROM "' + table_name + '"')
    cols = [column[0] for column in cursor.description]
    return pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)
