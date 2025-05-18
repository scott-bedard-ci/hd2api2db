import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from database_manager import DatabaseManager

TABLES = [
    'planet_history',
    'planet_status',
    'major_orders',
    'campaigns',
    'news',
    'war_status',
    'planet_infos',
    'home_worlds',
    'war_info',
    'planet_environmentals',
    'planets',
    'biomes',
    'environmentals',
    'factions',
]

def main():
    if '--force' not in sys.argv:
        print('WARNING: This will wipe ALL data from the database!')
        print('To proceed, run this script with the --force flag.')
        sys.exit(1)

    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        print('Disabling foreign key checks...')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in TABLES:
            print(f'Truncating table: {table}')
            cursor.execute(f'TRUNCATE TABLE {table};')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        conn.commit()
        print('All tables wiped. Database is now empty (schema preserved).')
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main() 
