#!/usr/bin/env python3
"""
SiK Python Game - Punto de entrada principal
===========================================

Autor: SiK Team
Fecha: 2024
Descripción: Punto de entrada principal del videojuego 2D desarrollado con Python y Pygame-ce.
             Inicializa el motor del juego, carga la configuración y ejecuta el bucle principal.
"""

import sys
import os
import logging
from pathlib import Path

# Añadir el directorio raíz al path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar logger ANTES de cualquier import de módulos del juego
from src.utils.logger import setup_logger
logger = setup_logger()
logger.info('Logger centralizado inicializado antes de imports de juego')

print('PYTHONPATH:', sys.path)

import importlib
for mod in ['src.ui.menu_manager', 'src.ui.menu_factory', 'src.ui.menu_callbacks']:
    try:
        m = importlib.import_module(mod)
        print(f"{mod} loaded from: {m.__file__}")
    except Exception as e:
        print(f"Error loading {mod}: {e}")

from src.core.game_engine import GameEngine
from src.utils.config_manager import ConfigManager


def main():
	"""
	Función principal que inicializa y ejecuta el juego.
	"""
	try:
		# Configurar logging
		logger.info("Iniciando SiK Python Game...")
		
		# Cargar configuración
		config = ConfigManager()
		logger.info("Configuración cargada correctamente")
		
		# Inicializar motor del juego
		game_engine = GameEngine(config)
		logger.info("Motor del juego inicializado")
		
		# Ejecutar bucle principal del juego
		game_engine.run()
		
	except KeyboardInterrupt:
		logger.info("Juego interrumpido por el usuario")
	except Exception as e:
		logger.error(f"Error crítico en el juego: {e}")
		raise
	finally:
		logger.info("Cerrando SiK Python Game...")


if __name__ == "__main__":
	main() 