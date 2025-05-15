# Fixtures removed; now using shared fixtures from conftest.py

import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.war_status_transformer import WarStatusTransformer
from database_manager import DatabaseManager
from war_status_fetcher import WarStatusFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_war_status_fetch_and_store():
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    transformer = WarStatusTransformer()
    db_manager = DatabaseManager()
    fetcher = WarStatusFetcher(api_client, transformer, db_manager)
    success = fetcher.fetch_and_store()
    assert success is not None
    print('test_war_status_fetch_and_store passed') 