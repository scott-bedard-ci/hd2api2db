from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

class PlanetHistoryTransformer:
    @staticmethod
    def transform(
        planet_history_data: List[Dict[str, Any]],
        planet_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Transform raw planet history data from API to database format."""
        transformed_history = []
        for entry in planet_history_data:
            transformed_item = {
                'planet_id': planet_id or entry.get('planetId'),
                'timestamp': entry.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'status': entry.get('status'),
                'current_health': entry.get('current_health'),
                'max_health': entry.get('max_health'),
                'player_count': entry.get('player_count'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            transformed_history.append(transformed_item)
        return transformed_history
