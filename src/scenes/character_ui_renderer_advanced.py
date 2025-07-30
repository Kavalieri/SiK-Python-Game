"""
Character UI Renderer Advanced - Renderizado Avanzado de Personajes
================================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado para renderizado avanzado de elementos
             de personajes (estadísticas, habilidades, información detallada).
"""

import logging
from typing import Any, Dict

import pygame

from .character_data import CharacterData


class CharacterUIRendererAdvanced:
    """
    Gestiona el renderizado avanzado de elementos de personajes.

    Responsabilidades:
    - Renderizado de estadísticas de personajes
    - Renderizado de habilidades de personajes
    - Renderizado de información detallada
    - Renderizado de efectos especiales

    Ejemplo de uso:
        >>> renderer = CharacterUIRendererAdvanced(ui_config)
        >>> renderer.render_character_stats(screen, "guerrero", 100, 100)
        >>> renderer.render_character_skills(screen, char_data, 100, 200)
    """

    def __init__(self, ui_config):
        """
        Inicializa el renderizador avanzado.

        Args:
            ui_config: Configuración de UI (CharacterUIConfiguration)
        """
        self.ui_config = ui_config
        self.logger = logging.getLogger(__name__)

        # Obtener configuración
        self.colors = ui_config.get_colors()
        self.fonts = ui_config.get_fonts()
        self.dimensions = ui_config.get_dimensions()

        self.logger.info("CharacterUIRendererAdvanced inicializado")

    def render_character_stats(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """
        Renderiza las estadísticas de un personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Coordenada X base
            y: Coordenada Y base
        """
        try:
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                self.logger.warning(
                    "No se encontraron datos para el personaje: %s", character_key
                )
                return

            stats = char_data.get("stats", {})
            if not stats:
                self.logger.warning(
                    "No se encontraron estadísticas para: %s", character_key
                )
                return

            # Renderizar título de estadísticas
            font_title = self.fonts["small"]
            title_surface = font_title.render(
                "Estadísticas:", True, self.colors["text_secondary"]
            )
            screen.blit(title_surface, (x, y))

            # Renderizar cada estadística
            current_y = y + 25
            font_stat = self.fonts["small"]

            for stat_name, stat_value in stats.items():
                stat_text = f"{stat_name.title()}: {stat_value}"
                stat_surface = font_stat.render(
                    stat_text, True, self.colors["text_primary"]
                )
                screen.blit(stat_surface, (x, current_y))
                current_y += 20

            self.logger.debug(
                "Estadísticas renderizadas para %s en (%d, %d)", character_key, x, y
            )

        except (KeyError, AttributeError) as e:
            self.logger.error(
                "Error renderizando estadísticas de %s: %s", character_key, e
            )

    def render_character_skills(
        self, screen: pygame.Surface, char_data: Dict[str, Any], x: int, y: int
    ):
        """
        Renderiza las habilidades de un personaje.

        Args:
            screen: Superficie donde renderizar
            char_data: Datos del personaje
            x: Coordenada X base
            y: Coordenada Y base
        """
        try:
            if char_data is None:
                self.logger.warning(
                    "char_data es None, no se pueden renderizar habilidades"
                )
                return

            skills = char_data.get("skills", [])
            if not skills:
                self.logger.warning("No se encontraron habilidades en char_data")
                return

            # Renderizar título de habilidades
            font_title = self.fonts["small"]
            title_surface = font_title.render(
                "Habilidades:", True, self.colors["text_secondary"]
            )
            screen.blit(title_surface, (x, y))

            # Renderizar cada habilidad
            current_y = y + 25
            font_skill = self.fonts["small"]

            for skill in skills:
                skill_name = (
                    skill
                    if isinstance(skill, str)
                    else skill.get("name", "Desconocida")
                )
                skill_surface = font_skill.render(
                    f"• {skill_name}", True, self.colors["text_primary"]
                )
                screen.blit(skill_surface, (x, current_y))
                current_y += 18

            self.logger.debug(
                "Habilidades renderizadas en (%d, %d): %d habilidades",
                x,
                y,
                len(skills),
            )

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
        """
        Renderiza la descripción de un personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Coordenada X base
            y: Coordenada Y base
            max_width: Ancho máximo del texto
        """
        try:
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                return

            description = char_data.get("description", "Sin descripción disponible.")

            # Renderizar descripción con wordwrap básico
            font = self.fonts["small"]
            words = description.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                test_surface = font.render(test_line, True, self.colors["text_primary"])

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
                line_surface = font.render(line, True, self.colors["text_primary"])
                screen.blit(line_surface, (x, current_y))
                current_y += 16

            self.logger.debug(
                "Descripción renderizada para %s: %d líneas", character_key, len(lines)
            )

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
        """
        Renderiza un panel completo de información del personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Coordenada X del panel
            y: Coordenada Y del panel
            width: Ancho del panel
            height: Alto del panel
        """
        # Dibujar fondo del panel
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.colors["panel_background"], panel_rect)
        pygame.draw.rect(screen, self.colors["panel_border"], panel_rect, 2)

        # Renderizar título del personaje
        try:
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                return

            name = char_data.get("name", character_key.title())
            font_title = self.fonts["normal"]
            title_surface = font_title.render(name, True, self.colors["text_highlight"])
            title_rect = title_surface.get_rect(centerx=x + width // 2, y=y + 10)
            screen.blit(title_surface, title_rect)

            # Renderizar estadísticas
            stats_y = y + 50
            self.render_character_stats(screen, character_key, x + 10, stats_y)

            # Renderizar habilidades
            skills_y = stats_y + 120
            self.render_character_skills(screen, char_data, x + 10, skills_y)

            # Renderizar descripción
            desc_y = skills_y + 100
            self.render_character_description(
                screen, character_key, x + 10, desc_y, width - 20
            )

            self.logger.debug("Panel de información renderizado para %s", character_key)

        except (KeyError, AttributeError) as e:
            self.logger.error(
                "Error renderizando panel de información de %s: %s", character_key, e
            )
