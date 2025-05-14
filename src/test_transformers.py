import os
os.environ['DB_NAME'] = 'helldivers2_test'
from transformers.planet_transformer import PlanetTransformer
from transformers.war_status_transformer import WarStatusTransformer
from transformers.news_transformer import NewsTransformer
from transformers.campaign_transformer import CampaignTransformer
from transformers.major_order_transformer import MajorOrderTransformer
from transformers.planet_history_transformer import PlanetHistoryTransformer
import pprint

def test_planet_transformer():
    print('Testing PlanetTransformer...')
    sample = [{
        'name': 'Super Earth',
        'sector': 'Alpha',
        'region': 'North',
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
        'description': 'Defend Super Earth',
        'targetPlanetId': 1,
        'expiryTime': '2024-06-05 23:59:59',
    }]
    result = MajorOrderTransformer.transform(sample)
    assert isinstance(result, list) and len(result) == 1
    pprint.pprint(result)

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

def main():
    test_planet_transformer()
    test_war_status_transformer()
    test_news_transformer()
    test_campaign_transformer()
    test_major_order_transformer()
    test_planet_history_transformer()
    print('All transformer tests passed!')

if __name__ == '__main__':
    main() 