"""
Tests para el sistema de enemigos avanzados
========================================

Autor: SiK Team
Fecha: 2024
Descripción: Tests unitarios para el sistema de enemigos con tipos y comportamientos.
"""

import pytest
import pygame
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.enemy_types import EnemyTypes, EnemyRarity, EnemyBehavior
from src.entities.enemy import Enemy
from src.utils.asset_manager import AssetManager
from src.utils.animation_manager import AnimationManager
from src.utils.config_manager import ConfigManager


class TestEnemySystem:
	"""Tests para el sistema de enemigos."""
	
	@pytest.fixture(autouse=True)
	def setup(self):
		"""Configuración inicial para los tests."""
		pygame.init()
		pygame.display.set_mode((800, 600))  # Necesario para cargar imágenes
		
		yield
		
		pygame.quit()
	
	def test_enemy_types_creation(self):
		"""Test de creación de tipos de enemigos."""
		# Verificar que todos los tipos existen
		assert EnemyTypes.ZOMBIE_NORMAL is not None
		assert EnemyTypes.ZOMBIE_RARE is not None
		assert EnemyTypes.ZOMBIE_ELITE is not None
		assert EnemyTypes.ZOMBIE_LEGENDARY is not None
		assert EnemyTypes.ZOMBIE_GIRL_NORMAL is not None
		assert EnemyTypes.ZOMBIE_GIRL_RARE is not None
		assert EnemyTypes.ZOMBIE_GIRL_ELITE is not None
		assert EnemyTypes.ZOMBIE_GIRL_LEGENDARY is not None
	
	def test_enemy_config_properties(self):
		"""Test de propiedades de configuración de enemigos."""
		config = EnemyTypes.ZOMBIE_NORMAL
		
		assert config.name == "Zombie Normal"
		assert config.rarity == EnemyRarity.NORMAL
		assert config.behavior == EnemyBehavior.CHASE
		assert config.health > 0
		assert config.speed > 0
		assert config.damage > 0
		assert config.score_value > 0
		assert len(config.color) == 3
		assert len(config.symbol) > 0
		assert len(config.size) == 2
	
	def test_enemy_creation(self):
		"""Test de creación de enemigos."""
		config = ConfigManager()
		asset_manager = AssetManager()
		animation_manager = AnimationManager(config, asset_manager)
		
		# Crear jugador simulado
		class MockPlayer:
			def __init__(self):
				self.x = 400
				self.y = 300
				self.is_alive = True
		
		player = MockPlayer()
		
		# Crear enemigo
		enemy = Enemy(100, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_NORMAL)
		
		assert enemy is not None
		assert enemy.enemy_config == EnemyTypes.ZOMBIE_NORMAL
		assert enemy.behavior == EnemyBehavior.CHASE
		assert enemy.rarity == EnemyRarity.NORMAL
		assert enemy.is_alive
		assert enemy.sprite is not None
	
	def test_enemy_info(self):
		"""Test de información de enemigos."""
		config = ConfigManager()
		asset_manager = AssetManager()
		animation_manager = AnimationManager(config, asset_manager)
		
		class MockPlayer:
			def __init__(self):
				self.x = 400
				self.y = 300
				self.is_alive = True
		
		player = MockPlayer()
		enemy = Enemy(100, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_ELITE)
		
		info = enemy.get_enemy_info()
		
		assert "name" in info
		assert "rarity" in info
		assert "behavior" in info
		assert "health" in info
		assert "damage" in info
		assert "score_value" in info
		assert info["name"] == "Zombie Elite"
		assert info["rarity"] == "elite"
		assert info["behavior"] == "swarm"
	
	def test_random_enemy_generation(self):
		"""Test de generación aleatoria de enemigos."""
		# Generar varios enemigos aleatorios
		enemies = []
		for _ in range(20):
			enemy_config = EnemyTypes.get_random_enemy()
			enemies.append(enemy_config)
		
		# Verificar que se generaron enemigos
		assert len(enemies) == 20
		assert all(enemy is not None for enemy in enemies)
		
		# Verificar que todos tienen las propiedades necesarias
		for enemy in enemies:
			assert hasattr(enemy, 'name')
			assert hasattr(enemy, 'rarity')
			assert hasattr(enemy, 'behavior')
			assert hasattr(enemy, 'health')
			assert hasattr(enemy, 'speed')
			assert hasattr(enemy, 'damage')
	
	def test_rarity_distribution(self):
		"""Test de distribución de rareza."""
		rarity_counts = {
			EnemyRarity.NORMAL: 0,
			EnemyRarity.RARE: 0,
			EnemyRarity.ELITE: 0,
			EnemyRarity.LEGENDARY: 0
		}
		
		# Generar muchos enemigos para verificar distribución
		for _ in range(100):
			enemy_config = EnemyTypes.get_random_enemy()
			rarity_counts[enemy_config.rarity] += 1
		
		# Verificar que se generaron enemigos de todas las rarezas
		assert rarity_counts[EnemyRarity.NORMAL] > 0
		assert rarity_counts[EnemyRarity.RARE] > 0
		assert rarity_counts[EnemyRarity.ELITE] > 0
		assert rarity_counts[EnemyRarity.LEGENDARY] > 0
		
		# Verificar que los normales son más comunes
		assert rarity_counts[EnemyRarity.NORMAL] > rarity_counts[EnemyRarity.LEGENDARY]
	
	def test_enemy_behaviors(self):
		"""Test de comportamientos de enemigos."""
		config = ConfigManager()
		asset_manager = AssetManager()
		animation_manager = AnimationManager(config, asset_manager)
		
		class MockPlayer:
			def __init__(self):
				self.x = 400
				self.y = 300
				self.is_alive = True
		
		player = MockPlayer()
		
		# Crear enemigos con diferentes comportamientos
		chase_enemy = Enemy(100, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_NORMAL)
		wander_enemy = Enemy(200, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_GIRL_RARE)
		ambush_enemy = Enemy(300, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_RARE)
		swarm_enemy = Enemy(400, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_ELITE)
		boss_enemy = Enemy(500, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_LEGENDARY)
		
		assert chase_enemy.behavior == EnemyBehavior.CHASE
		assert wander_enemy.behavior == EnemyBehavior.WANDER
		assert ambush_enemy.behavior == EnemyBehavior.AMBUSH
		assert swarm_enemy.behavior == EnemyBehavior.SWARM
		assert boss_enemy.behavior == EnemyBehavior.BOSS
	
	def test_enemy_collision(self):
		"""Test de colisiones de enemigos."""
		config = ConfigManager()
		asset_manager = AssetManager()
		animation_manager = AnimationManager(config, asset_manager)
		
		class MockPlayer:
			def __init__(self):
				self.x = 400
				self.y = 300
				self.is_alive = True
		
		player = MockPlayer()
		
		enemy1 = Enemy(100, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_NORMAL)
		enemy2 = Enemy(150, 100, asset_manager, animation_manager, config, player, EnemyTypes.ZOMBIE_RARE)
		
		# Verificar que los enemigos tienen rectángulos de colisión
		assert hasattr(enemy1, 'rect')
		assert hasattr(enemy2, 'rect')
		assert enemy1.rect is not None
		assert enemy2.rect is not None
	
	def test_enemy_stats_progression(self):
		"""Test de progresión de estadísticas según rareza."""
		# Verificar que los enemigos más raros son más fuertes
		normal = EnemyTypes.ZOMBIE_NORMAL
		rare = EnemyTypes.ZOMBIE_RARE
		elite = EnemyTypes.ZOMBIE_ELITE
		legendary = EnemyTypes.ZOMBIE_LEGENDARY
		
		# Vida debe aumentar con la rareza
		assert legendary.health > elite.health
		assert elite.health > rare.health
		assert rare.health > normal.health
		
		# Daño debe aumentar con la rareza
		assert legendary.damage > elite.damage
		assert elite.damage > rare.damage
		assert rare.damage > normal.damage
		
		# Puntos deben aumentar con la rareza
		assert legendary.score_value > elite.score_value
		assert elite.score_value > rare.score_value
		assert rare.score_value > normal.score_value


if __name__ == "__main__":
	pytest.main([__file__]) 