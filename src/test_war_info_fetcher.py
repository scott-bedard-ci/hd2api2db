import os
os.environ['DB_NAME'] = 'helldivers2_test'
from helldivers_api_client import Helldivers2ApiClient
from database_manager import DatabaseManager
from war_info_fetcher import WarInfoFetcher
from planet_fetcher import PlanetFetcher
from test_utils import clean_test_db, assert_using_test_db
import mysql.connector
import pprint
from transformers.planet_transformer import PlanetTransformer

def main():
    assert_using_test_db()
    clean_test_db()
    # Insert planet_id=0 as 'Unknown Planet' for foreign key integrity
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database='helldivers2_test'
    )
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO planets (id, name, sector, liberation_status) VALUES (0, 'Unknown Planet', 'Unknown', 'Unknown')")
    conn.commit()
    cursor.close()
    conn.close()
    # Set up dependencies
    api_client = Helldivers2ApiClient(max_retries=2, timeout=5)
    db_manager = DatabaseManager()
    planet_fetcher = PlanetFetcher(api_client, PlanetTransformer(), db_manager)
    war_info_fetcher = WarInfoFetcher(api_client, db_manager)
    # Run planet fetch and store first
    print('Running PlanetFetcher...')
    planet_result = planet_fetcher.fetch_and_store()
    assert planet_result is True
    # Print all planet IDs in the planets table
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database='helldivers2_test'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM planets ORDER BY id')
    planet_ids_in_db = [row[0] for row in cursor.fetchall()]
    print('Planet IDs in planets table:', planet_ids_in_db)
    cursor.close()
    conn.close()
    # Now run war info fetch and store
    print('Running WarInfoFetcher...')
    # Fetch war info data directly for analysis
    war_info_data = api_client.get_war_info()
    planet_ids_in_api = [pi['index'] for pi in war_info_data.get('planetInfos', [])]
    print('Planet IDs referenced in War Info API:', planet_ids_in_api)
    # Now try to store
    war_info_result = war_info_fetcher.fetch_and_store()
    assert war_info_result is True
    # Connect to DB and fetch results
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database='helldivers2_test'
    )
    cursor = conn.cursor(dictionary=True)
    print('war_info table:')
    cursor.execute('SELECT * FROM war_info ORDER BY war_id DESC LIMIT 1')
    pprint.pprint(cursor.fetchone())
    print('planet_infos table:')
    cursor.execute('SELECT * FROM planet_infos LIMIT 5')
    pprint.pprint(cursor.fetchall())
    print('home_worlds table:')
    cursor.execute('SELECT * FROM home_worlds LIMIT 5')
    pprint.pprint(cursor.fetchall())
    cursor.close()
    conn.close()
    print('WarInfoFetcher test passed!')

if __name__ == '__main__':
    main() 