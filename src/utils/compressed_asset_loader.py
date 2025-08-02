#!/usr/bin/env python3
"""
Compressed Asset Loader - Cargador de assets comprimidos
=======================================================

Autor: SiK Team (Auto-generado)
Fecha: 2025-01-16
Descripción: Carga assets de personajes desde archivos zip.
"""

import zipfile
import json
import pygame
from pathlib import Path
from typing import Optional
from io import BytesIO


class CompressedAssetLoader:
    """Cargador optimizado para assets comprimidos."""

    def __init__(self, compressed_path: Path):
        """
        Inicializa el cargador de assets.

        Args:
            compressed_path: Ruta al directorio de assets comprimidos
        """
        self.compressed_path = compressed_path
        self.loaded_characters = {}
        self.cache = {}

    def load_character(self, character_name: str) -> Optional[dict]:
        """
        Carga un personaje desde su archivo zip.

        Args:
            character_name: Nombre del personaje a cargar

        Returns:
            Diccionario con animaciones y manifest, o None si hay error
        """
        if character_name in self.loaded_characters:
            return self.loaded_characters[character_name]

        zip_path = self.compressed_path / f"{character_name}.zip"

        if not zip_path.exists():
            print(f"❌ No se encontró zip para personaje: {character_name}")
            return None

        try:
            character_data = {"animations": {}, "manifest": {}, "sprites": {}}

            with zipfile.ZipFile(zip_path, "r") as zf:
                # Cargar manifest
                manifest_data = zf.read("manifest.json")
                character_data["manifest"] = json.loads(manifest_data.decode("utf-8"))

                # Cargar sprites por animación
                for anim_type, filenames in character_data["manifest"][
                    "animations"
                ].items():
                    character_data["animations"][anim_type] = []

                    for filename in sorted(
                        filenames
                    ):  # Ordenar para secuencia correcta
                        sprite_data = zf.read(filename)

                        # Convertir bytes a Surface de pygame
                        sprite_surface = pygame.image.load(BytesIO(sprite_data))
                        character_data["sprites"][filename] = sprite_surface
                        character_data["animations"][anim_type].append(sprite_surface)

            # Cachear personaje cargado
            self.loaded_characters[character_name] = character_data

            print(
                f"✅ Personaje cargado: {character_name} ({len(character_data['sprites'])} sprites)"
            )
            return character_data

        except Exception as e:
            print(f"❌ Error cargando personaje {character_name}: {e}")
            return None

    def get_animation_frames(
        self, character_name: str, animation_type: str
    ) -> list[pygame.Surface]:
        """
        Obtiene frames de una animación específica.

        Args:
            character_name: Nombre del personaje
            animation_type: Tipo de animación (idle, run, attack, etc.)

        Returns:
            Lista de surfaces de pygame para la animación
        """
        character_data = self.load_character(character_name)
        if not character_data:
            return []

        return character_data["animations"].get(animation_type, [])

    def preload_character(self, character_name: str):
        """Pre-carga un personaje en memoria para acceso rápido."""
        self.load_character(character_name)

    def get_character_info(self, character_name: str) -> Optional[dict]:
        """Obtiene información del manifest de un personaje."""
        character_data = self.load_character(character_name)
        if character_data:
            return character_data["manifest"]
        return None

    def clear_cache(self):
        """Limpia el cache de personajes cargados."""
        self.loaded_characters.clear()
        self.cache.clear()

    def get_memory_usage(self) -> dict:
        """Obtiene información de uso de memoria."""
        total_sprites = sum(
            len(char_data["sprites"]) for char_data in self.loaded_characters.values()
        )
        loaded_chars = len(self.loaded_characters)

        return {
            "loaded_characters": loaded_chars,
            "total_sprites": total_sprites,
            "cached_characters": list(self.loaded_characters.keys()),
        }
