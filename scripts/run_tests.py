"""
Run Tests - Ejecutor de Tests
============================

Autor: SiK Team
Fecha: 2024
Descripción: Script maestro para ejecutar todos los tests del proyecto.
"""

import os
import sys
import subprocess
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_menu():
    """Muestra el menú de tests disponibles."""
    print("\n" + "=" * 50)
    print("🧪 SISTEMA DE TESTS - SiK Python Game")
    print("=" * 50)
    print("1. Test Simple de Movimiento del Jugador")
    print("2. Test del Fondo de Desierto")
    print("3. Test de Elementos del Mundo")
    print("4. Test de Generación de Mundo")
    print("5. Test del Sistema Completo")
    print("6. Test del Layout del Menú de Personajes")
    print("7. Ejecutar Todos los Tests")
    print("0. Salir")
    print("=" * 50)


def run_test(test_name, script_path):
    """Ejecuta un test específico."""
    print(f"\n🚀 Ejecutando: {test_name}")
    print("-" * 40)

    try:
        # Ejecutar el script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode == 0:
            print(f"✅ {test_name} completado exitosamente")
        else:
            print(f"❌ {test_name} falló con código {result.returncode}")

    except Exception as e:
        print(f"❌ Error ejecutando {test_name}: {e}")

    input("\nPresiona Enter para continuar...")


def run_all_tests():
    """Ejecuta todos los tests en secuencia."""
    tests = [
        ("Test Simple de Movimiento del Jugador", "test_simple_player.py"),
        ("Test del Fondo de Desierto", "test_desert_background.py"),
        ("Test de Elementos del Mundo", "test_world_elements.py"),
        ("Test de Generación de Mundo", "test_world_generation.py"),
        ("Test del Sistema Completo", "test_complete_system.py"),
        ("Test del Layout del Menú de Personajes", "test_simple_character_menu.py"),
    ]

    print("\n🚀 Ejecutando todos los tests...")
    print("=" * 50)

    for test_name, script_path in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=False,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__)),
            )

            if result.returncode == 0:
                print(f"✅ {test_name} - EXITOSO")
            else:
                print(f"❌ {test_name} - FALLÓ")

        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")

        print("-" * 30)

    print("\n🎉 Ejecución de todos los tests completada")
    input("\nPresiona Enter para continuar...")


def main():
    """Función principal del ejecutor de tests."""
    print("🧪 Bienvenido al Sistema de Tests de SiK Python Game")

    while True:
        show_menu()

        try:
            choice = input("\nSelecciona una opción (0-7): ").strip()

            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            elif choice == "1":
                run_test(
                    "Test Simple de Movimiento del Jugador", "test_simple_player.py"
                )
            elif choice == "2":
                run_test("Test del Fondo de Desierto", "test_desert_background.py")
            elif choice == "3":
                run_test("Test de Elementos del Mundo", "test_world_elements.py")
            elif choice == "4":
                run_test("Test de Generación de Mundo", "test_world_generation.py")
            elif choice == "5":
                run_test("Test del Sistema Completo", "test_complete_system.py")
            elif choice == "6":
                run_test(
                    "Test del Layout del Menú de Personajes",
                    "test_simple_character_menu.py",
                )
            elif choice == "7":
                run_all_tests()
            else:
                print("❌ Opción no válida. Por favor, selecciona 0-7.")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
