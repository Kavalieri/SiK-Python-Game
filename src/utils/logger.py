"""
Logger - Sistema de logging
==========================

Autor: SiK Team
Fecha: 2024
Descripción: Configuración del sistema de logging para el juego.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "SiK_Game",
    log_file: str = "logs/game.log",
    level: int = logging.INFO,
    max_bytes: int = 1024 * 1024,  # 1MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configura el sistema de logging del juego.

    Args:
            name: Nombre del logger
            log_file: Ruta al archivo de log
            level: Nivel de logging
            max_bytes: Tamaño máximo del archivo de log
            backup_count: Número de archivos de backup

    Returns:
            Logger configurado
    """
    # Crear directorio de logs si no existe
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers
    if logger.handlers:
        return logger

    # Formato para los logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para archivo con rotación
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Añadir handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Sistema de logging inicializado")
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Obtiene un logger específico.

    Args:
            name: Nombre del logger (opcional)

    Returns:
            Logger configurado
    """
    if name:
        return logging.getLogger(name)
    else:
        return logging.getLogger("SiK_Game")
