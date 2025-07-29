"""
World Generator - Generador de Mundo
==================================

Autor: SiK Team
Fecha: 2024
Descripción: Genera el mundo del juego con elementos distribuidos proceduralmente.
"""

import logging
import math
import os
import random
from typing import List, Optional

import pygame

from ..entities.tile import Tile, TileType


class WorldGenerator:
    """
    Generador de mundo que crea elementos distribuidos por el escenario.
    """

    def __init__(
        self, world_width: int, world_height: int, screen_width: int, screen_height: int
    ):
        """
        Inicializa el generador de mundo.

        Args:
                world_width: Ancho del mundo (3-4 veces la pantalla)
                world_height: Alto del mundo (3-4 veces la pantalla)
                screen_width: Ancho de la pantalla
                screen_height: Alto de la pantalla
        """
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)

        # Configuración de generación simplificada
        self.element_density = 0.00005  # Densidad muy baja
        self.min_distance = 300  # Distancia mínima entre elementos
        self.safe_zone_radius = 500  # Zona segura alrededor del centro

        # Cargar sprites disponibles
        self.available_sprites = self._load_available_sprites()

        self.logger.info(
            f"Generador de mundo inicializado - Mundo: {world_width}x{world_height}, Pantalla: {screen_width}x{screen_height}"
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
                self.logger.info(f"Cargados {len(sprites)} sprites de elementos")
            else:
                self.logger.warning(f"Directorio {elements_path} no encontrado")
        except Exception as e:
            self.logger.error(f"Error al cargar sprites: {e}")

        return sprites

    def generate_world(
        self, element_types: Optional[List[TileType]] = None
    ) -> List[Tile]:
        """
        Genera el mundo completo con elementos distribuidos.

        Returns:
                Lista de elementos generados
        """
        elements = []

        if element_types is None:
            element_types = []

        # Calcular número aproximado de elementos (baja densidad)
        total_area = self.world_width * self.world_height
        num_elements = int(total_area * self.element_density)

        self.logger.info(f"Generando {num_elements} elementos...")

        # Generar elementos
        attempts = 0
        max_attempts = num_elements * 20  # Evitar bucle infinito

        while len(elements) < num_elements and attempts < max_attempts:
            attempts += 1

            # Posición aleatoria
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)

            # Verificar zona segura (centro del mundo)
            center_x = self.world_width // 2
            center_y = self.world_height // 2
            distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

            if distance_to_center < self.safe_zone_radius:
                continue  # Saltar zona segura

            # Verificar distancia mínima con otros elementos
            if self._is_valid_position(x, y, elements):
                # Crear elemento con sprite real
                element = self._create_element_with_sprite(x, y)
                if element:
                    elements.append(element)

                    if len(elements) % 10 == 0:
                        self.logger.debug(f"Generados {len(elements)} elementos...")

        self.logger.info(f"Mundo generado con {len(elements)} elementos")
        return elements

    def _is_valid_position(
        self, x: float, y: float, existing_elements: List[Tile]
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
            if distance < self.min_distance:
                return False
        return True

    def _create_element_with_sprite(self, x: float, y: float) -> Optional[Tile]:
        """
        Crea un elemento usando sprites reales de assets/objects/elementos/.

        Args:
                x: Posición X
                y: Posición Y

        Returns:
                Elemento con sprite real o None si no se puede crear
        """
        if not self.available_sprites:
            # Fallback: crear elemento básico
            tile_type = random.choice(list(TileType))
            return Tile(x, y, tile_type)

        # Seleccionar sprite aleatorio
        sprite_filename = random.choice(self.available_sprites)
        sprite_path = f"assets/objects/elementos/{sprite_filename}"

        try:
            # Cargar sprite
            sprite = pygame.image.load(sprite_path).convert_alpha()

            # Determinar tipo de elemento basado en el nombre del archivo
            tile_type = self._get_tile_type_from_filename(sprite_filename)

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
            # Los elementos se crean con el tipo correcto, la colisión se maneja en el método has_collision()

            return element

        except Exception as e:
            self.logger.warning(f"No se pudo cargar sprite {sprite_filename}: {e}")
            # Fallback: crear elemento básico
            tile_type = random.choice(list(TileType))
            return Tile(x, y, tile_type)

    def _get_tile_type_from_filename(self, filename: str) -> TileType:
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

    def generate_cluster(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        num_elements: int,
        element_types: List[TileType] = None,
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
            x = max(0, min(self.world_width, x))
            y = max(0, min(self.world_height, y))

            # Crear elemento
            element = self._create_element_with_sprite(x, y)
            if element:
                elements.append(element)

        self.logger.debug(
            f"Cluster generado en ({center_x}, {center_y}) con {len(elements)} elementos"
        )
        return elements

    def generate_desert_oasis(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """
        Genera un oasis en el desierto.

        Args:
                center_x: Centro X del oasis
                center_y: Centro Y del oasis
                radius: Radio del oasis

        Returns:
                Lista de elementos del oasis
        """
        oasis_elements = [TileType.TREE, TileType.BUSH, TileType.FLOWER]
        return self.generate_cluster(center_x, center_y, radius, 15, oasis_elements)

    def generate_rock_formation(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """
        Genera una formación de rocas.

        Args:
                center_x: Centro X de la formación
                center_y: Centro Y de la formación
                radius: Radio de la formación

        Returns:
                Lista de elementos de la formación
        """
        return self.generate_cluster(center_x, center_y, radius, 8, [TileType.ROCK])

    def generate_cactus_field(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """
        Genera un campo de cactus.

        Args:
                center_x: Centro X del campo
                center_y: Centro Y del campo
                radius: Radio del campo

        Returns:
                Lista de elementos del campo
        """
        return self.generate_cluster(center_x, center_y, radius, 12, [TileType.TREE])

    def generate_ruins(
        self, center_x: float, center_y: float, radius: float
    ) -> List[Tile]:
        """
        Genera ruinas antiguas.

        Args:
                center_x: Centro X de las ruinas
                center_y: Centro Y de las ruinas
                radius: Radio de las ruinas

        Returns:
                Lista de elementos de las ruinas
        """
        ruins_elements = [TileType.ALTAR, TileType.CRYSTAL, TileType.ROCK]
        return self.generate_cluster(center_x, center_y, radius, 10, ruins_elements)
