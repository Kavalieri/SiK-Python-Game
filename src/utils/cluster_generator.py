"""
Cluster Generator - Generador de clusters de elementos
=====================================================

Autor: SiK Team
Fecha: 2024
Descripción: Genera clusters específicos de elementos del mundo.
"""

import logging
import math
import random

from ..entities.tile import Tile, TileType
from .world_core import WorldCore
from .world_validator import WorldValidator


class ClusterGenerator:
    """
    Generador de clusters específicos de elementos del mundo.
    """

    def __init__(self, world_core: WorldCore):
        """
        Inicializa el generador de clusters.

        Args:
            world_core: Núcleo del sistema de mundo
        """
        self.world_core = world_core
        self.logger = logging.getLogger(__name__)

    def generate_cluster(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        num_elements: int,
        element_types: list[TileType] | None = None,
    ) -> list[Tile]:
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
        elements = []

        if element_types is None:
            element_types = list(TileType)

        for _ in range(num_elements):
            # Posición aleatoria dentro del radio
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, radius)

            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)

            # Mantener dentro de los límites del mundo
            x, y = self.world_core.clamp_to_world(x, y)

            # Crear elemento
            validator = WorldValidator(self.world_core)
            element = validator.create_element_with_sprite(x, y)
            if element:
                elements.append(element)

        self.logger.debug(
            "Cluster generado en (%s, %s) con %s elementos",
            center_x,
            center_y,
            len(elements),
        )
        return elements

    def generate_desert_oasis(
        self, center_x: float, center_y: float, radius: float
    ) -> list[Tile]:
        """Genera un oasis en el desierto."""
        oasis_elements = []
        oasis_types = [TileType.TREE, TileType.FLOWER, TileType.BUSH]

        # Generar más elementos cerca del centro
        for ring in range(3):
            ring_radius = radius * (ring + 1) / 3
            num_elements = max(1, 8 - ring * 2)
            cluster_elements = self.generate_cluster(
                center_x, center_y, ring_radius, num_elements, oasis_types
            )
            oasis_elements.extend(cluster_elements)

        self.logger.info("Oasis generado con %s elementos", len(oasis_elements))
        return oasis_elements

    def generate_rock_formation(
        self, center_x: float, center_y: float, radius: float
    ) -> list[Tile]:
        """Genera una formación de rocas."""
        rock_types = [TileType.ROCK, TileType.ALTAR, TileType.CRYSTAL]
        num_elements = random.randint(3, 8)
        rock_elements = self.generate_cluster(
            center_x, center_y, radius, num_elements, rock_types
        )
        self.logger.info(
            "Formación de rocas generada con %s elementos", len(rock_elements)
        )
        return rock_elements

    def generate_cactus_field(
        self, center_x: float, center_y: float, radius: float
    ) -> list[Tile]:
        """Genera un campo de cactus."""
        cactus_types = [TileType.TREE]  # Los cactus se mapean como TREE
        num_elements = random.randint(5, 12)
        cactus_elements = self.generate_cluster(
            center_x, center_y, radius, num_elements, cactus_types
        )
        self.logger.info(
            "Campo de cactus generado con %s elementos", len(cactus_elements)
        )
        return cactus_elements

    def generate_ruins(
        self, center_x: float, center_y: float, radius: float
    ) -> list[Tile]:
        """Genera ruinas antiguas."""
        ruin_types = [TileType.ALTAR, TileType.CRYSTAL, TileType.ROCK]
        num_elements = random.randint(4, 10)
        ruin_elements = self.generate_cluster(
            center_x, center_y, radius, num_elements, ruin_types
        )
        self.logger.info("Ruinas generadas con %s elementos", len(ruin_elements))
        return ruin_elements
