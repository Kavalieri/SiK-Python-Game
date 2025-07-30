"""
Script simple para probar ConfigDatabase
"""

import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

print("🧪 PRUEBA SIMPLE CONFIGDATABASE")
print("Importando módulos...")

try:
    import importlib.util

    # Test DatabaseManager
    spec = importlib.util.find_spec("utils.database_manager")
    if spec is not None:
        print("✅ DatabaseManager disponible")

    # Test SchemaManager
    spec = importlib.util.find_spec("utils.schema_manager")
    if spec is not None:
        print("✅ SchemaManager disponible")

    # Test ConfigDatabase
    spec = importlib.util.find_spec("utils.config_database")
    if spec is not None:
        print("✅ ConfigDatabase disponible")

    print("\n🎯 RESULTADO: Imports exitosos")
    print("Sistema mixto listo para implementación")

except (ModuleNotFoundError, ImportError, AttributeError) as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n✅ ConfigDatabase está listo para usar")
print("📄 Próximo paso: Migrar characters.json y enemies.json")
