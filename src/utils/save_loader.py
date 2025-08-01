"""
Save Loader - Carga y Gestión de Archivos
==========================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado en carga de archivos de guardado y gestión de información.
"""

import json
import logging
import pickle
import zlib
from pathlib import Path
from typing import Any

from .config_manager import ConfigManager


class SaveLoader:
    """
    Gestor especializado en carga de archivos de guardado.
    """

    def __init__(self, config: ConfigManager, encryption_handler):
        """
        Inicializa el cargador de archivos.

        Args:
            config: Configuración del juego
            encryption_handler: Manejador de encriptación
        """
        self.config = config
        self.encryption_handler = encryption_handler
        self.logger = logging.getLogger(__name__)

        # Configuración de guardado
        self.saves_path = Path(config.get("paths", "saves", "saves"))
        self.max_save_files = 3

        # Crear directorio si no existe
        self.saves_path.mkdir(parents=True, exist_ok=True)

    def load_save_files_info(self) -> list[dict[str, Any]]:
        """
        Carga la información de los archivos de guardado existentes.

        Returns:
            Lista con información de archivos de guardado
        """
        save_files = []

        for i in range(self.max_save_files):
            save_file = self.saves_path / f"save_{i + 1}.dat"
            save_info_file = self.saves_path / f"save_{i + 1}_info.json"

            save_info = {
                "file_number": i + 1,
                "file_path": str(save_file),
                "info_path": str(save_info_file),
                "exists": save_file.exists(),
                "last_used": None,
                "player_name": None,
                "level": 1,
                "score": 0,
                "play_time": 0,
            }

            if save_info_file.exists():
                try:
                    with open(save_info_file, encoding="utf-8") as f:
                        info_data = json.load(f)
                        save_info.update(info_data)
                except (OSError, json.JSONDecodeError, ValueError) as e:
                    self.logger.error(
                        "Error al cargar información del archivo %d: %s", i + 1, e
                    )

            save_files.append(save_info)

        return save_files

    def load_save_file(
        self, save_file_number: int, save_files: list[dict[str, Any]]
    ) -> dict[str, Any] | None:
        """
        Carga un archivo de guardado específico.

        Args:
            save_file_number: Número del archivo de guardado (1-3)
            save_files: Lista de información de archivos

        Returns:
            Datos del guardado o None si hay error
        """
        if not 1 <= save_file_number <= self.max_save_files:
            self.logger.error(
                "Número de archivo de guardado inválido: %d", save_file_number
            )
            return None

        save_info = save_files[save_file_number - 1]
        if not save_info["exists"]:
            self.logger.error("El archivo de guardado %d no existe", save_file_number)
            return None

        try:
            save_file = Path(save_info["file_path"])

            # Leer archivo cifrado
            with open(save_file, "rb") as f:
                encrypted_data = f.read()

            # Descifrar datos
            decrypted_data = self.encryption_handler.decrypt_data(encrypted_data)

            # Descomprimir y deserializar
            decompressed_data = zlib.decompress(decrypted_data)
            save_data = pickle.loads(decompressed_data)

            self.logger.info(
                "Archivo de guardado %d cargado correctamente", save_file_number
            )
            return save_data

        except (OSError, ValueError, KeyError) as e:
            self.logger.error(
                "Error al cargar archivo de guardado %d: %s", save_file_number, e
            )
            return None

    def get_last_save_file(self, save_files: list[dict[str, Any]]) -> int | None:
        """
        Obtiene el número del último archivo de guardado utilizado.

        Args:
            save_files: Lista de información de archivos

        Returns:
            Número del archivo de guardado o None si no hay ninguno
        """
        last_used = None
        last_timestamp = None

        for save_info in save_files:
            if save_info["exists"] and save_info["last_used"]:
                if last_timestamp is None or save_info["last_used"] > last_timestamp:
                    last_timestamp = save_info["last_used"]
                    last_used = save_info["file_number"]

        return last_used

    def export_save_debug(
        self, save_file_number: int, output_path: str, save_files: list[dict[str, Any]]
    ) -> bool:
        """
        Exporta un archivo de guardado en formato legible para debug.

        Args:
            save_file_number: Número del archivo de guardado
            output_path: Ruta donde guardar el archivo de debug
            save_files: Lista de información de archivos

        Returns:
            True si se exportó correctamente
        """
        save_data = self.load_save_file(save_file_number, save_files)
        if save_data is None:
            return False

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)

            self.logger.info(
                "Archivo de guardado %d exportado para debug: %s",
                save_file_number,
                output_path,
            )
            return True

        except (OSError, ValueError) as e:
            self.logger.error("Error al exportar archivo de guardado: %s", e)
            return False

    def has_save_file(self, save_files: list[dict[str, Any]]) -> bool:
        """
        Verifica si existe algún archivo de guardado.

        Args:
            save_files: Lista de información de archivos

        Returns:
            True si existe al menos un archivo de guardado
        """
        return any(save_info["exists"] for save_info in save_files)
