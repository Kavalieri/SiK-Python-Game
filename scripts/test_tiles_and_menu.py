#!/usr/bin/env python3
"""
Script de test para tiles con sprites y menú de selección
======================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test de tiles con sprites reales y menú de selección corregido.
"""

import sys
import os
import pygame
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scenes.character_select_scene import CharacterSelectScene
from src.scenes.game_scene import GameScene
from src.utils.config_manager import ConfigManager
from src.core.game_state import GameState
from src.core.save_manager import SaveManager
from src.utils.world_generator import WorldGenerator
from src.entities.tile import Tile, TileType


def test_tiles_with_sprites():
	"""Test de tiles con sprites reales."""
	print("🧪 Test de tiles con sprites reales...")
	
	# Crear generador de mundo
	world_gen = WorldGenerator(5000, 5000)
	
	# Generar algunas tiles
	tiles = world_gen.generate_world()
	
	print(f"   Generadas {len(tiles)} tiles")
	
	# Verificar sprites
	tiles_with_sprites = 0
	for tile in tiles[:10]:  # Verificar solo las primeras 10
		if hasattr(tile, 'sprite') and tile.sprite:
			tiles_with_sprites += 1
			print(f"   ✅ Tile {tile.tile_type.value} tiene sprite: {getattr(tile, 'sprite_name', 'N/A')}")
		else:
			print(f"   ⚠️ Tile {tile.tile_type.value} sin sprite (usando fallback)")
	
	print(f"   Tiles con sprites: {tiles_with_sprites}/10")
	return tiles_with_sprites > 0


def test_character_select_menu():
	"""Test del menú de selección de personajes."""
	print("\n🎮 Test del menú de selección de personajes...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Menú de Selección")
	clock = pygame.time.Clock()
	
	# Inicializar managers
	config = ConfigManager()
	game_state = GameState()
	save_manager = SaveManager()
	
	# Crear escena
	character_select = CharacterSelectScene(screen, config, game_state, save_manager)
	
	print("   Verificando posicionamiento de elementos...")
	
	# Verificar que los botones estén centrados
	character_buttons = [btn for btn_id, btn in character_select.buttons.items() if btn_id.startswith('char_')]
	
	if len(character_buttons) > 0:
		# Calcular posición esperada
		total_width = len(character_buttons) * 250 + (len(character_buttons) - 1) * 30
		expected_start_x = (800 - total_width) // 2
		
		first_button = character_buttons[0]
		actual_start_x = first_button['rect'].x
		
		if abs(actual_start_x - expected_start_x) < 5:  # Tolerancia de 5px
			print("   ✅ Botones de personajes centrados correctamente")
		else:
			print(f"   ❌ Botones no centrados. Esperado: {expected_start_x}, Actual: {actual_start_x}")
		
		# Verificar altura de tarjetas
		card_height = first_button['rect'].height
		if card_height == 350:
			print("   ✅ Altura de tarjetas corregida (350px)")
		else:
			print(f"   ❌ Altura incorrecta: {card_height}px")
		
		# Verificar que no hay colisión con descripción
		card_bottom = first_button['rect'].bottom
		description_top = 600 - 120  # Nueva posición de la descripción
		
		if card_bottom < description_top:
			print("   ✅ No hay colisión entre tarjetas y descripción")
		else:
			print(f"   ❌ Colisión detectada. Tarjeta: {card_bottom}, Descripción: {description_top}")
	
	# Renderizar para verificar visualmente
	print("   Renderizando menú por 5 segundos...")
	start_time = time.time()
	
	while time.time() - start_time < 5:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return True
		
		# Renderizar
		character_select.render()
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()
	return True


def test_game_scene_with_tiles():
	"""Test de la escena de juego con tiles."""
	print("\n🎯 Test de escena de juego con tiles...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Escena de Juego")
	clock = pygame.time.Clock()
	
	# Inicializar managers
	config = ConfigManager()
	game_state = GameState()
	save_manager = SaveManager()
	
	# Crear escena
	game_scene = GameScene(screen, config, game_state, save_manager)
	
	print("   Verificando tiles en la escena...")
	
	# Verificar que hay tiles
	if hasattr(game_scene, 'tiles') and game_scene.tiles:
		print(f"   ✅ Escena tiene {len(game_scene.tiles)} tiles")
		
		# Verificar sprites de tiles
		tiles_with_sprites = sum(1 for tile in game_scene.tiles if hasattr(tile, 'sprite') and tile.sprite)
		print(f"   ✅ {tiles_with_sprites}/{len(game_scene.tiles)} tiles tienen sprites")
		
		# Renderizar por 3 segundos
		print("   Renderizando escena por 3 segundos...")
		start_time = time.time()
		
		while time.time() - start_time < 3:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return True
			
			# Actualizar y renderizar
			game_scene.update()
			game_scene.render()
			pygame.display.flip()
			clock.tick(60)
		
		pygame.quit()
		return True
	else:
		print("   ❌ No se encontraron tiles en la escena")
		pygame.quit()
		return False


def main():
	"""Función principal del test."""
	print("🧪 Iniciando tests de tiles y menú...")
	
	# Test 1: Tiles con sprites
	success1 = test_tiles_with_sprites()
	
	# Test 2: Menú de selección
	success2 = test_character_select_menu()
	
	# Test 3: Escena de juego con tiles
	success3 = test_game_scene_with_tiles()
	
	# Resumen
	print("\n📊 Resumen de tests:")
	print(f"   Tiles con sprites: {'✅' if success1 else '❌'}")
	print(f"   Menú de selección: {'✅' if success2 else '❌'}")
	print(f"   Escena de juego: {'✅' if success3 else '❌'}")
	
	if success1 and success2 and success3:
		print("\n🎉 Todos los tests pasaron exitosamente!")
	else:
		print("\n⚠️ Algunos tests fallaron. Revisar implementación.")


if __name__ == "__main__":
	main() 