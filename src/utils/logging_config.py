"""
Configuración centralizada de logging para SiK Python Game.
Gestiona niveles de log apropiados para desarrollo vs producción.
"""

import logging
import os


class LoggingConfig:
    """Configurador centralizado de logging para el juego."""

    # Niveles de logging predeterminados por módulo
    DEFAULT_LEVELS: dict[str, int] = {
        # Eventos críticos del juego
        "game_core": logging.WARNING,
        "player": logging.WARNING,
        "enemy": logging.WARNING,
        "collision": logging.WARNING,
        # Sistemas de estado
        "scene_manager": logging.WARNING,
        "save_system": logging.INFO,
        "config": logging.INFO,
        # Eventos innecesarios en runtime
        "mouse_events": logging.CRITICAL,
        "render_loops": logging.CRITICAL,
        "camera_movement": logging.CRITICAL,
        "background_updates": logging.CRITICAL,
        "ui_updates": logging.CRITICAL,
        # Desarrollo (solo para debug específico)
        "world_generation": logging.WARNING,
        "asset_loading": logging.INFO,
    }

    @classmethod
    def configure_logger(cls, name: str, level: int | None = None) -> logging.Logger:
        """
        Configura un logger con nivel apropiado.

        Args:
                name: Nombre del módulo/logger
                level: Nivel específico (opcional)

        Returns:
                Logger configurado
        """
        logger = logging.getLogger(name)

        # Determinar nivel apropiado
        if level is not None:
            log_level = level
        elif name in cls.DEFAULT_LEVELS:
            log_level = cls.DEFAULT_LEVELS[name]
        else:
            # Por defecto: solo warnings y errores
            log_level = logging.WARNING

        logger.setLevel(log_level)

        # Evitar handlers duplicados
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @classmethod
    def set_development_mode(cls, enabled: bool = True) -> None:
        """
        Activa/desactiva modo desarrollo con más logging.

        Args:
                enabled: True para modo desarrollo
        """
        if enabled:
            # Modo desarrollo: más verbose
            cls.DEFAULT_LEVELS.update(
                {
                    "game_core": logging.INFO,
                    "world_generation": logging.INFO,
                    "asset_loading": logging.DEBUG,
                }
            )
        else:
            # Modo producción: minimal logging
            cls.DEFAULT_LEVELS.update(
                {
                    "game_core": logging.WARNING,
                    "world_generation": logging.WARNING,
                    "asset_loading": logging.WARNING,
                }
            )

    @classmethod
    def silence_frequent_events(cls) -> None:
        """Silencia eventos que se ejecutan cada frame."""
        silent_modules = [
            "mouse_events",
            "render_loops",
            "camera_movement",
            "background_updates",
            "ui_updates",
        ]

        for module in silent_modules:
            cls.DEFAULT_LEVELS[module] = logging.CRITICAL


# Auto-configuración al importar
LoggingConfig.silence_frequent_events()

# Modo desarrollo basado en variable de entorno
if os.getenv("SIK_DEBUG_MODE", "false").lower() == "true":
    LoggingConfig.set_development_mode(True)
