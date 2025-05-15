# Fixtures removed; now using shared fixtures from conftest.py

import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.planet_transformer import PlanetTransformer
from database_manager import DatabaseManager
from planet_fetcher import PlanetFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_planet_fetch_and_store():
    # Set up config and logging
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    transformer = PlanetTransformer()
    db_manager = DatabaseManager()
    fetcher = PlanetFetcher(api_client, transformer, db_manager)
    # Run fetch and store
    success = fetcher.fetch_and_store()
    assert success is not None
    print('test_planet_fetch_and_store passed') 