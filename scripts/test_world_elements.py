"""
Test World Elements - Prueba de Elementos del Mundo
================================================

Autor: SiK Team
Fecha: 2024
Descripción: Script para probar la generación y renderizado de elementos del mundo.
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
from utils.camera import Camera
from entities.tile import Tile, TileType

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_world_elements():
	"""Prueba la generación y renderizado de elementos del mundo."""
	
	# Inicializar Pygame
	pygame.init()
	
	# Configuración de pantalla
	screen_width = 1200
	screen_height = 800
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Test - Elementos del Mundo")
	
	# Inicializar gestores
	config = ConfigManager()
	asset_manager = AssetManager()
	animation_manager = AnimationManager(config, asset_manager)
	
	# Calcular tamaño del mundo
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
	
	# Generar elementos básicos
	logger.info("Generando elementos básicos...")
	elements = world_generator.generate_world()
	logger.info(f"Elementos básicos generados: {len(elements)}")
	
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
	
	# Variables para control de cámara
	camera_x = world_width // 2 - screen_width // 2
	camera_y = world_height // 2 - screen_height // 2
	camera_speed = 200  # píxeles por segundo
	
	# Bucle principal
	clock = pygame.time.Clock()
	running = True
	
	logger.info("Iniciando prueba de elementos del mundo...")
	logger.info("Controles: Flechas para mover cámara, ESC para salir")
	
	while running:
		delta_time = clock.tick(60) / 1000.0
		
		# Manejar eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
		
		# Manejar input para mover cámara
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			camera_x -= camera_speed * delta_time
		if keys[pygame.K_RIGHT]:
			camera_x += camera_speed * delta_time
		if keys[pygame.K_UP]:
			camera_y -= camera_speed * delta_time
		if keys[pygame.K_DOWN]:
			camera_y += camera_speed * delta_time
		
		# Actualizar cámara
		camera.x = camera_x
		camera.y = camera_y
		camera.update(delta_time)
		
		# Renderizar
		screen.fill((50, 100, 150))
		
		# Renderizar elementos visibles
		visible_elements = 0
		for element in elements:
			if camera.is_visible(element.x, element.y, element.width, element.height):
				screen_x, screen_y = camera.world_to_screen(element.x, element.y)
				element.render(screen, (screen_x, screen_y))
				visible_elements += 1
		
		# Renderizar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Cámara: ({int(camera_x)}, {int(camera_y)})",
			f"Elementos totales: {len(elements)}",
			f"Elementos visibles: {visible_elements}",
			f"FPS: {int(clock.get_fps())}",
			"",
			"Áreas especiales:",
			f"Oasis: {len(oasis)} elementos",
			f"Rocas: {len(rocks)} elementos",
			f"Cactus: {len(cactus)} elementos",
			f"Ruinas: {len(ruins)} elementos",
			"",
			"Controles:",
			"Flechas - Mover cámara",
			"ESC - Salir"
		]
		
		for i, info in enumerate(debug_info):
			text = font.render(info, True, (255, 255, 255))
			screen.blit(text, (10, 10 + i * 25))
		
		# Mostrar controles de cámara
		camera_info = []
		if keys[pygame.K_LEFT]: camera_info.append("←")
		if keys[pygame.K_RIGHT]: camera_info.append("→")
		if keys[pygame.K_UP]: camera_info.append("↑")
		if keys[pygame.K_DOWN]: camera_info.append("↓")
		
		if camera_info:
			camera_text = font.render(f"Cámara: {' '.join(camera_info)}", True, (255, 255, 0))
		else:
			camera_text = font.render("Cámara: Estática", True, (255, 100, 100))
		
		screen.blit(camera_text, (10, screen_height - 50))
		
		pygame.display.flip()
	
	pygame.quit()
	logger.info("Prueba de elementos del mundo completada")

if __name__ == "__main__":
	test_world_elements() 