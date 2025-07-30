#!/usr/bin/env python3
"""
Script de debug para el GameEngine
"""

import sys
from pathlib import Path

# Importar GameEngine y ConfigManager
from src.core.game_engine import GameEngine
from src.utils.config_manager import ConfigManager

# Asegurar que el directorio raíz está en el path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def debug_game_engine():
    """Debug del GameEngine."""
    print("=== DEBUG DEL GAME ENGINE ===\n")

    try:
        # Crear configuración
        print("1. Creando configuración...")
        config = ConfigManager()
        print("✅ Configuración creada")

        # Crear GameEngine
        print("2. Creando GameEngine...")
        game_engine = GameEngine(config)
        print("✅ GameEngine creado")

        # Verificar que la pantalla se creó
        print("3. Verificando pantalla...")
        if game_engine.screen:
            print(f"✅ Pantalla creada: {game_engine.screen.get_size()}")
        else:
            print("❌ Pantalla no creada")
            return

        # Verificar escenas
        print("4. Verificando escenas...")
        if game_engine.scene_manager:
            print("✅ SceneManager creado")
            print(
                f"   Escenas disponibles: {list(game_engine.scene_manager.scenes.keys())}"
            )
            print(f"   Escena actual: {game_engine.scene_manager.current_scene}")
        else:
            print("❌ SceneManager no creado")
            return

        # Verificar menús
        print("5. Verificando menús...")
        if game_engine.menu_manager:
            print("✅ MenuManager creado")
            print(f"   Menús disponibles: {game_engine.menu_manager.get_menu_names()}")
        else:
            print("❌ MenuManager no creado")
            return

        print("\n6. Iniciando bucle principal...")
        print("✅ Presiona ESC para salir")

        # Ejecutar bucle principal
        game_engine.run()

        print("✅ Bucle principal completado")

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except ValueError as e:
        print(f"Valor inválido: {e}")
    except RuntimeError as e:
        print(f"Error de ejecución: {e}")


if __name__ == "__main__":
    debug_game_engine()
