from datetime import datetime

class PlanetTransformer:
    @staticmethod
    def transform(planet_items):
        """Transform (planet_id, planet_data) pairs from API to a normalized ingest format with id."""
        transformed_planets = []
        for planet_id, planet in planet_items:
            biome = planet.get('biome')
            if biome:
                biome_info = {
                    'slug': biome.get('slug'),
                    'description': biome.get('description'),
                }
            else:
                biome_info = None
            environmentals = [
                {'name': env.get('name'), 'description': env.get('description')}
                for env in planet.get('environmentals', [])
            ]
            transformed_planet = {
                'id': int(planet_id),
                'name': planet.get('name'),
                'sector': planet.get('sector'),
                'biome': biome_info,
                'environmentals': environmentals,
            }
            transformed_planets.append(transformed_planet)
        return transformed_planets 