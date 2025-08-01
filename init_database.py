#!/usr/bin/env python3
"""
Script de inicialización de base de datos SQLite
Crea todas las tablas necesarias para el funcionamiento del juego
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.database_manager import DatabaseManager
from src.utils.schema_manager import SchemaManager
from src.utils.config_manager import ConfigManager


def main():
	"""Inicializa la base de datos SQLite del juego."""
	print("=== INICIALIZANDO BASE DE DATOS SQLITE ===")
	
	try:
		# Inicializar configuración
		config = ConfigManager()
		print("✅ Configuración cargada")
		
		# Obtener ruta de la base de datos
		db_path = config.get("save_system", "database_path", "data/game.db")
		print(f"📁 Ruta de BD: {db_path}")
		
		# Crear directorio si no existe
		os.makedirs(os.path.dirname(db_path), exist_ok=True)
		
		# Inicializar gestor de base de datos
		db_manager = DatabaseManager(db_path)
		print("✅ DatabaseManager inicializado")
		
		# Inicializar gestor de esquemas
		schema_manager = SchemaManager(db_manager)
		print("✅ SchemaManager inicializado")
		
		# Verificar si ya está inicializada
		if schema_manager.is_schema_initialized():
			print("⚠️  La base de datos ya está inicializada")
			
			# Mostrar estado actual
			validation = schema_manager.validate_schema()
			if validation["valid"]:
				print("✅ Validación exitosa - BD operativa")
				print(f"🗃️  Tablas encontradas: {validation['tables_found']}")
			else:
				print("❌ Validación falló - recreando tablas...")
				schema_manager.create_all_tables()
		else:
			print("🔨 Creando todas las tablas...")
			if schema_manager.create_all_tables():
				print("✅ Todas las tablas creadas exitosamente")
			else:
				print("❌ Error creando tablas")
				return False
		
		# Validación final
		validation = schema_manager.validate_schema()
		if validation["valid"]:
			print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
			print(f"🗃️  Tablas disponibles: {', '.join(validation['tables_found'])}")
			return True
		else:
			print("❌ ERROR EN VALIDACIÓN FINAL")
			print(f"Errores: {validation['errors']}")
			return False
			
	except Exception as e:
		print(f"❌ ERROR CRÍTICO: {e}")
		import traceback
		traceback.print_exc()
		return False
	finally:
		# Cerrar conexiones
		if 'db_manager' in locals():
			db_manager.close_all_connections()
			print("🔒 Conexiones cerradas")


if __name__ == "__main__":
	success = main()
	sys.exit(0 if success else 1)
