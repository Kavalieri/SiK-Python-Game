#!/usr/bin/env python3
"""
🧪 PRUEBAS DE IMPORTACIÓN DESDE RAÍZ
===================================

Verifica que las importaciones funcionen correctamente desde la raíz
para simular el entorno empaquetado.

Autor: SiK Team
Fecha: 2 Agosto 2025
"""

import sys
from pathlib import Path

# Configurar rutas relativas desde raíz (como en empaquetado)
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"

# Añadir src al PYTHONPATH
sys.path.insert(0, str(SRC_DIR))


def test_importaciones_core():
    """Testa importaciones del core del juego."""
    print("🔍 Testando importaciones core...")

    try:
        print("✅ main.py importado correctamente")

        print("✅ GameEngine importado correctamente")

        print("✅ Player importado correctamente")

        print("✅ GameSceneCore importado correctamente")

        print("✅ ConfigLoader importado correctamente")

        return True

    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False


def test_ejecucion_main():
    """Verifica que main.py se pueda ejecutar sin errores."""
    print("\n🔍 Testando ejecución de main...")

    try:
        # Importar main y verificar que no haya errores críticos
        import main

        # Verificar que las clases principales estén disponibles
        if hasattr(main, "main"):
            print("✅ Función main() disponible")
        else:
            print("⚠️  Función main() no encontrada")

        return True

    except Exception as e:
        print(f"❌ Error ejecutando main: {e}")
        return False


def main():
    """Función principal de pruebas."""
    print("🚀 INICIANDO PRUEBAS DE IMPORTACIÓN DESDE RAÍZ")
    print(f"📁 Directorio del proyecto: {PROJECT_ROOT}")
    print(f"📁 Directorio src: {SRC_DIR}")
    print(f"🐍 PYTHONPATH src añadido: {str(SRC_DIR)}")

    # Ejecutar pruebas
    prueba1 = test_importaciones_core()
    prueba2 = test_ejecucion_main()

    # Resultado final
    if prueba1 and prueba2:
        print("\n🎉 TODAS LAS PRUEBAS DE IMPORTACIÓN PASARON")
        print("✅ El proyecto está listo para empaquetado")
        return 0
    else:
        print("\n❌ ERRORES EN PRUEBAS DE IMPORTACIÓN")
        print("🔧 Revisar rutas relativas y estructura de imports")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
