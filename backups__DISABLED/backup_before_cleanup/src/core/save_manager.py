"""
Save Manager - Gestor de Guardado
===============================

Autor: SiK Team
Fecha: 2024
Descripción: Gestor para guardar y cargar partidas del juego.
"""

import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path


class SaveManager:
    """
    Gestor de guardado y carga de partidas.
    """

    def __init__(self, save_directory: str = "saves"):
        """
        Inicializa el gestor de guardado.

        Args:
                save_directory: Directorio donde guardar las partidas
        """
        self.logger = logging.getLogger(__name__)
        self.save_directory = Path(save_directory)

        # Crear directorio de guardado si no existe
        self.save_directory.mkdir(exist_ok=True)

        self.logger.info(f"Gestor de guardado inicializado en: {self.save_directory}")

    def save_game(self, game_data: Dict[str, Any], slot: int = 1) -> bool:
        """
        Guarda una partida en el slot especificado.

        Args:
                game_data: Datos del juego a guardar
                slot: Número de slot (1-3)

        Returns:
                True si se guardó correctamente, False en caso contrario
        """
        try:
            # Validar slot
            if slot < 1 or slot > 3:
                self.logger.error(f"Slot inválido: {slot}. Debe ser entre 1 y 3.")
                return False

            # Crear nombre de archivo
            save_file = self.save_directory / f"save_slot_{slot}.json"

            # Añadir metadatos
            save_data = {
                "metadata": {
                    "version": "1.0.0",
                    "slot": slot,
                    "timestamp": self._get_timestamp(),
                },
                "game_data": game_data,
            }

            # Guardar archivo
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Partida guardada en slot {slot}: {save_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error al guardar partida en slot {slot}: {e}")
            return False

    def load_game(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Carga una partida del slot especificado.

        Args:
                slot: Número de slot (1-3)

        Returns:
                Datos del juego o None si no se pudo cargar
        """
        try:
            # Validar slot
            if slot < 1 or slot > 3:
                self.logger.error(f"Slot inválido: {slot}. Debe ser entre 1 y 3.")
                return None

            # Crear nombre de archivo
            save_file = self.save_directory / f"save_slot_{slot}.json"

            # Verificar si existe
            if not save_file.exists():
                self.logger.warning(f"No existe partida guardada en slot {slot}")
                return None

            # Cargar archivo
            with open(save_file, "r", encoding="utf-8") as f:
                save_data = json.load(f)

            # Verificar versión
            version = save_data.get("metadata", {}).get("version", "unknown")
            if version != "1.0.0":
                self.logger.warning(f"Versión de guardado diferente: {version}")

            self.logger.info(f"Partida cargada del slot {slot}: {save_file}")
            return save_data.get("game_data", {})

        except Exception as e:
            self.logger.error(f"Error al cargar partida del slot {slot}: {e}")
            return None

    def delete_save(self, slot: int) -> bool:
        """
        Elimina una partida guardada.

        Args:
                slot: Número de slot (1-3)

        Returns:
                True si se eliminó correctamente, False en caso contrario
        """
        try:
            # Validar slot
            if slot < 1 or slot > 3:
                self.logger.error(f"Slot inválido: {slot}. Debe ser entre 1 y 3.")
                return False

            # Crear nombre de archivo
            save_file = self.save_directory / f"save_slot_{slot}.json"

            # Verificar si existe
            if not save_file.exists():
                self.logger.warning(f"No existe partida guardada en slot {slot}")
                return False

            # Eliminar archivo
            save_file.unlink()

            self.logger.info(f"Partida eliminada del slot {slot}")
            return True

        except Exception as e:
            self.logger.error(f"Error al eliminar partida del slot {slot}: {e}")
            return False

    def get_save_info(self, slot: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de una partida guardada sin cargarla completamente.

        Args:
                slot: Número de slot (1-3)

        Returns:
                Información de la partida o None si no existe
        """
        try:
            # Validar slot
            if slot < 1 or slot > 3:
                return None

            # Crear nombre de archivo
            save_file = self.save_directory / f"save_slot_{slot}.json"

            # Verificar si existe
            if not save_file.exists():
                return None

            # Cargar solo metadatos
            with open(save_file, "r", encoding="utf-8") as f:
                save_data = json.load(f)

            metadata = save_data.get("metadata", {})
            game_data = save_data.get("game_data", {})

            # Extraer información relevante
            info = {
                "slot": slot,
                "timestamp": metadata.get("timestamp", "Unknown"),
                "version": metadata.get("version", "Unknown"),
                "player_name": game_data.get("player_name", "Unknown"),
                "score": game_data.get("score", 0),
                "level": game_data.get("level", 1),
                "lives": game_data.get("lives", 3),
                "character": game_data.get("selected_character", "Unknown"),
            }

            return info

        except Exception as e:
            self.logger.error(f"Error al obtener información del slot {slot}: {e}")
            return None

    def list_saves(self) -> Dict[int, Optional[Dict[str, Any]]]:
        """
        Lista todas las partidas guardadas.

        Returns:
                Diccionario con información de cada slot
        """
        saves = {}

        for slot in range(1, 4):
            saves[slot] = self.get_save_info(slot)

        return saves

    def has_save(self, slot: int) -> bool:
        """
        Verifica si existe una partida guardada en el slot especificado.

        Args:
                slot: Número de slot (1-3)

        Returns:
                True si existe, False en caso contrario
        """
        if slot < 1 or slot > 3:
            return False

        save_file = self.save_directory / f"save_slot_{slot}.json"
        return save_file.exists()

    def _get_timestamp(self) -> str:
        """
        Obtiene la marca de tiempo actual.

        Returns:
                Marca de tiempo en formato string
        """
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
