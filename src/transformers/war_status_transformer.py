"""Transforms war status responses into database-friendly structures."""

from datetime import datetime, UTC

class WarStatusTransformer:
    @staticmethod
    def transform(war_status_data):
        """Transform raw war status data from API to database format.
        Returns a dict with 'war_status' and 'planet_status' keys.
        """
        # Convert 'time' from int (seconds since epoch) to MySQL DATETIME string
        time_raw = war_status_data.get('time')
        if isinstance(time_raw, int):
            time_dt = datetime.fromtimestamp(time_raw, tz=UTC)
            time_str = time_dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            time_str = str(time_raw)
        war_status = {
            'war_id': war_status_data['warId'],
            'time': time_str,
            'impact_multiplier': war_status_data.get('impactMultiplier'),
            'story_beat_id32': war_status_data.get('storyBeatId32'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        planet_status_list = []
        for planet in war_status_data.get('planetStatus', []):
            planet_status = {
                'war_id': war_status_data['warId'],
                'planet_index': planet.get('index'),
                'owner': planet.get('owner'),
                'health': planet.get('health'),
                'regen_per_second': planet.get('regenPerSecond'),
                'players': planet.get('players'),
                'position_x': planet.get('position', {}).get('x'),
                'position_y': planet.get('position', {}).get('y'),
            }
            planet_status_list.append(planet_status)
        return {'war_status': war_status, 'planet_status': planet_status_list} 