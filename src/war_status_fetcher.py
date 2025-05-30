"""Updates the current war status and planet metrics."""
from __future__ import annotations
import logging
from typing import Any

class WarStatusFetcher:
    """Handles fetching, transforming and persisting war status."""
    def __init__(self, api_client: Any, transformer: Any, db_manager: Any) -> None:

        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self) -> bool:
        try:
            self.logger.info("Fetching war status data")
            war_status_data = self.api_client.get_war_status()

            self.logger.info("Transforming war status data")
            transformed_data = self.transformer.transform(war_status_data)

            self.logger.info("Storing war status data")
            self.db_manager.upsert_war_status(transformed_data)

            self.logger.info("War status data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating war status data: {str(e)}")
            return False
