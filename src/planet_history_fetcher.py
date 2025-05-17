"""Collects historical planet data for all planets."""

import logging

class PlanetHistoryFetcher:
    """Downloads planet history and records each entry."""
    def __init__(self, api_client, transformer, db_manager):
        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)  # Only log ERROR and above for this fetcher

    def fetch_and_store(self):
        try:
            self.logger.info("Fetching all planets for history update")
            planets = self.api_client.get_planets()
            success_count = 0
            failure_count = 0
            missing_planet_errors = []
            missing_planet_ids = set()

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
                        entry['planet_id'] = planet_id
                        result = self.db_manager.upsert_planet_history(entry)
                        if result and 'missing_planet_id' in result:
                            missing_planet_errors.append(result)
                            missing_planet_ids.add(result['missing_planet_id'])
                    success_count += 1
                except Exception as e:
                    self.logger.error(f"Error fetching history for planet {planet_id}: {str(e)}")
                    failure_count += 1

            self.logger.info(f"Planet history update completed. Success: {success_count}, Failures: {failure_count}")
            if missing_planet_errors:
                self.logger.warning(f"Missing planet_id errors encountered during ingestion:")
                for err in missing_planet_errors:
                    self.logger.warning(f"  planet_id={err['missing_planet_id']} context={err['context']} error={err['error']}")
            if missing_planet_ids:
                print(f"\nWARNING: The following planet_ids were referenced in planet_history but do not exist in the planets table: {sorted(missing_planet_ids)}\n")
            return {
                'success': success_count,
                'failures': failure_count,
                'missing_planet_errors': missing_planet_errors
            }
        except Exception as e:
            self.logger.error(f"Error in planet history update process: {str(e)}")
            return False 