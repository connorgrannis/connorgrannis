import pandas as pd
import sqlite3 as sq

# Replace text \n and \t with actual newline and tab characters.
def clean_string(strng):
    """ cleans up the query output """
    return str(strng).replace('\\n', '\n').replace('\\t', '\t')

# Print query results up to a specified max number of records).
def print_result(cursor, max_num_records):
    """ turns the results of a query into a dataframe and only returns a specified number of rows and
    
    Could modify to return df also and get rid of the other function?
    """
    print("------------------------------------------")
    df = create_dataframe_from_cursor(cursor)
    print(df.head(max_num_records))
    print("------------------------------------------")

def print_all_table_and_view_names(conn_or_cur):
    """ displays the tables and views that are part of the database """
    result = run_query(conn_or_cur,'SELECT name from sqlite_master where type= "table"')
    print("\nALL TABLE NAMES: ",result.fetchall())
    result = run_query(conn_or_cur,'SELECT name from sqlite_master where type= "view"')
    print("ALL VIEW NAMES:  ",result.fetchall())

def print_schema(conn_or_cur, table_or_view_name):
    """ displays the schema of a given table or view. Uses the `clean_string` function """
    #https://www.sqlite.com/schematab.html
    # Table "sqlite_schema" is correct, but "sqlite_master" is used for backward compatibility.)
    result = run_query(conn_or_cur,'SELECT sql from sqlite_master where name= "' + table_or_view_name + '"')
    print("\nSCHEMA: " + table_or_view_name)
    print(clean_string(result.fetchall()))

def print_table_or_view(conn_or_cur, table_name, max_num_records):
    """ uses the `print_results` function to quickly display the results of a query as a DataFrame """
    print("\nTABLE OR VIEW: " + table_name)
    result = run_query(conn_or_cur,'SELECT * FROM "' + table_name + '"')
    print_result(result, max_num_records)
