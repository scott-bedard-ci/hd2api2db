"""Tests for the ``CampaignFetcher`` class."""
# Fixtures removed; now using shared fixtures from conftest.py

import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.campaign_transformer import CampaignTransformer
from database_manager import DatabaseManager
from campaign_fetcher import CampaignFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_campaign_fetch_and_store():
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    transformer = CampaignTransformer()
    db_manager = DatabaseManager()
    fetcher = CampaignFetcher(api_client, transformer, db_manager)
    success = fetcher.fetch_and_store()
    assert success is not None
    print('test_campaign_fetch_and_store passed') 