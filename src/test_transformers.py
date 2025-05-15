import os
os.environ['DB_NAME'] = 'helldivers2_test'
from transformers.planet_transformer import PlanetTransformer
from transformers.war_status_transformer import WarStatusTransformer
from transformers.news_transformer import NewsTransformer
from transformers.campaign_transformer import CampaignTransformer
from transformers.major_order_transformer import MajorOrderTransformer
from transformers.planet_history_transformer import PlanetHistoryTransformer
from transformers.war_info_transformer import WarInfoTransformer
import pprint

def test_planet_transformer():
    print('Testing PlanetTransformer...')
    sample = [{
        'name': 'Super Earth',
        'sector': 'Alpha',
        'liberation': 'Liberated',
    }]
    result = PlanetTransformer.transform(sample)
    assert isinstance(result, list) and len(result) == 1
    pprint.pprint(result)

def test_war_status_transformer():
    print('Testing WarStatusTransformer...')
    sample = {
        'warId': 801,
        'time': 39349470,
        'impactMultiplier': 0.0128,
        'storyBeatId32': 724770796,
        'planetStatus': [
            {
                'index': 0,
                'owner': 1,
                'health': 1000000,
                'regenPerSecond': 1388.8889,
                'players': 649,
                'position': {'x': 0.0, 'y': 0.0}
            },
            {
                'index': 1,
                'owner': 1,
                'health': 1000000,
                'regenPerSecond': 1388.8889,
                'players': 0,
                'position': {'x': 0.05, 'y': 0.10}
            }
        ]
    }
    result = WarStatusTransformer.transform(sample)
    assert isinstance(result, dict)
    assert 'war_status' in result and 'planet_status' in result
    pprint.pprint(result)

def test_news_transformer():
    print('Testing NewsTransformer...')
    sample = [{
        'id': 101,
        'published': '2024-06-01 10:00:00',
        'type': 'announcement',
        'tagIds': [1, 2, 3],
        'message': 'Helldivers unite!'
    }]
    result = NewsTransformer.transform(sample)
    assert isinstance(result, list) and len(result) == 1
    pprint.pprint(result)

def test_campaign_transformer():
    print('Testing CampaignTransformer...')
    sample = [{
        'name': 'Operation Freedom',
        'description': 'Liberate all planets.',
        'startDate': '2024-06-01',
        'endDate': '2024-06-10',
    }]
    result = CampaignTransformer.transform(sample)
    assert isinstance(result, list) and len(result) == 1
    pprint.pprint(result)

def test_major_order_transformer():
    print('Testing MajorOrderTransformer...')
    sample = [{
        'id32': 1234567890,
        'expiresIn': 3600,
        'progress': [0, 1, 0],
        'setting': {
            'flags': 2,
            'overrideBrief': 'Defend Super Earth from the Illuminate.',
            'overrideTitle': 'DEFENSE MISSION',
            'reward': {'amount': 100, 'id32': 555, 'type': 1},
            'rewards': [{'amount': 100, 'id32': 555, 'type': 1}],
            'taskDescription': 'Hold the line for 24 hours.',
            'tasks': [
                {'type': 1, 'valueTypes': [1, 2], 'values': [10, 20]},
                {'type': 2, 'valueTypes': [3], 'values': [5]}
            ],
            'type': 7
        }
    }]
    result = MajorOrderTransformer.transform(sample)
    assert isinstance(result, list) and len(result) == 1
    order = result[0]
    # Check all new fields
    assert order['id32'] == 1234567890
    assert order['expires_in'] == 3600
    assert order['expiry_time'] is not None
    assert order['progress'] == '[0, 1, 0]'
    assert order['flags'] == 2
    assert order['override_brief'] == 'Defend Super Earth from the Illuminate.'
    assert order['override_title'] == 'DEFENSE MISSION'
    assert order['reward'] == '{"amount": 100, "id32": 555, "type": 1}'
    assert order['rewards'] == '[{"amount": 100, "id32": 555, "type": 1}]'
    assert order['task_description'] == 'Hold the line for 24 hours.'
    assert order['tasks'] == '[{"type": 1, "valueTypes": [1, 2], "values": [10, 20]}, {"type": 2, "valueTypes": [3], "values": [5]}]'
    assert order['order_type'] == 7
    assert order['created_at'] is not None
    assert order['updated_at'] is not None
    pprint.pprint(order)

def test_planet_history_transformer():
    print('Testing PlanetHistoryTransformer...')
    sample = [{
        'planetId': 1,
        'timestamp': '2024-06-01 12:00:00',
        'status': 'Liberated',
    }]
    result = PlanetHistoryTransformer.transform(sample)
    assert isinstance(result, list) and len(result) == 1
    pprint.pprint(result)

def test_war_info_transformer():
    print('Testing WarInfoTransformer...')
    sample = {
        'warId': 801,
        'startDate': 1706040313,
        'endDate': 1833653095,
        'layoutVersion': 40,
        'minimumClientVersion': '0.3.0',
        'planetInfos': [
            {
                'index': 0,
                'position': {'x': 0, 'y': 0},
                'waypoints': [1, 2],
                'sector': 0,
                'maxHealth': 1000000,
                'disabled': False,
                'initialOwner': 1
            },
            {
                'index': 1,
                'position': {'x': 1.1, 'y': 2.2},
                'waypoints': [],
                'sector': 1,
                'maxHealth': 900000,
                'disabled': True,
                'initialOwner': 2
            }
        ],
        'homeWorlds': [
            {'race': 1, 'planetIndices': [0]},
            {'race': 2, 'planetIndices': [1]}
        ],
        'capitalInfos': [],
        'planetPermanentEffects': []
    }
    result = WarInfoTransformer.transform(sample)
    print('war_info:', result['war_info'])
    print('planet_infos:', result['planet_infos'])
    print('home_worlds:', result['home_worlds'])
    assert result['war_info']['war_id'] == 801
    assert len(result['planet_infos']) == 2
    assert result['planet_infos'][0]['planet_id'] == 0
    assert result['planet_infos'][1]['disabled'] is True
    assert len(result['home_worlds']) == 2
    assert result['home_worlds'][0]['faction_id'] == 1
    assert result['home_worlds'][1]['planet_id'] == 1

def main():
    test_planet_transformer()
    test_war_status_transformer()
    test_news_transformer()
    test_campaign_transformer()
    test_major_order_transformer()
    test_planet_history_transformer()
    test_war_info_transformer()
    print('All transformer tests passed!')

if __name__ == '__main__':
    main() 