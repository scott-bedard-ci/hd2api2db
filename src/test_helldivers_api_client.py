import logging
from helldivers_api_client import Helldivers2ApiClient
import pprint

logging.basicConfig(level=logging.INFO)

def main():
    client = Helldivers2ApiClient(max_retries=2, timeout=5)

    print('Testing get_war_status...')
    war_status = client.get_war_status()
    assert war_status is not None, 'get_war_status() returned None'
    print('get_war_status() OK:', type(war_status), '\n')

    print('Testing get_war_info...')
    war_info = client.get_war_info()
    assert war_info is not None, 'get_war_info() returned None'
    print('get_war_info() OK:', type(war_info), '\n')
    print('Sample war_info response:')
    pprint.pprint(war_info)

    print('Testing get_news...')
    news = client.get_news()
    assert news is not None, 'get_news() returned None'
    print('get_news() OK:', type(news), '\n')

    print('Testing get_campaign...')
    campaign = client.get_campaign()
    assert campaign is not None, 'get_campaign() returned None'
    print('get_campaign() OK:', type(campaign), '\n')

    print('Testing get_major_orders...')
    major_orders = client.get_major_orders()
    assert major_orders is not None, 'get_major_orders() returned None'
    print('get_major_orders() OK:', type(major_orders), '\n')
    print('Sample major_orders response:')
    pprint.pprint(major_orders)

    print('Testing get_planets...')
    planets = client.get_planets()
    assert planets is not None, 'get_planets() returned None'
    print('get_planets() OK:', type(planets), '\n')

    print('Testing get_planet_history (planet_index=127)...')
    planet_history = client.get_planet_history(127)
    assert planet_history is not None, 'get_planet_history() returned None'
    print('get_planet_history() OK:', type(planet_history), '\n')
    print('Sample planet_history response:')
    pprint.pprint(planet_history)

    print('All API client tests passed!')

if __name__ == '__main__':
    main() 