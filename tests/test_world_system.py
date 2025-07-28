"""
Tests para el sistema de mundo y tiles
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Tests unitarios para el sistema de mundo y tiles.
"""

import pytest
import pygame
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.tile import Tile, TileType
from src.utils.world_generator import WorldGenerator


class TestWorldSystem:
	"""Tests para el sistema de mundo y tiles."""
	
	@pytest.fixture(autouse=True)
	def setup(self):
		"""Configuración inicial para los tests."""
		pygame.init()
		pygame.display.set_mode((800, 600))  # Necesario para cargar imágenes
		
		yield
		
		pygame.quit()
	
	def test_tile_creation(self):
		"""Test de creación de tiles."""
		# Crear tile de árbol
		tile = Tile(100, 100, TileType.TREE)
		
		assert tile.tile_type == TileType.TREE
		assert tile.x == 100
		assert tile.y == 100
		assert tile.is_alive
		assert tile.sprite is not None
		assert tile.width == 80
		assert tile.height == 120
	
	def test_tile_collision(self):
		"""Test de colisiones de tiles."""
		# Tile con colisión
		tree = Tile(100, 100, TileType.TREE)
		assert tree.has_collision() == True
		
		# Tile sin colisión
		flower = Tile(200, 200, TileType.FLOWER)
		assert flower.has_collision() == False
	
	def test_tile_info(self):
		"""Test de información de tiles."""
		tile = Tile(150, 150, TileType.ROCK)
		info = tile.get_tile_info()
		
		assert info["type"] == "rock"
		assert info["name"] == "Roca"
		assert info["position"] == (150, 150)
		assert info["collision"] == True
	
	def test_random_tile_creation(self):
		"""Test de creación de tiles aleatorios."""
		tile = Tile.create_random(300, 300)
		
		assert tile.x == 300
		assert tile.y == 300
		assert tile.tile_type in TileType
		assert tile.is_alive
	
	def test_world_generator_creation(self):
		"""Test de creación del generador de mundo."""
		generator = WorldGenerator(1000, 1000)
		
		assert generator.world_width == 1000
		assert generator.world_height == 1000
		assert generator.tile_density > 0
		assert generator.min_distance > 0
	
	def test_world_generation(self):
		"""Test de generación de mundo básico."""
		generator = WorldGenerator(2000, 2000)
		tiles = generator.generate_world()
		
		assert len(tiles) > 0
		assert all(isinstance(tile, Tile) for tile in tiles)
		
		# Verificar que no hay tiles en la zona segura
		center_x, center_y = 1000, 1000
		for tile in tiles:
			distance = ((tile.x - center_x) ** 2 + (tile.y - center_y) ** 2) ** 0.5
			assert distance >= generator.safe_zone_radius
	
	def test_cluster_generation(self):
		"""Test de generación de clusters."""
		generator = WorldGenerator(1000, 1000)
		
		# Generar cluster de árboles
		forest_tiles = generator.generate_cluster(500, 500, 100, 10, [TileType.TREE])
		
		assert len(forest_tiles) == 10
		assert all(tile.tile_type == TileType.TREE for tile in forest_tiles)
		
		# Verificar que están dentro del radio
		for tile in forest_tiles:
			distance = ((tile.x - 500) ** 2 + (tile.y - 500) ** 2) ** 0.5
			assert distance <= 100
	
	def test_special_area_generation(self):
		"""Test de generación de áreas especiales."""
		generator = WorldGenerator(1000, 1000)
		
		# Bosque
		forest = generator.generate_forest(200, 200, 150)
		assert len(forest) == 20
		assert all(tile.tile_type in [TileType.TREE, TileType.BUSH] for tile in forest)
		
		# Campo de cristales
		crystals = generator.generate_crystal_field(800, 200, 100)
		assert len(crystals) == 15
		assert all(tile.tile_type == TileType.CRYSTAL for tile in crystals)
		
		# Formación de rocas
		rocks = generator.generate_rock_formation(200, 800, 80)
		assert len(rocks) == 10
		assert all(tile.tile_type == TileType.ROCK for tile in rocks)
		
		# Jardín
		garden = generator.generate_garden(800, 800, 120)
		assert len(garden) == 25
		assert all(tile.tile_type in [TileType.FLOWER, TileType.BUSH] for tile in garden)
	
	def test_tile_distribution(self):
		"""Test de distribución de tiles."""
		generator = WorldGenerator(1000, 1000)
		tiles = generator.generate_world()
		
		# Verificar que no hay tiles muy cercanos
		for i, tile1 in enumerate(tiles):
			for tile2 in tiles[i+1:]:
				distance = ((tile1.x - tile2.x) ** 2 + (tile1.y - tile2.y) ** 2) ** 0.5
				assert distance >= generator.min_distance or distance == 0
	
	def test_tile_types_coverage(self):
		"""Test de cobertura de tipos de tiles."""
		all_types = Tile.get_all_types()
		assert len(all_types) == 6  # TREE, ROCK, BUSH, FLOWER, CRYSTAL, ALTAR
		
		# Verificar que todos los tipos están en la configuración
		for tile_type in all_types:
			assert tile_type in Tile.TILE_CONFIGS
			config = Tile.TILE_CONFIGS[tile_type]
			assert "name" in config
			assert "color" in config
			assert "collision" in config
			assert "symbol" in config
	
	def test_tile_rendering(self):
		"""Test de renderizado de tiles."""
		tile = Tile(100, 100, TileType.ALTAR)
		
		# Verificar que tiene sprite
		assert tile.sprite is not None
		assert tile.sprite.get_width() == tile.width
		assert tile.sprite.get_height() == tile.height


if __name__ == "__main__":
	pytest.main([__file__]) 