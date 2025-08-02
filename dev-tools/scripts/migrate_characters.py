#!/usr/bin/env python3
"""
Migración de datos de personajes a SQLite
==========================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Script para migrar datos de characters.json a la base de datos SQLite.
"""

import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.utils.config_database import ConfigDatabase
    from src.utils.database_manager import DatabaseManager
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print(f"   Directorio de trabajo: {Path.cwd()}")
    print(f"   Directorio del proyecto: {project_root}")
    sys.exit(1)


def migrate_character_data():
    """Migra datos de characters.json a SQLite."""
    print("🔄 Iniciando migración de datos de personajes...")
    
    # Cargar datos del JSON
    characters_file = project_root / "config" / "characters.json"
    if not characters_file.exists():
        print(f"❌ No se encuentra {characters_file}")
        return False
        
    try:
        with open(characters_file, encoding="utf-8") as f:
            data = json.load(f)
        
        characters = data.get("characters", {})
        print(f"📚 Encontrados {len(characters)} personajes en JSON")
        
        # Inicializar base de datos
        db_manager = DatabaseManager("data/game.db")
        config_db = ConfigDatabase(db_manager)
        
        # Migrar cada personaje
        migrated = 0
        for char_name, char_data in characters.items():
            try:
                # Adaptar estructura para SQLite
                character_record = {
                    "nombre": char_name,
                    "nombre_mostrar": char_data.get("nombre", char_name),
                    "tipo": char_data.get("tipo", ""),
                    "descripcion": char_data.get("descripcion", ""),
                    "stats": char_data.get("stats", {}),
                    "ataques": char_data.get("ataques", []),
                    "sprite_config": {
                        "escala_sprite": char_data.get("escala_sprite", 1.0),
                        "color_placeholder": char_data.get("color_placeholder", [255, 255, 255]),
                        "símbolo": char_data.get("símbolo", "?")
                    },
                    "activo": True
                }
                
                success = config_db.save_character_data(character_record)
                if success:
                    print(f"✅ {char_name} migrado exitosamente")
                    migrated += 1
                else:
                    print(f"❌ Error migrando {char_name}")
                    
            except Exception as e:
                print(f"❌ Error procesando {char_name}: {e}")
        
        print(f"\n🎯 Migración completada: {migrated}/{len(characters)} personajes")
        
        # Verificar migración
        print("\n🔍 Verificando migración...")
        for char_name in characters.keys():
            retrieved = config_db.get_character_data(char_name)
            if retrieved:
                print(f"✅ {char_name} verificado en base de datos")
            else:
                print(f"❌ {char_name} NO encontrado en base de datos")
        
        return migrated > 0
        
    except Exception as e:
        print(f"💥 Error en migración: {e}")
        return False


if __name__ == "__main__":
    success = migrate_character_data()
    sys.exit(0 if success else 1)
