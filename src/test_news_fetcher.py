# Fixtures removed; now using shared fixtures from conftest.py

import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.news_transformer import NewsTransformer
from database_manager import DatabaseManager
from news_fetcher import NewsFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_news_fetch_and_store():
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    transformer = NewsTransformer()
    db_manager = DatabaseManager()
    fetcher = NewsFetcher(api_client, transformer, db_manager)
    success = fetcher.fetch_and_store()
    assert success is not None
    print('test_news_fetch_and_store passed') 