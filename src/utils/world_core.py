"""
World Core - Núcleo del generador de mundo
=========================================

Autor: SiK Team
Fecha: 2024
Descripción: Núcleo del sistema de generación de mundo con configuración base.
"""

import logging
import os
import random
from typing import List

from ..entities.tile import TileType


class WorldCore:
    """
    Núcleo del sistema de generación de mundo con configuración base.
    """

    def __init__(
        self, world_width: int, world_height: int, screen_width: int, screen_height: int
    ):
        """
        Inicializa el núcleo del generador de mundo.

        Args:
            world_width: Ancho del mundo (3-4 veces la pantalla)
            world_height: Alto del mundo (3-4 veces la pantalla)
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        self.logger = logging.getLogger(__name__)

        # Dimensiones del mundo
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Configuración de generación
        self.element_density = (
            0.0001  # Elementos por píxel cuadrado (muy baja densidad)
        )
        self.min_distance = 100  # Distancia mínima entre elementos
        self.safe_zone_radius = 300  # Radio libre alrededor del centro

        # Sprites disponibles
        self.available_sprites = self._load_available_sprites()

        self.logger.info(
            "WorldCore inicializado: %sx%s, sprites: %s",
            world_width,
            world_height,
            len(self.available_sprites),
        )

    def _load_available_sprites(self) -> List[str]:
        """
        Carga los sprites disponibles de assets/objects/elementos/.

        Returns:
            Lista de nombres de archivos de sprites disponibles
        """
        sprites = []
        elements_path = "assets/objects/elementos"

        try:
            if os.path.exists(elements_path):
                for filename in os.listdir(elements_path):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                        sprites.append(filename)
                self.logger.info("Cargados %s sprites de elementos", len(sprites))
            else:
                self.logger.warning("Directorio %s no encontrado", elements_path)
        except (OSError, IOError, PermissionError) as e:
            self.logger.error("Error al cargar sprites: %s", e)

        return sprites

    def get_tile_type_from_filename(self, filename: str) -> TileType:
        """
        Determina el tipo de tile basado en el nombre del archivo.

        Args:
            filename: Nombre del archivo

        Returns:
            Tipo de tile correspondiente
        """
        filename_lower = filename.lower()

        if "cactus" in filename_lower:
            return TileType.TREE
        elif "bush" in filename_lower:
            return TileType.BUSH
        elif "grass" in filename_lower:
            return TileType.FLOWER
        elif "stone" in filename_lower or "rock" in filename_lower:
            return TileType.ROCK
        elif "crate" in filename_lower:
            return TileType.ALTAR
        elif "skeleton" in filename_lower:
            return TileType.CRYSTAL
        elif "sign" in filename_lower:
            return TileType.ALTAR
        elif "tree" in filename_lower:
            return TileType.TREE
        else:
            # Por defecto, asignar aleatoriamente
            return random.choice(list(TileType))

    def calculate_total_elements(self) -> int:
        """
        Calcula el número total de elementos a generar.

        Returns:
            Número de elementos basado en el área y densidad
        """
        total_area = self.world_width * self.world_height
        return int(total_area * self.element_density)

    def is_in_safe_zone(self, x: float, y: float) -> bool:
        """
        Verifica si una posición está en la zona segura (centro del mundo).

        Args:
            x: Posición X
            y: Posición Y

        Returns:
            True si está en zona segura
        """
        center_x = self.world_width // 2
        center_y = self.world_height // 2
        distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        return distance_to_center < self.safe_zone_radius

    def clamp_to_world(self, x: float, y: float) -> tuple[float, float]:
        """
        Mantiene las coordenadas dentro de los límites del mundo.

        Args:
            x: Posición X
            y: Posición Y

        Returns:
            Coordenadas ajustadas (x, y)
        """
        x = max(0, min(self.world_width, x))
        y = max(0, min(self.world_height, y))
        return x, y
