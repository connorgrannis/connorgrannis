import os
import sqlite3 as sql
import pandas as pd

class SQL:
    def __init__(self, file_name):
        self.connection = self.connect_db(file_name)
        self.cursor = self.get_cursor()
    # Connect to a SQLite database (will be created if it doesn't exist).
    def connect_db(self, file_name):
        if not os.path.isfile(file_name):
            print('Database file does not exist and will be created.')
        try:
            conn = sql.connect(file_name)
            print("Database connection established.")
            return conn
        except Error:
            print(Error)
            return None
    # Create a cursor to use to access the data.
    def get_cursor(self):
        try:
            cur = self.connection.cursor()
            print('Cursor created.')
            return cur
        except Error:
            print(Error)
            return None
    # Run a SQLite query and return the result.
    def run_query(self, query_string):
        """ wraps a query in a try/except block """
        try:
            result = self.connection.execute(query_string)
            self.result = result
        except:
            print("Query error")
            result = None
        return result
    # Run a query and immediately display the results
    def quick_query(self, query_string):
        """ this is temporary. Just a look. it's not saved anywhere"""
        result = self.run_query(query_string)
        self.print_result(result)
    # Replace text \n and \t with actual newline and tab characters.
    def clean_string(self, strng):
        """ cleans up the query output """
        return str(strng).replace('\\n', '\n').replace('\\t', '\t')
    # Print query results up to a specified max number of records).
    def print_result(self, result, max_num_records=10):
        """ turns the results of a query into a dataframe and only returns a specified number of rows and
        Could modify to return df also and get rid of the other function?
        """
        print("------------------------------------------")
        df = self.create_dataframe_from_cursor(result)
        print(df.head(max_num_records))
        print("------------------------------------------")
    def print_all_table_and_view_names(self):
        """ displays the tables and views that are part of the database """
        result = self.run_query('SELECT name from sqlite_master where type= "table"')
        print("\nALL TABLE NAMES: ",result.fetchall())
        result = self.run_query('SELECT name from sqlite_master where type= "view"')
        print("ALL VIEW NAMES:  ",result.fetchall())
    def print_schema(self, table_or_view_name):
        """ displays the schema of a given table or view. Uses the `clean_string` function """
        #https://www.sqlite.com/schematab.html
        # Table "sqlite_schema" is correct, but "sqlite_master" is used for backward compatibility.)
        result = self.run_query('SELECT sql from sqlite_master where name= "' + table_or_view_name + '"')
        print("\nSCHEMA: " + table_or_view_name)
        print(self.clean_string(result.fetchall()))
    def print_table_or_view(self, table_name, max_num_records=10):
        """ uses the `print_result` function to quickly display the results of a query as a DataFrame """
        print("\nTABLE OR VIEW: " + table_name)
        result = self.run_query('SELECT * FROM "' + table_name + '"')
        self.print_result(result, max_num_records)
    # Create a SQLite table from a Pandas DataFrame.
    def create_table_from_dataframe(self, pdf, table_name):
        """ takes a pandas dataframe and converts it to a sql TABLE"""
        # pretty sure `if_exists='replace'` doesn't work with sqlite3
        pdf.to_sql(table_name, self.connection, if_exists='replace', index = False)
    # Create a Pandas DataFrame from a SQLite cursor.
    def create_dataframe_from_cursor(self, result):
        """ creates a pandas dataframe from the result of a query """
        cols = [column[0] for column in result.description]
        return pd.DataFrame.from_records(data = result.fetchall(), columns = cols)
    # Create a Pandas DataFrame from a SQLite table (or view).
    def create_dataframe_from_table(self, table_name):
        """ turns a table into a dataframe """
        cursor = self.run_query('SELECT * FROM "' + table_name + '"')
        cols = [column[0] for column in cursor.description]
        return pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)
    # Close the connection to the database.
    def close_db(self):
        # save all changes to file
        self.connection.commit()
        # close the cursor and db connection
        self.cursor.close()
        self.connection.close()



file = r"C:\Users\cxg042\OneDrive - Nationwide Children's Hospital\BrainAge\demo.csv"
conn = SQL(":memory:")
df = pd.read_csv(file)

# read from pandas
conn.create_table_from_dataframe(df, "demo")

# print all table names
conn.print_all_table_and_view_names()

# print a table
conn.print_table_or_view('demo', max_num_records=5)

# convert sql back to pandas
conn.create_dataframe_from_table('demo')

# print schema
conn.print_schema('demo')

# run a query
result = conn.run_query("""select age from demo where study = 'sce' """)

# quick query
conn.quick_query("""select age from demo where study = 'sce' """)

# print the result
conn.print_result(conn.result, max_num_records=5)
# re-running the query because the cursor is emptied after accessing it
result = conn.run_query("""select age from demo where study = 'sce' """)
conn.print_result(result, max_num_records=5)

# close
conn.close_db()
