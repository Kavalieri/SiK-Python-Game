"""
HUD Rendering - Sistema de Renderizado del HUD
=============================================

Autor: SiK Team
Fecha: 2024
Descripción: Métodos especializados para renderizar todos los elementos del HUD.
"""

from typing import TYPE_CHECKING, Dict, Optional

import pygame

from .hud_elements import HUDEffectUtils

if TYPE_CHECKING:
    from ..core.game_state import GameState
    from .hud_elements import HUDConfiguration, HUDElement


class HUDRenderer:
    """Renderizador especializado para elementos del HUD."""

    def __init__(
        self,
        screen: pygame.Surface,
        config: "HUDConfiguration",
        fonts: Dict[str, pygame.font.Font],
    ):
        self.screen = screen
        self.config = config
        self.fonts = fonts
        self.hud_elements: Dict[str, "HUDElement"] = {}

    def set_hud_elements(self, elements: Dict[str, "HUDElement"]):
        """Establece los elementos del HUD a renderizar."""
        self.hud_elements = elements

    def render_background_panels(self):
        """Renderiza los paneles de fondo del HUD."""
        # Barra superior semi-transparente
        top_surface = pygame.Surface((self.config.screen_width, 60))
        top_surface.set_alpha(180)
        top_surface.fill(self.config.colors["dark_gray"])
        self.screen.blit(top_surface, (0, 0))

        # Barra inferior semi-transparente
        bottom_surface = pygame.Surface((self.config.screen_width, 40))
        bottom_surface.set_alpha(180)
        bottom_surface.fill(self.config.colors["dark_gray"])
        self.screen.blit(bottom_surface, (0, self.config.screen_height - 40))

        # Barra lateral derecha
        side_surface = pygame.Surface((80, self.config.screen_height - 200))
        side_surface.set_alpha(150)
        side_surface.fill(self.config.colors["dark_gray"])
        self.screen.blit(side_surface, (self.config.screen_width - 80, 100))

    def render_player_info(self, game_state: "GameState"):
        """Renderiza la información del jugador."""
        element = self.hud_elements.get("player_info")
        if not element or not element.visible:
            return

        # Nombre del jugador
        player_text = self.fonts["medium"].render(
            f"Jugador: {game_state.player_name}", True, self.config.colors["white"]
        )
        self.screen.blit(player_text, (element.x, element.y))

        # Barra de vida
        health_element = self.hud_elements.get("health_bar")
        if health_element:
            health_percentage = game_state.lives / 3.0  # Asumiendo 3 vidas máximas
            self._render_bar(
                health_element, health_percentage, self.config.colors["red"], "Vida"
            )

        # Barra de escudo
        shield_element = self.hud_elements.get("shield_bar")
        if shield_element:
            # Placeholder para escudo (implementar cuando esté disponible)
            shield_percentage = 1.0
            self._render_bar(
                shield_element, shield_percentage, self.config.colors["blue"], "Escudo"
            )

    def render_game_info(self, game_state: "GameState"):
        """Renderiza la información general del juego."""
        element = self.hud_elements.get("game_info")
        if not element or not element.visible:
            return

        # Puntuación centrada
        score_text = self.fonts["large"].render(
            f"Puntuación: {game_state.score:,}", True, self.config.colors["yellow"]
        )
        score_rect = score_text.get_rect()
        score_rect.centerx = element.x + element.width // 2
        score_rect.y = element.y
        self.screen.blit(score_text, score_rect)

        # Nivel
        level_element = self.hud_elements.get("level_info")
        if level_element:
            level_text = self.fonts["medium"].render(
                f"Nivel: {game_state.level}", True, self.config.colors["white"]
            )
            level_rect = level_text.get_rect()
            level_rect.centerx = level_element.x + level_element.width // 2
            level_rect.y = level_element.y
            self.screen.blit(level_text, level_rect)

    def render_score_info(self, game_state: "GameState"):
        """Renderiza información de puntuación en la esquina derecha."""
        element = self.hud_elements.get("score_info")
        if not element or not element.visible:
            return

        # Score actual
        score_text = self.fonts["medium"].render(
            f"Score: {game_state.score:,}", True, self.config.colors["white"]
        )
        self.screen.blit(score_text, (element.x, element.y))

        # High score (si está disponible)
        if hasattr(game_state, "high_score"):
            high_score_text = self.fonts["small"].render(
                f"Record: {game_state.high_score:,}", True, self.config.colors["yellow"]
            )
            self.screen.blit(high_score_text, (element.x, element.y + 20))

    def render_minimap(self, player_pos: Optional[tuple] = None):
        """Renderiza un mini-mapa básico."""
        element = self.hud_elements.get("minimap")
        if not element or not element.visible:
            return

        # Fondo del mini-mapa
        minimap_surface = pygame.Surface((element.width, element.height))
        minimap_surface.set_alpha(200)
        minimap_surface.fill(self.config.colors["dark_gray"])

        # Borde
        pygame.draw.rect(
            minimap_surface,
            self.config.colors["white"],
            (0, 0, element.width, element.height),
            2,
        )

        # Posición del jugador (centro del mini-mapa)
        if player_pos:
            center_x = element.width // 2
            center_y = element.height // 2
            pygame.draw.circle(
                minimap_surface, self.config.colors["green"], (center_x, center_y), 3
            )

        self.screen.blit(minimap_surface, (element.x, element.y))

    def render_active_effects(self, player):
        """Renderiza los efectos activos del jugador."""
        if not hasattr(player, "get_active_effects"):
            return

        active_effects = player.get_active_effects()
        if not active_effects:
            return

        # Renderizar cada efecto activo
        y_offset = 130
        for effect_type, remaining_time in active_effects.items():
            if remaining_time > 0:
                effect_name = HUDEffectUtils.get_effect_name(effect_type)
                time_text = f"{effect_name}: {remaining_time:.1f}s"

                # Color según el tipo de efecto
                color = HUDEffectUtils.get_effect_color(effect_type)

                text_surface = self.fonts["small"].render(time_text, True, color)
                self.screen.blit(text_surface, (10, y_offset))
                y_offset += 20

    def _render_bar(
        self, element: "HUDElement", percentage: float, color: tuple, label: str
    ):
        """Renderiza una barra de progreso genérica."""
        # Fondo de la barra
        bar_bg = pygame.Surface((element.width, element.height))
        bar_bg.fill(self.config.colors["dark_gray"])
        self.screen.blit(bar_bg, (element.x, element.y))

        # Barra de progreso
        if percentage > 0:
            progress_width = int(element.width * percentage)
            progress_surface = pygame.Surface((progress_width, element.height))
            progress_surface.fill(color)
            self.screen.blit(progress_surface, (element.x, element.y))

        # Borde
        pygame.draw.rect(
            self.screen,
            self.config.colors["white"],
            (element.x, element.y, element.width, element.height),
            1,
        )

        # Texto de la barra
        if self.fonts.get("small"):
            bar_text = self.fonts["small"].render(
                f"{label}: {int(percentage * 100)}%", True, self.config.colors["white"]
            )
            text_x = element.x + 5
            text_y = element.y + (element.height - bar_text.get_height()) // 2
            self.screen.blit(bar_text, (text_x, text_y))
