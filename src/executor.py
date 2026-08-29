"""
Phase 1: Execute generated SQL against the SQLite database and return results.
"""
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/chinook.db")


def get_schema(db_path: str = DB_PATH) -> str:
    """Return a plain-text description of all tables and columns."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    schema_lines = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info('{table}');")
        cols = [f"{row[1]} ({row[2]})" for row in cursor.fetchall()]
        schema_lines.append(f"Table {table}: " + ", ".join(cols))

    conn.close()
    return "\n".join(schema_lines)


def run_sql(sql: str, db_path: str = DB_PATH):
    """Execute a SQL query and return (columns, rows). Raises on error."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    rows = cursor.fetchall()
    conn.close()
    return columns, rows
