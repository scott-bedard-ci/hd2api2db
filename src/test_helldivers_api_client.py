"""Tests for the ``Helldivers2ApiClient`` HTTP wrapper."""
# Fixtures removed; now using shared fixtures from conftest.py

import pytest
import pprint
from helldivers_api_client import Helldivers2ApiClient
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_helldivers_api_client():
    config = Config()
    logger = setup_logging(config)
    api_client = Helldivers2ApiClient()
    # Example: test fetching planets
    planets = api_client.get_planets()
    assert planets is not None
    print('test_helldivers_api_client passed')

    print('Testing get_war_status...')
    war_status = api_client.get_war_status()
    assert war_status is not None, 'get_war_status() returned None'
    print('get_war_status() OK:', type(war_status), '\n')

    print('Testing get_war_info...')
    war_info = api_client.get_war_info()
    assert war_info is not None, 'get_war_info() returned None'
    print('get_war_info() OK:', type(war_info), '\n')
    print('Sample war_info response:')
    pprint.pprint(war_info)

    print('Testing get_news...')
    news = api_client.get_news()
    assert news is not None, 'get_news() returned None'
    print('get_news() OK:', type(news), '\n')

    print('Testing get_campaign...')
    campaign = api_client.get_campaign()
    assert campaign is not None, 'get_campaign() returned None'
    print('get_campaign() OK:', type(campaign), '\n')

    print('Testing get_major_orders...')
    major_orders = api_client.get_major_orders()
    assert major_orders is not None, 'get_major_orders() returned None'
    print('get_major_orders() OK:', type(major_orders), '\n')
    print('Sample major_orders response:')
    pprint.pprint(major_orders)

    print('Testing get_planet_history (planet_index=127)...')
    planet_history = api_client.get_planet_history(127)
    assert planet_history is not None, 'get_planet_history() returned None'
    print('get_planet_history() OK:', type(planet_history), '\n')
    print('Sample planet_history response:')
    pprint.pprint(planet_history)

    print('All API client tests passed!') 
