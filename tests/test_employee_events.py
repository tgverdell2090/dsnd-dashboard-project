import pytest
from pathlib import Path
import sqlite3

# Create project_root variable 
project_root = Path(__file__).parent.parent.absolute()

@pytest.fixture
def db_path():
    """Return path to employee_events.db file"""
    path = project_root / 'python-package' / 'employee_events' / 'employee_events.db'
    print(f"Database path: {path}")  # Debug print
    return path

def test_db_exists(db_path):
    """Assert database file exists"""
    print(f"Checking if database exists at: {db_path}")  # Debug print
    assert db_path.is_file(), f"Database file not found at {db_path}"

@pytest.fixture
def db_conn(db_path):
    """Create database connection"""
    try:
        conn = sqlite3.connect(db_path)
        yield conn
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to connect to database: {e}")

@pytest.fixture
def table_names(db_conn):
    """Get list of table names from database"""
    try:
        name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        names = [x[0] for x in name_tuples]
        print(f"Found tables: {names}")  # Debug print
        return names
    except sqlite3.Error as e:
        pytest.fail(f"Failed to get table names: {e}")

def test_employee_table_exists(table_names):
    """Assert employee table exists"""
    assert 'employee' in table_names, "Employee table not found in database"

def test_team_table_exists(table_names):
    """Assert team table exists"""
    assert 'team' in table_names, "Team table not found in database"

def test_employee_events_table_exists(table_names):
    """Assert employee_events table exists"""
    assert 'employee_events' in table_names, "Employee_events table not found in database"