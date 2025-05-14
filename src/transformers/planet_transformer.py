from datetime import datetime

class PlanetTransformer:
    @staticmethod
    def transform(planets_data):
        """Transform raw planet data from API to a normalized ingest format."""
        transformed_planets = []
        for planet in planets_data:
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
                'name': planet.get('name'),
                'sector': planet.get('sector'),
                'biome': biome_info,
                'environmentals': environmentals,
            }
            transformed_planets.append(transformed_planet)
        return transformed_planets 