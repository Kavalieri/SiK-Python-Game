"""
Game Engine Events - Manejo de Eventos y Callbacks
=================================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de eventos y callbacks del motor del juego.
"""

import pygame

from utils.logger import get_logger


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
            # Solo registrar eventos importantes como INFO, el resto como DEBUG
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.logger.info("Evento QUIT detectado - Cerrando juego")
                self.core.running = False
            elif event.type != pygame.MOUSEMOTION:  # pylint: disable=no-member
                self.logger.debug("Evento global: %s - %s", event.type, event)
            # Logging detallado de eventos
            self._log_event(event)

            if event.type != pygame.QUIT:  # pylint: disable=no-member
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
        try:
            # Buscar el save más reciente de los 3 slots
            saves_info = self.core.save_manager.get_save_files_info()
            last_save_slot = None
            last_timestamp = None

            for save_info in saves_info:
                if save_info.get("exists", False):
                    timestamp = save_info.get("timestamp")
                    if timestamp and (
                        last_timestamp is None or timestamp > last_timestamp
                    ):
                        last_timestamp = timestamp
                        last_save_slot = save_info.get(
                            "file_number", save_info.get("slot")
                        )

            if last_save_slot:
                self.logger.info("Continuando juego desde slot: %d", last_save_slot)
                save_data = self.core.save_manager.load_save(last_save_slot)
                if save_data:
                    # Cargar datos al game_state aquí si es necesario
                    self.core.scene_manager.change_scene("game")
                else:
                    self.logger.error(
                        "Error cargando datos del slot %d", last_save_slot
                    )
            else:
                self.logger.warning("No hay partidas guardadas para continuar")
        except (AttributeError, KeyError, ValueError) as e:
            self.logger.error("Error en continue_game: %s", e)

    def handle_slot_selection(self, slot: int):
        """Maneja la selección de un slot de guardado."""
        self.logger.info("Slot seleccionado: %s", slot)

        # Verificar el modo de selección
        mode = getattr(self.core.game_state, "slot_selection_mode", "load_game")

        if mode == "new_game":
            # Nuevo juego: establecer slot activo y ir a selección de personaje
            self.logger.info("Modo nuevo juego - navegando a selección de personaje")
            # Establecer slot activo temporalmente en game_state
            self.core.game_state.active_slot = slot
            self.core.scene_manager.change_scene("character_select")
        else:
            # Cargar juego: cargar la partida del slot directamente
            self.logger.info("Modo cargar juego - cargando partida del slot %s", slot)
            try:
                game_data = self.core.save_manager.load_save(slot)
                if game_data:
                    self.core.game_state.load_state(game_data)
                    self.core.scene_manager.change_scene("game")
                else:
                    self.logger.error("No se pudo cargar la partida del slot %s", slot)
                    self.core.scene_manager.change_scene("slot_selection")
            except (OSError, ValueError, KeyError) as e:
                self.logger.error("Error cargando partida: %s", e)
                self.core.scene_manager.change_scene("slot_selection")

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
