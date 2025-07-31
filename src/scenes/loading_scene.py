"""
Loading Scene - Escena de Carga Principal
==========================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada principal para la escena de carga con todos los componentes integrados.
"""

from typing import Callable

import pygame

from ..utils.config_manager import ConfigManager
from .loading_scene_core import LoadingSceneCore
from .loading_scene_events import LoadingSceneEvents
from .loading_scene_logic import LoadingSceneLogic
from .loading_scene_renderer import LoadingSceneRenderer


class LoadingScene:
    """
    Escena de carga principal que integra todos los componentes.
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
        Inicializa la escena de carga.

        Args:
            screen: Superficie de pantalla
            config: Configuración del juego
            game_state: Estado del juego
            save_manager: Gestor de guardado
            on_loading_complete: Callback cuando termine la carga
        """
        # Inicializar componentes especializados
        self.core = LoadingSceneCore(
            screen, config, game_state, save_manager, on_loading_complete
        )
        self.logic = LoadingSceneLogic(self.core)
        self.renderer = LoadingSceneRenderer(self.core)
        self.events = LoadingSceneEvents(self.core)

        # Iniciar carga automáticamente
        self.start_background_loading()

    def enter(self):
        """
        Se ejecuta cuando se entra en la escena de carga.
        """
        self.start_background_loading()

    def start_background_loading(self):
        """Inicia la carga en segundo plano."""
        self.logic.start_background_loading()

    def handle_event(self, event: pygame.event.Event):
        """
        Maneja eventos de la escena de carga.

        Args:
            event: Evento de pygame
        """
        self.events.handle_event(event)

    def update(self):
        """Actualiza la lógica de la escena de carga."""
        self.core.update()

    def render(self):
        """Renderiza la escena de carga."""
        self.renderer.render_all()

    # Métodos de acceso para compatibilidad con API existente
    @property
    def loading_progress(self) -> float:
        """Progreso de carga actual."""
        return self.core.loading_progress

    @property
    def loading_complete(self) -> bool:
        """Estado de carga completada."""
        return self.core.loading_complete

    @property
    def loading_messages(self) -> list:
        """Mensajes de carga."""
        return self.core.loading_messages

    @property
    def current_message_index(self) -> int:
        """Índice del mensaje actual."""
        return self.core.current_message_index

    def get_system_info(self) -> dict:
        """
        Obtiene información completa del sistema de carga.

        Returns:
            Información del sistema
        """
        return {
            "core_state": self.core.get_loading_state(),
            "logic_info": self.logic.get_loading_info(),
            "event_stats": self.events.get_event_statistics(),
            "modules_loaded": {
                "core": True,
                "logic": True,
                "renderer": True,
                "events": True,
            },
        }

    def force_complete(self):
        """Fuerza la completación de la carga."""
        self.logic.stop_loading()

    def can_advance(self) -> bool:
        """Verifica si se puede avanzar."""
        return self.core.can_advance()

    def is_loading_active(self) -> bool:
        """Verifica si la carga está activa."""
        return self.logic.is_loading_active()

    def exit(self):
        """
        Se llama cuando se sale de la escena.
        Limpia recursos y detiene procesos de carga si están activos.
        """
        if self.logic.is_loading_active():
            self.logic.stop_loading()
        # Limpieza adicional si es necesaria
