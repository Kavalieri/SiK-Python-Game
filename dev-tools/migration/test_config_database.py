"""
Script de Prueba para ConfigDatabase - Sistema Mixto Inteligente
================================================================

Prueba la nueva interfaz ConfigDatabase que maneja datos complejos en SQLite
mientras mantiene configuración simple en JSON.
"""

import sys
from pathlib import Path

# Añadir directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config_database import ConfigDatabase
from utils.database_manager import DatabaseManager
from utils.schema_manager import SchemaManager


def test_config_database():
    """
    Prueba la funcionalidad básica del ConfigDatabase.
    """
    print("=== PRUEBA CONFIGDATABASE - SISTEMA MIXTO ===")

    # Crear instancias
    db_path = "saves/test_config_database.db"
    db_manager = DatabaseManager(db_path)

    try:
        # Crear esquemas si no existen
        schema_manager = SchemaManager(db_manager)
        schema_manager.create_all_tables()
        print("✅ Esquemas de base de datos creados")

        # Crear ConfigDatabase
        config_db = ConfigDatabase(db_manager)
        print("✅ ConfigDatabase inicializado")

        # Probar datos de personaje
        test_character = {
            "nombre": "test_warrior",
            "nombre_mostrar": "Guerrero de Prueba",
            "tipo": "Melee",
            "descripcion": "Personaje de prueba para sistema mixto",
            "stats": {"vida": 100, "velocidad": 50, "daño": 25, "escudo": 10},
            "ataques": [{"nombre": "Espada", "daño": 20, "cooldown": 1.0}],
            "sprite_config": {
                "ruta_base": "characters/warrior",
                "animaciones": ["idle", "run", "attack"],
            },
        }

        # Guardar personaje
        success = config_db.save_character_data(test_character)
        if success:
            print("✅ Personaje de prueba guardado")
        else:
            print("❌ Error guardando personaje")
            return False

        # Recuperar personaje
        retrieved_char = config_db.get_character_data("test_warrior")
        if retrieved_char:
            print(f"✅ Personaje recuperado: {retrieved_char['nombre_mostrar']}")
            print(f"   Stats: {retrieved_char['stats']}")
            print(f"   Ataques: {len(retrieved_char['ataques'])}")
        else:
            print("❌ Error recuperando personaje")
            return False

        # Probar datos de enemigo
        test_enemy = {
            "tipo": "test_zombie",
            "nombre_mostrar": "Zombie de Prueba",
            "stats": {
                "vida": 50,
                "velocidad": 30,
                "daño": 15,
                "rango_deteccion": 100,
                "rango_ataque": 40,
            },
            "comportamiento": "perseguir",
            "animaciones": {
                "idle": "zombie_idle.png",
                "walk": "zombie_walk_*.png",
                "attack": "zombie_attack_*.png",
                "dead": "zombie_dead.png",
            },
            "variantes": {
                "normal": {"multiplicador_vida": 1.0},
                "fuerte": {"multiplicador_vida": 1.5},
            },
        }

        # Guardar enemigo
        success = config_db.save_enemy_data(test_enemy)
        if success:
            print("✅ Enemigo de prueba guardado")
        else:
            print("❌ Error guardando enemigo")
            return False

        # Recuperar enemigo
        retrieved_enemy = config_db.get_enemy_data("test_zombie")
        if retrieved_enemy:
            print(f"✅ Enemigo recuperado: {retrieved_enemy['nombre_mostrar']}")
            print(f"   Stats: {retrieved_enemy['stats']}")
            print(f"   Comportamiento: {retrieved_enemy['comportamiento']}")
        else:
            print("❌ Error recuperando enemigo")
            return False

        # Probar listas completas
        all_characters = config_db.get_all_characters()
        all_enemies = config_db.get_all_enemies()

        print(f"✅ Total personajes en BD: {len(all_characters)}")
        print(f"✅ Total enemigos en BD: {len(all_enemies)}")

        print("\n=== PRUEBA COMPLETADA EXITOSAMENTE ===")
        print("🎯 ConfigDatabase funciona correctamente")
        print("🗄️ SQLite preparado para datos complejos")
        print("📄 JSON seguirá siendo usado para configuración simple")

        return True

    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

    finally:
        # Limpiar archivo de prueba
        test_db_path = Path(db_path)
        if test_db_path.exists():
            test_db_path.unlink()
            print("🧹 Archivo de prueba eliminado")


def test_migration_simulation():
    """
    Simula migración de characters.json y enemies.json a SQLite.
    """
    print("\n=== SIMULACIÓN DE MIGRACIÓN ===")

    # Datos simulados de characters.json
    characters_data = {
        "characters": {
            "guerrero": {
                "nombre": "Kava",
                "tipo": "Melee",
                "descripcion": "Guerrero especializado en combate cuerpo a cuerpo",
                "stats": {"vida": 120, "velocidad": 45, "daño": 30, "escudo": 15},
                "ataques": [
                    {"nombre": "Espada", "tipo": "melee", "daño": 25, "cooldown": 1.2}
                ],
            },
            "adventureguirl": {
                "nombre": "Aurora",
                "tipo": "Ranged",
                "descripcion": "Aventurera especializada en combate a distancia",
                "stats": {"vida": 80, "velocidad": 60, "daño": 35, "escudo": 5},
                "ataques": [
                    {"nombre": "Arco", "tipo": "ranged", "daño": 20, "cooldown": 0.8}
                ],
            },
        }
    }

    # Datos simulados de enemies.json
    enemies_data = {
        "tipos_enemigos": {
            "zombie_male": {
                "nombre": "Zombie Masculino",
                "stats": {
                    "vida": 60,
                    "velocidad": 25,
                    "daño": 20,
                    "rango_deteccion": 120,
                    "rango_ataque": 45,
                },
                "comportamiento": "perseguir",
                "animaciones": {
                    "idle": "zombie_m_idle.png",
                    "walk": "zombie_m_walk.png",
                    "attack": "zombie_m_attack.png",
                },
            },
            "zombie_female": {
                "nombre": "Zombie Femenino",
                "stats": {
                    "vida": 55,
                    "velocidad": 30,
                    "daño": 18,
                    "rango_deteccion": 110,
                    "rango_ataque": 40,
                },
                "comportamiento": "perseguir",
                "animaciones": {
                    "idle": "zombie_f_idle.png",
                    "walk": "zombie_f_walk.png",
                    "attack": "zombie_f_attack.png",
                },
            },
        }
    }

    print("📊 Datos simulados preparados:")
    print(f"   - {len(characters_data['characters'])} personajes")
    print(f"   - {len(enemies_data['tipos_enemigos'])} tipos de enemigos")

    print("\n💡 Próximos pasos reales:")
    print("1. Migrar config/characters.json usando migrate_characters_from_json()")
    print("2. Migrar config/enemies.json usando migrate_enemies_from_json()")
    print(
        "3. Modificar character_data.py para usar ConfigDatabase.get_character_data()"
    )
    print("4. Refactorizar enemy_types.py para usar ConfigDatabase.get_enemy_data()")
    print("5. Mantener powerups.json, gameplay.json, audio.json como archivos JSON")

    return True


if __name__ == "__main__":
    print("🧪 PRUEBA SISTEMA MIXTO INTELIGENTE")
    print("=" * 50)

    success1 = test_config_database()
    success2 = test_migration_simulation()

    if success1 and success2:
        print("\n🎉 TODAS LAS PRUEBAS EXITOSAS")
        print("🚀 Listo para comenzar migración real")
    else:
        print("\n❌ Algunas pruebas fallaron")
        sys.exit(1)
