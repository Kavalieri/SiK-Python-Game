"""
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
        print(f"\n=== Ejecutando: {test_path} ===")
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
    print(f"\n=== RESUMEN ===")
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
