"""Fetches static war information such as planet layout and home worlds."""
from __future__ import annotations
import logging
from typing import Any
from transformers.war_info_transformer import WarInfoTransformer

class WarInfoFetcher:
    """Load and store war info, ensuring referenced factions exist."""
    def __init__(self, api_client: Any, db_manager: Any) -> None:
        self.api_client = api_client
        self.db_manager = db_manager
        self.transformer = WarInfoTransformer()
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self) -> bool:
        try:
            self.logger.info("Fetching war info data")
            war_info_data = self.api_client.get_war_info()

            self.logger.info("Transforming war info data")
            transformed = self.transformer.transform(war_info_data)

            # Ensure all referenced factions exist (by id)
            faction_ids = set()
            for pi in transformed['planet_infos']:
                if pi.get('initial_faction_id') is not None:
                    faction_ids.add(pi['initial_faction_id'])
            for hw in transformed['home_worlds']:
                if hw.get('faction_id') is not None:
                    faction_ids.add(hw['faction_id'])
            for faction_id in faction_ids:
                self.db_manager.get_or_create_faction_by_id(faction_id)

            self.logger.info("Storing war_info row")
            self.db_manager.upsert_war_info(transformed['war_info'])

            self.logger.info("Storing planet_infos rows")
            skipped = self.db_manager.upsert_planet_infos(transformed['war_info']['war_id'], transformed['planet_infos'])
            if skipped:
                for skip in skipped:
                    self.logger.warning(f"Skipped planet_info with missing planet_id: {skip['planet_id']} (error: {skip['error']})")
                self.logger.error(f"Skipped {len(skipped)} planet_infos due to missing planet_id.")

            self.logger.info("Storing home_worlds rows")
            self.db_manager.upsert_home_worlds(transformed['war_info']['war_id'], transformed['home_worlds'])

            self.logger.info("War info data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating war info data: {str(e)}")
            return False
