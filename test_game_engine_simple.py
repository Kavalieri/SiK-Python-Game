#!/usr/bin/env python3
"""
Script de prueba que simula el GameEngine de forma simplificada
"""

import sys
import pygame
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.config_manager import ConfigManager
from src.core.game_state import GameState
from src.utils.save_manager import SaveManager
from src.ui.menu_manager import MenuManager

def test_game_engine_simple():
    """Prueba el GameEngine de forma simplificada."""
    print("=== PRUEBA DE GAME ENGINE SIMPLIFICADO ===\n")
    
    try:
        # Inicializar pygame
        pygame.init()
        
        # Crear pantalla
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Test - Game Engine Simple")
        
        # Crear componentes
        config = ConfigManager()
        game_state = GameState()
        save_manager = SaveManager(config)
        
        # Crear menú manager
        menu_manager = MenuManager(screen, config, game_state, save_manager)
        
        # Mostrar menú de bienvenida
        menu_manager.show_menu('welcome')
        
        print("✅ Componentes inicializados")
        print("✅ Menú de bienvenida mostrado")
        print("✅ Presiona ESC para salir")
        
        # Bucle principal simplificado
        running = True
        clock = pygame.time.Clock()
        fps = config.get_fps()
        
        while running:
            # Procesar eventos
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Actualizar menú
            menu_manager.update(events)
            
            # Renderizar
            screen.fill((0, 0, 0))
            menu_manager.render()
            pygame.display.flip()
            
            # Controlar FPS
            clock.tick(fps)
        
        pygame.quit()
        print("✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_game_engine_simple() 