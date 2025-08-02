#!/usr/bin/env python3
"""
Cargador de Assets de Characters Separado
=========================================

Autor: SiK Team (Auto-generado)
Fecha: 2025-08-02
Descripción: Sistema de carga para players y enemies separados.
"""

import json
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, List
import pygame


class CharacterAssetLoader:
    """Cargador especializado para assets de personajes separados por tipo."""

    def __init__(self, assets_root: Path) -> None:
        """
        Inicializa el cargador de assets de personajes.

        Args:
                assets_root: Ruta raíz a la carpeta assets
        """
        self.assets_root = assets_root
        self.characters_root = assets_root / "characters"
        self.players_root = self.characters_root / "players"
        self.enemies_root = self.characters_root / "enemies"

        # Cache para evitar cargas repetidas
        self._player_cache: Dict[str, Dict[str, Any]] = {}
        self._enemy_cache: Dict[str, Dict[str, Any]] = {}

    def get_available_players(self) -> List[str]:
        """Obtiene lista de personajes jugables disponibles."""
        if not self.players_root.exists():
            return []

        players = []
        for zip_file in self.players_root.glob("*.zip"):
            players.append(zip_file.stem)

        return sorted(players)

    def get_available_enemies(self) -> List[str]:
        """Obtiene lista de enemigos disponibles."""
        if not self.enemies_root.exists():
            return []

        enemies = []
        for zip_file in self.enemies_root.glob("*.zip"):
            enemies.append(zip_file.stem)

        return sorted(enemies)

    def load_player(self, player_name: str) -> Optional[Dict[str, Any]]:
        """
        Carga un personaje jugable.

        Args:
                player_name: Nombre del personaje jugable

        Returns:
                Diccionario con datos del personaje o None si falla
        """
        if player_name in self._player_cache:
            return self._player_cache[player_name]

        zip_path = self.players_root / f"{player_name}.zip"
        if not zip_path.exists():
            return None

        player_data = self._load_character_from_zip(zip_path)
        if player_data:
            player_data["type"] = "player"
            self._player_cache[player_name] = player_data

        return player_data

    def load_enemy(self, enemy_name: str) -> Optional[Dict[str, Any]]:
        """
        Carga un enemigo.

        Args:
                enemy_name: Nombre del enemigo

        Returns:
                Diccionario con datos del enemigo o None si falla
        """
        if enemy_name in self._enemy_cache:
            return self._enemy_cache[enemy_name]

        zip_path = self.enemies_root / f"{enemy_name}.zip"
        if not zip_path.exists():
            return None

        enemy_data = self._load_character_from_zip(zip_path)
        if enemy_data:
            enemy_data["type"] = "enemy"
            self._enemy_cache[enemy_name] = enemy_data

        return enemy_data

    def _load_character_from_zip(self, zip_path: Path) -> Optional[Dict[str, Any]]:
        """
        Carga un personaje desde un archivo ZIP.

        Args:
                zip_path: Ruta al archivo ZIP del personaje

        Returns:
                Diccionario con datos del personaje
        """
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Leer manifest
                manifest_data = zip_ref.read("manifest.json")
                manifest = json.loads(manifest_data.decode("utf-8"))

                # Cargar sprites por animación
                animations = {}
                for animation_name, animation_info in manifest.get(
                    "animations", {}
                ).items():
                    frames = []
                    for frame_file in animation_info.get("frames", []):
                        frame_data = zip_ref.read(frame_file)
                        # Crear surface de pygame desde los datos
                        surface = pygame.image.load_extended(
                            pygame.io.BytesIO(frame_data)
                        )
                        frames.append(surface)

                    animations[animation_name] = {
                        "frames": frames,
                        "frame_count": len(frames),
                        "duration": animation_info.get("duration", 100),
                    }

                return {
                    "name": manifest.get("name", zip_path.stem),
                    "animations": animations,
                    "metadata": manifest.get("metadata", {}),
                    "stats": manifest.get("stats", {}),
                }

        except Exception as e:
            print(f"Error cargando personaje desde {zip_path}: {e}")
            return None

    def preload_all_players(self) -> None:
        """Precarga todos los personajes jugables disponibles."""
        for player_name in self.get_available_players():
            self.load_player(player_name)

    def preload_all_enemies(self) -> None:
        """Precarga todos los enemigos disponibles."""
        for enemy_name in self.get_available_enemies():
            self.load_enemy(enemy_name)

    def clear_cache(self) -> None:
        """Limpia la caché de personajes cargados."""
        self._player_cache.clear()
        self._enemy_cache.clear()

    def get_character_info(self) -> Dict[str, Any]:
        """
        Obtiene información resumida de todos los personajes.

        Returns:
                Diccionario con información de players y enemies
        """
        return {
            "players": {
                "available": self.get_available_players(),
                "count": len(self.get_available_players()),
            },
            "enemies": {
                "available": self.get_available_enemies(),
                "count": len(self.get_available_enemies()),
            },
            "total": len(self.get_available_players())
            + len(self.get_available_enemies()),
        }
