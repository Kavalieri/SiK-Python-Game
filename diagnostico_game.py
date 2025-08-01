#!/usr/bin/env python3
"""
Script de diagnóstico para la escena del juego
"""

import sys
from pathlib import Path
import traceback

print("=== DIAGNÓSTICO GAME SCENE ===")

# Añadir path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    print("1. Inicializando pygame...")
    import pygame
    pygame.init()
    print("   ✓ pygame inicializado")
    
    print("2. Creando ventana...")
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test GameScene")
    print("   ✓ Ventana creada")
    
    print("3. Importando configuración...")
    from src.utils.config_manager import ConfigManager
    config = ConfigManager()
    print("   ✓ Configuración cargada")
    
    print("4. Creando game_state mock...")
    class MockGameState:
        selected_character = "guerrero"
        
    game_state = MockGameState()
    print("   ✓ GameState creado")
    
    print("5. Importando GameScene...")
    from src.scenes.game_scene_core import GameScene
    print("   ✓ GameScene importado")
    
    print("6. Creando GameScene...")
    scene = GameScene(screen, config, game_state, None)
    print("   ✓ GameScene creado")
    
    print("7. Probando renderizado...")
    scene.render()
    print("   ✓ Renderizado completado")
    
    print("8. Mostrando ventana por 3 segundos...")
    pygame.display.flip()
    pygame.time.wait(3000)
    
    pygame.quit()
    print("✓ Prueba completada exitosamente")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nTraceback completo:")
    traceback.print_exc()

print("=== FIN DIAGNÓSTICO GAME SCENE ===")
