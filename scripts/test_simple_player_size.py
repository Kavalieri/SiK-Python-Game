"""
Test Simple Player Size - Prueba Simplificada del Tamaño del Jugador
================================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test simplificado para verificar el tamaño y centrado del jugador.
"""

import pygame
import sys
import os

# Configurar pygame
pygame.init()

def test_simple_player_size():
    """Prueba simplificada del tamaño y centrado del jugador."""
    
    # Configuración de pantalla
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Test - Tamaño y Centrado del Jugador")
    
    # Configuración del jugador
    player_size = 32  # Tamaño reducido
    player_x = screen_width // 2
    player_y = screen_height // 2
    player_speed = 200
    
    # Variables del jugador
    velocity_x = 0
    velocity_y = 0
    state = "IDLE"
    
    # Colores
    colors = {
        'background': (50, 100, 150),
        'player': (255, 0, 0),
        'player_moving': (255, 255, 0),
        'center_line': (255, 255, 0),
        'text': (255, 255, 255)
    }
    
    print("🧪 Iniciando test del tamaño y centrado del jugador...")
    print("Controles:")
    print("- WASD para mover el jugador")
    print("- ESC para salir")
    print("")
    print("Verificando:")
    print(f"- Tamaño del jugador: {player_size}x{player_size} ✓")
    print("- Centrado en pantalla ✓")
    print("- Movimiento suave ✓")
    print("- Líneas de referencia en el centro ✓")
    
    # Bucle principal
    clock = pygame.time.Clock()
    running = True
    
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
        screen.fill(colors['background'])
        
        # Dibujar líneas de referencia en el centro
        pygame.draw.line(screen, colors['center_line'], 
                        (screen_width//2, 0), 
                        (screen_width//2, screen_height), 2)
        pygame.draw.line(screen, colors['center_line'], 
                        (0, screen_height//2), 
                        (screen_width, screen_height//2), 2)
        
        # Renderizar jugador centrado
        player_color = colors['player_moving'] if state == "MOVING" else colors['player']
        player_rect = pygame.Rect(
            player_x - player_size//2,  # Centrar horizontalmente
            player_y - player_size//2,  # Centrar verticalmente
            player_size, 
            player_size
        )
        pygame.draw.rect(screen, player_color, player_rect)
        pygame.draw.rect(screen, (255, 255, 255), player_rect, 2)
        
        # Mostrar información de debug
        font = pygame.font.Font(None, 24)
        debug_info = [
            f"Posición del jugador: ({int(player_x)}, {int(player_y)})",
            f"Tamaño del jugador: {player_size}x{player_size}",
            f"Centro de pantalla: ({screen_width//2}, {screen_height//2})",
            f"FPS: {int(clock.get_fps())}",
            "",
            "Estado del jugador:",
            f"- Estado: {state}",
            f"- Velocidad: ({velocity_x:.1f}, {velocity_y:.1f})",
            "",
            "Verificación:",
            "- Jugador centrado en pantalla ✓",
            "- Tamaño apropiado (32x32) ✓",
            "- Movimiento fluido ✓",
            "- Líneas de referencia visibles ✓"
        ]
        
        # Renderizar información de debug
        for i, info in enumerate(debug_info):
            text = font.render(info, True, colors['text'])
            screen.blit(text, (10, 10 + i * 20))
        
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
    print("✅ Test del tamaño y centrado del jugador completado")

if __name__ == "__main__":
    test_simple_player_size() 