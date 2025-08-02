"""
World Validator - Validador de posiciones y elementos
====================================================

Autor: SiK Team
Fecha: 2024
Descripción: Valida posiciones y crea elementos con sprites del mundo.
"""

import logging
import random

import pygame

from entities.tile import Tile, TileType

from .world_core import WorldCore


class WorldValidator:
    """
    Validador de posiciones y creador de elementos con sprites.
    """

    def __init__(self, world_core: WorldCore):
        """
        Inicializa el validador de mundo.

        Args:
            world_core: Núcleo del sistema de mundo
        """
        self.world_core = world_core
        self.logger = logging.getLogger(__name__)

    def is_valid_position(
        self, x: float, y: float, existing_elements: list[Tile]
    ) -> bool:
        """
        Verifica si una posición es válida para colocar un elemento.

        Args:
            x: Posición X
            y: Posición Y
            existing_elements: Lista de elementos existentes

        Returns:
            True si la posición es válida
        """
        for element in existing_elements:
            distance = ((x - element.x) ** 2 + (y - element.y) ** 2) ** 0.5
            if distance < self.world_core.min_distance:
                return False
        return True

    def create_element_with_sprite(self, x: float, y: float) -> Tile | None:
        """
        Crea un elemento usando sprites reales de assets/objects/elementos/.

        Args:
            x: Posición X
            y: Posición Y

        Returns:
            Elemento con sprite real o None si no se puede crear
        """
        if not self.world_core.available_sprites:
            # Fallback: crear elemento básico
            tile_type = random.choice(list(TileType))
            return Tile(x, y, tile_type)

        # Seleccionar sprite aleatorio
        sprite_filename = random.choice(self.world_core.available_sprites)
        sprite_path = f"assets/objects/elementos/{sprite_filename}"

        try:
            # Cargar sprite
            sprite = pygame.image.load(sprite_path).convert_alpha()

            # Determinar tipo de elemento basado en el nombre del archivo
            tile_type = self.world_core.get_tile_type_from_filename(sprite_filename)

            # Crear elemento
            element = Tile(x, y, tile_type)

            # Escalar sprite a tamaño apropiado (entre 32 y 64 píxeles)
            target_size = random.randint(32, 64)
            scaled_sprite = pygame.transform.scale(sprite, (target_size, target_size))
            element.sprite = scaled_sprite
            element.width = target_size
            element.height = target_size
            element.sprite_name = sprite_filename

            # Configurar colisión según el tipo
            # Los elementos se crean con el tipo correcto,
            # la colisión se maneja en el método has_collision()

            return element

        except (FileNotFoundError, AttributeError, ValueError) as e:
            self.logger.warning("No se pudo cargar sprite %s: %s", sprite_filename, e)
            # Fallback: crear elemento básico
            tile_type = random.choice(list(TileType))
            return Tile(x, y, tile_type)

    def validate_world_bounds(self, elements: list[Tile]) -> list[Tile]:
        """Valida que todos los elementos estén dentro de los límites del mundo."""
        valid_elements = []

        for element in elements:
            if (
                0 <= element.x <= self.world_core.world_width
                and 0 <= element.y <= self.world_core.world_height
            ):
                valid_elements.append(element)

        return valid_elements

    def validate_safe_zone(self, elements: list[Tile]) -> list[Tile]:
        """Valida que ningún elemento esté en la zona segura."""
        return [e for e in elements if not self.world_core.is_in_safe_zone(e.x, e.y)]

    def validate_minimum_distance(self, elements: list[Tile]) -> list[Tile]:
        """Valida que todos los elementos mantengan distancia mínima entre sí."""
        valid_elements = []

        for element in elements:
            is_valid = True
            for valid_element in valid_elements:
                distance = (
                    (element.x - valid_element.x) ** 2
                    + (element.y - valid_element.y) ** 2
                ) ** 0.5
                if distance < self.world_core.min_distance:
                    is_valid = False
                    break

            if is_valid:
                valid_elements.append(element)

        return valid_elements
