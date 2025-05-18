"""Transforms campaign API responses into DB-ready dictionaries."""
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List

class CampaignTransformer:
    @staticmethod
    def transform(campaign_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform raw campaign data from API to normalized ingest format."""
        transformed_campaigns = []
        for campaign in campaign_data:
            # Biome info
            biome = campaign.get('biome')
            biome_info = None
            if biome:
                biome_info = {
                    'slug': biome.get('slug'),
                    'description': biome.get('description'),
                }
            # Faction info
            faction_name = campaign.get('faction')
            # Expire datetime
            expire_dt = None
            expire_raw = campaign.get('expireDateTime')
            if expire_raw:
                try:
                    expire_dt = datetime.utcfromtimestamp(float(expire_raw)).strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    expire_dt = None
            transformed_item = {
                'name': campaign.get('name'),
                'planet_index': campaign.get('planetIndex'),
                'biome': biome_info,
                'faction': faction_name,
                'defense': campaign.get('defense'),
                'expire_datetime': expire_dt,
                'health': campaign.get('health'),
                'max_health': campaign.get('maxHealth'),
                'percentage': campaign.get('percentage'),
                'players': campaign.get('players'),
            }
            transformed_campaigns.append(transformed_item)
        return transformed_campaigns
