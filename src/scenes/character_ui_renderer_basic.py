"""
Character UI Renderer Basic - Renderizado Básico de Personajes
===========================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado para renderizado básico de elementos
             de personajes (título, tarjetas, imágenes básicas).
"""

import logging

import pygame

from .character_data import CharacterData


class CharacterUIRendererBasic:
    """
    Gestiona el renderizado básico de elementos de personajes.

    Responsabilidades:
    - Renderizado de título de pantalla
    - Renderizado de tarjetas de personajes
    - Renderizado de imágenes básicas
    - Creación de placeholders

    Ejemplo de uso:
        >>> renderer = CharacterUIRendererBasic(ui_config)
        >>> renderer.render_title(screen)
        >>> renderer.render_character_card(screen, "guerrero", 100, 100, True)
    """

    def __init__(self, ui_config):
        """
        Inicializa el renderizador básico.

        Args:
            ui_config: Configuración de UI (CharacterUIConfiguration)
        """
        self.ui_config = ui_config
        self.logger = logging.getLogger(__name__)

        # Obtener configuración
        self.colors = ui_config.get_colors()
        self.fonts = ui_config.get_fonts()
        self.dimensions = ui_config.get_dimensions()

        self.logger.info("CharacterUIRendererBasic inicializado")

    def render_title(self, screen: pygame.Surface):
        """
        Renderiza el título de la pantalla de selección de personajes.

        Args:
            screen: Superficie donde renderizar
        """
        title_text = "Selecciona tu Personaje"
        font = self.fonts["title"]
        text_surface = font.render(title_text, True, self.colors["text_primary"])

        # Centrar el título en la parte superior
        text_rect = text_surface.get_rect(
            centerx=screen.get_width() // 2, y=self.dimensions["margin"] * 2
        )

        screen.blit(text_surface, text_rect)
        self.logger.debug("Título renderizado en posición: %s", text_rect.center)

    def render_character_card(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        is_selected: bool = False,
    ):
        """
        Renderiza una tarjeta completa de personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje a renderizar
            x: Coordenada X de la tarjeta
            y: Coordenada Y de la tarjeta
            is_selected: Si la tarjeta está seleccionada
        """
        card_width = self.dimensions["card_width"]
        card_height = self.dimensions["card_height"]

        # Color del borde según selección
        border_color = (
            self.colors["selected_border"]
            if is_selected
            else self.colors["panel_border"]
        )
        border_width = 4 if is_selected else 2

        # Dibujar fondo de la tarjeta
        card_rect = pygame.Rect(x, y, card_width, card_height)
        pygame.draw.rect(screen, self.colors["card_background"], card_rect)
        pygame.draw.rect(screen, border_color, card_rect, border_width)

        # Renderizar imagen del personaje
        self._render_character_image(screen, character_key, x, y)

        # Renderizar nombre del personaje
        self._render_character_name(screen, character_key, x, y, card_width)

        self.logger.debug(
            "Tarjeta renderizada - Personaje: %s, Posición: (%d, %d), Seleccionado: %s",
            character_key,
            x,
            y,
            is_selected,
        )

    def _render_character_image(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """
        Renderiza la imagen de un personaje o un placeholder.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Coordenada X base
            y: Coordenada Y base
        """
        image_size = self.dimensions["image_size"]
        margin = self.dimensions["margin"]

        # Posición centrada para la imagen
        img_x = x + (self.dimensions["card_width"] - image_size) // 2
        img_y = y + margin

        try:
            # Intentar cargar imagen real del personaje
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                raise KeyError(f"No data found for character: {character_key}")

            image_path = char_data.get("image_path")

            if image_path:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (image_size, image_size))
                screen.blit(image, (img_x, img_y))
                self.logger.debug("Imagen cargada: %s", image_path)
            else:
                raise FileNotFoundError("No image path found")

        except (FileNotFoundError, KeyError, OSError) as e:
            # Renderizar placeholder si falla la carga
            self.logger.warning("Error cargando imagen %s: %s", character_key, e)
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
        """
        Renderiza el nombre de un personaje en su tarjeta.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Coordenada X base
            y: Coordenada Y base
            card_width: Ancho de la tarjeta
        """
        try:
            char_data = CharacterData.get_character_data(character_key)
            if char_data is None:
                raise KeyError(f"No data found for character: {character_key}")
            name = char_data.get("name", character_key.title())
        except (KeyError, AttributeError):
            name = character_key.title()

        font = self.fonts["normal"]
        text_surface = font.render(name, True, self.colors["text_primary"])

        # Centrar el nombre en la parte inferior de la tarjeta
        text_rect = text_surface.get_rect(
            centerx=x + card_width // 2, y=y + self.dimensions["card_height"] - 40
        )

        screen.blit(text_surface, text_rect)
        self.logger.debug(
            "Nombre renderizado: %s en posición: %s", name, text_rect.center
        )

    def create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """
        Crea un placeholder público para personajes.

        Args:
            character_key: Clave del personaje
            size: Tamaño del placeholder

        Returns:
            pygame.Surface: Superficie placeholder
        """
        return self._create_character_placeholder(character_key, size)

    def _create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """
        Crea un placeholder visual para un personaje cuando no hay imagen.

        Args:
            character_key: Clave del personaje
            size: Tamaño del placeholder

        Returns:
            pygame.Surface: Superficie con el placeholder
        """
        placeholder = pygame.Surface((size, size))
        placeholder.fill(self.colors["placeholder_bg"])

        # Dibujar borde
        pygame.draw.rect(
            placeholder, self.colors["placeholder_border"], placeholder.get_rect(), 2
        )

        # Renderizar inicial del personaje en el centro
        initial = character_key[0].upper() if character_key else "?"
        font = self.fonts["title"]
        text_surface = font.render(initial, True, self.colors["placeholder_text"])
        text_rect = text_surface.get_rect(center=(size // 2, size // 2))
        placeholder.blit(text_surface, text_rect)

        self.logger.debug(
            "Placeholder creado para %s: %dx%d", character_key, size, size
        )
        return placeholder
