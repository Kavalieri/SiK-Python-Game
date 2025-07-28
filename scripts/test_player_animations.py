#!/usr/bin/env python3
"""
Script de test para animaciones del jugador y fondo de desierto
============================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test de animaciones del jugador y fondo dinámico de desierto.
"""

import sys
import os
import pygame
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.player import Player
from src.utils.config_manager import ConfigManager
from src.utils.animation_manager import AnimationManager
from src.utils.asset_manager import AssetManager
from src.utils.desert_background import DesertBackground


def test_player_animations():
	"""Test de animaciones del jugador y fondo de desierto."""
	print("🧪 Iniciando test de animaciones del jugador...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Animaciones del Jugador")
	clock = pygame.time.Clock()
	
	# Inicializar managers
	config = ConfigManager()
	asset_manager = AssetManager()
	animation_manager = AnimationManager(config, asset_manager)
	
	# Crear fondo de desierto
	desert_bg = DesertBackground(800, 600)
	
	# Crear jugador
	player = Player(
		x=400, y=300,
		character_name="guerrero",
		config=config,
		animation_manager=animation_manager
	)
	
	print("🎮 Test de animaciones iniciado")
	print("   - Usa WASD para mover el jugador")
	print("   - Observa las animaciones de idle, walk y attack")
	print("   - El jugador rota según la dirección del mouse")
	print("   - El fondo de desierto se actualiza dinámicamente")
	
	# Variables de test
	test_time = 0
	last_attack_time = 0
	
	# Bucle de simulación
	running = True
	start_time = time.time()
	
	while running:
		# Manejar eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		# Obtener entrada
		keys = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		mouse_buttons = pygame.mouse.get_pressed()
		
		# Simular disparo automático cada 2 segundos
		current_time = time.time()
		if current_time - last_attack_time > 2.0:
			mouse_buttons = (True, False, False)  # Simular clic izquierdo
			last_attack_time = current_time
			print("   Disparo automático simulado")
		
		# Actualizar jugador
		player.handle_input(keys, mouse_pos, mouse_buttons)
		player.update(1.0 / 60.0)
		
		# Actualizar fondo
		desert_bg.update(1.0 / 60.0)
		
		# Renderizar
		desert_bg.render(screen)
		
		# Renderizar jugador
		player.render(screen)
		
		# Mostrar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Posición: ({player.x:.1f}, {player.y:.1f})",
			f"Velocidad: ({player.velocity.x:.1f}, {player.velocity.y:.1f})",
			f"Mirando: {'Derecha' if player.facing_right else 'Izquierda'}",
			f"Estado: {player.current_animation_state.value}",
			f"Timer disparo: {player.shoot_timer:.2f}"
		]
		
		for i, info in enumerate(debug_info):
			text_surface = font.render(info, True, (255, 255, 255))
			screen.blit(text_surface, (10, 10 + i * 25))
		
		pygame.display.flip()
		clock.tick(60)
		
		# Salir después de 30 segundos
		if current_time - start_time > 30:
			print("   Test completado, saliendo...")
			break
	
	# Limpiar
	pygame.quit()
	print("✅ Test de animaciones del jugador completado")


if __name__ == "__main__":
	test_player_animations() 