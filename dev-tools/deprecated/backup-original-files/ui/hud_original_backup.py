"""
HUD - Heads Up Display
=====================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de interfaz de usuario que muestra información del jugador durante el juego.
"""

import logging
from dataclasses import dataclass

import pygame

from ..core.game_state import GameState
from ..entities.powerup import PowerupType
from ..utils.config_manager import ConfigManager


@dataclass
class HUDElement:
    """Elemento del HUD con su posición y configuración."""

    name: str
    x: int
    y: int
    width: int
    height: int
    visible: bool = True
    alpha: int = 255
    element_type: str = "text"  # 'text', 'bar', 'effects_panel'
    text: str = ""


class HUD:
    """
    Sistema de HUD profesional que muestra información del jugador.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state: GameState
    ):
        """
        Inicializa el sistema de HUD.

        Args:
                screen: Superficie de Pygame donde renderizar
                config: Configuración del juego
                game_state: Estado del juego
        """
        self.screen = screen
        self.config = config
        self.game_state = game_state
        self.logger = logging.getLogger(__name__)

        # Configuración del HUD
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.hud_elements: dict[str, HUDElement] = {}
        self.fonts: dict[str, pygame.font.Font] = {}
        self.colors: dict[str, tuple[int, int, int]] = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "gray": (128, 128, 128),
            "dark_gray": (64, 64, 64),
            "light_gray": (192, 192, 192),
        }

        self._initialize_hud_elements()
        self._initialize_fonts()

        self.logger.info("Sistema de HUD inicializado")

    def _initialize_hud_elements(self):
        """Inicializa los elementos del HUD con sus posiciones."""
        # Barra superior
        self.hud_elements["top_bar"] = HUDElement(
            "top_bar", 0, 0, self.screen_width, 60
        )

        # Información del jugador (izquierda)
        self.hud_elements["player_info"] = HUDElement("player_info", 10, 10, 200, 40)
        self.hud_elements["health_bar"] = HUDElement("health_bar", 10, 50, 200, 20)
        self.hud_elements["shield_bar"] = HUDElement("shield_bar", 10, 75, 200, 15)

        # Información del juego (centro superior)
        self.hud_elements["game_info"] = HUDElement(
            "game_info", self.screen_width // 2 - 150, 10, 300, 40
        )
        self.hud_elements["level_info"] = HUDElement(
            "level_info", self.screen_width // 2 - 100, 50, 200, 20
        )
        self.hud_elements["time_info"] = HUDElement(
            "time_info", self.screen_width // 2 - 100, 75, 200, 20
        )

        # Puntuación (derecha)
        self.hud_elements["score_info"] = HUDElement(
            "score_info", self.screen_width - 210, 10, 200, 40
        )
        self.hud_elements["high_score"] = HUDElement(
            "high_score", self.screen_width - 210, 50, 200, 20
        )
        self.hud_elements["combo_info"] = HUDElement(
            "combo_info", self.screen_width - 210, 75, 200, 20
        )

        # Barra lateral derecha para powerups
        self.hud_elements["powerup_bar"] = HUDElement(
            "powerup_bar", self.screen_width - 80, 100, 70, self.screen_height - 200
        )

        # Barra inferior para información adicional
        self.hud_elements["bottom_bar"] = HUDElement(
            "bottom_bar", 0, self.screen_height - 40, self.screen_width, 40
        )

        # Indicadores de estado
        self.hud_elements["status_indicators"] = HUDElement(
            "status_indicators", 10, self.screen_height - 80, 300, 30
        )

        self.logger.debug(
            f"HUD elements initialized: {len(self.hud_elements)} elements"
        )

    def _initialize_fonts(self):
        """Inicializa las fuentes para el HUD."""
        try:
            # Intentar cargar fuente personalizada
            font_path = (
                self.config.get("paths", "assets", "assets") + "/fonts/arcade.ttf"
            )
            self.fonts["large"] = pygame.font.Font(font_path, 24)
            self.fonts["medium"] = pygame.font.Font(font_path, 18)
            self.fonts["small"] = pygame.font.Font(font_path, 14)
            self.fonts["tiny"] = pygame.font.Font(font_path, 12)
        except Exception:
            # Usar fuentes por defecto si no se encuentra la personalizada
            self.fonts["large"] = pygame.font.Font(None, 24)
            self.fonts["medium"] = pygame.font.Font(None, 18)
            self.fonts["small"] = pygame.font.Font(None, 14)
            self.fonts["tiny"] = pygame.font.Font(None, 12)
            self.logger.warning(
                "Fuente personalizada no encontrada, usando fuentes por defecto"
            )

    def render(self):
        """Renderiza todos los elementos del HUD."""
        self._render_background()
        self._render_player_info()
        self._render_game_info()
        self._render_score_info()
        self._render_powerup_bar()
        self._render_status_indicators()
        self._render_bottom_bar()

    def _render_background(self):
        """Renderiza el fondo del HUD."""
        # Barra superior semi-transparente
        top_surface = pygame.Surface((self.screen_width, 100))
        top_surface.set_alpha(180)
        top_surface.fill(self.colors["dark_gray"])
        self.screen.blit(top_surface, (0, 0))

        # Barra inferior semi-transparente
        bottom_surface = pygame.Surface((self.screen_width, 40))
        bottom_surface.set_alpha(180)
        bottom_surface.fill(self.colors["dark_gray"])
        self.screen.blit(bottom_surface, (0, self.screen_height - 40))

        # Barra lateral derecha
        side_surface = pygame.Surface((80, self.screen_height - 200))
        side_surface.set_alpha(150)
        side_surface.fill(self.colors["dark_gray"])
        self.screen.blit(side_surface, (self.screen_width - 80, 100))

    def _render_player_info(self):
        """Renderiza la información del jugador."""
        element = self.hud_elements["player_info"]
        if not element.visible:
            return

        # Nombre del jugador
        player_text = self.fonts["medium"].render(
            f"Jugador: {self.game_state.player_name}", True, self.colors["white"]
        )
        self.screen.blit(player_text, (element.x, element.y))

        # Barra de vida
        health_element = self.hud_elements["health_bar"]
        health_percentage = self.game_state.lives / 3.0  # Asumiendo 3 vidas máximas
        self._render_bar(health_element, health_percentage, self.colors["red"], "Vida")

        # Barra de escudo (si existe)
        shield_element = self.hud_elements["shield_bar"]
        shield_percentage = getattr(self.game_state, "shield", 0) / 100.0
        if shield_percentage > 0:
            self._render_bar(
                shield_element, shield_percentage, self.colors["blue"], "Escudo"
            )

    def _render_game_info(self):
        """Renderiza la información del juego."""
        element = self.hud_elements["game_info"]
        if not element.visible:
            return

        # Información del nivel
        level_text = self.fonts["medium"].render(
            f"Nivel {self.game_state.level}", True, self.colors["yellow"]
        )
        self.screen.blit(level_text, (element.x, element.y))

        # Información de tiempo (si está disponible)
        time_element = self.hud_elements["time_info"]
        time_remaining = getattr(self.game_state, "time_remaining", 0)
        if time_remaining > 0:
            time_text = self.fonts["small"].render(
                f"Tiempo: {time_remaining:.1f}s", True, self.colors["white"]
            )
            self.screen.blit(time_text, (time_element.x, time_element.y))

    def _render_score_info(self):
        """Renderiza la información de puntuación."""
        element = self.hud_elements["score_info"]
        if not element.visible:
            return

        # Puntuación actual
        score_text = self.fonts["medium"].render(
            f"Puntos: {self.game_state.score:,}", True, self.colors["white"]
        )
        self.screen.blit(score_text, (element.x, element.y))

        # Puntuación máxima
        high_score_element = self.hud_elements["high_score"]
        high_score_text = self.fonts["small"].render(
            f"Récord: {self.game_state.high_score:,}", True, self.colors["yellow"]
        )
        self.screen.blit(high_score_text, (high_score_element.x, high_score_element.y))

        # Combo (si existe)
        combo_element = self.hud_elements["combo_info"]
        combo = getattr(self.game_state, "combo", 0)
        if combo > 0:
            combo_text = self.fonts["small"].render(
                f"Combo: x{combo}", True, self.colors["orange"]
            )
            self.screen.blit(combo_text, (combo_element.x, combo_element.y))

    def _render_powerup_bar(self):
        """Renderiza la barra de powerups."""
        element = self.hud_elements["powerup_bar"]
        if not element.visible:
            return

        # Título de la barra
        title_text = self.fonts["small"].render("POWERUPS", True, self.colors["white"])
        self.screen.blit(title_text, (element.x + 5, element.y - 20))

        # Aquí se renderizarían los powerups activos
        # Por ahora solo un placeholder
        powerups = getattr(self.game_state, "active_powerups", [])
        for i, powerup in enumerate(powerups[:5]):  # Máximo 5 powerups visibles
            y_pos = element.y + i * 30
            powerup_text = self.fonts["tiny"].render(
                powerup.name[:8], True, self.colors["green"]
            )
            self.screen.blit(powerup_text, (element.x + 5, y_pos))

    def _render_status_indicators(self):
        """Renderiza los indicadores de estado."""
        element = self.hud_elements["status_indicators"]
        if not element.visible:
            return

        # Indicadores de estado (ejemplo: pausa, modo especial, etc.)
        status_indicators = []

        if self.game_state.status.value == "paused":
            status_indicators.append(("PAUSA", self.colors["yellow"]))

        if getattr(self.game_state, "invulnerable", False):
            status_indicators.append(("INVULNERABLE", self.colors["purple"]))

        if getattr(self.game_state, "rage_mode", False):
            status_indicators.append(("RAGE MODE", self.colors["red"]))

        for i, (status, color) in enumerate(status_indicators):
            status_text = self.fonts["small"].render(status, True, color)
            self.screen.blit(status_text, (element.x + i * 120, element.y))

    def _render_bottom_bar(self):
        """Renderiza la barra inferior."""
        element = self.hud_elements["bottom_bar"]
        if not element.visible:
            return

        # Información adicional en la barra inferior
        # Por ejemplo: controles, estado del juego, etc.
        controls_text = self.fonts["tiny"].render(
            "WASD: Mover | Ratón: Apuntar | Clic: Disparar | ESC: Pausa",
            True,
            self.colors["light_gray"],
        )
        self.screen.blit(controls_text, (element.x + 10, element.y + 10))

    def _render_bar(
        self,
        element: HUDElement,
        percentage: float,
        color: tuple[int, int, int],
        label: str,
    ):
        """
        Renderiza una barra de progreso.

        Args:
                element: Elemento del HUD donde renderizar
                percentage: Porcentaje de llenado (0.0 a 1.0)
                color: Color de la barra
                label: Etiqueta de la barra
        """
        if not element.visible:
            return

        # Fondo de la barra
        pygame.draw.rect(
            self.screen,
            self.colors["gray"],
            (element.x, element.y, element.width, element.height),
        )

        # Barra de progreso
        fill_width = int(element.width * percentage)
        if fill_width > 0:
            pygame.draw.rect(
                self.screen, color, (element.x, element.y, fill_width, element.height)
            )

        # Borde de la barra
        pygame.draw.rect(
            self.screen,
            self.colors["white"],
            (element.x, element.y, element.width, element.height),
            2,
        )

        # Etiqueta
        label_text = self.fonts["tiny"].render(label, True, self.colors["white"])
        self.screen.blit(label_text, (element.x, element.y - 15))

    def show_message(
        self, message: str, duration: float = 3.0, color: tuple[int, int, int] = None
    ):
        """
        Muestra un mensaje temporal en el HUD.

        Args:
                message: Mensaje a mostrar
                duration: Duración en segundos
                color: Color del mensaje
        """
        if color is None:
            color = self.colors["white"]

        # Renderizar mensaje centrado
        text_surface = self.fonts["large"].render(message, True, color)
        text_rect = text_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )

        # Fondo semi-transparente
        bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
        bg_surface.set_alpha(180)
        bg_surface.fill(self.colors["black"])
        bg_rect = bg_surface.get_rect(center=text_rect.center)

        self.screen.blit(bg_surface, bg_rect)
        self.screen.blit(text_surface, text_rect)

        self.logger.debug(f"Mensaje mostrado: {message}")

    def toggle_element(self, element_name: str):
        """
        Alterna la visibilidad de un elemento del HUD.

        Args:
                element_name: Nombre del elemento a alternar
        """
        if element_name in self.hud_elements:
            self.hud_elements[element_name].visible = not self.hud_elements[
                element_name
            ].visible
            self.logger.debug(
                f"Elemento {element_name} alternado: {self.hud_elements[element_name].visible}"
            )

    def update(self):
        """Actualiza el HUD."""
        # Por ahora no hay lógica de actualización específica
        pass

    def update_game_state(self, game_state: GameState):
        """
        Actualiza el estado del juego para el HUD.

        Args:
                game_state: Nuevo estado del juego
        """
        self.game_state = game_state

    def _render_active_effects(self):
        """Renderiza los efectos activos del jugador."""
        if not hasattr(self, "game_state") or not self.game_state:
            return

        # Obtener efectos activos del jugador (si existe)
        player = getattr(self.game_state, "current_player", None)
        if not player or not hasattr(player, "get_active_effects"):
            return

        active_effects = player.get_active_effects()
        if not active_effects:
            return

        # Renderizar cada efecto activo
        y_offset = 130
        for effect_type, remaining_time in active_effects.items():
            if remaining_time > 0:
                effect_name = self._get_effect_name(effect_type)
                time_text = f"{effect_name}: {remaining_time:.1f}s"

                # Color según el tipo de efecto
                color = self._get_effect_color(effect_type)

                text_surface = self.effects_font.render(time_text, True, color)
                self.screen.blit(text_surface, (10, y_offset))
                y_offset += 20

    def _get_effect_name(self, effect_type: PowerupType) -> str:
        """Obtiene el nombre legible del efecto."""
        names = {
            PowerupType.SPEED: "Velocidad",
            PowerupType.DAMAGE: "Daño",
            PowerupType.SHIELD: "Escudo",
            PowerupType.RAPID_FIRE: "Disparo Rápido",
            PowerupType.DOUBLE_SHOT: "Doble Disparo",
            PowerupType.HEALTH: "Vida",
        }
        return names.get(effect_type, effect_type.value)

    def _get_effect_color(self, effect_type: PowerupType) -> tuple:
        """Obtiene el color para el tipo de efecto."""
        colors = {
            PowerupType.SPEED: (0, 255, 0),  # Verde
            PowerupType.DAMAGE: (255, 0, 0),  # Rojo
            PowerupType.SHIELD: (0, 0, 255),  # Azul
            PowerupType.RAPID_FIRE: (255, 255, 0),  # Amarillo
            PowerupType.DOUBLE_SHOT: (255, 0, 255),  # Magenta
            PowerupType.HEALTH: (255, 165, 0),  # Naranja
        }
        return colors.get(effect_type, (255, 255, 255))
