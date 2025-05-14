from datetime import datetime

class PlanetHistoryTransformer:
    @staticmethod
    def transform(planet_history_data, planet_id=None):
        """Transform raw planet history data from API to database format."""
        transformed_history = []
        for entry in planet_history_data:
            transformed_item = {
                'planet_id': planet_id or entry.get('planetId'),
                'timestamp': entry.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'status': entry.get('status'),
                # Add other fields as needed based on your schema
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            transformed_history.append(transformed_item)
        return transformed_history 