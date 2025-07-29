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
from pathlib import Path

# Añadir el directorio raíz al path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.game_engine import GameEngine
from src.utils.config_manager import ConfigManager
from src.utils.logger import setup_logger


def main():
    """
    Función principal que inicializa y ejecuta el juego.
    """
    try:
        # Configurar logging
        logger = setup_logger()
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
