"""
Loading Scene Events - Manejo de eventos
=========================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Manejo de eventos y transiciones de la escena de carga.
"""

from typing import TYPE_CHECKING

import pygame

from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .loading_scene_core import LoadingSceneCore


class LoadingSceneEvents:
    """
    Manejo de eventos para la escena de carga.
    """

    def __init__(self, core: "LoadingSceneCore"):
        """
        Inicializa el manejador de eventos.

        Args:
            core: Núcleo de la escena de carga
        """
        self.core = core
        self.logger = get_logger("SiK_Game")

    def handle_event(self, event: pygame.event.Event):
        """
        Maneja eventos de la escena de carga.

        Args:
            event: Evento de pygame
        """
        self.logger.info("[LoadingScene] Evento recibido: %s - %s", event.type, event)

        # Manejo de eventos de sistema
        if self._handle_system_events(event):
            return

        # Manejo de eventos de interacción
        self._handle_interaction_events(event)

    def _handle_system_events(self, event: pygame.event.Event) -> bool:
        """
        Maneja eventos del sistema.

        Args:
            event: Evento de pygame

        Returns:
            True si el evento fue manejado
        """
        if event.type == pygame.QUIT:
            self.logger.info("Evento QUIT recibido - cerrando aplicación")
            pygame.quit()
            exit()
            return True

        return False

    def _handle_interaction_events(self, event: pygame.event.Event):
        """
        Maneja eventos de interacción del usuario.

        Args:
            event: Evento de pygame
        """
        # Solo permitir avanzar si la carga está completa
        if not self.core.can_advance():
            return

        # Detectar input del usuario para continuar
        if self._is_continue_input(event):
            self.logger.info("Input de continuación detectado")
            self.core.mark_as_advanced()

            # Ejecutar callback si está definido
            if self.core.on_loading_complete:
                self.logger.info("Ejecutando callback de carga completada")
                self.core.on_loading_complete()
            else:
                self.logger.warning("No hay callback definido para carga completada")

    def _is_continue_input(self, event: pygame.event.Event) -> bool:
        """
        Verifica si el evento es un input de continuación.

        Args:
            event: Evento de pygame

        Returns:
            True si es un input de continuación
        """
        # Teclas
        if event.type == pygame.KEYDOWN:
            # Cualquier tecla excepto modificadores
            excluded_keys = {
                pygame.K_LSHIFT,
                pygame.K_RSHIFT,
                pygame.K_LCTRL,
                pygame.K_RCTRL,
                pygame.K_LALT,
                pygame.K_RALT,
                pygame.K_LGUI,
                pygame.K_RGUI,
                pygame.K_CAPSLOCK,
                pygame.K_NUMLOCK,
                pygame.K_SCROLLLOCK,
            }
            return event.key not in excluded_keys

        # Clicks del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True

        # Joystick/gamepad
        if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION):
            return True

        return False

    def get_event_statistics(self) -> dict:
        """
        Obtiene estadísticas de eventos manejados.

        Returns:
            Estadísticas de eventos
        """
        return {
            "can_advance": self.core.can_advance(),
            "loading_complete": self.core.loading_complete,
            "has_advanced": self.core._has_advanced,
            "callback_available": self.core.on_loading_complete is not None,
        }

    def simulate_continue_event(self):
        """Simula un evento de continuación para testing."""
        fake_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        self.handle_event(fake_event)
        self.logger.debug("Evento de continuación simulado")
