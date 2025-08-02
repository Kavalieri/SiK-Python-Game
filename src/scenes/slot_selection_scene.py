"""
Slot Selection Scene - Escena de Selección de Slots de Guardado
=============================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Escena para seleccionar slots de guardado con gestión de slots activos.
"""

import pygame

from core.scene_manager import Scene
from ui.menu_manager import MenuManager
from utils.config_manager import ConfigManager
from utils.logger import get_logger


class SlotSelectionScene(Scene):
    """
    Escena de selección de slots de guardado.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")
        # Inicializar menú
        self.menu_manager = MenuManager(screen, config, game_state, save_manager)
        self.logger.info(
            "[SlotSelectionScene] Escena de selección de slots inicializada"
        )

    def enter(self):
        super().enter()
        # Actualizar título según el modo
        mode = getattr(self.game_state, "slot_selection_mode", "load_game")
        if mode == "new_game":
            self.logger.info(
                "[SlotSelectionScene] Modo: Nuevo Juego - Seleccionar slot"
            )
        else:
            self.logger.info(
                "[SlotSelectionScene] Modo: Cargar Juego - Seleccionar slot"
            )

        self.menu_manager.show_menu("save")
        self.logger.info(
            "[SlotSelectionScene] Entrando en escena de selección de slots"
        )

    def handle_event(self, event: pygame.event.Event):
        """
        Maneja eventos de la escena de selección de slots.

        Args:
            event: Evento de Pygame a procesar.
        """
        self.logger.debug(
            "[SlotSelectionScene] Evento recibido: %s - %s", event.type, event
        )
        if event.type == 768:  # pygame.KEYDOWN
            self.logger.info("[SlotSelectionScene] Tecla pulsada: %s", event.key)
            if event.key == 27:  # pygame.K_ESCAPE
                self.logger.info(
                    "[SlotSelectionScene] ESC presionado - volviendo al menú principal"
                )
                self.game_state.scene_manager.change_scene("main_menu")
        elif event.type == 1025:  # pygame.MOUSEBUTTONDOWN
            self.logger.info(
                "[SlotSelectionScene] Click ratón: %s en %s", event.button, event.pos
            )
        self.menu_manager.update([event])

    def update(self):
        """
        Actualiza la lógica de la escena de selección de slots.
        """
        # Método vacío, pero necesario para la estructura.
        return

    def render(self):
        self.screen.fill((20, 20, 60))
        self.menu_manager.render()
        self._render_additional_info()

    def _render_additional_info(self):
        """
        Renderiza información adicional en la escena.
        """
        font = pygame.font.Font(None, 24)
        instructions = [
            "Selecciona un slot para continuar",
            "ESC - Volver al menú principal",
            "Los slots activos se muestran en amarillo",
        ]
        y_offset = 50
        for instruction in instructions:
            text_surface = font.render(instruction, True, (200, 200, 200))
            text_rect = text_surface.get_rect(
                center=(self.screen.get_width() // 2, y_offset)
            )
            self.screen.blit(text_surface, text_rect)
            y_offset += 30
