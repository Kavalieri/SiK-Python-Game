"""
Tests para el sistema de proyectiles
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Tests unitarios para el sistema de proyectiles.
"""

import pytest
import pygame
import sys
import os
from unittest.mock import Mock, MagicMock

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.projectile import Projectile
from src.entities.enemy import Enemy
from src.utils.config_manager import ConfigManager


class TestProjectileSystem:
	"""Tests para el sistema de proyectiles."""
	
	@pytest.fixture
	def config(self):
		"""Configuración de prueba."""
		config = ConfigManager()
		config.config = {
			'display': {
				'width': 1280,
				'height': 720
			}
		}
		return config
	
	@pytest.fixture
	def asset_manager(self):
		"""Asset manager mock."""
		return Mock()
	
	@pytest.fixture
	def animation_manager(self):
		"""Animation manager mock."""
		return Mock()
	
	def test_projectile_creation(self, config):
		"""Test de creación de proyectil."""
		projectile = Projectile(100, 100, 200, 200, 25.0, 500.0, config)
		
		assert projectile.x == 100
		assert projectile.y == 100
		assert projectile.stats.damage == 25.0
		assert projectile.stats.speed == 500.0
		assert projectile.alive == True
		assert projectile.entity_type.value == "projectile"
	
	def test_projectile_movement(self, config):
		"""Test de movimiento del proyectil."""
		projectile = Projectile(100, 100, 200, 200, 25.0, 500.0, config)
		
		# Verificar que tiene velocidad
		assert projectile.velocity_x != 0 or projectile.velocity_y != 0
		
		# Simular movimiento
		initial_x, initial_y = projectile.x, projectile.y
		projectile.update(1.0/60.0)  # Un frame a 60 FPS
		
		# Verificar que se movió
		assert projectile.x != initial_x or projectile.y != initial_y
	
	def test_projectile_out_of_bounds(self, config):
		"""Test de eliminación por salir de pantalla."""
		# Crear proyectil fuera de pantalla
		projectile = Projectile(-100, -100, -200, -200, 25.0, 500.0, config)
		
		# Debería estar vivo inicialmente
		assert projectile.alive == True
		
		# Actualizar - debería detectar que está fuera de pantalla
		projectile.update(1.0/60.0)
		
		# Debería estar muerto
		assert projectile.alive == False
	
	def test_projectile_damage(self, config):
		"""Test de daño del proyectil."""
		projectile = Projectile(100, 100, 200, 200, 50.0, 500.0, config)
		
		assert projectile.get_damage() == 50.0
	
	def test_projectile_collision(self, config, asset_manager, animation_manager):
		"""Test de colisión entre proyectil y enemigo."""
		projectile = Projectile(100, 100, 200, 200, 25.0, 500.0, config)
		enemy = Enemy(100, 100, asset_manager, animation_manager, config)
		
		# Verificar que colisionan
		assert projectile.rect.colliderect(enemy.rect)
		
		# Simular impacto
		initial_health = enemy.stats.health
		projectile.on_hit()
		
		# Verificar que el proyectil murió
		assert projectile.alive == False
	
	def test_projectile_direction_calculation(self, config):
		"""Test de cálculo de dirección del proyectil."""
		# Proyectil hacia la derecha
		projectile = Projectile(100, 100, 200, 100, 25.0, 500.0, config)
		assert projectile.velocity_x > 0
		assert abs(projectile.velocity_y) < 0.1  # Casi horizontal
		
		# Proyectil hacia arriba
		projectile = Projectile(100, 100, 100, 0, 25.0, 500.0, config)
		assert projectile.velocity_y < 0
		assert abs(projectile.velocity_x) < 0.1  # Casi vertical


if __name__ == "__main__":
	# Ejecutar tests
	pytest.main([__file__, "-v"]) 