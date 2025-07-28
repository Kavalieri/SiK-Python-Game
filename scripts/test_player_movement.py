"""
Test Player Movement - Prueba de Movimiento del Jugador
===================================================

Autor: SiK Team
Fecha: 2024
Descripción: Script para probar el movimiento del jugador y su comportamiento de idle.
"""

import pygame
import sys
import os
import logging

# Configurar entorno de test
from test_config import setup_test_environment
setup_test_environment()

from utils.config_manager import ConfigManager
from utils.asset_manager import AssetManager
from utils.animation_manager import AnimationManager
from entities.player import Player
from entities.character_data import CHARACTER_DATA

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_player_movement():
	"""Prueba el movimiento del jugador y su comportamiento de idle."""
	
	# Inicializar Pygame
	pygame.init()
	
	# Configuración de pantalla
	screen_width = 800
	screen_height = 600
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Test - Movimiento del Jugador")
	
	# Inicializar gestores
	config = ConfigManager()
	asset_manager = AssetManager()
	animation_manager = AnimationManager(config, asset_manager)
	
	# Crear jugador en el centro de la pantalla
	player = Player(screen_width//2, screen_height//2, "guerrero", config, animation_manager)
	
	# Bucle principal
	clock = pygame.time.Clock()
	running = True
	
	logger.info("Iniciando prueba de movimiento del jugador...")
	logger.info("Controles: WASD para mover, ESC para salir")
	logger.info("El jugador debe detenerse cuando no se presionen teclas")
	
	while running:
		delta_time = clock.tick(60) / 1000.0
		
		# Manejar eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
		
		# Manejar input del jugador
		keys = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		mouse_buttons = pygame.mouse.get_pressed()
		player.handle_input(keys, mouse_pos, mouse_buttons)
		
		# Actualizar jugador
		player.update(delta_time)
		
		# Renderizar
		screen.fill((50, 100, 150))
		
		# Renderizar jugador
		player.render(screen, (player.x, player.y))
		
		# Renderizar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Posición: ({int(player.x)}, {int(player.y)})",
			f"Velocidad: ({player.velocity.x:.1f}, {player.velocity.y:.1f})",
			f"Estado: {player.state.value}",
			f"Animación: {player.current_animation_state.value}",
			f"Mirando derecha: {player.facing_right}",
			f"FPS: {int(clock.get_fps())}",
			"",
			"Controles:",
			"WASD - Mover",
			"Mouse - Apuntar",
			"Clic izquierdo - Disparar",
			"ESC - Salir"
		]
		
		for i, info in enumerate(debug_info):
			text = font.render(info, True, (255, 255, 255))
			screen.blit(text, (10, 10 + i * 25))
		
		# Mostrar estado de teclas presionadas
		key_info = []
		if keys[pygame.K_w]: key_info.append("W")
		if keys[pygame.K_a]: key_info.append("A")
		if keys[pygame.K_s]: key_info.append("S")
		if keys[pygame.K_d]: key_info.append("D")
		
		if key_info:
			key_text = font.render(f"Teclas: {' '.join(key_info)}", True, (255, 255, 0))
		else:
			key_text = font.render("Teclas: Ninguna", True, (255, 100, 100))
		
		screen.blit(key_text, (10, screen_height - 50))
		
		pygame.display.flip()
	
	pygame.quit()
	logger.info("Prueba de movimiento completada")

if __name__ == "__main__":
	test_player_movement() 