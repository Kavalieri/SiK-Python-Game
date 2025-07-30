#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migración characters.json → SQLite
===================================

Script de migración para el sistema mixto inteligente:
- Migra config/characters.json → SQLite tabla personajes
- Prepara la eliminación de character_data.py hardcodeado
- Primer paso del sistema mixto
"""

import logging
import sys
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))


def setup_logging():
    """Configurar logging para la migración."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def migrate_characters():
    """Ejecutar migración de characters.json."""
    try:
        print("=== MIGRACIÓN CHARACTERS.JSON → SQLITE ===")
        print()

        # 1. Importar módulos necesarios
        print("[1/5] Importando módulos...")
        from src.utils.config_database import ConfigDatabase
        from src.utils.database_manager import DatabaseManager

        # 2. Inicializar base de datos
        print("[2/5] Inicializando base de datos...")
        db_manager = DatabaseManager()
        config_db = ConfigDatabase(db_manager)

        # 3. Verificar archivo characters.json
        print("[3/5] Verificando archivo characters.json...")
        json_path = Path("config/characters.json")
        if not json_path.exists():
            print(f"ERROR: Archivo {json_path} no encontrado")
            return False

        # 4. Ejecutar migración
        print("[4/5] Ejecutando migración...")
        config_db.migrate_characters_from_json(str(json_path))

        # 5. Verificar migración
        print("[5/5] Verificando migración...")
        all_characters = config_db.get_all_characters()
        print(f"Personajes migrados: {len(all_characters)}")

        for char_info in all_characters:
            char_name = (
                char_info
                if isinstance(char_info, str)
                else char_info.get("nombre", "unknown")
            )
            char_data = config_db.get_character_data(char_name)
            if char_data:
                print(f"  ✓ {char_name}: {char_data.get('nombre', 'Sin nombre')}")
            else:
                print(f"  ✗ {char_name}: Error al recuperar datos")

        print()
        print("=== MIGRACIÓN COMPLETADA EXITOSAMENTE ===")
        print()
        print("PRÓXIMOS PASOS:")
        print("1. Actualizar src/entities/character_data.py para usar ConfigDatabase")
        print("2. Eliminar diccionario CHARACTER_DATA hardcodeado")
        print("3. Migrar config/enemies.json")

        return True

    except ImportError as e:
        print(f"ERROR de importación: {e}")
        print("Verifique que los módulos estén disponibles")
        return False
    except Exception as e:
        print(f"ERROR durante migración: {e}")
        return False


if __name__ == "__main__":
    setup_logging()

    print("Iniciando migración del sistema mixto...")
    print("Fase 1: characters.json → SQLite")
    print()

    success = migrate_characters()

    if success:
        print("✓ Migración exitosa")
        sys.exit(0)
    else:
        print("✗ Migración falló")
        sys.exit(1)
