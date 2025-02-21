# Import the QueryBase class
from employee_events.query_base import QueryBase

# Define Employee class inheriting from QueryBase
class Employee(QueryBase):
    # Set class attribute name
    name = "employee"

    def names(self):
        """Returns a list of tuples containing employee names and IDs"""
        sql = """
        SELECT 
            first_name || ' ' || last_name as full_name,
            employee_id
        FROM employee
        ORDER BY last_name, first_name
        """
        return self.query(sql)

    def username(self, id):
        """Returns full name for a specific employee ID"""
        sql = f"""
        SELECT 
            first_name || ' ' || last_name as full_name
        FROM employee
        WHERE employee_id = {id}
        """
        return self.query(sql)

    def model_data(self, id):
        """Returns data needed for ML model as pandas DataFrame"""
        sql = f"""
        SELECT 
            SUM(positive_events) positive_events,
            SUM(negative_events) negative_events
        FROM {self.name}
        JOIN employee_events
            USING({self.name}_id)
        WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(sql)