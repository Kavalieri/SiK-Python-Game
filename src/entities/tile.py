"""
Tile System - Sistema de Tiles del Escenario
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de tiles para elementos del escenario como árboles, rocas, etc.
"""

import logging
import random
from enum import Enum
from typing import Optional

import pygame

from .entity import Entity, EntityStats, EntityType


class TileType(Enum):
    """Tipos de tiles disponibles."""

    TREE = "tree"
    ROCK = "rock"
    BUSH = "bush"
    FLOWER = "flower"
    CRYSTAL = "crystal"
    ALTAR = "altar"


class Tile(Entity):
    """
    Tile del escenario que decora el mundo.
    """

    # Configuración de tiles
    TILE_CONFIGS = {
        TileType.TREE: {
            "name": "Árbol",
            "width": 80,
            "height": 120,
            "color": (34, 139, 34),  # Verde bosque
            "collision": True,
            "symbol": "🌳",
        },
        TileType.ROCK: {
            "name": "Roca",
            "width": 60,
            "height": 40,
            "color": (105, 105, 105),  # Gris roca
            "collision": True,
            "symbol": "🪨",
        },
        TileType.BUSH: {
            "name": "Arbusto",
            "width": 50,
            "height": 60,
            "color": (0, 100, 0),  # Verde oscuro
            "collision": False,
            "symbol": "🌿",
        },
        TileType.FLOWER: {
            "name": "Flor",
            "width": 30,
            "height": 40,
            "color": (255, 20, 147),  # Rosa
            "collision": False,
            "symbol": "🌸",
        },
        TileType.CRYSTAL: {
            "name": "Cristal",
            "width": 40,
            "height": 60,
            "color": (0, 191, 255),  # Azul claro
            "collision": False,
            "symbol": "💎",
        },
        TileType.ALTAR: {
            "name": "Altar",
            "width": 100,
            "height": 80,
            "color": (139, 69, 19),  # Marrón
            "collision": True,
            "symbol": "🏛",
        },
    }

    def __init__(
        self,
        x: float,
        y: float,
        tile_type: TileType,
        sprite_name: Optional[str] = None,
    ):
        """
        Inicializa un tile.

        Args:
                x: Posición X
                y: Posición Y
                tile_type: Tipo de tile
        """
        config = self.TILE_CONFIGS[tile_type]

        # Crear estadísticas básicas
        stats = EntityStats(
            health=float("inf"),  # Los tiles no tienen vida
            max_health=float("inf"),
            speed=0.0,
            damage=0.0,
            armor=0.0,
            attack_speed=0.0,
            attack_range=0.0,
        )

        super().__init__(
            entity_type=EntityType.TILE,
            x=x,
            y=y,
            width=config["width"],
            height=config["height"],
            stats=stats,
        )

        self.tile_type = tile_type
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.sprite_name = sprite_name

        # Configurar sprite
        self._setup_sprite()

        self.logger.debug(f"Tile {tile_type.value} creado en ({x}, {y})")

    def _setup_sprite(self):
        """Configura el sprite del tile."""
        try:
            # Crear sprite con el color del tile
            self.sprite = pygame.Surface((self.width, self.height))
            self.sprite.fill(self.config["color"])

            # Añadir borde para definición
            border_color = tuple(max(0, c - 50) for c in self.config["color"])
            pygame.draw.rect(
                self.sprite, border_color, (0, 0, self.width, self.height), 2
            )

            # Añadir símbolo
            self._add_symbol()

        except Exception as e:
            self.logger.error(f"Error al crear sprite de tile: {e}")
            # Sprite por defecto
            self.sprite = pygame.Surface((self.width, self.height))
            self.sprite.fill((128, 128, 128))

    def _add_symbol(self):
        """Añade un símbolo al sprite según el tipo de tile."""
        try:
            font = pygame.font.Font(None, min(self.width, self.height) // 2)
            symbol = self.config["symbol"]
            text = font.render(symbol, True, (255, 255, 255))

            # Centrar el símbolo
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.sprite.blit(text, text_rect)
        except Exception as e:
            self.logger.warning(f"No se pudo añadir símbolo al tile: {e}")

    def _update_logic(self, delta_time: float):
        """Actualiza la lógica específica del tile."""
        # Los tiles son estáticos, no necesitan lógica de actualización
        pass

    def has_collision(self) -> bool:
        """
        Verifica si el tile tiene colisión.

        Returns:
                True si el tile bloquea el movimiento
        """
        return self.config["collision"]

    def get_tile_info(self) -> dict:
        """
        Obtiene información del tile.

        Returns:
                Dict con información del tile
        """
        return {
            "type": self.tile_type.value,
            "name": self.config["name"],
            "position": (self.x, self.y),
            "size": (self.width, self.height),
            "collision": self.config["collision"],
        }

    @classmethod
    def create_random(cls, x: float, y: float) -> "Tile":
        """
        Crea un tile aleatorio.

        Args:
                x: Posición X
                y: Posición Y

        Returns:
                Tile aleatorio
        """
        tile_type = random.choice(list(TileType))
        return cls(x, y, tile_type)

    @classmethod
    def get_all_types(cls) -> list:
        """Obtiene todos los tipos de tiles disponibles."""
        return list(TileType)
