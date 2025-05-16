import pytest
from database_manager import DatabaseManager
from test_utils import clean_test_db, assert_using_test_db
import json

def test_upsert_planet():
    db = DatabaseManager()
    # Ensure biome_id=1 exists
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO biomes (id, slug, description) VALUES (1, 'test-biome', 'Test Biome')")
    conn.commit()
    cursor.close()
    conn.close()
    planet_id = db.upsert_planet({'id': 123, 'name': 'TestPlanet', 'sector': 1}, biome_id=1)
    assert planet_id == 123

def test_upsert_planet_id_zero():
    db = DatabaseManager()
    # Ensure biome_id=1 exists
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO biomes (id, slug, description) VALUES (1, 'test-biome', 'Test Biome')")
    conn.commit()
    cursor.close()
    conn.close()
    # Test upserting planet_id 0 (Super Earth)
    planet_id = db.upsert_planet({'id': 0, 'name': 'Super Earth', 'sector': 0}, biome_id=1)
    assert planet_id == 0

def test_upsert_war_status():
    db = DatabaseManager()
    data = {
        'war_status': {'war_id': 1, 'time': '2024-01-01 00:00:00', 'impact_multiplier': 1.0, 'story_beat_id32': 0, 'created_at': '2024-01-01 00:00:00'},
        'planet_status': []
    }
    db.upsert_war_status(data)

def test_upsert_news():
    db = DatabaseManager()
    news_data = {'id': 1, 'published': '2024-01-01 00:00:00', 'type': 'news', 'tagIds': '[]', 'message': 'Test', 'created_at': '2024-01-01 00:00:00'}
    db.upsert_news(news_data)

def test_upsert_campaign():
    db = DatabaseManager()
    # Ensure biome_id=1 exists
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO biomes (id, slug, description) VALUES (1, 'test-biome', 'Test Biome')")
    conn.commit()
    cursor.close()
    conn.close()
    campaign_data = {'name': 'Operation Freedom', 'planet_index': 1, 'defense': 100, 'expire_datetime': '2024-01-01 00:00:00', 'health': 100, 'max_health': 200, 'percentage': 50, 'players': 10}
    db.upsert_campaign(campaign_data, biome_id=1, faction_id=1)

def test_upsert_major_order():
    db = DatabaseManager()
    major_order_data = {
        'id32': 1,
        'expires_in': 1000,
        'expiry_time': '2024-01-01 00:00:00',
        'progress': json.dumps({}),
        'flags': 0,
        'override_brief': '',
        'override_title': '',
        'reward': json.dumps({}),
        'rewards': json.dumps([]),
        'task_description': '',
        'tasks': json.dumps([]),
        'order_type': 0,
        'created_at': '2024-01-01 00:00:00',
        'updated_at': '2024-01-01 00:00:00'
    }
    db.upsert_major_order(major_order_data)

def test_upsert_planet_history():
    db = DatabaseManager()
    planet_history_data = {'planet_id': 1, 'timestamp': '2024-01-01 00:00:00', 'status': 'Liberated', 'current_health': 100, 'max_health': 200, 'player_count': 10}
    db.upsert_planet_history(planet_history_data) 