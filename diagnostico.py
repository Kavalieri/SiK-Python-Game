#!/usr/bin/env python3
"""
Script de diagnóstico para encontrar el problema de arranque
"""

import sys
from pathlib import Path

print("=== DIAGNÓSTICO DE ARRANQUE ===")

# Añadir path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
print(f"✓ Path añadido: {project_root}")

try:
    print("1. Importando pygame...")
    import pygame
    print("   ✓ pygame importado")
    
    print("2. Importando pygame_gui...")
    import pygame_gui
    print("   ✓ pygame_gui importado")
    
    print("3. Inicializando pygame...")
    pygame.init()
    print("   ✓ pygame inicializado")
    
    print("4. Importando ConfigManager...")
    from src.utils.config_manager import ConfigManager
    print("   ✓ ConfigManager importado")
    
    print("5. Importando Logger...")
    from src.utils.logger import setup_logger
    print("   ✓ Logger importado")
    
    print("6. Configurando logger...")
    logger = setup_logger()
    print("   ✓ Logger configurado")
    
    print("7. Importando GameEngine...")
    from src.core.game_engine import GameEngine
    print("   ✓ GameEngine importado")
    
    print("8. Cargando configuración...")
    config = ConfigManager()
    print("   ✓ Configuración cargada")
    
    print("9. Creando GameEngine...")
    engine = GameEngine(config)
    print("   ✓ GameEngine creado")
    
    print("10. Iniciando juego...")
    engine.run()
    
except Exception as e:
    print(f"❌ ERROR en paso: {e}")
    import traceback
    traceback.print_exc()

print("=== FIN DIAGNÓSTICO ===")
