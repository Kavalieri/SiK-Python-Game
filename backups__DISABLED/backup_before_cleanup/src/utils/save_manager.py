"""
Save Manager - Gestor de Guardado
================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de guardado con cifrado y gestión de archivos de partida.
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import pickle
import zlib

from .config_manager import ConfigManager
# Importación diferida para evitar importación circular
# from ..core.game_state import GameState


class SaveManager:
    """
    Gestiona el sistema de guardado del juego con cifrado y múltiples archivos.
    """

    def __init__(self, config: ConfigManager):
        """
        Inicializa el gestor de guardado.

        Args:
                config: Configuración del juego
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Configuración de guardado
        self.saves_path = Path(config.get("paths", "saves", "saves"))
        self.max_save_files = 3
        self.encryption_key = self._generate_encryption_key()

        # Crear directorio de guardados si no existe
        self.saves_path.mkdir(parents=True, exist_ok=True)

        # Información de archivos de guardado
        self.save_files = self._load_save_files_info()
        self.current_save_file = None

        self.logger.info(f"Gestor de guardado inicializado en: {self.saves_path}")

    def _generate_encryption_key(self) -> str:
        """
        Genera una clave de cifrado basada en la configuración del juego.

        Returns:
                Clave de cifrado
        """
        # Usar información del juego para generar una clave única
        game_title = self.config.get("game", "title", "SiK Python Game")
        version = self.config.get("game", "version", "0.1.0")

        key_string = f"{game_title}_{version}_save_key"
        return hashlib.sha256(key_string.encode()).hexdigest()[:32]

    def _load_save_files_info(self) -> List[Dict[str, Any]]:
        """
        Carga la información de los archivos de guardado existentes.

        Returns:
                Lista con información de archivos de guardado
        """
        save_files = []

        for i in range(self.max_save_files):
            save_file = self.saves_path / f"save_{i+1}.dat"
            save_info_file = self.saves_path / f"save_{i+1}_info.json"

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
                    with open(save_info_file, "r", encoding="utf-8") as f:
                        info_data = json.load(f)
                        save_info.update(info_data)
                except Exception as e:
                    self.logger.error(
                        f"Error al cargar información del archivo {i+1}: {e}"
                    )

            save_files.append(save_info)

        return save_files

    def get_save_files_info(self) -> List[Dict[str, Any]]:
        """
        Obtiene información de todos los archivos de guardado.

        Returns:
                Lista con información de archivos de guardado
        """
        return self.save_files.copy()

    def create_new_save(self, save_file_number: int) -> bool:
        """
        Crea un nuevo archivo de guardado.

        Args:
                save_file_number: Número del archivo de guardado (1-3)

        Returns:
                True si se creó correctamente
        """
        if not 1 <= save_file_number <= self.max_save_files:
            self.logger.error(
                f"Número de archivo de guardado inválido: {save_file_number}"
            )
            return False

        # Verificar si el archivo ya existe
        save_info = self.save_files[save_file_number - 1]
        if save_info["exists"]:
            self.logger.warning(f"El archivo de guardado {save_file_number} ya existe")
            return False

        self.current_save_file = save_file_number
        self.logger.info(f"Nuevo archivo de guardado creado: {save_file_number}")
        return True

    def load_save(self, save_file_number: int) -> Optional[Dict[str, Any]]:
        """
        Carga un archivo de guardado.

        Args:
                save_file_number: Número del archivo de guardado (1-3)

        Returns:
                Datos del guardado o None si hay error
        """
        if not 1 <= save_file_number <= self.max_save_files:
            self.logger.error(
                f"Número de archivo de guardado inválido: {save_file_number}"
            )
            return None

        save_info = self.save_files[save_file_number - 1]
        if not save_info["exists"]:
            self.logger.error(f"El archivo de guardado {save_file_number} no existe")
            return None

        try:
            save_file = Path(save_info["file_path"])

            # Leer archivo cifrado
            with open(save_file, "rb") as f:
                encrypted_data = f.read()

            # Descifrar datos
            decrypted_data = self._decrypt_data(encrypted_data)

            # Descomprimir y deserializar
            decompressed_data = zlib.decompress(decrypted_data)
            save_data = pickle.loads(decompressed_data)

            self.current_save_file = save_file_number
            self.logger.info(
                f"Archivo de guardado {save_file_number} cargado correctamente"
            )

            return save_data

        except Exception as e:
            self.logger.error(
                f"Error al cargar archivo de guardado {save_file_number}: {e}"
            )
            return None

    def save_game(self, game_state, additional_data: Dict[str, Any] = None) -> bool:
        """
        Guarda el estado del juego.

        Args:
                game_state: Estado del juego a guardar
                additional_data: Datos adicionales a guardar

        Returns:
                True si se guardó correctamente
        """
        if self.current_save_file is None:
            self.logger.error("No hay archivo de guardado seleccionado")
            return False

        try:
            # Preparar datos para guardar
            save_data = {
                "game_state": game_state.get_state_dict(),
                "additional_data": additional_data or {},
                "save_timestamp": datetime.now().isoformat(),
                "game_version": self.config.get("game", "version", "0.1.0"),
            }

            # Serializar y comprimir datos
            serialized_data = pickle.dumps(save_data)
            compressed_data = zlib.compress(serialized_data)

            # Cifrar datos
            encrypted_data = self._encrypt_data(compressed_data)

            # Guardar archivo cifrado
            save_info = self.save_files[self.current_save_file - 1]
            save_file = Path(save_info["file_path"])

            with open(save_file, "wb") as f:
                f.write(encrypted_data)

            # Actualizar información del archivo
            self._update_save_info(save_info, game_state)

            # Guardar información del archivo
            info_file = Path(save_info["info_path"])
            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(save_info, f, indent=4, ensure_ascii=False)

            self.logger.info(f"Juego guardado en archivo {self.current_save_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error al guardar el juego: {e}")
            return False

    def _update_save_info(self, save_info: Dict[str, Any], game_state):
        """
        Actualiza la información del archivo de guardado.

        Args:
                save_info: Información del archivo de guardado
                game_state: Estado del juego
        """
        save_info["exists"] = True
        save_info["last_used"] = datetime.now().isoformat()
        save_info["player_name"] = game_state.player_name
        save_info["level"] = game_state.level
        save_info["score"] = game_state.score
        save_info["play_time"] = getattr(game_state, "play_time", 0)

    def delete_save(self, save_file_number: int) -> bool:
        """
        Elimina un archivo de guardado.

        Args:
                save_file_number: Número del archivo de guardado (1-3)

        Returns:
                True si se eliminó correctamente
        """
        if not 1 <= save_file_number <= self.max_save_files:
            self.logger.error(
                f"Número de archivo de guardado inválido: {save_file_number}"
            )
            return False

        save_info = self.save_files[save_file_number - 1]
        if not save_info["exists"]:
            self.logger.warning(f"El archivo de guardado {save_file_number} no existe")
            return False

        try:
            # Eliminar archivo de guardado
            save_file = Path(save_info["file_path"])
            if save_file.exists():
                save_file.unlink()

            # Eliminar archivo de información
            info_file = Path(save_info["info_path"])
            if info_file.exists():
                info_file.unlink()

            # Resetear información
            save_info["exists"] = False
            save_info["last_used"] = None
            save_info["player_name"] = None
            save_info["level"] = 1
            save_info["score"] = 0
            save_info["play_time"] = 0

            # Si era el archivo actual, deseleccionarlo
            if self.current_save_file == save_file_number:
                self.current_save_file = None

            self.logger.info(f"Archivo de guardado {save_file_number} eliminado")
            return True

        except Exception as e:
            self.logger.error(
                f"Error al eliminar archivo de guardado {save_file_number}: {e}"
            )
            return False

    def _encrypt_data(self, data: bytes) -> bytes:
        """
        Cifra los datos usando la clave de cifrado.

        Args:
                data: Datos a cifrar

        Returns:
                Datos cifrados
        """
        # Implementación simple de cifrado XOR
        # En producción, usar una biblioteca de cifrado más robusta
        key_bytes = self.encryption_key.encode()
        encrypted = bytearray()

        for i, byte in enumerate(data):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted.append(byte ^ key_byte)

        return bytes(encrypted)

    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Descifra los datos usando la clave de cifrado.

        Args:
                encrypted_data: Datos cifrados

        Returns:
                Datos descifrados
        """
        # El cifrado XOR es simétrico, por lo que descifrar es igual que cifrar
        return self._encrypt_data(encrypted_data)

    def get_last_save_file(self) -> Optional[int]:
        """
        Obtiene el número del último archivo de guardado utilizado.

        Returns:
                Número del archivo de guardado o None si no hay ninguno
        """
        last_used = None
        last_timestamp = None

        for save_info in self.save_files:
            if save_info["exists"] and save_info["last_used"]:
                if last_timestamp is None or save_info["last_used"] > last_timestamp:
                    last_timestamp = save_info["last_used"]
                    last_used = save_info["file_number"]

        return last_used

    def auto_save(self, game_state, additional_data: Dict[str, Any] = None) -> bool:
        """
        Guarda automáticamente el juego en el archivo actual o el último usado.

        Args:
                game_state: Estado del juego a guardar
                additional_data: Datos adicionales a guardar

        Returns:
                True si se guardó correctamente
        """
        # Si no hay archivo actual, usar el último
        if self.current_save_file is None:
            last_save = self.get_last_save_file()
            if last_save:
                self.current_save_file = last_save
            else:
                # Crear nuevo archivo si no hay ninguno
                self.current_save_file = 1
                self.create_new_save(1)

        return self.save_game(game_state, additional_data)

    def export_save_debug(self, save_file_number: int, output_path: str) -> bool:
        """
        Exporta un archivo de guardado en formato legible para debug.

        Args:
                save_file_number: Número del archivo de guardado
                output_path: Ruta donde guardar el archivo de debug

        Returns:
                True si se exportó correctamente
        """
        save_data = self.load_save(save_file_number)
        if save_data is None:
            return False

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)

            self.logger.info(
                f"Archivo de guardado {save_file_number} exportado para debug: {output_path}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Error al exportar archivo de guardado: {e}")
            return False

    def import_save_debug(self, save_file_number: int, input_path: str) -> bool:
        """
        Importa un archivo de guardado desde formato de debug.

        Args:
                save_file_number: Número del archivo de guardado
                input_path: Ruta del archivo de debug a importar

        Returns:
                True si se importó correctamente
        """
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)

            # Crear archivo de guardado desde datos de debug
            self.current_save_file = save_file_number

            # Crear un GameState temporal para guardar
            from ..core.game_state import GameState

            temp_game_state = GameState()
            temp_game_state.load_state(save_data.get("game_state", {}))

            return self.save_game(temp_game_state, save_data.get("additional_data", {}))

        except Exception as e:
            self.logger.error(f"Error al importar archivo de guardado: {e}")
            return False
