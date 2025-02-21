from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).parent.absolute() / 'employee_events.db'

# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    def pandas_query(self, sql_query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as pandas DataFrame
        
        Args:
            sql_query (str): SQL query string to execute
            
        Returns:
            pd.DataFrame: Query results as a pandas DataFrame
        """
        # Create connection to database
        connection = connect(db_path)
        
        # Use pandas read_sql to execute query and convert to DataFrame
        df = pd.read_sql(sql_query, connection)
        
        # Close connection
        connection.close()
        
        return df
    
    def query(self, sql_query: str) -> list:
        """
        Execute SQL query and return results as list of tuples
        
        Args:
            sql_query (str): SQL query string to execute
            
        Returns:
            list: Query results as list of tuples
        """
        # Create connection and cursor
        connection = connect(db_path)
        cursor = connection.cursor()
        
        # Execute query and fetch all results
        result = cursor.execute(sql_query).fetchall()
        
        # Close connection
        connection.close()
        
        return result
