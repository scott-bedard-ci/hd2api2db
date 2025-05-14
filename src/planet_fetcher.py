import logging

class PlanetFetcher:
    def __init__(self, api_client, transformer, db_manager):
        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self):
        try:
            self.logger.info("Fetching planet data")
            planet_data = self.api_client.get_planets()
            if isinstance(planet_data, dict):
                planet_data = list(planet_data.values())

            self.logger.info("Transforming planet data")
            transformed_data = self.transformer.transform(planet_data)

            self.logger.info("Storing planet data")
            for planet in transformed_data:
                # 1. Biome
                biome_id = None
                if planet['biome'] and planet['biome']['slug']:
                    biome_id = self.db_manager.get_or_create_biome(
                        planet['biome']['slug'],
                        planet['biome']['description']
                    )
                # 2. Planet
                planet_id = self.db_manager.upsert_planet(planet, biome_id)
                # 3. Environmentals
                environmental_ids = []
                for env in planet['environmentals']:
                    if env['name']:
                        environmental_id = self.db_manager.get_or_create_environmental(
                            env['name'], env['description']
                        )
                        environmental_ids.append(environmental_id)
                # 4. Link planet to environmentals
                if environmental_ids:
                    self.db_manager.upsert_planet_environmentals(planet_id, environmental_ids)

            self.logger.info("Planet data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating planet data: {str(e)}")
            return False 