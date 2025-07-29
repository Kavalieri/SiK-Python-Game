"""
Test Config Manager - Pruebas del gestor de configuración
=======================================================

Autor: SiK Team
Fecha: 2024
Descripción: Pruebas unitarias para el ConfigManager.
"""

import pytest
import tempfile
import json
from pathlib import Path
from src.utils.config_manager import ConfigManager


class TestConfigManager:
	"""Pruebas para el ConfigManager."""
	
	def test_default_config(self):
		"""Prueba que la configuración por defecto se carga correctamente."""
		config = ConfigManager()
		
		# Verificar secciones principales
		assert "game" in config.config
		assert "display" in config.config
		assert "audio" in config.config
		assert "input" in config.config
		assert "paths" in config.config
		
		# Verificar valores por defecto
		assert config.get("game", "title") == "SiK Python Game"
		assert config.get("display", "width") == 1280
		assert config.get("display", "height") == 720
		assert config.get("display", "fps") == 60
	
	def test_get_with_default(self):
		"""Prueba el método get con valor por defecto."""
		config = ConfigManager()
		
		# Valor que no existe
		result = config.get("nonexistent", "key", "default_value")
		assert result == "default_value"
		
		# Valor que existe
		result = config.get("game", "title", "default_value")
		assert result == "SiK Python Game"
	
	def test_set_value(self):
		"""Prueba establecer un valor de configuración."""
		config = ConfigManager()
		
		# Establecer valor en sección existente
		config.set("game", "debug", True)
		assert config.get("game", "debug") == True
		
		# Establecer valor en nueva sección
		config.set("new_section", "new_key", "new_value")
		assert config.get("new_section", "new_key") == "new_value"
	
	def test_get_section(self):
		"""Prueba obtener una sección completa."""
		config = ConfigManager()
		
		game_section = config.get_section("game")
		assert isinstance(game_section, dict)
		assert "title" in game_section
		assert "version" in game_section
	
	def test_load_from_file(self):
		"""Prueba cargar configuración desde archivo."""
		with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
			test_config = {
				"game": {
					"title": "Test Game",
					"debug": True
				},
				"display": {
					"width": 1920,
					"height": 1080
				}
			}
			json.dump(test_config, f)
			temp_file = f.name
		
		try:
			config = ConfigManager(temp_file)
			
			# Verificar que se cargaron los valores del archivo
			assert config.get("game", "title") == "Test Game"
			assert config.get("game", "debug") == True
			assert config.get("display", "width") == 1920
			assert config.get("display", "height") == 1080
			
			# Verificar que se mantienen valores por defecto no especificados
			assert config.get("display", "fps") == 60
			
		finally:
			Path(temp_file).unlink()
	
	def test_save_config(self):
		"""Prueba guardar configuración en archivo."""
		with tempfile.TemporaryDirectory() as temp_dir:
			config_file = Path(temp_dir) / "test_config.json"
			config = ConfigManager(str(config_file))
			
			# Modificar configuración
			config.set("game", "title", "Saved Game")
			config.set("display", "width", 1600)
			
			# Guardar configuración
			config.save_config()
			
			# Verificar que el archivo se creó
			assert config_file.exists()
			
			# Cargar configuración desde el archivo guardado
			new_config = ConfigManager(str(config_file))
			assert new_config.get("game", "title") == "Saved Game"
			assert new_config.get("display", "width") == 1600 