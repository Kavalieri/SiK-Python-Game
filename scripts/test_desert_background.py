"""
Test Desert Background - Prueba del Fondo de Desierto
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Script para probar el fondo dinámico de desierto con efectos.
"""

import pygame
import sys
import os
import logging

# Configurar entorno de test
from test_config import setup_test_environment
setup_test_environment()

from utils.desert_background import DesertBackground

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_desert_background():
	"""Prueba el fondo dinámico de desierto."""
	
	# Inicializar Pygame
	pygame.init()
	
	# Configuración de pantalla
	screen_width = 1200
	screen_height = 800
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Test - Fondo de Desierto")
	
	# Crear fondo de desierto
	background = DesertBackground(screen_width, screen_height)
	
	# Variables para simular movimiento de cámara
	camera_x = 0
	camera_y = 0
	camera_speed = 100  # píxeles por segundo
	
	# Bucle principal
	clock = pygame.time.Clock()
	running = True
	
	logger.info("Iniciando prueba del fondo de desierto...")
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
		
		# Actualizar fondo
		background.update(delta_time)
		
		# Renderizar
		screen.fill((0, 0, 0))
		
		# Renderizar fondo con offset de cámara
		camera_offset = (camera_x, camera_y)
		background.render(screen, camera_offset)
		
		# Renderizar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Cámara: ({int(camera_x)}, {int(camera_y)})",
			f"Tiempo: {background.time:.1f}s",
			f"Viento: {background.wind_strength:.2f}",
			f"Partículas: {len(background.sand_particles)}",
			f"Dunas: {len(background.dunes)}",
			f"FPS: {int(clock.get_fps())}",
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
	logger.info("Prueba del fondo de desierto completada")

if __name__ == "__main__":
	test_desert_background() 