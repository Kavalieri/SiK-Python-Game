"""
Save Encryption - Sistema de Encriptación XOR
==============================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado en encriptación/desencriptación de archivos de guardado.
"""

import hashlib
import logging
from typing import Any, Dict

from .config_manager import ConfigManager


class SaveEncryption:
    """
    Sistema de encriptación para archivos de guardado usando XOR.
    """

    def __init__(self, config: ConfigManager):
        """
        Inicializa el sistema de encriptación.

        Args:
            config: Configuración del juego
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.encryption_key = self._generate_encryption_key()

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

    def encrypt_data(self, data: bytes) -> bytes:
        """
        Cifra los datos usando la clave de cifrado XOR.

        Args:
            data: Datos a cifrar

        Returns:
            Datos cifrados
        """
        # Implementación de cifrado XOR
        # En producción, considerar usar una biblioteca de cifrado más robusta
        key_bytes = self.encryption_key.encode()
        encrypted = bytearray()

        for i, byte in enumerate(data):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted.append(byte ^ key_byte)

        return bytes(encrypted)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Descifra los datos usando la clave de cifrado XOR.

        Args:
            encrypted_data: Datos cifrados

        Returns:
            Datos descifrados
        """
        # El cifrado XOR es simétrico, por lo que descifrar es igual que cifrar
        return self.encrypt_data(encrypted_data)

    def validate_encryption_integrity(
        self, original_data: bytes, encrypted_data: bytes
    ) -> bool:
        """
        Valida la integridad de la encriptación.

        Args:
            original_data: Datos originales
            encrypted_data: Datos encriptados

        Returns:
            True si la encriptación/desencriptación es correcta
        """
        try:
            decrypted_data = self.decrypt_data(encrypted_data)
            return original_data == decrypted_data
        except Exception as e:
            self.logger.error("Error validando integridad de encriptación: %s", e)
            return False

    def generate_data_checksum(self, data: bytes) -> str:
        """
        Genera un checksum de los datos para verificación de integridad.

        Args:
            data: Datos para generar checksum

        Returns:
            Checksum hexadecimal
        """
        return hashlib.md5(data).hexdigest()

    def verify_data_checksum(self, data: bytes, expected_checksum: str) -> bool:
        """
        Verifica el checksum de los datos.

        Args:
            data: Datos a verificar
            expected_checksum: Checksum esperado

        Returns:
            True si el checksum coincide
        """
        actual_checksum = self.generate_data_checksum(data)
        return actual_checksum == expected_checksum

    def create_encrypted_package(self, data: bytes) -> Dict[str, Any]:
        """
        Crea un paquete encriptado con metadatos de verificación.

        Args:
            data: Datos a encriptar

        Returns:
            Paquete encriptado con metadatos
        """
        # Generar checksum de datos originales
        checksum = self.generate_data_checksum(data)

        # Encriptar datos
        encrypted_data = self.encrypt_data(data)

        # Crear paquete con metadatos
        package = {
            "encrypted_data": encrypted_data,
            "checksum": checksum,
            "encryption_version": "1.0",
            "key_version": hashlib.md5(self.encryption_key.encode()).hexdigest()[:8],
        }

        return package

    def extract_encrypted_package(self, package: Dict[str, Any]) -> bytes:
        """
        Extrae y valida datos de un paquete encriptado.

        Args:
            package: Paquete encriptado con metadatos

        Returns:
            Datos desencriptados

        Raises:
            ValueError: Si la validación falla
        """
        try:
            # Extraer datos encriptados
            encrypted_data = package["encrypted_data"]
            expected_checksum = package["checksum"]

            # Desencriptar datos
            decrypted_data = self.decrypt_data(encrypted_data)

            # Verificar integridad
            if not self.verify_data_checksum(decrypted_data, expected_checksum):
                raise ValueError(
                    "Checksum de datos no coincide - archivo posiblemente corrupto"
                )

            return decrypted_data

        except KeyError as e:
            raise ValueError(f"Paquete encriptado inválido - falta campo: {e}")
        except Exception as e:
            raise ValueError(f"Error extrayendo paquete encriptado: {e}")

    def get_encryption_info(self) -> Dict[str, str]:
        """
        Obtiene información sobre el sistema de encriptación actual.

        Returns:
            Información de encriptación
        """
        return {
            "encryption_method": "XOR",
            "key_length": str(len(self.encryption_key)),
            "key_hash": hashlib.md5(self.encryption_key.encode()).hexdigest()[:8],
            "supported_versions": ["1.0"],
        }
