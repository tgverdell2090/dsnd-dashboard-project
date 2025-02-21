# Import the QueryBase class
from employee_events.query_base import QueryBase

# Import dependencies for sql execution
from employee_events.sql_execution import QueryMixin

# Create a subclass of QueryBase called `Team`
class Team(QueryBase):
    # Set the class attribute `name` to the string "team"
    name = "team"

    def names(self):
        """Returns a list of tuples containing team names and IDs"""
        sql = """
        SELECT 
            team_name,
            team_id
        FROM team
        ORDER BY team_name
        """
        return self.query(sql)

    def username(self, id):
        """Returns team name for a specific team ID"""
        sql = f"""
        SELECT 
            team_name
        FROM team
        WHERE team_id = {id}
        """
        return self.query(sql)

    def model_data(self, id):
        """Returns data needed for ML model as pandas DataFrame"""
        sql = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        return self.pandas_query(sql)