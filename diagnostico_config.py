#!/usr/bin/env python3
"""
Script de diagnóstico específico para ConfigManager
"""

import sys
from pathlib import Path
import traceback

print("=== DIAGNÓSTICO CONFIG MANAGER ===")

# Añadir path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    print("1. Importando ConfigManager...")
    from src.utils.config_manager import ConfigManager
    print("   ✓ ConfigManager importado")
    
    print("2. Verificando archivo config.json...")
    config_file = Path("config.json")
    if config_file.exists():
        print(f"   ✓ config.json existe: {config_file.stat().st_size} bytes")
    else:
        print("   ❌ config.json NO existe")
        
    print("3. Verificando directorio data...")
    data_dir = Path("data")
    if data_dir.exists():
        print(f"   ✓ Directorio data existe")
        db_file = data_dir / "game.db"
        if db_file.exists():
            print(f"   ✓ game.db existe: {db_file.stat().st_size} bytes")
        else:
            print("   ❌ game.db NO existe")
    else:
        print("   ❌ Directorio data NO existe")
    
    print("4. Creando ConfigManager...")
    config = ConfigManager()
    print("   ✓ ConfigManager creado exitosamente")
    
    print("5. Probando acceso básico...")
    display_config = config.get_section("display")
    print(f"   ✓ Configuración display: {len(display_config) if display_config else 0} elementos")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nTraceback completo:")
    traceback.print_exc()

print("=== FIN DIAGNÓSTICO CONFIG ===")
