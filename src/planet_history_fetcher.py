import logging

class PlanetHistoryFetcher:
    def __init__(self, api_client, transformer, db_manager):
        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self):
        try:
            self.logger.info("Fetching all planets for history update")
            planets = self.api_client.get_planets()
            success_count = 0
            failure_count = 0

            if isinstance(planets, dict):
                items = planets.items()
            elif isinstance(planets, list):
                items = enumerate(planets)
            else:
                self.logger.error("Unexpected planets data structure")
                return False

            for planet_id, planet in items:
                try:
                    self.logger.info(f"Fetching history for planet {planet.get('name')} (id: {planet_id})")
                    history_data = self.api_client.get_planet_history(planet_id)
                    transformed_data = self.transformer.transform(history_data, planet_id)
                    for entry in transformed_data:
                        self.db_manager.upsert_planet_history(entry)
                    success_count += 1
                except Exception as e:
                    self.logger.error(f"Error fetching history for planet {planet_id}: {str(e)}")
                    failure_count += 1

            self.logger.info(f"Planet history update completed. Success: {success_count}, Failures: {failure_count}")
            return success_count > 0
        except Exception as e:
            self.logger.error(f"Error in planet history update process: {str(e)}")
            return False 