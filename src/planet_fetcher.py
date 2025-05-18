"""Imports planet definitions and their environmentals."""
from __future__ import annotations
import logging
from typing import Any, Iterable, Optional

class PlanetFetcher:
    """Transforms planet data and persists each record."""
    def __init__(
        self,
        api_client: Any,
        transformer: Any,
        db_manager: Any,
    ) -> None:
        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self) -> bool:
        try:
            self.logger.info("Fetching planet data")
            planet_data = self.api_client.get_planets()
            # If dict, keep items for id; if list, enumerate for id
            if isinstance(planet_data, dict):
                items = planet_data.items()
            elif isinstance(planet_data, list):
                items = enumerate(planet_data)
            else:
                self.logger.error("Unexpected planet data structure")
                return False

            self.logger.info("Transforming planet data")
            transformed_data = self.transformer.transform(items)

            self.logger.info("Storing planet data")
            for planet in transformed_data:
                print(f"Importing planet: {planet['name']} (id: {planet['id']})")
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
