"""
Test World Generation - Prueba de Generación de Mundo
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Script para probar la nueva generación de mundo y movimiento del jugador.
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

def test_world_generation():
	"""Prueba la generación del mundo y el movimiento del jugador."""
	
	# Inicializar Pygame
	pygame.init()
	
	# Configuración de pantalla
	screen_width = 1200
	screen_height = 800
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Test - Generación de Mundo")
	
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
	
	# Generar mundo
	logger.info("Generando mundo...")
	elements = world_generator.generate_world()
	logger.info(f"Mundo generado con {len(elements)} elementos")
	
	# Generar áreas especiales
	logger.info("Generando áreas especiales...")
	oasis = world_generator.generate_desert_oasis(1000, 1000, 300)
	rocks = world_generator.generate_rock_formation(4000, 1000, 250)
	cactus = world_generator.generate_cactus_field(1000, 4000, 200)
	ruins = world_generator.generate_ruins(4000, 4000, 280)
	
	elements.extend(oasis)
	elements.extend(rocks)
	elements.extend(cactus)
	elements.extend(ruins)
	
	logger.info(f"Total de elementos: {len(elements)}")
	
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
	
	logger.info("Iniciando bucle de prueba...")
	logger.info("Controles: WASD para mover, ESC para salir")
	
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
		
		# Actualizar cámara para seguir al jugador
		camera.follow_target(player.x, player.y)
		camera.update(delta_time)
		
		# Actualizar fondo
		background.update(delta_time)
		
		# Renderizar
		screen.fill((0, 0, 0))
		
		# Renderizar fondo
		camera_offset = (camera.x, camera.y)
		background.render(screen, camera_offset)
		
		# Renderizar elementos
		for element in elements:
			if camera.is_visible(element.x, element.y, element.width, element.height):
				screen_x, screen_y = camera.world_to_screen(element.x, element.y)
				element.render(screen, (screen_x, screen_y))
		
		# Renderizar jugador
		if camera.is_visible(player.x, player.y, player.width, player.height):
			screen_x, screen_y = camera.world_to_screen(player.x, player.y)
			player.render(screen, (screen_x, screen_y))
		
		# Renderizar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Jugador: ({int(player.x)}, {int(player.y)})",
			f"Cámara: ({int(camera.x)}, {int(camera.y)})",
			f"Elementos: {len(elements)}",
			f"FPS: {int(clock.get_fps())}",
			f"Estado: {player.state.value}",
			f"Velocidad: ({player.velocity.x:.1f}, {player.velocity.y:.1f})"
		]
		
		for i, info in enumerate(debug_info):
			text = font.render(info, True, (255, 255, 255))
			screen.blit(text, (10, 10 + i * 25))
		
		pygame.display.flip()
	
	pygame.quit()
	logger.info("Prueba completada")

if __name__ == "__main__":
	test_world_generation() 