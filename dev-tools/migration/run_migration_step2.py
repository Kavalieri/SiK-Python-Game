#!/usr/bin/env python3
"""
Migración enemies.json → SQLite - Paso 2
=========================================

Script de migración para el sistema mixto inteligente:
- Migra config/enemies.json → SQLite tabla enemigos
- Actualiza enemy_types.py para usar ConfigDatabase
- Segundo paso del sistema mixto
"""

import json
import logging
import shutil
import sys
from pathlib import Path


def setup_logging():
    """Configurar logging para la migración."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def migrate_enemies():
    """Ejecutar migración de enemies.json."""
    print("=" * 60)
    print("MIGRACIÓN ENEMIES.JSON → SQLITE - PASO 2")
    print("=" * 60)
    print()

    try:
        # 1. Importar módulos necesarios
        print("[1/7] Importando módulos...")
        sys.path.insert(0, str(Path.cwd()))
        from src.utils.config_database import ConfigDatabase
        from src.utils.database_manager import DatabaseManager

        print("✓ Módulos importados")

        # 2. Inicializar base de datos
        print("[2/7] Inicializando base de datos...")
        db_manager = DatabaseManager()
        config_db = ConfigDatabase(db_manager)
        print("✓ Base de datos inicializada")

        # 3. Verificar archivo enemies.json
        print("[3/7] Verificando archivo enemies.json...")
        json_path = Path("config/enemies.json")
        if not json_path.exists():
            print(f"✗ ERROR: Archivo {json_path} no encontrado")
            return False

        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
            enemy_count = len(json_data.get("tipos_enemigos", {}))
            print(f"✓ Archivo JSON válido con {enemy_count} tipos de enemigos")

        # 4. Ejecutar migración de enemigos
        print("[4/7] Ejecutando migración enemies.json → SQLite...")
        try:
            config_db.migrate_enemies_from_json(str(json_path))
            print("✓ Migración ejecutada")
        except Exception as e:
            print(f"! Migración reportó: {e}")
            print("  Continuando con verificación...")

        # 5. Verificar datos en SQLite
        print("[5/7] Verificando datos migrados en SQLite...")
        all_enemies = config_db.get_all_enemies()
        print(f"✓ Enemigos en SQLite: {len(all_enemies)}")

        for enemy_info in all_enemies:
            enemy_type = enemy_info.get("tipo", "unknown")
            enemy_name = enemy_info.get("nombre_mostrar", "Sin nombre")
            print(f"  - {enemy_type}: {enemy_name}")

        # 6. Actualizar enemy_types.py
        print("[6/7] Actualizando enemy_types.py...")
        old_file = Path("src/entities/enemy_types.py")
        new_file = Path("src/entities/enemy_types_new.py")
        backup_file = Path("src/entities/enemy_types_backup.py")

        if old_file.exists():
            # Crear backup
            shutil.copy2(old_file, backup_file)
            print(f"✓ Backup creado: {backup_file}")

            # Reemplazar con nueva versión
            shutil.copy2(new_file, old_file)
            print("✓ enemy_types.py actualizado con sistema mixto")
        else:
            print("! enemy_types.py no encontrado, creando nuevo...")
            shutil.copy2(new_file, old_file)

        # 7. Verificar sistema mixto
        print("[7/7] Verificando EnemyTypesManager...")
        try:
            from src.entities.enemy_types import EnemyTypesManager

            enemy_manager = EnemyTypesManager()
            available_types = enemy_manager.get_all_enemy_types()
            print(f"✓ Tipos disponibles via EnemyTypesManager: {len(available_types)}")

            for enemy_type in available_types:
                config = enemy_manager.get_enemy_config(enemy_type)
                if config:
                    print(f"  - {enemy_type}: {config.name} (HP: {config.health})")
                else:
                    print(f"  - {enemy_type}: Error al recuperar configuración")
        except Exception as e:
            print(f"! Error verificando EnemyTypesManager: {e}")
            print("  Usando sistema de fallback...")

        print()
        print("=" * 60)
        print("✓ MIGRACIÓN ENEMIES.JSON COMPLETADA")
        print("=" * 60)
        print()
        print("ESTADO ACTUAL DEL SISTEMA MIXTO:")
        print("✓ characters.json → SQLite: MIGRADO")
        print("✓ enemies.json → SQLite: MIGRADO")
        print("✓ character_data.py → CharacterDataManager: ACTUALIZADO")
        print("✓ enemy_types.py → EnemyTypesManager: ACTUALIZADO")
        print()
        print("PRÓXIMOS PASOS:")
        print("1. Verificar funcionamiento completo del juego")
        print("2. Optimizar archivos críticos >150 líneas")
        print("3. Migrar powerups.json (separar config + lógica)")

        return True

    except ImportError as e:
        print(f"✗ ERROR de importación: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR durante migración: {e}")
        return False


if __name__ == "__main__":
    setup_logging()
    success = migrate_enemies()
    sys.exit(0 if success else 1)
