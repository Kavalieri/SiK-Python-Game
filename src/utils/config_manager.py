"""
Config Manager - Gestor de configuración
=======================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona la configuración del juego desde archivos y valores por defecto.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
	"""
	Gestiona la configuración del juego.
	"""
	
	def __init__(self, config_file: str = "config.json"):
		"""
		Inicializa el gestor de configuración.
		
		Args:
			config_file: Ruta al archivo de configuración
		"""
		self.logger = logging.getLogger(__name__)
		self.config_file = Path(config_file)
		self.config = self._load_default_config()
		
		self.logger.info("Cargando configuración...")
		self._load_config()
		self.logger.info("Configuración cargada correctamente")
	
	def _load_default_config(self) -> Dict[str, Any]:
		"""
		Carga la configuración por defecto.
		
		Returns:
			Configuración por defecto
		"""
		return {
			"game": {
				"title": "SiK Python Game",
				"version": "0.1.0",
				"debug": False
			},
			"display": {
				"width": 1280,
				"height": 720,
				"fps": 60,
				"fullscreen": False,
				"vsync": True
			},
			"audio": {
				"master_volume": 1.0,
				"music_volume": 0.7,
				"sfx_volume": 0.8,
				"enabled": True
			},
			"input": {
				"keyboard_enabled": True,
				"gamepad_enabled": True,
				"mouse_enabled": True
			},
			"paths": {
				"assets": "assets",
				"saves": "saves",
				"logs": "logs"
			}
		}
	
	def _load_config(self):
		"""Carga la configuración desde archivo."""
		try:
			if self.config_file.exists():
				with open(self.config_file, 'r', encoding='utf-8') as f:
					file_config = json.load(f)
					self._merge_config(file_config)
					self.logger.info(f"Configuración cargada desde: {self.config_file}")
			else:
				self.logger.warning(f"Archivo de configuración no encontrado: {self.config_file}")
				self.save_config()
				
		except Exception as e:
			self.logger.error(f"Error al cargar configuración: {e}")
	
	def _merge_config(self, file_config: Dict[str, Any]):
		"""
		Combina la configuración del archivo con la por defecto.
		
		Args:
			file_config: Configuración del archivo
		"""
		for section, values in file_config.items():
			if section in self.config:
				if isinstance(values, dict):
					self.config[section].update(values)
				else:
					self.config[section] = values
			else:
				self.config[section] = values
	
	def save_config(self):
		"""Guarda la configuración actual en archivo."""
		try:
			self.config_file.parent.mkdir(parents=True, exist_ok=True)
			with open(self.config_file, 'w', encoding='utf-8') as f:
				json.dump(self.config, f, indent=4, ensure_ascii=False)
			self.logger.info(f"Configuración guardada en: {self.config_file}")
			
		except Exception as e:
			self.logger.error(f"Error al guardar configuración: {e}")
	
	def get(self, section: str, key: str, default: Any = None) -> Any:
		"""
		Obtiene un valor de configuración.
		
		Args:
			section: Sección de configuración
			key: Clave del valor
			default: Valor por defecto si no existe
			
		Returns:
			Valor de configuración
		"""
		try:
			return self.config[section][key]
		except KeyError:
			self.logger.warning(f"Configuración no encontrada: {section}.{key}")
			return default
	
	def set(self, section: str, key: str, value: Any):
		"""
		Establece un valor de configuración.
		
		Args:
			section: Sección de configuración
			key: Clave del valor
			value: Valor a establecer
		"""
		if section not in self.config:
			self.config[section] = {}
		
		self.config[section][key] = value
		self.logger.debug(f"Configuración actualizada: {section}.{key} = {value}")
	
	def get_section(self, section: str) -> Dict[str, Any]:
		"""
		Obtiene una sección completa de configuración.
		
		Args:
			section: Nombre de la sección
			
		Returns:
			Sección de configuración
		"""
		return self.config.get(section, {})
	
	def reload(self):
		"""Recarga la configuración desde archivo."""
		self.logger.info("Recargando configuración...")
		self._load_config() 