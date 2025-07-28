#!/usr/bin/env python3
"""
Script de test para el sistema de carga
====================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del sistema de carga con pantalla de progreso.
"""

import sys
import os
import pygame
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scenes.loading_scene import LoadingScene
from src.utils.config_manager import ConfigManager
from src.core.game_state import GameState
from src.core.save_manager import SaveManager


def test_loading_system():
	"""Test del sistema de carga."""
	print("🧪 Iniciando test del sistema de carga...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Sistema de Carga")
	clock = pygame.time.Clock()
	
	# Inicializar managers
	config = ConfigManager()
	game_state = GameState()
	save_manager = SaveManager()
	
	# Callback de finalización
	def on_loading_complete():
		print("✅ Carga completada - Callback ejecutado")
	
	# Crear escena de carga
	loading_scene = LoadingScene(screen, config, game_state, save_manager, on_loading_complete)
	
	print("🎮 Iniciando simulación de carga...")
	print("   - La pantalla mostrará el progreso de carga")
	print("   - Los mensajes cambiarán automáticamente")
	print("   - Al completarse, se ejecutará el callback")
	
	# Bucle de simulación
	running = True
	start_time = time.time()
	
	while running:
		# Manejar eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			loading_scene.handle_event(event)
		
		# Actualizar escena
		loading_scene.update()
		
		# Renderizar
		loading_scene.render()
		pygame.display.flip()
		
		# Controlar FPS
		clock.tick(60)
		
		# Mostrar progreso en consola
		elapsed = time.time() - start_time
		if elapsed > 0 and elapsed % 1 < 0.1:  # Cada segundo
			print(f"   Progreso: {loading_scene.loading_progress:.1%} - {loading_scene.loading_messages[loading_scene.current_message_index]}")
		
		# Salir después de completar la carga
		if loading_scene.loading_complete and elapsed > 6:  # 6 segundos total
			print("   Carga completada, saliendo en 2 segundos...")
			time.sleep(2)
			break
	
	# Limpiar
	pygame.quit()
	print("✅ Test del sistema de carga completado")


if __name__ == "__main__":
	test_loading_system() 