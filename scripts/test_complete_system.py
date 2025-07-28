"""
Test Complete System - Prueba del Sistema Completo
================================================

Autor: SiK Team
Fecha: 2024
Descripción: Script para probar el sistema completo con todas las mejoras integradas.
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
from utils.world_generator import WorldGenerator
from utils.desert_background import DesertBackground
from utils.camera import Camera
from entities.player import Player
from entities.tile import Tile, TileType

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_system():
	"""Prueba el sistema completo con todas las mejoras."""
	
	# Inicializar Pygame
	pygame.init()
	
	# Configuración de pantalla
	screen_width = 1200
	screen_height = 800
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Test - Sistema Completo")
	
	# Inicializar gestores
	config = ConfigManager()
	asset_manager = AssetManager()
	animation_manager = AnimationManager(config, asset_manager)
	
	# Calcular tamaño del mundo (4 veces la pantalla)
	world_width = screen_width * 4
	world_height = screen_height * 4
	
	logger.info(f"Pantalla: {screen_width}x{screen_height}")
	logger.info(f"Mundo: {world_width}x{world_height}")
	
	# Crear generador de mundo
	world_generator = WorldGenerator(
		world_width=world_width,
		world_height=world_height,
		screen_width=screen_width,
		screen_height=screen_height
	)
	
	# Generar mundo completo
	logger.info("Generando mundo completo...")
	elements = world_generator.generate_world()
	
	# Generar áreas especiales
	oasis = world_generator.generate_desert_oasis(1000, 1000, 300)
	rocks = world_generator.generate_rock_formation(4000, 1000, 250)
	cactus = world_generator.generate_cactus_field(1000, 4000, 200)
	ruins = world_generator.generate_ruins(4000, 4000, 280)
	
	elements.extend(oasis)
	elements.extend(rocks)
	elements.extend(cactus)
	elements.extend(ruins)
	
	logger.info(f"Mundo generado con {len(elements)} elementos")
	
	# Crear cámara
	camera = Camera(
		screen_width=screen_width,
		screen_height=screen_height,
		world_width=world_width,
		world_height=world_height
	)
	
	# Crear jugador en el centro del mundo
	player_x = world_width // 2
	player_y = world_height // 2
	player = Player(player_x, player_y, "guerrero", config, animation_manager)
	player.world_width = world_width
	player.world_height = world_height
	
	# Crear fondo de desierto
	background = DesertBackground(screen_width, screen_height)
	
	# Bucle principal
	clock = pygame.time.Clock()
	running = True
	
	logger.info("Iniciando prueba del sistema completo...")
	logger.info("Controles: WASD para mover jugador, Flechas para cámara libre, ESC para salir")
	
	while running:
		delta_time = clock.tick(60) / 1000.0
		
		# Manejar eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				elif event.key == pygame.K_SPACE:
					# Cambiar entre modo jugador y modo cámara libre
					logger.info("Cambiando modo de control...")
		
		# Manejar input del jugador
		keys = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		mouse_buttons = pygame.mouse.get_pressed()
		
		# Modo jugador (WASD mueve al jugador)
		if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
			player.handle_input(keys, mouse_pos, mouse_buttons)
			# La cámara sigue al jugador
			camera.follow_target(player.x, player.y)
		else:
			# Modo cámara libre (flechas mueven la cámara)
			camera_speed = 200
			if keys[pygame.K_LEFT]:
				camera.x -= camera_speed * delta_time
			if keys[pygame.K_RIGHT]:
				camera.x += camera_speed * delta_time
			if keys[pygame.K_UP]:
				camera.y -= camera_speed * delta_time
			if keys[pygame.K_DOWN]:
				camera.y += camera_speed * delta_time
		
		# Actualizar entidades
		player.update(delta_time)
		camera.update(delta_time)
		background.update(delta_time)
		
		# Renderizar
		screen.fill((0, 0, 0))
		
		# Renderizar fondo con offset de cámara
		camera_offset = (camera.x, camera.y)
		background.render(screen, camera_offset)
		
		# Renderizar elementos visibles
		visible_elements = 0
		for element in elements:
			if camera.is_visible(element.x, element.y, element.width, element.height):
				screen_x, screen_y = camera.world_to_screen(element.x, element.y)
				element.render(screen, (screen_x, screen_y))
				visible_elements += 1
		
		# Renderizar jugador
		if camera.is_visible(player.x, player.y, player.width, player.height):
			screen_x, screen_y = camera.world_to_screen(player.x, player.y)
			player.render(screen, (screen_x, screen_y))
		
		# Renderizar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Jugador: ({int(player.x)}, {int(player.y)})",
			f"Cámara: ({int(camera.x)}, {int(camera.y)})",
			f"Elementos: {len(elements)} (visibles: {visible_elements})",
			f"Estado jugador: {player.state.value}",
			f"Animación: {player.current_animation_state.value}",
			f"Velocidad: ({player.velocity.x:.1f}, {player.velocity.y:.1f})",
			f"FPS: {int(clock.get_fps())}",
			"",
			"Controles:",
			"WASD - Mover jugador (cámara sigue)",
			"Flechas - Mover cámara libre",
			"Mouse - Apuntar",
			"Clic izquierdo - Disparar",
			"ESPACIO - Cambiar modo",
			"ESC - Salir"
		]
		
		for i, info in enumerate(debug_info):
			text = font.render(info, True, (255, 255, 255))
			screen.blit(text, (10, 10 + i * 25))
		
		# Mostrar modo actual
		if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
			mode_text = font.render("Modo: Jugador", True, (0, 255, 0))
		else:
			mode_text = font.render("Modo: Cámara Libre", True, (255, 255, 0))
		
		screen.blit(mode_text, (10, screen_height - 50))
		
		pygame.display.flip()
	
	pygame.quit()
	logger.info("Prueba del sistema completo finalizada")

if __name__ == "__main__":
	test_complete_system() 