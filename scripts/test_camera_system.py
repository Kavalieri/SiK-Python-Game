#!/usr/bin/env python3
"""
Script de test para el sistema de cámara
======================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del sistema de cámara y movimiento libre.
"""

import sys
import os
import pygame
import math

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.camera import Camera
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.utils.config_manager import ConfigManager
from src.utils.asset_manager import AssetManager
from src.utils.animation_manager import AnimationManager


def test_camera_system():
	"""Test del sistema de cámara."""
	print("🧪 Iniciando test del sistema de cámara...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Sistema de Cámara")
	clock = pygame.time.Clock()
	
	# Configuración
	config = ConfigManager()
	asset_manager = AssetManager()
	animation_manager = AnimationManager(config, asset_manager)
	
	# Crear cámara
	camera = Camera(800, 600, 5000, 5000)
	
	# Crear jugador en el centro del mundo
	player = Player(2500, 2500, "guerrero", config, animation_manager)
	
	# Crear enemigo
	enemy = Enemy(2600, 2600, asset_manager, animation_manager, config, player)
	
	print(f"✅ Cámara creada - Mundo: {camera.world_width}x{camera.world_height}")
	print(f"✅ Jugador creado en ({player.x}, {player.y})")
	print(f"✅ Enemigo creado en ({enemy.x}, {enemy.y})")
	
	# Test de conversión de coordenadas
	world_x, world_y = 1000, 1000
	screen_x, screen_y = camera.world_to_screen(world_x, world_y)
	print(f"✅ Coordenadas mundo ({world_x}, {world_y}) -> Pantalla ({screen_x}, {screen_y})")
	
	# Test de visibilidad
	is_visible = camera.is_visible(world_x, world_y, 50, 50)
	print(f"✅ Objeto en ({world_x}, {world_y}) visible: {is_visible}")
	
	# Test de seguimiento
	camera.follow_target(player.x, player.y)
	camera.update(1.0/60.0)
	print(f"✅ Cámara siguiendo al jugador - Posición: {camera.get_position()}")
	
	# Limpiar
	pygame.quit()
	print("✅ Test del sistema de cámara completado")


if __name__ == "__main__":
	test_camera_system() 