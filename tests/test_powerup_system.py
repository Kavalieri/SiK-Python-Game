"""
Tests para el sistema de powerups
===============================

Autor: SiK Team
Fecha: 2024
Descripción: Tests unitarios para el sistema de powerups y efectos temporales.
"""

import pytest
import pygame
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.powerup import Powerup, PowerupType, PowerupEffect
from src.entities.player import Player
from src.utils.config_manager import ConfigManager
from src.utils.animation_manager import AnimationManager
from src.utils.asset_manager import AssetManager


class TestPowerupSystem:
	"""Tests para el sistema de powerups."""
	
	@pytest.fixture(autouse=True)
	def setup(self):
		"""Configuración inicial para los tests."""
		pygame.init()
		pygame.display.set_mode((800, 600))  # Necesario para cargar imágenes
		self.config = ConfigManager()
		self.asset_manager = AssetManager()
		self.animation_manager = AnimationManager(self.config, self.asset_manager)
		self.player = Player(400, 300, "guerrero", self.config, self.animation_manager)
		
		yield
		
		pygame.quit()
	
	def test_powerup_creation(self):
		"""Test de creación de powerups."""
		# Crear powerup de velocidad
		powerup = Powerup(100, 100, PowerupType.SPEED)
		
		assert powerup.powerup_type == PowerupType.SPEED
		assert powerup.x == 100
		assert powerup.y == 100
		assert powerup.is_alive
		assert powerup.sprite is not None
	
	def test_powerup_effect_application(self):
		"""Test de aplicación de efectos de powerups."""
		# Estadísticas base del jugador
		base_speed = self.player.stats.speed
		base_damage = self.player.stats.damage
		
		# Aplicar powerup de velocidad
		speed_effect = PowerupEffect(
			type=PowerupType.SPEED,
			duration=10.0,
			value=1.5,
			description="Aumenta la velocidad"
		)
		
		self.player.apply_powerup(speed_effect)
		
		# Verificar que la velocidad aumentó
		assert self.player.stats.speed == base_speed * 1.5
		assert self.player.has_effect(PowerupType.SPEED)
		assert self.player.get_effect_remaining_time(PowerupType.SPEED) > 0
	
	def test_multiple_effects(self):
		"""Test de múltiples efectos simultáneos."""
		# Aplicar múltiples powerups
		effects = [
			PowerupEffect(PowerupType.SPEED, 10.0, 1.5, "Velocidad"),
			PowerupEffect(PowerupType.DAMAGE, 15.0, 2.0, "Daño"),
			PowerupEffect(PowerupType.SHIELD, 12.0, 0.5, "Escudo")
		]
		
		for effect in effects:
			self.player.apply_powerup(effect)
		
		# Verificar que todos los efectos están activos
		active_effects = self.player.get_active_effects()
		assert len(active_effects) == 3
		assert PowerupType.SPEED in active_effects
		assert PowerupType.DAMAGE in active_effects
		assert PowerupType.SHIELD in active_effects
	
	def test_effect_expiration(self):
		"""Test de expiración de efectos."""
		# Aplicar efecto de corta duración
		short_effect = PowerupEffect(
			type=PowerupType.SPEED,
			duration=0.1,  # 0.1 segundos
			value=1.5,
			description="Velocidad corta"
		)
		
		self.player.apply_powerup(short_effect)
		assert self.player.has_effect(PowerupType.SPEED)
		
		# Simular paso del tiempo
		self.player.update(0.2)  # Más tiempo que la duración
		
		# Verificar que el efecto expiró
		assert not self.player.has_effect(PowerupType.SPEED)
		assert self.player.get_effect_remaining_time(PowerupType.SPEED) == 0
	
	def test_instant_effect(self):
		"""Test de efectos instantáneos."""
		# Reducir vida del jugador primero
		self.player.stats.health = 100
		original_health = self.player.stats.health
		
		# Aplicar powerup de vida (efecto instantáneo)
		health_effect = PowerupEffect(
			type=PowerupType.HEALTH,
			duration=0.0,  # Instantáneo
			value=50.0,
			description="Restaura vida"
		)
		
		self.player.apply_powerup(health_effect)
		
		# Verificar que la vida aumentó
		assert self.player.stats.health > original_health
		# Verificar que no hay efecto activo (es instantáneo)
		assert not self.player.has_effect(PowerupType.HEALTH)
	
	def test_random_powerup_creation(self):
		"""Test de creación de powerups aleatorios."""
		powerup = Powerup.create_random(200, 200)
		
		assert powerup.x == 200
		assert powerup.y == 200
		assert powerup.powerup_type in PowerupType
		assert powerup.is_alive
	
	def test_powerup_visual_effects(self):
		"""Test de efectos visuales de powerups."""
		powerup = Powerup(100, 100, PowerupType.DAMAGE)
		
		# Verificar que tiene sprite
		assert powerup.sprite is not None
		
		# Verificar efecto de flotación
		original_offset = powerup.float_offset
		powerup.update(1.0)
		assert powerup.float_offset != original_offset
	
	def test_powerup_configs(self):
		"""Test de configuraciones de powerups."""
		for powerup_type in PowerupType:
			config = Powerup.POWERUP_CONFIGS[powerup_type]
			
			assert "name" in config
			assert "color" in config
			assert "duration" in config
			assert "value" in config
			assert "description" in config
	
	def test_effect_recalculation(self):
		"""Test de recálculo de estadísticas con efectos."""
		base_speed = self.player.base_stats.speed
		
		# Aplicar efecto de velocidad
		speed_effect = PowerupEffect(PowerupType.SPEED, 10.0, 2.0, "Velocidad x2")
		self.player.apply_powerup(speed_effect)
		
		# Verificar que las estadísticas se recalculan
		assert self.player.stats.speed == base_speed * 2.0
		
		# Simular expiración (más tiempo que la duración)
		for _ in range(12):  # Simular 12 segundos
			self.player.update(1.0)
		
		# Verificar que las estadísticas vuelven a la normalidad
		assert abs(self.player.stats.speed - base_speed) < 0.1  # Tolerancia para errores de punto flotante


if __name__ == "__main__":
	pytest.main([__file__]) 