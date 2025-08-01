#!/usr/bin/env python3
"""
Solución unificada de base de datos SQLite
Inicializa ambas bases de datos para resolver conflictos de rutas
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.database_manager import DatabaseManager
from src.utils.schema_manager import SchemaManager


def inicializar_bd(ruta_bd: str, nombre: str):
	"""Inicializa una base de datos específica."""
	print(f"\n=== INICIALIZANDO {nombre}: {ruta_bd} ===")
	
	try:
		# Crear directorio si no existe
		os.makedirs(os.path.dirname(ruta_bd), exist_ok=True)
		
		# Inicializar
		db_manager = DatabaseManager(ruta_bd)
		schema_manager = SchemaManager(db_manager)
		
		# Crear tablas
		print("🔨 Creando tablas...")
		if schema_manager.create_all_tables():
			print("✅ Tablas creadas exitosamente")
			
			# Validar
			validation = schema_manager.validate_schema()
			if validation["valid"]:
				print(f"✅ Validación exitosa")
				print(f"🗃️  Tablas: {', '.join(validation['tables_found'])}")
				return True
			else:
				print(f"❌ Validación falló: {validation['errors']}")
				return False
		else:
			print("❌ Error creando tablas")
			return False
			
	except Exception as e:
		print(f"❌ ERROR: {e}")
		return False
	finally:
		if 'db_manager' in locals():
			db_manager.close_all_connections()


def main():
	"""Función principal."""
	print("=== SOLUCIONANDO PROBLEMA DE BASES DE DATOS ===")
	
	# Inicializar ambas bases de datos
	bd1_ok = inicializar_bd("data/game.db", "BD PRINCIPAL")
	bd2_ok = inicializar_bd("saves/game_database.db", "BD MÓDULOS")
	
	if bd1_ok and bd2_ok:
		print("\n✅ AMBAS BASES DE DATOS INICIALIZADAS CORRECTAMENTE")
		print("🎮 El juego debería funcionar sin errores SQLite")
		return True
	else:
		print("\n❌ ERROR EN INICIALIZACIÓN")
		return False


if __name__ == "__main__":
	success = main()
	sys.exit(0 if success else 1)
