# Import dependencies needed to execute sql queries
from sqlite3 import connect
from pathlib import Path
import pandas as pd
from functools import wraps

# Import QueryMixin from sql_execution module
from employee_events.sql_execution import QueryMixin

# Get database path
db_path = Path(__file__).parent.absolute() / 'employee_events.db'

# Define QueryBase class with QueryMixin inheritance
class QueryBase(QueryMixin):
    # Create class attribute name
    name = ""
    
    def names(self):
        """Return list of names from the database"""
        return []
    
    def event_counts(self, id):
        """
        Get event counts grouped by date for a given ID
        
        Args:
            id: ID to filter events by
        Returns:
            pandas DataFrame with event counts by date
        """
        # Query that groups events by date and sums positive/negative events
        query = f"""
        SELECT 
            event_date,
            SUM(positive_events) as positive_events,
            SUM(negative_events) as negative_events
        FROM employee_events
        WHERE {self.name}_id = {id}
        GROUP BY event_date
        ORDER BY event_date
        """
        
        return self.pandas_query(query)
    
    def notes(self, id):
        """
        Get notes for a given ID
        
        Args:
            id: ID to get notes for
        Returns:
            pandas DataFrame with notes and dates
        """
        # Query to get notes for the given entity type and ID
        query = f"""
        SELECT note_date, note
        FROM notes
        WHERE {self.name}_id = {id}
        ORDER BY note_date
        """
        
        return self.pandas_query(query)

