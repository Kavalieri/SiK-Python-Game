"""
Character Assets Loader - Carga de Configuración y Sprites Individuales
====================================================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Gestión de carga de configuración y sprites individuales de personajes.
"""

import json
import logging
from pathlib import Path
from typing import Any

import pygame

from .asset_loader import AssetLoader


class CharacterAssetsLoader:
    """Gestor de carga de configuración y sprites individuales."""

    def __init__(self, asset_loader: AssetLoader):
        """
        Inicializa el cargador de assets de personajes.

        Args:
            asset_loader: Instancia del cargador base de assets
        """
        self.asset_loader = asset_loader
        self.logger = logging.getLogger(__name__)
        self.animation_config = self._load_animation_config()

        self.logger.info("CharacterAssetsLoader inicializado")

    def _load_animation_config(self) -> dict[str, Any]:
        """
        Carga la configuración de animaciones desde config/animations.json.

        Returns:
            Diccionario con configuración de animaciones
        """
        config_path = Path("config/animations.json")

        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
                self.logger.info("Configuración de animaciones cargada exitosamente")
                return config
        except FileNotFoundError:
            self.logger.warning(
                "Archivo config/animations.json no encontrado, usando configuración vacía"
            )
        except json.JSONDecodeError as e:
            self.logger.error("Error al decodificar config/animations.json: %s", e)
        except OSError as e:
            self.logger.error(
                "Error de acceso al archivo config/animations.json: %s", e
            )

        # Fallback: estructura vacía
        self.logger.warning(
            "No se pudo cargar config/animations.json, usando configuración vacía."
        )
        return {"characters": {}, "sprite_paths": []}

    def get_character_sprite(
        self, character_name: str, animation: str, frame: int = 1, scale: float = 1.0
    ) -> pygame.Surface | None:
        """
        Obtiene un sprite de personaje específico.

        Args:
            character_name: Nombre del personaje
            animation: Tipo de animación
            frame: Número de frame
            scale: Factor de escala

        Returns:
            Superficie del sprite o None si falla
        """
        # Verificar si el personaje existe en la configuración
        if character_name not in self.animation_config["characters"]:
            self.logger.warning(
                "Personaje no encontrado en configuración: %s", character_name
            )
            return self.asset_loader.create_placeholder(64, 64, scale)

        # Leer escala personalizada si no se ha especificado un scale explícito
        if scale == 1.0:
            char_config = self.animation_config["characters"][character_name]
            scale = char_config.get("escala_sprite", 1.0)

        # Verificar si la animación existe para este personaje
        available_animations = self.animation_config["characters"][character_name][
            "animations"
        ]
        if animation not in available_animations:
            self.logger.warning(
                "Animación '%s' no disponible para %s. Disponibles: %s",
                animation,
                character_name,
                available_animations,
            )
            return self.asset_loader.create_placeholder(64, 64, scale)

        # Usar rutas desde config
        sprite_paths = self.animation_config.get(
            "sprite_paths",
            [
                "characters/used/{character}/{animation}_{frame}_.png",
                "characters/used/{character}/{animation}_{frame}.png",
                "characters/{character}/{animation}_{frame}_.png",
                "characters/{character}/{animation}_{frame}.png",
            ],
        )
        animation_capitalized = animation.capitalize()
        possible_paths = [
            path.format(
                character=character_name, animation=animation_capitalized, frame=frame
            )
            for path in sprite_paths
        ]

        for path in possible_paths:
            sprite = self.asset_loader.load_image(path, scale)
            if sprite and not self.asset_loader.is_placeholder_sprite(sprite):
                return sprite

        self.logger.warning(
            "Sprite no encontrado: %s/%s_%d, creando placeholder",
            character_name,
            animation_capitalized,
            frame,
        )
        return self.asset_loader.create_placeholder(64, 64, scale)

    def is_character_available(self, character_name: str) -> bool:
        """
        Verifica si un personaje está disponible en la configuración.

        Args:
            character_name: Nombre del personaje

        Returns:
            True si el personaje está disponible
        """
        return character_name in self.animation_config["characters"]

    def get_available_animations(self, character_name: str) -> list:
        """
        Obtiene las animaciones disponibles para un personaje.

        Args:
            character_name: Nombre del personaje

        Returns:
            Lista de animaciones disponibles
        """
        if not self.is_character_available(character_name):
            return []

        return self.animation_config["characters"][character_name].get("animations", [])

    def get_character_config(self, character_name: str) -> dict[str, Any]:
        """
        Obtiene la configuración completa de un personaje.

        Args:
            character_name: Nombre del personaje

        Returns:
            Diccionario con configuración del personaje
        """
        if not self.is_character_available(character_name):
            return {}

        return self.animation_config["characters"][character_name]
