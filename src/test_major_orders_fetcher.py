import os
os.environ['DB_NAME'] = 'helldivers2_test'
from helldivers_api_client import Helldivers2ApiClient
from transformers.major_order_transformer import MajorOrderTransformer
from database_manager import DatabaseManager
from major_orders_fetcher import MajorOrdersFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db
import mysql.connector
import pprint


def main():
    assert_using_test_db()
    clean_test_db()
    # Set up config and logging
    config = Config()
    logger = setup_logging(config)

    # Initialize dependencies
    api_client = Helldivers2ApiClient()
    transformer = MajorOrderTransformer()
    db_manager = DatabaseManager()
    fetcher = MajorOrdersFetcher(api_client, transformer, db_manager)

    # Run fetch and store
    print('Running MajorOrdersFetcher...')
    success = fetcher.fetch_and_store()
    print('Success:', success)

    # Verify DB contents
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'helldivers2_test'),
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM major_orders LIMIT 5;')
    rows = cursor.fetchall()
    print('Sample rows from major_orders:')
    for row in rows:
        pprint.pprint(row)
    cursor.close()
    conn.close()
    clean_test_db()

if __name__ == "__main__":
    main() 