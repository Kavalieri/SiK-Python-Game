#!/usr/bin/env python3
"""
Universal Asset Loader - Cargador universal de assets comprimidos
================================================================

Autor: SiK Team (Auto-generado)
Fecha: 2025-08-02
Descripción: Cargador universal para todos los tipos de assets del juego.
"""

import zipfile
import json
import pygame
from pathlib import Path
from typing import Optional
from io import BytesIO


class UniversalAssetLoader:
    """Cargador universal para todos los assets comprimidos del juego."""

    def __init__(self, assets_root: Path):
        """
        Inicializa el cargador universal.

        Args:
                assets_root: Ruta raíz de los assets
        """
        self.assets_root = assets_root
        self.loaded_assets = {}
        self.cache = {}

    def load_character(
        self, character_name: str, character_type: str = "player"
    ) -> Optional[dict]:
        """
        Carga un personaje desde assets/characters/players/ o assets/characters/enemies/.

        Args:
                character_name: Nombre del personaje
                character_type: Tipo de personaje ("player" o "enemy")

        Returns:
                Datos del personaje con animaciones
        """
        if character_type not in ["player", "enemy"]:
            character_type = "player"  # Default seguro

        category = f"characters/{character_type}s"  # players o enemies
        return self._load_zip_asset(category, character_name)

    def load_environment_elements(self) -> Optional[dict]:
        """Carga elementos del entorno."""
        return self._load_zip_asset("environment", "elements")

    def load_projectiles(self) -> Optional[dict]:
        """Carga proyectiles y explosiones."""
        return self._load_zip_asset("attack/ranged", "projectiles")

    def load_items(self, category: str) -> Optional[dict]:
        """
        Carga items por categoría.

        Args:
                category: weapons, armor, consumables, treasures
        """
        return self._load_zip_asset("items", category)

    def load_powerups(self) -> Optional[dict]:
        """Carga powerups."""
        return self._load_zip_asset("powerups", "powerups")

    def load_ui_elements(self, ui_type: str) -> Optional[dict]:
        """
        Carga elementos de UI.

        Args:
                ui_type: buttons, health_bars, inventory, icons
        """
        return self._load_zip_asset("ui", ui_type)

    def load_world_tiles(self) -> Optional[dict]:
        """Carga tiles del mundo."""
        return self._load_zip_asset("world", "tiles")

    def _load_zip_asset(self, category: str, asset_name: str) -> Optional[dict]:
        """
        Carga un asset desde un archivo zip.

        Args:
                category: Categoría del asset (characters, items, etc.)
                asset_name: Nombre del asset

        Returns:
                Datos del asset o None si hay error
        """
        cache_key = f"{category}/{asset_name}"

        if cache_key in self.loaded_assets:
            return self.loaded_assets[cache_key]

        zip_path = self.assets_root / category / f"{asset_name}.zip"

        if not zip_path.exists():
            print(f"❌ No se encontró: {zip_path}")
            return None

        try:
            asset_data = {
                "category": category,
                "name": asset_name,
                "manifest": {},
                "assets": {},
                "sprites": {},
            }

            with zipfile.ZipFile(zip_path, "r") as zf:
                # Cargar manifest
                if "manifest.json" in zf.namelist():
                    manifest_data = zf.read("manifest.json")
                    asset_data["manifest"] = json.loads(manifest_data.decode("utf-8"))

                # Cargar todos los archivos PNG
                for file_name in zf.namelist():
                    if file_name.endswith(".png"):
                        sprite_data = zf.read(file_name)
                        sprite_surface = pygame.image.load(BytesIO(sprite_data))
                        asset_data["sprites"][file_name] = sprite_surface

                # Organizar según el tipo de asset
                if category == "characters":
                    self._organize_character_animations(asset_data)
                elif category in ["attack/ranged", "environment"]:
                    self._organize_animations(asset_data)
                else:
                    self._organize_static_assets(asset_data)

            # Cachear asset cargado
            self.loaded_assets[cache_key] = asset_data

            print(
                f"✅ Asset cargado: {category}/{asset_name} ({len(asset_data['sprites'])} archivos)"
            )
            return asset_data

        except Exception as e:
            print(f"❌ Error cargando {category}/{asset_name}: {e}")
            return None

    def _organize_character_animations(self, asset_data: dict):
        """Organiza sprites de personajes en animaciones."""
        manifest = asset_data.get("manifest", {})
        animations = manifest.get("animations", {})

        asset_data["animations"] = {}

        for anim_type, filenames in animations.items():
            asset_data["animations"][anim_type] = []
            for filename in sorted(filenames):
                if filename in asset_data["sprites"]:
                    asset_data["animations"][anim_type].append(
                        asset_data["sprites"][filename]
                    )

    def _organize_animations(self, asset_data: dict):
        """Organiza sprites con animaciones (proyectiles, efectos)."""
        manifest = asset_data.get("manifest", {})
        animations = manifest.get("animations", {})

        asset_data["animations"] = {}

        for anim_type, filenames in animations.items():
            asset_data["animations"][anim_type] = []
            for filename in sorted(filenames):
                if filename in asset_data["sprites"]:
                    asset_data["animations"][anim_type].append(
                        asset_data["sprites"][filename]
                    )

    def _organize_static_assets(self, asset_data: dict):
        """Organiza assets estáticos (items, UI, etc.)."""
        # Para assets estáticos, mantener sprites tal como están
        asset_data["assets"] = asset_data["sprites"].copy()

    def get_character_animation_frames(
        self, character_name: str, animation_type: str, character_type: str = "player"
    ) -> list[pygame.Surface]:
        """
        Obtiene frames de una animación de personaje.

        Args:
                character_name: Nombre del personaje
                animation_type: Tipo de animación
                character_type: Tipo de personaje ("player" o "enemy")

        Returns:
                Lista de surfaces para la animación
        """
        character_data = self.load_character(character_name, character_type)
        if character_data and "animations" in character_data:
            return character_data["animations"].get(animation_type, [])
        return []

    def get_projectile_animation_frames(
        self, animation_type: str
    ) -> list[pygame.Surface]:
        """Obtiene frames de animación de proyectiles."""
        projectile_data = self.load_projectiles()
        if projectile_data and "animations" in projectile_data:
            return projectile_data["animations"].get(animation_type, [])
        return []

    def get_item_sprite(
        self, category: str, item_name: str
    ) -> Optional[pygame.Surface]:
        """
        Obtiene sprite de un item específico.

        Args:
                category: Categoría del item
                item_name: Nombre del archivo del item

        Returns:
                Surface del item o None
        """
        item_data = self.load_items(category)
        if item_data and "sprites" in item_data:
            return item_data["sprites"].get(item_name)
        return None

    def get_ui_sprite(
        self, ui_type: str, element_name: str
    ) -> Optional[pygame.Surface]:
        """Obtiene sprite de elemento de UI."""
        ui_data = self.load_ui_elements(ui_type)
        if ui_data and "sprites" in ui_data:
            return ui_data["sprites"].get(element_name)
        return None

    def get_tile_sprite(self, tile_name: str) -> Optional[pygame.Surface]:
        """Obtiene sprite de un tile del mundo."""
        tile_data = self.load_world_tiles()
        if tile_data and "sprites" in tile_data:
            return tile_data["sprites"].get(tile_name)
        return None

    def preload_category(self, category: str):
        """Pre-carga toda una categoría de assets."""
        if category == "characters":
            # Cargar personajes jugables
            players = ["adventureguirl", "robot", "guerrero"]
            for player in players:
                self.load_character(player, "player")

            # Cargar enemigos
            enemies = ["zombieguirl", "zombiemale"]
            for enemy in enemies:
                self.load_character(enemy, "enemy")
        elif category == "players":
            players = ["adventureguirl", "robot", "guerrero"]
            for player in players:
                self.load_character(player, "player")
        elif category == "enemies":
            enemies = ["zombieguirl", "zombiemale"]
            for enemy in enemies:
                self.load_character(enemy, "enemy")
        elif category == "items":
            item_categories = ["weapons", "armor", "consumables", "treasures"]
            for item_cat in item_categories:
                self.load_items(item_cat)
        elif category == "ui":
            ui_types = ["buttons", "health_bars"]
            for ui_type in ui_types:
                self.load_ui_elements(ui_type)
        else:
            print(f"⚠️ Categoría de pre-carga no reconocida: {category}")

    def clear_cache(self):
        """Limpia toda la cache de assets."""
        self.loaded_assets.clear()
        self.cache.clear()

    def get_memory_usage(self) -> dict:
        """Obtiene información de uso de memoria."""
        total_sprites = sum(
            len(asset_data.get("sprites", {}))
            for asset_data in self.loaded_assets.values()
        )
        loaded_categories = set(
            asset_data.get("category") for asset_data in self.loaded_assets.values()
        )

        return {
            "loaded_assets": len(self.loaded_assets),
            "total_sprites": total_sprites,
            "categories": list(loaded_categories),
            "assets_by_category": {
                category: [
                    key for key in self.loaded_assets.keys() if key.startswith(category)
                ]
                for category in loaded_categories
            },
        }

    def list_available_assets(self) -> dict:
        """Lista todos los assets disponibles por categoría."""
        available = {}

        # Buscar en cada categoría
        categories = [
            ("players", ["adventureguirl", "robot", "guerrero"]),
            ("enemies", ["zombieguirl", "zombiemale"]),
            ("items", ["weapons", "armor", "consumables", "treasures"]),
            ("ui", ["buttons", "health_bars"]),
            ("environment", ["elements"]),
            ("attack/ranged", ["projectiles"]),
            ("powerups", ["powerups"]),
            ("world", ["tiles"]),
        ]

        for category, expected_assets in categories:
            category_path = self.assets_root / category
            if category_path.exists():
                available[category] = []
                for asset_name in expected_assets:
                    zip_path = category_path / f"{asset_name}.zip"
                    if zip_path.exists():
                        available[category].append(asset_name)

        return available
