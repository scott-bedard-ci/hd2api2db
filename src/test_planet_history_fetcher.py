import os
os.environ['DB_NAME'] = 'helldivers2_test'
from helldivers_api_client import Helldivers2ApiClient
from transformers.planet_history_transformer import PlanetHistoryTransformer
from database_manager import DatabaseManager
from planet_history_fetcher import PlanetHistoryFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db


def main():
    assert_using_test_db()
    clean_test_db()
    # Set up config and logging
    config = Config()
    logger = setup_logging(config)

    # Initialize dependencies
    api_client = Helldivers2ApiClient()
    transformer = PlanetHistoryTransformer()
    db_manager = DatabaseManager()
    fetcher = PlanetHistoryFetcher(api_client, transformer, db_manager)

    # Run fetch and store
    print('Running PlanetHistoryFetcher...')
    success = fetcher.fetch_and_store()
    print('Success:', success)
    clean_test_db()

if __name__ == "__main__":
    main() 