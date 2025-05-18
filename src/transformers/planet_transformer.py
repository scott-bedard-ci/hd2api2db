"""Normalizes planet API results for database insertion."""
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Iterable, List

class PlanetTransformer:
    @staticmethod
    def transform(planet_items: Iterable[tuple[int, Dict[str, Any]]]) -> List[Dict[str, Any]]:
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
