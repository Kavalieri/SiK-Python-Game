"""
Game Engine Events - Manejo de Eventos y Callbacks
=================================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de eventos y callbacks del motor del juego.
"""

import pygame

from ..utils.logger import get_logger


class GameEngineEvents:
    """Sistema de manejo de eventos y callbacks del motor."""

    def __init__(self, core):
        """
        Inicializa el sistema de eventos.

        Args:
            core: Instancia de GameEngineCore
        """
        self.core = core
        self.logger = get_logger("SiK_Game")
        self._mouse_log_counter = 0

    def handle_events(self):
        """Procesa todos los eventos de Pygame."""
        for event in pygame.event.get():
            self.logger.info("Evento global: %s - %s", event.type, event)
            # Logging detallado de eventos
            self._log_event(event)

            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.logger.info("Evento QUIT detectado - Cerrando juego")
                self.core.running = False
            else:
                self.core.scene_manager.handle_event(event)

    def _log_event(self, event: pygame.event.Event):
        """Registra eventos de Pygame para debug."""
        if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
            self.logger.debug(
                "MOUSE CLICK: %s en (%s, %s)", event.button, event.pos[0], event.pos[1]
            )
        elif event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
            self.logger.debug(
                "MOUSE RELEASE: %s en (%s, %s)",
                event.button,
                event.pos[0],
                event.pos[1],
            )
        elif event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
            # Solo loggear movimiento cada 10 frames para no saturar
            self._mouse_log_counter += 1
            if self._mouse_log_counter % 10 == 0:
                self.logger.debug("MOUSE MOTION: (%s, %s)", event.pos[0], event.pos[1])
        elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            self.logger.debug(
                "KEY DOWN: %s (scancode: %s)",
                pygame.key.name(event.key),
                event.scancode,
            )
        elif event.type == pygame.KEYUP:  # pylint: disable=no-member
            self.logger.debug(
                "KEY UP: %s (scancode: %s)", pygame.key.name(event.key), event.scancode
            )
        elif event.type == pygame.MOUSEWHEEL:  # pylint: disable=no-member
            self.logger.debug("MOUSE WHEEL: %s en (%s, %s)", event.y, event.x, event.y)

    def handle_continue_game(self):
        """Maneja la acción de continuar juego desde el último slot activo."""
        last_save = self.core.save_manager.get_last_save_file()
        if last_save:
            self.logger.info("Continuando juego desde: %s", last_save)
            self.core.save_manager.load_save(last_save, self.core.game_state)
            self.core.scene_manager.change_scene("game")
        else:
            self.logger.warning("No hay partida guardada para continuar")

    def handle_slot_selection(self, slot: int):
        """Maneja la selección de un slot de guardado."""
        self.logger.info("Slot seleccionado: %s", slot)
        # Lógica para activar el slot y navegar a selección de personaje
        self.core.save_manager.set_active_slot(slot)
        self.core.scene_manager.change_scene("character_select")

    def handle_clear_slot(self, slot: int):
        """Maneja el vaciado de un slot de guardado."""
        self.logger.info("Vaciar slot: %s", slot)
        self.core.save_manager.clear_slot(slot)
        self.core.scene_manager.change_scene("slot_selection")

    def handle_character_selection(self, character: str):
        """Maneja la selección de personaje tras elegir slot."""
        self.logger.info("Personaje seleccionado: %s", character)
        self.core.game_state.selected_character = character
        self.core.scene_manager.change_scene("game")

    def handle_save_game(self):
        """Maneja el guardado manual desde el menú de pausa."""
        self.logger.info("Guardando partida manualmente en slot activo")
        self.core.save_manager.save_game()

    def log_and_quit_menu(self):
        """Diferencia el cierre por botón Salir del menú y el cierre de ventana."""
        self.logger.info(
            "Botón Salir pulsado - Cierre solicitado por el usuario desde el menú"
        )
        self.core.running = False
