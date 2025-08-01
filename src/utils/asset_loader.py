"""
Asset Loader - Módulo Base de Carga de Assets
============================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Carga básica de archivos con sistema de caché optimizado.
"""

import logging
import os
from pathlib import Path
from typing import Any

import pygame


class AssetLoader:
    """Cargador base de assets con sistema de caché optimizado."""

    def __init__(self, base_path: str = "assets"):
        """
        Inicializa el cargador de assets.

        Args:
            base_path: Ruta base de los assets
        """
        self.base_path = Path(base_path)
        self.cache = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info("AssetLoader inicializado con base_path: %s", base_path)

    def load_image(self, path: str, scale: float = 1.0) -> pygame.Surface | None:
        """
        Carga una imagen con caché.

        Args:
            path: Ruta de la imagen
            scale: Factor de escala

        Returns:
            Superficie de pygame o None si falla
        """
        cache_key = f"{path}_{scale}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        full_path = self.base_path / path

        try:
            if full_path.exists():
                image = pygame.image.load(str(full_path)).convert_alpha()
                if scale != 1.0:
                    new_size = (
                        int(image.get_width() * scale),
                        int(image.get_height() * scale),
                    )
                    image = pygame.transform.scale(image, new_size)

                self.cache[cache_key] = image
                self.logger.debug("Imagen cargada: %s", path)
                return image
            else:
                self.logger.warning("Imagen no encontrada: %s", path)
                return self.create_placeholder(64, 64, scale)
        except OSError as e:
            self.logger.error("Error cargando imagen %s: %s", path, e)
            return self.create_placeholder(64, 64, scale)

    def load_image_direct(self, path: str) -> pygame.Surface | None:
        """
        Carga una imagen directamente sin caché.

        Args:
            path: Ruta de la imagen

        Returns:
            Superficie de pygame o None si falla
        """
        try:
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                self.logger.debug("Imagen cargada directamente: %s", path)
                return image
            else:
                self.logger.warning("Imagen no encontrada: %s", path)
                return self.create_placeholder(64, 64, 1.0)
        except OSError as e:
            self.logger.error("Error cargando imagen %s: %s", path, e)
            return self.create_placeholder(64, 64, 1.0)

    def create_placeholder(
        self, width: int, height: int, scale: float = 1.0
    ) -> pygame.Surface:
        """
        Crea un sprite placeholder.

        Args:
            width: Ancho del placeholder
            height: Alto del placeholder
            scale: Factor de escala

        Returns:
            Superficie del placeholder
        """
        final_width = int(width * scale)
        final_height = int(height * scale)
        placeholder = pygame.Surface(
            (final_width, final_height),
            flags=pygame.constants.SRCALPHA,  # pylint: disable=c-extension-no-member
        )
        placeholder.fill((255, 0, 255, 128))  # Magenta semi-transparente
        return placeholder

    def clear_cache(self):
        """Limpia la caché de imágenes."""
        self.cache.clear()
        self.logger.info("Caché de imágenes limpiada")

    def get_cache_info(self) -> dict[str, Any]:
        """
        Obtiene información sobre la caché.

        Returns:
            Información de la caché
        """
        return {"cache_size": len(self.cache), "cached_items": list(self.cache.keys())}

    def is_placeholder_sprite(self, sprite: pygame.Surface) -> bool:
        """
        Verifica si un sprite es un placeholder.

        Args:
            sprite: Superficie de pygame

        Returns:
            True si es un placeholder
        """
        if sprite.get_width() == 64 and sprite.get_height() == 64:
            colors = set()
            for x in range(0, 64, 8):
                for y in range(0, 64, 8):
                    color = sprite.get_at((x, y))
                    colors.add((color.r, color.g, color.b, color.a))
            if len(colors) <= 3:
                return True
        return False
