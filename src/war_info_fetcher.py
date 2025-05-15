import logging
from transformers.war_info_transformer import WarInfoTransformer

class WarInfoFetcher:
    def __init__(self, api_client, db_manager):
        self.api_client = api_client
        self.db_manager = db_manager
        self.transformer = WarInfoTransformer()
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self):
        try:
            self.logger.info("Fetching war info data")
            war_info_data = self.api_client.get_war_info()

            self.logger.info("Transforming war info data")
            transformed = self.transformer.transform(war_info_data)

            self.logger.info("Storing war_info row")
            self.db_manager.upsert_war_info(transformed['war_info'])

            self.logger.info("Storing planet_infos rows")
            self.db_manager.upsert_planet_infos(transformed['war_info']['war_id'], transformed['planet_infos'])

            self.logger.info("Storing home_worlds rows")
            self.db_manager.upsert_home_worlds(transformed['war_info']['war_id'], transformed['home_worlds'])

            self.logger.info("War info data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating war info data: {str(e)}")
            return False 