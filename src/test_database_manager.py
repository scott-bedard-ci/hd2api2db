import os
os.environ['DB_NAME'] = 'helldivers2_test'
from database_manager import DatabaseManager
import datetime
from test_utils import clean_test_db, assert_using_test_db

def main():
    assert_using_test_db()
    clean_test_db()
    db = DatabaseManager()

    # Test upsert_planet
    print('Testing upsert_planet...')
    db.upsert_planet({
        'name': 'Super Earth',
        'sector': 'Alpha',
        'region': 'North',
        'liberation_status': 'Liberated',
    })
    print('upsert_planet OK')

    # Test upsert_war_status
    print('Testing upsert_war_status...')
    db.upsert_war_status({
        'war_status': {
            'war_id': 801,
            'time': '2024-06-01 12:00:00',
            'impact_multiplier': 0.0128,
            'story_beat_id32': 724770796,
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        },
        'planet_status': [
            {
                'war_id': 801,
                'planet_index': 0,
                'owner': 1,
                'health': 1000000,
                'regen_per_second': 1388.8889,
                'players': 649,
                'position_x': 0.0,
                'position_y': 0.0,
            },
            {
                'war_id': 801,
                'planet_index': 1,
                'owner': 1,
                'health': 1000000,
                'regen_per_second': 1388.8889,
                'players': 0,
                'position_x': 0.05,
                'position_y': 0.10,
            }
        ]
    })
    print('upsert_war_status OK')

    # Test upsert_news
    print('Testing upsert_news...')
    db.upsert_news({
        'id': 101,
        'published': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'announcement',
        'tagIds': '[1, 2, 3]',
        'message': 'Helldivers unite!',
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })
    print('upsert_news OK')

    # Test upsert_campaign
    print('Testing upsert_campaign...')
    db.upsert_campaign({
        'name': 'Operation Freedom',
        'description': 'Free all planets.',
        'start_date': datetime.date.today().strftime('%Y-%m-%d'),
        'end_date': (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
    })
    print('upsert_campaign OK')

    # Test upsert_major_order
    print('Testing upsert_major_order...')
    db.upsert_major_order({
        'description': 'Defend Super Earth',
        'target_planet_id': 1,
        'expiry_time': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
    })
    print('upsert_major_order OK')

    # Test upsert_planet_history
    print('Testing upsert_planet_history...')
    db.upsert_planet_history({
        'planet_id': 1,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'Liberated',
    })
    print('upsert_planet_history OK')

    print('All DatabaseManager upsert tests passed!')
    clean_test_db()

if __name__ == '__main__':
    main() 