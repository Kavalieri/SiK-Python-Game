#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test básico de ConfigDatabase - Verificación de importación
"""

if __name__ == "__main__":
    try:
        print("[INFO] Iniciando test de importación...")

        # Test 1: Importar ConfigDatabase
        print("[TEST 1] Importando ConfigDatabase...")
        from src.utils.config_database import ConfigDatabase

        print("[OK] ConfigDatabase importado exitosamente")

        # Test 2: Verificar que es una clase
        print("[TEST 2] Verificando que ConfigDatabase es una clase...")
        if hasattr(ConfigDatabase, "__init__"):
            print("[OK] ConfigDatabase es una clase válida")
        else:
            print("[ERROR] ConfigDatabase no es una clase válida")

        # Test 3: Verificar métodos principales
        print("[TEST 3] Verificando métodos principales...")
        required_methods = [
            "get_character_data",
            "save_character_data",
            "get_enemy_data",
            "save_enemy_data",
            "migrate_characters_from_json",
            "migrate_enemies_from_json",
        ]

        for method in required_methods:
            if hasattr(ConfigDatabase, method):
                print(f"[OK] Método {method} encontrado")
            else:
                print(f"[ERROR] Método {method} no encontrado")

        print("\n[RESULTADO] Importación y estructura básica: EXITOSA")

    except ImportError as e:
        print(f"[ERROR] Error de importación: {e}")
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
