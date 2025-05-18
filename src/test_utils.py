"""Utility helpers shared across tests for DB cleanup."""

import os
from database_manager import DatabaseManager

def assert_using_test_db():
    db_name = os.environ.get('DB_NAME')
    if not db_name or not db_name.endswith('_test'):
        raise RuntimeError(f"Test aborted: DB_NAME ('{db_name}') does not end with '_test'. Refusing to run tests on non-test database.")

def clean_test_db():
    """Truncate all relevant tables in the test database to ensure a clean state."""
    db = DatabaseManager()
    tables = [
        'planet_history',
        'major_orders',
        'campaigns',
        'news',
        'war_status',
        'planets',
    ]
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        # Disable foreign key checks for truncation
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in tables:
            cursor.execute(f'TRUNCATE TABLE {table};')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        conn.commit()
    finally:
        cursor.close()
        conn.close() 