from __future__ import annotations

import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
from mysql.connector import errors as mysql_errors
from typing import Any, Dict, Iterable, List, Optional

load_dotenv()

# Helper to select DB credentials based on USE_TEST_DB
def get_db_credentials() -> Dict[str, Any]:
    use_test_db = os.getenv("USE_TEST_DB", "false").lower() == "true"
    prefix = "TEST_DB_" if use_test_db else "LIVE_DB_"
    return {
        "host": os.getenv(f"{prefix}HOST", "localhost"),
        "port": int(os.getenv(f"{prefix}PORT", 3306)),
        "user": os.getenv(f"{prefix}USER", "root"),
        "password": os.getenv(f"{prefix}PASSWORD", ""),
        "database": os.getenv(f"{prefix}NAME", "helldivers2_test" if use_test_db else "helldivers2"),
    }

class DatabaseManager:
    def __init__(self) -> None:
        creds = get_db_credentials()
        self.pool = pooling.MySQLConnectionPool(
            pool_name="helldivers2_pool",
            pool_size=5,
            host=creds["host"],
            port=creds["port"],
            user=creds["user"],
            password=creds["password"],
            database=creds["database"],
        )

    def get_connection(self) -> Any:
        return self.pool.get_connection()

    def upsert_planet(self, planet_data: Dict[str, Any], biome_id: Optional[int]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Upsert by id (from API)
            cursor.execute("SELECT id FROM planets WHERE id = %s", (planet_data['id'],))
            row = cursor.fetchone()
            if row:
                planet_id = row[0]
                cursor.execute("UPDATE planets SET name = %s, sector = %s, biome_id = %s WHERE id = %s", (planet_data['name'], planet_data['sector'], biome_id, planet_id))
            else:
                cursor.execute("INSERT INTO planets (id, name, sector, biome_id) VALUES (%s, %s, %s, %s)", (planet_data['id'], planet_data['name'], planet_data['sector'], biome_id))
                planet_id = planet_data['id']
            conn.commit()
            return planet_id
        finally:
            cursor.close()
            conn.close()

    def upsert_war_status(self, data: Dict[str, Any]) -> None:
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

    def upsert_news(self, news_data: Dict[str, Any]) -> None:
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

    def upsert_campaign(
        self,
        campaign_data: Dict[str, Any],
        biome_id: Optional[int],
        faction_id: Optional[int],
    ) -> None:
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

    def upsert_major_order(self, major_order_data: Dict[str, Any]) -> None:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO major_orders (
                id32, expires_in, expiry_time, progress, flags, override_brief, override_title, reward, rewards, task_description, tasks, order_type, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                expires_in=VALUES(expires_in),
                expiry_time=VALUES(expiry_time),
                progress=VALUES(progress),
                flags=VALUES(flags),
                override_brief=VALUES(override_brief),
                override_title=VALUES(override_title),
                reward=VALUES(reward),
                rewards=VALUES(rewards),
                task_description=VALUES(task_description),
                tasks=VALUES(tasks),
                order_type=VALUES(order_type),
                updated_at=VALUES(updated_at)
            """
            cursor.execute(query, (
                major_order_data['id32'],
                major_order_data['expires_in'],
                major_order_data['expiry_time'],
                major_order_data['progress'],
                major_order_data['flags'],
                major_order_data['override_brief'],
                major_order_data['override_title'],
                major_order_data['reward'],
                major_order_data['rewards'],
                major_order_data['task_description'],
                major_order_data['tasks'],
                major_order_data['order_type'],
                major_order_data['created_at'],
                major_order_data['updated_at'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_planet_history(self, planet_history_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        missing_planet_ids = []
        try:
            query = """
            INSERT INTO planet_history (planet_id, timestamp, status, current_health, max_health, player_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                status=VALUES(status),
                current_health=VALUES(current_health),
                max_health=VALUES(max_health),
                player_count=VALUES(player_count)
            """
            try:
                cursor.execute(query, (
                    planet_history_data['planet_id'],
                    planet_history_data['timestamp'],
                    planet_history_data['status'],
                    planet_history_data['current_health'],
                    planet_history_data['max_health'],
                    planet_history_data['player_count'],
                ))
                conn.commit()
                return None  # No error
            except mysql_errors.IntegrityError as e:
                conn.rollback()
                if e.errno == 1452:
                    missing_planet_ids.append(planet_history_data['planet_id'])
                    return {
                        'missing_planet_id': planet_history_data['planet_id'],
                        'context': {
                            'timestamp': planet_history_data.get('timestamp'),
                            'status': planet_history_data.get('status'),
                        },
                        'error': str(e)
                    }
                else:
                    raise
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def get_or_create_biome(self, slug: str, description: str) -> int:
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

    def get_or_create_environmental(self, name: str, description: str) -> int:
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

    def upsert_planet_environmentals(self, planet_id: int, environmental_ids: Iterable[int]) -> None:
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

    def get_or_create_faction(self, name: str) -> int:
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

    def get_or_create_faction_by_id(self, faction_id: int) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM factions WHERE id = %s", (faction_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            cursor.execute("INSERT INTO factions (id, name) VALUES (%s, %s)", (faction_id, f"Unknown ({faction_id})"))
            conn.commit()
            return faction_id
        finally:
            cursor.close()
            conn.close()

    def upsert_war_info(self, war_info_data: Dict[str, Any]) -> None:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO war_info (war_id, start_date, end_date, layout_version, minimum_client_version, capital_infos, planet_permanent_effects, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                start_date=VALUES(start_date),
                end_date=VALUES(end_date),
                layout_version=VALUES(layout_version),
                minimum_client_version=VALUES(minimum_client_version),
                capital_infos=VALUES(capital_infos),
                planet_permanent_effects=VALUES(planet_permanent_effects),
                updated_at=NOW()
            """
            cursor.execute(query, (
                war_info_data['war_id'],
                war_info_data['start_date'],
                war_info_data['end_date'],
                war_info_data['layout_version'],
                war_info_data['minimum_client_version'],
                war_info_data['capital_infos'],
                war_info_data['planet_permanent_effects'],
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_planet_infos(self, war_id: int, planet_infos: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        skipped = []
        try:
            # Delete existing planet_infos for this war_id
            cursor.execute("DELETE FROM planet_infos WHERE war_id = %s", (war_id,))
            # Insert new planet_infos one by one, robust to FK errors
            query = """
            INSERT INTO planet_infos (war_id, planet_id, position_x, position_y, waypoints, sector, max_health, disabled, initial_faction_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for pi in planet_infos:
                try:
                    cursor.execute(query, (
                        war_id,
                        pi['planet_id'],
                        pi['position_x'],
                        pi['position_y'],
                        pi['waypoints'],
                        pi['sector'],
                        pi['max_health'],
                        pi['disabled'],
                        pi['initial_faction_id'],
                    ))
                except mysql.connector.errors.IntegrityError as e:
                    if e.errno == 1452:
                        skipped.append({'planet_id': pi['planet_id'], 'error': str(e)})
                    else:
                        raise
            conn.commit()
            return skipped
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def upsert_home_worlds(self, war_id: int, home_worlds: Iterable[Dict[str, Any]]) -> None:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Delete existing home_worlds for this war_id
            cursor.execute("DELETE FROM home_worlds WHERE war_id = %s", (war_id,))
            # Bulk insert new home_worlds
            query = """
            INSERT INTO home_worlds (war_id, faction_id, planet_id)
            VALUES (%s, %s, %s)
            """
            values = [(
                war_id,
                hw['faction_id'],
                hw['planet_id'],
            ) for hw in home_worlds]
            if values:
                cursor.executemany(query, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    # Add similar methods for war_status, news, campaigns, major_orders, planet_history
