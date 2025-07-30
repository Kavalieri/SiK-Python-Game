"""
Limpieza y Organización de Tests
===============================

Autor: SiK Team
Fecha: 2024
Descripción: Script para limpiar y organizar todos los tests redundantes.
"""

import os
import shutil


def cleanup_tests():
    """Limpia y organiza todos los tests redundantes."""

    print("=== LIMPIEZA Y ORGANIZACIÓN DE TESTS ===")

    # Lista de archivos de test a eliminar (redundantes)
    files_to_delete = [
        # Tests de personajes redundantes
        "scripts/test_character_select_final.py",
        "scripts/test_sprites_and_buttons.py",
        "scripts/test_character_select_simple.py",
        "scripts/test_simple_character_navigation.py",
        "scripts/test_character_navigation.py",
        "scripts/test_simple_character_menu.py",
        "scripts/test_character_select_menu.py",
        "scripts/test_character_system.py",
        # Tests de jugador redundantes
        "scripts/test_simple_player_size.py",
        "scripts/test_player_size.py",
        "scripts/test_simple_player.py",
        "scripts/test_player_movement.py",
        "scripts/test_player_animations.py",
        # Tests de sistema redundantes
        "scripts/test_complete_system.py",
        "scripts/test_complete_character_system.py",
        "scripts/test_world_generation.py",
        "scripts/test_world_elements.py",
        "scripts/test_desert_background.py",
        "scripts/test_tiles_and_menu.py",
        "scripts/test_loading_system.py",
        "scripts/test_camera_system.py",
        # Tests duplicados en tests/
        "tests/test_enemy_system.py",  # Ya existe en scripts/
        "tests/test_powerup_system.py",  # Ya existe en scripts/
        "tests/test_projectile_system.py",  # Ya existe en scripts/
        "tests/test_world_system.py",  # Ya existe en scripts/
    ]

    # Lista de archivos a mover a tests/
    files_to_move = [
        ("scripts/test_enemy_system.py", "tests/test_enemy_system.py"),
        ("scripts/test_powerup_system.py", "tests/test_powerup_system.py"),
        ("scripts/test_projectile_system.py", "tests/test_projectile_system.py"),
        ("scripts/test_world_system.py", "tests/test_world_system.py"),
        ("scripts/test_config.py", "tests/test_config.py"),
    ]

    # Archivos a mantener en scripts/
    files_to_keep = [
        "scripts/run_tests.py",
        "scripts/reorganize_characters.py",
        "scripts/clean_asset_names.py",
        "scripts/MEJORAS_IMPLEMENTADAS.md",
        "scripts/README.md",
    ]

    print(f"Archivos a eliminar: {len(files_to_delete)}")
    print(f"Archivos a mover: {len(files_to_move)}")
    print(f"Archivos a mantener: {len(files_to_keep)}")

    # Eliminar archivos redundantes
    deleted_count = 0
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✓ Eliminado: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error eliminando {file_path}: {e}")
        else:
            print(f"⚠ No encontrado: {file_path}")

    # Mover archivos a tests/
    moved_count = 0
    for src, dst in files_to_move:
        if os.path.exists(src):
            try:
                # Crear directorio de destino si no existe
                os.makedirs(os.path.dirname(dst), exist_ok=True)

                # Mover archivo
                shutil.move(src, dst)
                print(f"✓ Movido: {src} → {dst}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Error moviendo {src}: {e}")
        else:
            print(f"⚠ No encontrado: {src}")

    # Crear archivo de índice de tests
    create_test_index()

    # Crear script de ejecución unificado
    create_unified_runner()

    print("\n=== RESUMEN ===")
    print(f"Archivos eliminados: {deleted_count}")
    print(f"Archivos movidos: {moved_count}")
    print("Limpieza completada")


