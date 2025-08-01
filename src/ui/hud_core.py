"""
HUD Core - Núcleo del Sistema HUD
================================

Autor: SiK Team
Fecha: 2024
Descripción: Clase principal del HUD que coordina elementos, configuración y renderizado.
"""

import logging

import pygame

from ..core.game_state import GameState
from ..utils.config_manager import ConfigManager
from .hud_elements import HUDConfiguration, HUDElement
from .hud_rendering import HUDRenderer


class HUDCore:
    """
    Núcleo del sistema HUD que coordina todos los componentes.

    Gestiona la configuración, elementos y renderizado del HUD durante el juego.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state: GameState
    ):
        """
        Inicializa el sistema HUD.

        Args:
            screen: Superficie de Pygame donde renderizar
            config: Configuración del juego
            game_state: Estado actual del juego
        """
        self.screen = screen
        self.config = config
        self.game_state = game_state
        self.logger = logging.getLogger(__name__)

        # Dimensiones de pantalla
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Configuración del HUD
        self.hud_config = HUDConfiguration(self.screen_width, self.screen_height)

        # Elementos del HUD
        self.hud_elements: dict[str, HUDElement] = self.hud_config.get_hud_elements()

        # Sistema de fuentes
        self.fonts: dict[str, pygame.font.Font] = {}
        self._initialize_fonts()

        # Renderizador especializado
        self.renderer = HUDRenderer(self.screen, self.hud_config, self.fonts)
        self.renderer.set_hud_elements(self.hud_elements)

        # Estado del HUD
        self.visible = True
        self.debug_mode = False

        self.logger.info("Sistema HUD Core inicializado")

    def _initialize_fonts(self):
        """Inicializa las fuentes del HUD."""
        try:
            for size_name, size in self.hud_config.font_sizes.items():
                self.fonts[size_name] = pygame.font.Font(None, size)

            # Fuente específica para efectos
            self.fonts["effects"] = pygame.font.Font(None, 16)

            self.logger.debug("Fuentes del HUD inicializadas")

        except (pygame.error, FileNotFoundError) as e:  # pylint: disable=no-member
            self.logger.error("Error inicializando fuentes: %s", e)
            # Fallback a fuente por defecto
            default_font = pygame.font.Font(None, 24)
            for size_name in self.hud_config.font_sizes:
                self.fonts[size_name] = default_font

    def update(self, delta_time: float):
        """
        Actualiza el estado del HUD.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        if not self.visible:
            return

        # Actualizar visibilidad de elementos según estado del juego
        self._update_element_visibility()

        # Aquí se pueden añadir animaciones, efectos, etc.
        # El delta_time se usará para futuras animaciones
        _ = delta_time  # Silenciar warning temporalmente

    def _update_element_visibility(self):
        """Actualiza la visibilidad de elementos según el estado del juego."""
        # Ejemplo: Ocultar ciertos elementos en pantalla de pausa
        if hasattr(self.game_state, "status"):
            is_paused = str(self.game_state.status).lower() == "paused"

            # En pausa, ocultar algunos elementos dinámicos
            if "minimap" in self.hud_elements:
                self.hud_elements["minimap"].visible = not is_paused

    def render(self, player=None):
        """
        Renderiza todos los elementos del HUD.

        Args:
            player: Referencia al jugador para información específica
        """
        if not self.visible:
            return

        try:
            # Renderizar paneles de fondo
            self.renderer.render_background_panels()

            # Renderizar información del jugador
            self.renderer.render_player_info(self.game_state)

            # Renderizar información del juego
            self.renderer.render_game_info(self.game_state)

            # Renderizar información de puntuación
            self.renderer.render_score_info(self.game_state)

            # Renderizar mini-mapa
            player_pos = None
            if player and hasattr(player, "position"):
                player_pos = (player.position.x, player.position.y)
            self.renderer.render_minimap(player_pos)

            # Renderizar efectos activos
            if player:
                self.renderer.render_active_effects(player)

            # Renderizar elementos de debug si está habilitado
            if self.debug_mode:
                self._render_debug_info()

        except (AttributeError, KeyError) as e:
            self.logger.error("Error renderizando HUD: %s", e)

    def _render_debug_info(self):
        """Renderiza información de debug del HUD."""
        if not self.fonts.get("small"):
            return

        debug_info = [
            f"HUD Elements: {len(self.hud_elements)}",
            f"Screen: {self.screen_width}x{self.screen_height}",
            f"Visible: {sum(1 for e in self.hud_elements.values() if e.visible)}"
            f"/{len(self.hud_elements)}",
        ]

        y_offset = 5
        for info in debug_info:
            debug_text = self.fonts["small"].render(
                info, True, self.hud_config.colors["yellow"]
            )
            self.screen.blit(debug_text, (5, y_offset))
            y_offset += 15

    def toggle_visibility(self):
        """Alterna la visibilidad del HUD."""
        self.visible = not self.visible
        self.logger.debug("HUD visibility: %s", self.visible)

    def toggle_debug_mode(self):
        """Alterna el modo debug del HUD."""
        self.debug_mode = not self.debug_mode
        self.logger.debug("HUD debug mode: %s", self.debug_mode)

    def set_element_visibility(self, element_name: str, visible: bool):
        """
        Establece la visibilidad de un elemento específico.

        Args:
            element_name: Nombre del elemento
            visible: Si debe ser visible
        """
        if element_name in self.hud_elements:
            self.hud_elements[element_name].visible = visible
            self.logger.debug("Element '%s' visibility: %s", element_name, visible)

    def get_element_bounds(self, element_name: str) -> pygame.Rect | None:
        """
        Obtiene los límites de un elemento del HUD.

        Args:
            element_name: Nombre del elemento

        Returns:
            Rectángulo del elemento o None si no existe
        """
        element = self.hud_elements.get(element_name)
        if element:
            return pygame.Rect(element.x, element.y, element.width, element.height)
        return None
