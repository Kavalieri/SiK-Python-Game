"""Character UI Renderer Advanced - Renderizado Avanzado de Personajes"""

import logging
from typing import Any, Dict

import pygame

from .character_data import CharacterData


class CharacterUIRendererAdvanced:
    """Gestiona el renderizado avanzado de elementos de personajes."""

    def __init__(self, ui_config):
        self.ui_config = ui_config
        self.logger = logging.getLogger(__name__)
        self.colors = ui_config.get_colors()
        self.fonts = ui_config.get_fonts()
        self.dimensions = ui_config.get_dimensions()

    def render_character_stats(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """Renderiza las estadísticas de un personaje."""
        try:
            char_data = CharacterData.get_character_data(character_key)
            if not char_data:
                return
            stats = char_data.get("stats", {})
            if not stats:
                return

            # Título
            title_surface = self.fonts["small"].render(
                "Estadísticas:", True, self.colors["text_secondary"]
            )
            screen.blit(title_surface, (x, y))

            # Estadísticas
            current_y = y + 25
            for stat_name, stat_value in stats.items():
                stat_text = f"{stat_name.title()}: {stat_value}"
                stat_surface = self.fonts["small"].render(
                    stat_text, True, self.colors["text"]
                )
                screen.blit(stat_surface, (x, current_y))
                current_y += 20
        except (KeyError, AttributeError) as e:
            self.logger.error(
                "Error renderizando estadísticas de %s: %s", character_key, e
            )

    def render_character_skills(
        self, screen: pygame.Surface, char_data: Dict[str, Any], x: int, y: int
    ):
        """Renderiza las habilidades de un personaje."""
        try:
            if not char_data:
                return
            skills = char_data.get("skills", [])
            if not skills:
                return

            # Título
            title_surface = self.fonts["small"].render(
                "Habilidades:", True, self.colors["text_secondary"]
            )
            screen.blit(title_surface, (x, y))

            # Habilidades
            current_y = y + 25
            for skill in skills:
                skill_name = (
                    skill
                    if isinstance(skill, str)
                    else skill.get("name", "Desconocida")
                )
                skill_surface = self.fonts["small"].render(
                    f"• {skill_name}", True, self.colors["text"]
                )
                screen.blit(skill_surface, (x, current_y))
                current_y += 18
        except (KeyError, AttributeError, TypeError) as e:
            self.logger.error("Error renderizando habilidades: %s", e)

    def render_character_description(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        max_width: int = 300,
    ):
        """Renderiza la descripción de un personaje."""
        try:
            char_data = CharacterData.get_character_data(character_key)
            if not char_data:
                return
            description = char_data.get("description", "Sin descripción disponible.")

            # Wordwrap básico
            font = self.fonts["small"]
            words = description.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                test_surface = font.render(test_line, True, self.colors["text"])
                if test_surface.get_width() <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            # Renderizar líneas
            current_y = y
            for line in lines:
                line_surface = font.render(line, True, self.colors["text"])
                screen.blit(line_surface, (x, current_y))
                current_y += 16
        except (KeyError, AttributeError) as e:
            self.logger.error(
                "Error renderizando descripción de %s: %s", character_key, e
            )

    def render_character_info_panel(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        width: int = 300,
        height: int = 400,
    ):
        """Renderiza un panel completo de información del personaje."""
        # Fondo del panel
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.colors["panel_background"], panel_rect)
        pygame.draw.rect(screen, self.colors["panel_border"], panel_rect, 2)

        try:
            char_data = CharacterData.get_character_data(character_key)
            if not char_data:
                return

            # Título
            name = char_data.get("name", character_key.title())
            title_surface = self.fonts["normal"].render(
                name, True, self.colors["text_highlight"]
            )
            title_rect = title_surface.get_rect(centerx=x + width // 2, y=y + 10)
            screen.blit(title_surface, title_rect)

            # Componentes
            self.render_character_stats(screen, character_key, x + 10, y + 50)
            self.render_character_skills(screen, char_data, x + 10, y + 170)
            self.render_character_description(
                screen, character_key, x + 10, y + 270, width - 20
            )
        except (KeyError, AttributeError) as e:
            self.logger.error(
                "Error renderizando panel de información de %s: %s", character_key, e
            )
