# Fixtures removed; now using shared fixtures from conftest.py

import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.major_order_transformer import MajorOrderTransformer
from database_manager import DatabaseManager
from major_orders_fetcher import MajorOrdersFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_major_orders_fetch_and_store():
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    transformer = MajorOrderTransformer()
    db_manager = DatabaseManager()
    fetcher = MajorOrdersFetcher(api_client, transformer, db_manager)
    success = fetcher.fetch_and_store()
    assert success is not None
    print('test_major_orders_fetch_and_store passed') 