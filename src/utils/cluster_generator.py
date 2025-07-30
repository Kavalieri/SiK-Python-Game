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
from typing import List, Optional

from ..entities.tile import Tile, TileType
from .world_core import WorldCore


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
            from .world_validator import WorldValidator

            validator = WorldValidator(self.world_core)
            element = validator.create_element_with_sprite(x, y)
            if element:
                elements.append(element)

        self.logger.debug(
            f"Cluster generado en ({center_x}, {center_y}) con {len(elements)} elementos"
        )
        return elements

    def generate_desert_oasis(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
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

        self.logger.info(f"Oasis generado con {len(oasis_elements)} elementos")
        return oasis_elements

    def generate_rock_formation(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera una formación de rocas."""
        rock_types = [TileType.ROCK, TileType.ALTAR, TileType.CRYSTAL]
        num_elements = random.randint(3, 8)
        rock_elements = self.generate_cluster(
            center_x, center_y, radius, num_elements, rock_types
        )
        self.logger.info(
            f"Formación de rocas generada con {len(rock_elements)} elementos"
        )
        return rock_elements

    def generate_cactus_field(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera un campo de cactus."""
        cactus_types = [TileType.TREE]  # Los cactus se mapean como TREE
        num_elements = random.randint(5, 12)
        cactus_elements = self.generate_cluster(
            center_x, center_y, radius, num_elements, cactus_types
        )
        self.logger.info(
            f"Campo de cactus generado con {len(cactus_elements)} elementos"
        )
        return cactus_elements

    def generate_ruins(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """Genera ruinas antiguas."""
        ruin_types = [TileType.ALTAR, TileType.CRYSTAL, TileType.ROCK]
        num_elements = random.randint(4, 10)
        ruin_elements = self.generate_cluster(
            center_x, center_y, radius, num_elements, ruin_types
        )
        self.logger.info(f"Ruinas generadas con {len(ruin_elements)} elementos")
        return ruin_elements
