"""
World Generator - Generador de Mundo (FACHADA)
==============================================

Autor: SiK Team
Fecha: 2024
Descripción: Fachada del sistema modular de generación de mundo.
Mantiene API original para compatibilidad con delegación a módulos especializados.
"""

import logging
import random
from typing import List, Optional

from ..entities.tile import Tile, TileType
from .cluster_generator import ClusterGenerator
from .world_core import WorldCore
from .world_validator import WorldValidator


class WorldGenerator:
    """
    Fachada del sistema de generación de mundo - delega a módulos especializados.
    Mantiene 100% compatibilidad con API original.
    """

    def __init__(
        self, world_width: int, world_height: int, screen_width: int, screen_height: int
    ):
        """
        Inicializa el generador de mundo modular.

        Args:
            world_width: Ancho del mundo (3-4 veces la pantalla)
            world_height: Alto del mundo (3-4 veces la pantalla)
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        self.logger = logging.getLogger(__name__)

        # Inicializar módulos especializados
        self.core = WorldCore(world_width, world_height, screen_width, screen_height)
        self.validator = WorldValidator(self.core)
        self.cluster_generator = ClusterGenerator(self.core)

        # Propiedades para compatibilidad con API original
        self.world_width = self.core.world_width
        self.world_height = self.core.world_height
        self.screen_width = self.core.screen_width
        self.screen_height = self.core.screen_height

        self.logger.info("WorldGenerator inicializado con sistema modular")

    def generate_world(
        self, element_types: Optional[List[TileType]] = None
    ) -> List[Tile]:
        """
        Genera el mundo completo con elementos distribuidos.

        Args:
            element_types: Tipos de elementos permitidos (None = todos)

        Returns:
            Lista de elementos generados
        """
        elements = []

        if element_types is None:
            element_types = list(TileType)

        # Calcular número aproximado de elementos
        num_elements = self.core.calculate_total_elements()
        self.logger.info("Generando %d elementos...", num_elements)

        # Generar elementos
        attempts = 0
        max_attempts = num_elements * 20  # Evitar bucle infinito

        while len(elements) < num_elements and attempts < max_attempts:
            attempts += 1

            # Posición aleatoria
            x = random.randint(0, self.core.world_width)
            y = random.randint(0, self.core.world_height)

            # Verificar zona segura
            if self.core.is_in_safe_zone(x, y):
                continue

            # Verificar distancia mínima con otros elementos
            if self.validator.is_valid_position(x, y, elements):
                # Crear elemento con sprite real
                element = self.validator.create_element_with_sprite(x, y)
                if element:
                    elements.append(element)

                    if len(elements) % 10 == 0:
                        self.logger.debug("Generados %d elementos...", len(elements))

        self.logger.info("Mundo generado con %d elementos", len(elements))
        return elements

    def generate_cluster(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        num_elements: int,
        element_types: Optional[List[TileType]] = None,
    ) -> List[Tile]:
        """
        Genera un cluster de elementos en una zona específica.

        Args:
            center_x: Centro X del cluster
            center_y: Centro Y del cluster
            radius: Radio del cluster
            num_elements: Número de elementos a generar
            element_types: Tipos de elementos permitidos (None = todos)

        Returns:
            Lista de elementos del cluster
        """
        return self.cluster_generator.generate_cluster(
            center_x, center_y, radius, num_elements, element_types
        )

    def generate_desert_oasis(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera un oasis en el desierto."""
        return self.cluster_generator.generate_desert_oasis(center_x, center_y, radius)

    def generate_rock_formation(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera una formación de rocas."""
        return self.cluster_generator.generate_rock_formation(
            center_x, center_y, radius
        )

    def generate_cactus_field(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera un campo de cactus."""
        return self.cluster_generator.generate_cactus_field(center_x, center_y, radius)

    def generate_ruins(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera ruinas antiguas."""
        return self.cluster_generator.generate_ruins(center_x, center_y, radius)

    # Métodos de compatibilidad con API original
    def _load_available_sprites(self) -> List[str]:
        """Delegado a WorldCore para compatibilidad."""
        return self.core.available_sprites

    def _is_valid_position(
        self, x: float, y: float, existing_elements: List[Tile]
    ) -> bool:
        """Delegado a WorldValidator para compatibilidad."""
        return self.validator.is_valid_position(x, y, existing_elements)

    def _create_element_with_sprite(self, x: float, y: float) -> Optional[Tile]:
        """Delegado a WorldValidator para compatibilidad."""
        return self.validator.create_element_with_sprite(x, y)

    def _get_tile_type_from_filename(self, filename: str) -> TileType:
        """Delegado a WorldCore para compatibilidad."""
        return self.core.get_tile_type_from_filename(filename)