def create_test_index():
    """Crea un archivo de índice de tests."""

    index_content = '''"""
Índice de Tests
==============

Autor: SiK Team
Fecha: 2024
Descripción: Índice de todos los tests disponibles en el proyecto.

TESTS PRINCIPALES:
=================

1. tests/test_unified_system.py
   - Test unificado que combina todas las funcionalidades
   - Sistema de personajes, animación, powerups, UI, navegación
   - Interfaz gráfica con resultados en tiempo real
   - Uso: python tests/test_unified_system.py

2. tests/test_config_manager.py
   - Test del sistema de configuración
   - Verificación de carga y guardado de configuraciones
   - Uso: python tests/test_config_manager.py

3. tests/test_enemy_system.py
   - Test del sistema de enemigos
   - Verificación de tipos, comportamientos y sprites
   - Uso: python tests/test_enemy_system.py

4. tests/test_powerup_system.py
   - Test del sistema de powerups
   - Verificación de sprites y efectos
   - Uso: python tests/test_powerup_system.py

5. tests/test_projectile_system.py
   - Test del sistema de proyectiles
   - Verificación de tipos y comportamientos
   - Uso: python tests/test_projectile_system.py

6. tests/test_world_system.py
   - Test del sistema de mundo
   - Verificación de generación y elementos
   - Uso: python tests/test_world_system.py

SCRIPTS DE UTILIDAD:
===================

1. scripts/run_tests.py
   - Ejecutor de tests automatizado
   - Uso: python scripts/run_tests.py

2. scripts/reorganize_characters.py
   - Reorganización de directorios de personajes
   - Uso: python scripts/reorganize_characters.py

3. scripts/clean_asset_names.py
   - Limpieza de nombres de assets
   - Uso: python scripts/clean_asset_names.py

EJECUCIÓN RÁPIDA:
================

Para ejecutar todos los tests:
python scripts/run_tests.py

Para ejecutar el test unificado:
python tests/test_unified_system.py

Para ejecutar un test específico:
python tests/test_[nombre].py
'''

    with open("tests/README.md", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("✓ Creado: tests/README.md")


def create_unified_runner():
    """Crea un script de ejecución unificado."""

    runner_content = '''"""
Ejecutor Unificado de Tests
==========================

Autor: SiK Team
Fecha: 2024
Descripción: Script para ejecutar todos los tests de manera unificada.
"""

import sys
import os
import subprocess
import time

def run_test(test_path):
    """Ejecuta un test específico."""
    try:
        print(f"\\n=== Ejecutando: {test_path} ===")
        result = subprocess.run([sys.executable, test_path],
                              capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print(f"✓ {test_path}: EXITOSO")
            return True
        else:
            print(f"✗ {test_path}: FALLIDO")
            print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ {test_path}: TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ {test_path}: ERROR - {e}")
        return False

def main():
    """Función principal."""
    print("=== EJECUTOR UNIFICADO DE TESTS ===")

    # Lista de tests a ejecutar
    tests = [
        "tests/test_unified_system.py",
        "tests/test_config_manager.py",
        "tests/test_enemy_system.py",
        "tests/test_powerup_system.py",
        "tests/test_projectile_system.py",
        "tests/test_world_system.py"
    ]

    # Verificar que los archivos existen
    existing_tests = []
    for test in tests:
        if os.path.exists(test):
            existing_tests.append(test)
        else:
            print(f"⚠ Test no encontrado: {test}")

    if not existing_tests:
        print("No se encontraron tests para ejecutar")
        return

    # Ejecutar tests
    start_time = time.time()
    successful_tests = 0

    for test in existing_tests:
        if run_test(test):
            successful_tests += 1

    end_time = time.time()
    total_time = end_time - start_time

    # Resumen
    print(f"\\n=== RESUMEN ===")
    print(f"Tests ejecutados: {len(existing_tests)}")
    print(f"Tests exitosos: {successful_tests}")
    print(f"Tests fallidos: {len(existing_tests) - successful_tests}")
    print(f"Tiempo total: {total_time:.2f} segundos")

    if successful_tests == len(existing_tests):
        print("✓ Todos los tests pasaron exitosamente")
    else:
        print("✗ Algunos tests fallaron")

if __name__ == "__main__":
    main()
'''

    with open("scripts/run_unified_tests.py", "w", encoding="utf-8") as f:
        f.write(runner_content)

    print("✓ Creado: scripts/run_unified_tests.py")


if __name__ == "__main__":
    cleanup_tests()
