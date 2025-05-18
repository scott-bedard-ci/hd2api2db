"""Tests for the ``WarInfoFetcher`` module."""
# Fixtures removed; now using shared fixtures from conftest.py

import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.war_info_transformer import WarInfoTransformer
from database_manager import DatabaseManager
from war_info_fetcher import WarInfoFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_war_info_fetch_and_store():
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    transformer = WarInfoTransformer()
    db_manager = DatabaseManager()
    fetcher = WarInfoFetcher(api_client, db_manager)
    success = fetcher.fetch_and_store()
    assert success is not None
    print('test_war_info_fetch_and_store passed') 
