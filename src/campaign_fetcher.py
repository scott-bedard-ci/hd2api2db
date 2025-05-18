from __future__ import annotations

import logging
from typing import Any

class CampaignFetcher:
    def __init__(self, api_client: Any, transformer: Any, db_manager: Any) -> None:
        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self) -> bool:
        try:
            self.logger.info("Fetching campaign data")
            campaign_data = self.api_client.get_campaigns()

            self.logger.info("Transforming campaign data")
            transformed_data = self.transformer.transform(campaign_data)

            self.logger.info("Storing campaign data")
            for campaign in transformed_data:
                print(f"Importing campaign: {campaign['name']}")
                # 1. Biome
                biome_id = None
                if campaign['biome'] and campaign['biome']['slug']:
                    biome_id = self.db_manager.get_or_create_biome(
                        campaign['biome']['slug'],
                        campaign['biome']['description']
                    )
                # 2. Faction
                faction_id = None
                if campaign['faction']:
                    faction_id = self.db_manager.get_or_create_faction(campaign['faction'])
                # 3. Upsert campaign
                self.db_manager.upsert_campaign(campaign, biome_id, faction_id)

            self.logger.info("Campaign data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating campaign data: {str(e)}")
            return False
