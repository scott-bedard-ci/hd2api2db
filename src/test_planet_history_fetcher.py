"""Tests for the ``PlanetHistoryFetcher`` class."""
# Fixtures removed; now using shared fixtures from conftest.py

import os
import pytest
from helldivers_api_client import Helldivers2ApiClient
from transformers.planet_history_transformer import PlanetHistoryTransformer
from database_manager import DatabaseManager
from planet_history_fetcher import PlanetHistoryFetcher
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_missing_planet_id_reporting():
    # Set up config and logging
    config = Config()
    logger = setup_logging(config)
    db_manager = DatabaseManager()
    # Use a dummy fetcher with a fake transformer to simulate missing planet_id
    class DummyApiClient:
        def get_planets(self):
            # Return a dict with a single planet with id 9999 (which does not exist in planets table)
            return {9999: {'name': 'Fake Planet'}}
        def get_planet_history(self, planet_id):
            # Return a single history entry
            return [{
                'planetId': planet_id,
                'timestamp': '2024-06-01 12:00:00',
                'status': 'Liberated',
                'current_health': 1000,
                'max_health': 2000,
                'player_count': 10
            }]
    transformer = PlanetHistoryTransformer()
    fetcher = PlanetHistoryFetcher(DummyApiClient(), transformer, db_manager)
    result = fetcher.fetch_and_store()
    assert isinstance(result, dict)
    assert 'missing_planet_errors' in result
    assert len(result['missing_planet_errors']) > 0
    assert result['missing_planet_errors'][0]['missing_planet_id'] == 9999
    print('test_missing_planet_id_reporting passed') 
