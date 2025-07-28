"""
Test Simple Player - Prueba Simplificada del Jugador
=================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test simplificado para verificar el movimiento del jugador.
"""

import pygame
import sys
import os

# Configurar pygame
pygame.init()

def test_simple_player():
	"""Prueba básica del movimiento del jugador."""
	
	# Configuración de pantalla
	screen_width = 800
	screen_height = 600
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Test - Movimiento Simple del Jugador")
	
	# Crear jugador simple
	player_x = screen_width // 2
	player_y = screen_height // 2
	player_speed = 200
	player_size = 32
	
	# Variables del jugador
	velocity_x = 0
	velocity_y = 0
	state = "IDLE"
	
	# Bucle principal
	clock = pygame.time.Clock()
	running = True
	
	print("🧪 Iniciando test de movimiento simple...")
	print("Controles: WASD para mover, ESC para salir")
	print("El jugador debe detenerse cuando no se presionen teclas")
	
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
		
		# Movimiento con WASD
		movement_x = 0
		movement_y = 0
		
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			movement_y -= 1
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			movement_y += 1
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			movement_x -= 1
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			movement_x += 1
		
		# Normalizar movimiento diagonal
		if movement_x != 0 and movement_y != 0:
			movement_x *= 0.707
			movement_y *= 0.707
		
		# Aplicar movimiento
		if movement_x != 0 or movement_y != 0:
			velocity_x = movement_x * player_speed
			velocity_y = movement_y * player_speed
			state = "MOVING"
		else:
			# Detener el movimiento cuando no hay input
			velocity_x = 0
			velocity_y = 0
			state = "IDLE"
		
		# Actualizar posición
		player_x += velocity_x * delta_time
		player_y += velocity_y * delta_time
		
		# Mantener jugador en pantalla
		player_x = max(player_size//2, min(screen_width - player_size//2, player_x))
		player_y = max(player_size//2, min(screen_height - player_size//2, player_y))
		
		# Renderizar
		screen.fill((50, 100, 150))
		
		# Renderizar jugador
		player_color = (255, 0, 0) if state == "MOVING" else (255, 255, 0)
		pygame.draw.circle(screen, player_color, (int(player_x), int(player_y)), player_size//2)
		
		# Renderizar información de debug
		font = pygame.font.Font(None, 24)
		debug_info = [
			f"Posición: ({int(player_x)}, {int(player_y)})",
			f"Velocidad: ({velocity_x:.1f}, {velocity_y:.1f})",
			f"Estado: {state}",
			f"FPS: {int(clock.get_fps())}",
			"",
			"Controles:",
			"WASD - Mover",
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
	print("✅ Test de movimiento simple completado")

if __name__ == "__main__":
	test_simple_player() 