import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="helldivers2_pool",
            pool_size=5,
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "helldivers2"),
        )

    def get_connection(self):
        return self.pool.get_connection()

    def upsert_planet(self, planet_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO planets (name, sector, region, liberation_status)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                sector=VALUES(sector),
                region=VALUES(region),
                liberation_status=VALUES(liberation_status)
            """
            cursor.execute(query, (
                planet_data['name'],
                planet_data['sector'],
                planet_data['region'],
                planet_data['liberation_status'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_war_status(self, data):
        """
        Expects data to be a dict with 'war_status' and 'planet_status' keys.
        'war_status' is a dict for the war_status table.
        'planet_status' is a list of dicts for the planet_status table.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Upsert war_status
            ws = data['war_status']
            query_ws = """
            INSERT INTO war_status (war_id, time, impact_multiplier, story_beat_id32, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                time=VALUES(time),
                impact_multiplier=VALUES(impact_multiplier),
                story_beat_id32=VALUES(story_beat_id32)
            """
            cursor.execute(query_ws, (
                ws['war_id'],
                ws['time'],
                ws['impact_multiplier'],
                ws['story_beat_id32'],
                ws['created_at'],
            ))
            # Upsert planet_status (replace all for this war_id)
            # First, delete existing planet_status for this war_id
            cursor.execute("DELETE FROM planet_status WHERE war_id = %s", (ws['war_id'],))
            # Then, bulk insert
            ps_list = data['planet_status']
            if ps_list:
                query_ps = """
                INSERT INTO planet_status (war_id, planet_index, owner, health, regen_per_second, players, position_x, position_y)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [(
                    ps['war_id'],
                    ps['planet_index'],
                    ps['owner'],
                    ps['health'],
                    ps['regen_per_second'],
                    ps['players'],
                    ps['position_x'],
                    ps['position_y'],
                ) for ps in ps_list]
                cursor.executemany(query_ps, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_news(self, news_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO news (id, published, type, tagIds, message, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                published=VALUES(published),
                type=VALUES(type),
                tagIds=VALUES(tagIds),
                message=VALUES(message)
            """
            cursor.execute(query, (
                news_data['id'],
                news_data['published'],
                news_data['type'],
                news_data['tagIds'],
                news_data['message'],
                news_data['created_at'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_campaign(self, campaign_data, biome_id, faction_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO campaigns (name, planet_index, biome_id, faction_id, defense, expire_datetime, health, max_health, percentage, players)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                biome_id=VALUES(biome_id),
                faction_id=VALUES(faction_id),
                defense=VALUES(defense),
                expire_datetime=VALUES(expire_datetime),
                health=VALUES(health),
                max_health=VALUES(max_health),
                percentage=VALUES(percentage),
                players=VALUES(players)
            """
            cursor.execute(query, (
                campaign_data['name'],
                campaign_data['planet_index'],
                biome_id,
                faction_id,
                campaign_data['defense'],
                campaign_data['expire_datetime'],
                campaign_data['health'],
                campaign_data['max_health'],
                campaign_data['percentage'],
                campaign_data['players'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_major_order(self, major_order_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO major_orders (description, target_planet_id, expiry_time)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                target_planet_id=VALUES(target_planet_id),
                expiry_time=VALUES(expiry_time)
            """
            cursor.execute(query, (
                major_order_data['description'],
                major_order_data['target_planet_id'],
                major_order_data['expiry_time'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_planet_history(self, planet_history_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO planet_history (planet_id, timestamp, status)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                status=VALUES(status)
            """
            cursor.execute(query, (
                planet_history_data['planet_id'],
                planet_history_data['timestamp'],
                planet_history_data['status'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def get_or_create_biome(self, slug, description):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM biomes WHERE slug = %s", (slug,))
            row = cursor.fetchone()
            if row:
                return row[0]
            cursor.execute("INSERT INTO biomes (slug, description) VALUES (%s, %s)", (slug, description))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_or_create_environmental(self, name, description):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM environmentals WHERE name = %s", (name,))
            row = cursor.fetchone()
            if row:
                return row[0]
            cursor.execute("INSERT INTO environmentals (name, description) VALUES (%s, %s)", (name, description))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def upsert_planet(self, planet_data, biome_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Upsert by name and sector (assume unique together)
            cursor.execute("SELECT id FROM planets WHERE name = %s AND sector = %s", (planet_data['name'], planet_data['sector']))
            row = cursor.fetchone()
            if row:
                planet_id = row[0]
                cursor.execute("UPDATE planets SET biome_id = %s WHERE id = %s", (biome_id, planet_id))
            else:
                cursor.execute("INSERT INTO planets (name, sector, biome_id) VALUES (%s, %s, %s)", (planet_data['name'], planet_data['sector'], biome_id))
                planet_id = cursor.lastrowid
            conn.commit()
            return planet_id
        finally:
            cursor.close()
            conn.close()

    def upsert_planet_environmentals(self, planet_id, environmental_ids):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for environmental_id in environmental_ids:
                cursor.execute(
                    "INSERT IGNORE INTO planet_environmentals (planet_id, environmental_id) VALUES (%s, %s)",
                    (planet_id, environmental_id)
                )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_or_create_faction(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM factions WHERE name = %s", (name,))
            row = cursor.fetchone()
            if row:
                return row[0]
            cursor.execute("INSERT INTO factions (name) VALUES (%s)", (name,))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # Add similar methods for war_status, news, campaigns, major_orders, planet_history 