#!/usr/bin/env python3
"""
Script de test para el sistema de powerups
========================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del sistema de powerups y efectos temporales.
"""

import sys
import os
import pygame
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.powerup import Powerup, PowerupType, PowerupEffect
from src.entities.player import Player
from src.utils.config_manager import ConfigManager
from src.utils.animation_manager import AnimationManager
from src.utils.asset_manager import AssetManager


def test_powerup_system():
	"""Test del sistema de powerups."""
	print("🧪 Iniciando test del sistema de powerups...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Sistema de Powerups")
	clock = pygame.time.Clock()
	
	# Configuración
	config = ConfigManager()
	asset_manager = AssetManager()
	animation_manager = AnimationManager(config, asset_manager)
	
	# Crear jugador
	player = Player(400, 300, "guerrero", config, animation_manager)
	
	# Crear powerups de prueba
	powerups = []
	for i, powerup_type in enumerate(PowerupType):
		x = 100 + (i * 100)
		y = 100
		powerup = Powerup(x, y, powerup_type)
		powerups.append(powerup)
		print(f"✅ Powerup {powerup_type.value} creado en ({x}, {y})")
	
	# Test de efectos
	print("\n📊 Probando efectos de powerups...")
	
	# Aplicar powerup de velocidad
	speed_effect = PowerupEffect(
		type=PowerupType.SPEED,
		duration=5.0,
		value=1.5,
		description="Aumenta la velocidad"
	)
	
	player.apply_powerup(speed_effect)
	print(f"✅ Powerup de velocidad aplicado - Velocidad: {player.stats.speed}")
	
	# Aplicar powerup de daño
	damage_effect = PowerupEffect(
		type=PowerupType.DAMAGE,
		duration=10.0,
		value=2.0,
		description="Aumenta el daño"
	)
	
	player.apply_powerup(damage_effect)
	print(f"✅ Powerup de daño aplicado - Daño: {player.stats.damage}")
	
	# Verificar efectos activos
	active_effects = player.get_active_effects()
	print(f"✅ Efectos activos: {len(active_effects)}")
	for effect_type, remaining_time in active_effects.items():
		print(f"   - {effect_type.value}: {remaining_time:.1f}s restantes")
	
	# Test de powerup de vida (instantáneo)
	health_effect = PowerupEffect(
		type=PowerupType.HEALTH,
		duration=0.0,
		value=50.0,
		description="Restaura vida"
	)
	
	original_health = player.stats.health
	player.apply_powerup(health_effect)
	print(f"✅ Powerup de vida aplicado - Vida: {original_health} -> {player.stats.health}")
	
	# Simular paso del tiempo
	print("\n⏰ Simulando paso del tiempo...")
	for i in range(3):
		time.sleep(1)
		player.update(1.0)
		active_effects = player.get_active_effects()
		print(f"   Tiempo {i+1}s - Efectos activos: {len(active_effects)}")
	
	# Limpiar
	pygame.quit()
	print("✅ Test del sistema de powerups completado")


if __name__ == "__main__":
	test_powerup_system() 