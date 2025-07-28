#!/usr/bin/env python3
"""
Script de prueba simple para verificar el bucle principal del juego
"""

import sys
import pygame
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.config_manager import ConfigManager

def test_simple_game():
    """Prueba un bucle de juego simple."""
    print("=== PRUEBA DE BUCLE PRINCIPAL ===\n")
    
    try:
        # Inicializar pygame
        pygame.init()
        
        # Crear pantalla
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Test - Bucle Principal")
        
        # Crear configuración
        config = ConfigManager()
        
        # Configurar reloj
        clock = pygame.time.Clock()
        fps = config.get_fps()
        
        print(f"✅ Pygame inicializado")
        print(f"✅ Pantalla creada: 1280x720")
        print(f"✅ FPS configurado: {fps}")
        print("✅ Presiona ESC para salir")
        
        # Bucle principal
        running = True
        frame_count = 0
        
        while running:
            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Actualizar lógica (aquí iría la lógica del juego)
            frame_count += 1
            
            # Renderizar
            screen.fill((50, 50, 100))  # Fondo azul
            
            # Dibujar texto de prueba
            font = pygame.font.Font(None, 36)
            text = font.render(f"Frame: {frame_count} - Presiona ESC para salir", True, (255, 255, 255))
            text_rect = text.get_rect(center=(640, 360))
            screen.blit(text, text_rect)
            
            # Actualizar pantalla
            pygame.display.flip()
            
            # Controlar FPS
            clock.tick(fps)
        
        pygame.quit()
        print(f"✅ Prueba completada - {frame_count} frames renderizados")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_game() 