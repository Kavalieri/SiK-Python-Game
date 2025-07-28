#!/usr/bin/env python3
"""
Script de test para el menú de selección de personajes
===================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del menú de selección de personajes funcional.
"""

import sys
import os
import pygame
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scenes.character_select_scene import CharacterSelectScene
from src.utils.config_manager import ConfigManager
from src.core.game_state import GameState
from src.core.save_manager import SaveManager


def test_character_select_menu():
	"""Test del menú de selección de personajes."""
	print("🧪 Iniciando test del menú de selección de personajes...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Menú de Selección de Personajes")
	clock = pygame.time.Clock()
	
	# Inicializar managers
	config = ConfigManager()
	game_state = GameState()
	save_manager = SaveManager()
	
	# Crear escena de selección de personajes
	character_select_scene = CharacterSelectScene(screen, config, game_state, save_manager)
	
	print("🎮 Menú de selección de personajes iniciado")
	print("   - Haz clic en los personajes para seleccionarlos")
	print("   - Usa los botones 'Volver' y 'Comenzar Juego'")
	print("   - Observa cómo cambia la información del personaje seleccionado")
	
	# Simular clics para probar funcionalidad
	test_clicks = [
		(400, 250),  # Clic en Kava
		(680, 250),  # Clic en Sara
		(960, 250),  # Clic en Guiral
		(400, 250),  # Volver a Kava
		(50, 520),   # Botón Volver
		(600, 520),  # Botón Comenzar Juego
	]
	
	click_index = 0
	last_click_time = 0
	
	# Bucle de simulación
	running = True
	start_time = time.time()
	
	while running:
		# Manejar eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			character_select_scene.handle_event(event)
		
		# Simular clics automáticos para demostración
		current_time = time.time()
		if (current_time - last_click_time > 2.0 and 
			click_index < len(test_clicks)):
			
			# Simular clic
			click_pos = test_clicks[click_index]
			character_select_scene._handle_click(click_pos)
			
			print(f"   Clic simulado en posición {click_pos}")
			if click_index < 3:
				character_names = ["Kava", "Sara", "Guiral"]
				print(f"   Personaje seleccionado: {character_names[click_index]}")
			elif click_index == 3:
				print("   Volviendo a seleccionar Kava")
			elif click_index == 4:
				print("   Botón 'Volver' presionado")
			elif click_index == 5:
				print("   Botón 'Comenzar Juego' presionado")
			
			click_index += 1
			last_click_time = current_time
		
		# Actualizar escena
		character_select_scene.update()
		
		# Renderizar
		character_select_scene.render()
		pygame.display.flip()
		
		# Controlar FPS
		clock.tick(60)
		
		# Salir después de completar las pruebas
		if click_index >= len(test_clicks) and (current_time - last_click_time) > 3.0:
			print("   Pruebas completadas, saliendo...")
			break
	
	# Limpiar
	pygame.quit()
	print("✅ Test del menú de selección de personajes completado")


if __name__ == "__main__":
	test_character_select_menu() 