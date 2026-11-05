import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sales.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_schema():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = [row[0] for row in cursor.fetchall()]

    schema = ""

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        schema += f"\nTABLE: {table}\n"

        for column in columns:
            column_name = column[1]
            column_type = column[2]

            schema += (
                f"  - {column_name}: {column_type}\n"
            )

    connection.close()

    return schema


def execute_query(sql):
    connection = get_connection()

    try:
        df = pd.read_sql_query(
            sql,
            connection
        )

        return df, None

    except Exception as error:
        return pd.DataFrame(), str(error)

    finally:
        connection.close()