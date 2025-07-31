"""Character UI Renderer Basic - Renderizado Básico de Personajes"""

import logging

import pygame

from .character_data import CharacterData


class CharacterUIRendererBasic:
    """Gestiona el renderizado básico de elementos de personajes."""

    def __init__(self, ui_config):
        self.ui_config = ui_config
        self.logger = logging.getLogger(__name__)
        self.colors = ui_config.get_colors()
        self.fonts = ui_config.get_fonts()
        self.dimensions = ui_config.get_dimensions()

    def render_title(self, screen: pygame.Surface):
        """Renderiza el título de la pantalla de selección de personajes."""
        title_text = "Selecciona tu Personaje"
        font = self.fonts["title"]
        text_surface = font.render(title_text, True, self.colors["text_primary"])
        text_rect = text_surface.get_rect(
            centerx=screen.get_width() // 2, y=self.dimensions["margin"] * 2
        )
        screen.blit(text_surface, text_rect)

    def render_character_card(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        is_selected: bool = False,
    ):
        """Renderiza una tarjeta completa de personaje."""
        card_width = self.dimensions["card_width"]
        card_height = self.dimensions["card_height"]
        border_color = (
            self.colors["selected_border"]
            if is_selected
            else self.colors["panel_border"]
        )
        border_width = 4 if is_selected else 2

        card_rect = pygame.Rect(x, y, card_width, card_height)
        pygame.draw.rect(screen, self.colors["card_background"], card_rect)
        pygame.draw.rect(screen, border_color, card_rect, border_width)

        self._render_character_image(screen, character_key, x, y)
        self._render_character_name(screen, character_key, x, y, card_width)

    def _render_character_image(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """Renderiza la imagen de un personaje o un placeholder."""
        image_size = self.dimensions["image_size"]
        margin = self.dimensions["margin"]
        img_x = x + (self.dimensions["card_width"] - image_size) // 2
        img_y = y + margin

        try:
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                raise KeyError(f"No data found for character: {character_key}")
            image_path = char_data.get("image_path")
            if image_path:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (image_size, image_size))
                screen.blit(image, (img_x, img_y))
            else:
                raise FileNotFoundError("No image path found")
        except (FileNotFoundError, KeyError, OSError):
            placeholder = self.create_character_placeholder(character_key, image_size)
            screen.blit(placeholder, (img_x, img_y))

    def _render_character_name(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        card_width: int,
    ):
        """Renderiza el nombre de un personaje en su tarjeta."""
        try:
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                raise KeyError(f"No data found for character: {character_key}")
            name = char_data.get("name", character_key.title())
        except (KeyError, AttributeError):
            name = character_key.title()

        font = self.fonts["normal"]
        text_surface = font.render(name, True, self.colors["text_primary"])
        text_rect = text_surface.get_rect(
            centerx=x + card_width // 2, y=y + self.dimensions["card_height"] - 40
        )
        screen.blit(text_surface, text_rect)

    def create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """Crea un placeholder público para personajes."""
        return self._create_character_placeholder(character_key, size)

    def _create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """Crea un placeholder visual para un personaje cuando no hay imagen."""
        placeholder = pygame.Surface((size, size))
        placeholder.fill(self.colors["placeholder_bg"])
        pygame.draw.rect(
            placeholder, self.colors["placeholder_border"], placeholder.get_rect(), 2
        )

        initial = character_key[0].upper() if character_key else "?"
        font = self.fonts["title"]
        text_surface = font.render(initial, True, self.colors["placeholder_text"])
        text_rect = text_surface.get_rect(center=(size // 2, size // 2))
        placeholder.blit(text_surface, text_rect)
        return placeholder
