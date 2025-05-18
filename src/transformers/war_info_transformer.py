from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

class WarInfoTransformer:
    @staticmethod
    def transform(war_info_data: Dict[str, Any]) -> Dict[str, Any]:
        # Top-level war_info row
        war_info = {
            'war_id': war_info_data['warId'],
            'start_date': datetime.fromtimestamp(war_info_data['startDate']),
            'end_date': datetime.fromtimestamp(war_info_data['endDate']),
            'layout_version': war_info_data.get('layoutVersion'),
            'minimum_client_version': war_info_data.get('minimumClientVersion'),
            'capital_infos': json.dumps(war_info_data.get('capitalInfos', [])),
            'planet_permanent_effects': json.dumps(war_info_data.get('planetPermanentEffects', [])),
        }

        # planet_infos rows
        planet_infos = []
        for pi in war_info_data.get('planetInfos', []):
            planet_infos.append({
                'planet_id': pi['index'],
                'position_x': pi['position']['x'],
                'position_y': pi['position']['y'],
                'waypoints': json.dumps(pi.get('waypoints', [])),
                'sector': pi.get('sector'),
                'max_health': pi.get('maxHealth'),
                'disabled': pi.get('disabled'),
                'initial_faction_id': pi.get('initialOwner'),
            })

        # home_worlds rows
        home_worlds = []
        for hw in war_info_data.get('homeWorlds', []):
            faction_id = hw['race']
            for planet_id in hw.get('planetIndices', []):
                home_worlds.append({
                    'faction_id': faction_id,
                    'planet_id': planet_id
                })

        return {
            'war_info': war_info,
            'planet_infos': planet_infos,
            'home_worlds': home_worlds
        }
