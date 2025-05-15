import pytest
from transformers.planet_transformer import PlanetTransformer
from transformers.war_status_transformer import WarStatusTransformer
from transformers.news_transformer import NewsTransformer
from transformers.campaign_transformer import CampaignTransformer
from transformers.major_order_transformer import MajorOrderTransformer
from transformers.planet_history_transformer import PlanetHistoryTransformer
from transformers.war_info_transformer import WarInfoTransformer
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

def test_planet_transformer():
    transformer = PlanetTransformer()
    # Pass a list of dicts as expected
    result = transformer.transform([
        {'name': 'Test', 'sector': 1, 'liberation_status': 'Liberated', 'biome': None, 'environmentals': []}
    ])
    assert isinstance(result, list)
    assert result[0]['name'] == 'Test'

def test_war_status_transformer():
    transformer = WarStatusTransformer()
    # Use correct keys and structure
    result = transformer.transform({
        'warId': 1,
        'time': 1234567890,
        'impactMultiplier': 1.0,
        'storyBeatId32': 0,
        'planetStatus': [
            {
                'index': 1,
                'owner': 2,
                'health': 100,
                'regenPerSecond': 0.5,
                'players': 10,
                'position': {'x': 1.0, 'y': 2.0}
            }
        ]
    })
    assert isinstance(result, dict)
    assert 'war_status' in result
    assert 'planet_status' in result
    assert isinstance(result['planet_status'], list)

def test_news_transformer():
    transformer = NewsTransformer()
    # Pass a list of dicts as expected
    result = transformer.transform([
        {'id': 1, 'published': 1710000000, 'type': 'news', 'tagIds': [], 'message': 'Test', 'created_at': '2024-01-01 00:00:00'}
    ])
    assert isinstance(result, list)
    assert result[0]['id'] == 1

def test_campaign_transformer():
    transformer = CampaignTransformer()
    # Pass a list of dicts as expected
    result = transformer.transform([
        {'name': 'Campaign', 'planetIndex': 1, 'biome': None, 'faction': None, 'defense': 100, 'expireDateTime': None, 'health': 100, 'maxHealth': 200, 'percentage': 50, 'players': 10}
    ])
    assert isinstance(result, list)
    assert result[0]['name'] == 'Campaign'

def test_major_order_transformer():
    transformer = MajorOrderTransformer()
    # Pass a list of dicts as expected, with correct keys
    result = transformer.transform([
        {'id32': 1, 'expiresIn': 1000, 'progress': {}, 'setting': {'flags': 0, 'overrideBrief': '', 'overrideTitle': '', 'reward': {}, 'rewards': [], 'taskDescription': '', 'tasks': [], 'type': ''}}
    ])
    assert isinstance(result, list)
    assert result[0]['id32'] == 1

def test_planet_history_transformer():
    transformer = PlanetHistoryTransformer()
    # Pass a list of dicts as expected
    result = transformer.transform([
        {'planetId': 1, 'timestamp': '2024-01-01 00:00:00', 'status': 'Liberated', 'current_health': 100, 'max_health': 200, 'player_count': 10}
    ])
    assert isinstance(result, list)
    assert result[0]['planet_id'] == 1

def test_war_info_transformer():
    transformer = WarInfoTransformer()
    # Use a minimal valid war_info_data structure
    result = transformer.transform({
        'warId': 1,
        'startDate': 1710000000,
        'endDate': 1710003600,
        'layoutVersion': 1,
        'minimumClientVersion': '1.0.0',
        'capitalInfos': [],
        'planetPermanentEffects': [],
        'planetInfos': [
            {'index': 1, 'position': {'x': 1.0, 'y': 2.0}, 'waypoints': [], 'sector': 1, 'maxHealth': 100, 'disabled': False, 'initialOwner': 1}
        ],
        'homeWorlds': [
            {'race': 1, 'planetIndices': [1]}
        ]
    })
    assert isinstance(result, dict)
    assert 'war_info' in result
    assert 'planet_infos' in result
    assert 'home_worlds' in result 