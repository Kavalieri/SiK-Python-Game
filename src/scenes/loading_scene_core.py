"""
Loading Scene Core - Núcleo de la escena de carga
==================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Configuración y estado central de la escena de carga.
"""

import json
import random
from collections.abc import Callable
from typing import Any

import pygame

from core.scene_manager import Scene
from utils.config_manager import ConfigManager
from utils.logger import get_logger


class LoadingSceneCore(Scene):
    """
    Núcleo de la escena de carga - configuración y estado.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        config: ConfigManager,
        game_state,
        save_manager,
        on_loading_complete: Callable | None = None,
    ):
        """
        Inicializa el núcleo de la escena de carga.

        Args:
            screen: Superficie de pantalla
            config: Configuración del juego
            game_state: Estado del juego
            save_manager: Gestor de guardado
            on_loading_complete: Callback cuando termine la carga
        """
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")
        self.logger.info("[LoadingScene] Escena de carga inicializada")

        # Estado de carga
        self.loading_progress = 0.0
        self.loading_complete = False

        # Cargar configuración de pantalla de carga
        self.loading_screen_config = self._load_loading_screen_config()

        # Mensajes de carga desde configuración
        self.loading_messages = self.loading_screen_config.get(
            "messages",
            [
                "Inicializando motor del juego...",
                "Cargando configuración...",
                "Preparando recursos gráficos...",
                "Generando mundo...",
                "Cargando personajes...",
                "Preparando enemigos...",
                "Configurando controles...",
                "¡Listo para jugar!",
            ],
        )
        self.current_message_index = 0
        self.message_timer = 0
        self.message_duration = 1.0

        # Callback de finalización
        self.on_loading_complete = on_loading_complete

        # Control de avance
        self._has_advanced = False

        self.tips = self.loading_screen_config.get(
            "tips",
            [
                "Rompe las cajas para encontrar valiosas recompensas.",
                "Prioriza la supervivencia: cuanto más avances, más puntos obtienes.",
                "Los cactus dañan al contacto, ¡evítalos!",
            ],
        )
        self.title = self.loading_screen_config.get("title", "SiK Python Game")
        self.subtitle = self.loading_screen_config.get("subtitle", "Cargando...")
        self.version = self.loading_screen_config.get("version", "v1.0.0")
        self.current_tip = random.choice(self.tips)

        self.logger.info("Escena de carga inicializada")

    def _load_loading_screen_config(self) -> dict[str, Any]:
        """
        Carga la configuración de la pantalla de carga desde un archivo JSON.

        Returns:
            Configuración de la pantalla de carga
        """
        try:
            with open("config/loading_screen.json", encoding="utf-8") as f:
                config = json.load(f)
                self.logger.info(
                    "Configuración de pantalla de carga cargada correctamente."
                )
                return config
        except FileNotFoundError:
            self.logger.warning(
                "Archivo de configuración de carga no encontrado. Usando valores por defecto."
            )
        except json.JSONDecodeError as e:
            self.logger.error("Error al decodificar JSON: %s", e)
        except OSError as e:
            self.logger.error("Error inesperado al cargar configuración: %s", e)
        return {}

    def get_loading_state(self) -> dict[str, Any]:
        """
        Obtiene el estado actual de carga.

        Returns:
            Estado actual de carga
        """
        return {
            "progress": self.loading_progress,
            "complete": self.loading_complete,
            "current_message": (
                self.loading_messages[self.current_message_index]
                if self.current_message_index < len(self.loading_messages)
                else ""
            ),
            "message_index": self.current_message_index,
            "has_advanced": self._has_advanced,
        }

    def update_loading_progress(self, progress: float, message_index: int):
        """
        Actualiza el progreso de carga.

        Args:
            progress: Progreso de 0.0 a 1.0
            message_index: Índice del mensaje actual
        """
        self.loading_progress = min(1.0, max(0.0, progress))
        self.current_message_index = message_index

        if self.loading_progress >= 1.0:
            self.loading_complete = True
            self.current_message_index = len(self.loading_messages) - 1

    def mark_as_advanced(self):
        """Marca que el usuario ha avanzado desde la pantalla de carga."""
        self._has_advanced = True

    def can_advance(self) -> bool:
        """
        Verifica si se puede avanzar desde la pantalla de carga.

        Returns:
            True si se puede avanzar
        """
        return self.loading_complete and not self._has_advanced

    def has_advanced(self) -> bool:
        """
        Verifica si ya se ha avanzado desde la pantalla de carga.

        Returns:
            True si ya se ha avanzado
        """
        return self._has_advanced

    def update(self):
        """Actualiza la lógica del núcleo."""
        # Actualizar timer de mensajes
        self.message_timer += 1.0 / 60.0  # Asumiendo 60 FPS

    def handle_event(self, event: pygame.event.Event):
        """Maneja eventos básicos."""
        self.logger.debug("Evento recibido: %s", event.type)

    def render(self):
        """Renderizado básico - debe ser implementado por las clases especializadas."""
        self.logger.debug("Renderizado básico llamado")
