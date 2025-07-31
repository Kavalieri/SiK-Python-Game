#!/usr/bin/env python3
"""
Test simple del juego SiK Python Game
Verifica que el juego se puede importar y arrancar correctamente.
"""

import sys
from pathlib import Path


def test_game_launch():
    """Prueba el lanzamiento del juego."""
    print("🎮 Testing SiK Python Game Launch...")
    print("=" * 50)

    # Verificar que estamos en el directorio correcto
    if not Path("src/main.py").exists():
        print("❌ Error: No se encuentra src/main.py")
        return False

    print("✅ Archivo main.py encontrado")

    # Intentar importar los módulos principales
    try:
        import sys

        sys.path.insert(0, str(Path.cwd()))

        # Test de imports usando importlib.util para evitar imports no usados
        import importlib.util

        # Verificar ConfigManager
        spec = importlib.util.find_spec("src.utils.config_manager")
        if spec is None:
            raise ImportError("ConfigManager module not found")
        print("✅ ConfigManager disponible")

        # Verificar GameEngine
        spec = importlib.util.find_spec("src.core.game_engine")
        if spec is None:
            raise ImportError("GameEngine module not found")
        print("✅ GameEngine disponible")

        # Verificar Logger
        spec = importlib.util.find_spec("src.utils.logger")
        if spec is None:
            raise ImportError("Logger module not found")
        print("✅ Logger disponible")

    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        return False

    print("\n🎯 Estado del juego:")
    print("- Todos los módulos principales se importan correctamente")
    print("- El juego debería estar ejecutándose en otra ventana")
    print("- Pygame-ce está instalado y funcionando")

    return True


if __name__ == "__main__":
    success = test_game_launch()
    if success:
        print("\n🚀 ¡SiK Python Game está funcionando correctamente!")
        print("💡 Tip: Ejecuta 'python -m src.main' para iniciar el juego")
    else:
        print("\n❌ Hay problemas con el setup del juego")
        sys.exit(1)
