import pandas as pd
import sqlite3 as sq

# Create a SQLite table from a Pandas DataFrame.
def create_table_from_dataframe(connection, pdf, table_name):
    """ takes a pandas dataframe and converts it to a sql TABLE"""
    # pretty sure `if_exists='replace'` doesn't work with sqlite3
    pdf.to_sql(table_name, connection, if_exists='replace', index = False)

# Create a SQLite table by reading a CSV file.  Uses Pandas.
def create_table_from_csv(connection, file_name, table_name):
    """ Uses the `create_table_from_dataframe` function to convert a csv into a sql table"""
    pdf = pd.read_csv(file_name)
    create_table_from_dataframe(connection, pdf, table_name)

# Create a SQLite table by reading a worksheet in an excel file.  Uses Pandas.
def create_table_from_excel(connection, file_name, sheet_name, table_name):
    pdf = pd.read_excel(file_name, sheet_name)
    create_table_from_dataframe(connection, pdf, table_name)
