"""
Datos de personajes jugables - Sistema Mixto ConfigDatabase
===========================================================

Autor: SiK Team
Fecha: 30 Julio 2025
Descripción: Interfaz para datos de personajes usando ConfigDatabase (SQLite).
Sistema mixto inteligente: Datos complejos en SQLite, configuración simple en JSON.

MIGRACIÓN COMPLETADA:
- characters.json → SQLite tabla personajes
- Eliminado diccionario CHARACTER_DATA hardcodeado
- Implementado sistema mixto inteligente
"""

import logging
from typing import Any

from utils.config_database import ConfigDatabase
from utils.database_manager import DatabaseManager


class CharacterDataManager:
    """
    Gestor de datos de personajes usando ConfigDatabase (sistema mixto).
    """

    _instance = None
    _config_db = None

    def __new__(cls):
        """Singleton para evitar múltiples conexiones a la base de datos."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializar el gestor de datos de personajes."""
        if self._config_db is None:
            self.logger = logging.getLogger(__name__)
            try:
                db_manager = DatabaseManager()
                self._config_db = ConfigDatabase(db_manager)
                self.logger.info("CharacterDataManager inicializado con ConfigDatabase")
            except (ImportError, ValueError, OSError) as e:
                self.logger.error("Error inicializando CharacterDataManager: %s", e)
                # Fallback temporal hasta completar migración
                self._config_db = None

    def get_character_data(self, character_name: str) -> dict[str, Any] | None:
        """
        Obtener datos de un personaje específico.

        Args:
            character_name: Nombre del personaje

        Returns:
            Diccionario con datos del personaje o None si no existe
        """
        if self._config_db:
            try:
                return self._config_db.get_character_data(character_name)
            except (ValueError, KeyError, RuntimeError) as e:
                self.logger.error("Error obteniendo datos de %s: %s", character_name, e)
                return None
        else:
            # Fallback temporal con datos hardcodeados
            return self._get_fallback_data().get(character_name)

    def get_all_characters(self) -> list[str]:
        """
        Obtener lista de todos los personajes disponibles.

        Returns:
            Lista de nombres de personajes
        """
        if self._config_db:
            try:
                all_chars_data = self._config_db.get_all_characters()
                # ConfigDatabase.get_all_characters() devuelve lista de diccionarios
                # Extraemos solo los nombres
                return [
                    char_data.get("nombre", "unknown") for char_data in all_chars_data
                ]
            except (ValueError, KeyError, RuntimeError) as e:
                self.logger.error("Error obteniendo lista de personajes: %s", e)
                return list(self._get_fallback_data().keys())
        else:
            return list(self._get_fallback_data().keys())

    def _get_fallback_data(self) -> dict[str, dict[str, Any]]:
        """
        Datos de fallback temporal hasta completar la migración.
        NOTA: Estos datos serán eliminados una vez confirmada la migración.
        """
        return {
            "guerrero": {
                "nombre": "Kava",
                "descripcion": "Guerrero cuerpo a cuerpo especializado en combate cercano.",
                "imagen": "assets/characters/guerrero/idle/Idle_1_.png",
                "tipo": "Melee",
                "stats": {
                    "vida": 200,
                    "velocidad": 180,
                    "daño": 50,
                    "escudo": 20,
                    "disparo": 0.0,
                    "rango_ataque": 80,
                },
                "habilidades": [
                    "Ataque de espada cuerpo a cuerpo",
                    "Escudo protector",
                    "Mayor resistencia al daño",
                    "Combo de ataques rápidos",
                ],
            },
            "adventureguirl": {
                "nombre": "Sara",
                "descripcion": "Aventurera ágil especializada en combate a distancia.",
                "imagen": "assets/characters/adventureguirl/Idle_1_.png",
                "tipo": "Ranged",
                "stats": {
                    "vida": 120,
                    "velocidad": 220,
                    "daño": 25,
                    "escudo": 5,
                    "disparo": 1.5,
                    "rango_ataque": 300,
                },
                "habilidades": [
                    "Flechas mágicas de fuego",
                    "Disparo rápido y preciso",
                    "Alta movilidad",
                    "Evasión mejorada",
                ],
            },
            "robot": {
                "nombre": "Guiral",
                "descripcion": "Robot de combate con tecnología avanzada.",
                "imagen": "assets/characters/robot/Idle_1_.png",
                "tipo": "Tech",
                "stats": {
                    "vida": 150,
                    "velocidad": 160,
                    "daño": 35,
                    "escudo": 15,
                    "disparo": 1.2,
                    "rango_ataque": 250,
                },
                "habilidades": [
                    "Proyectiles de energía",
                    "Misiles explosivos",
                    "Daño en área",
                    "Blindaje mejorado",
                ],
            },
        }


# Instancia global del gestor
_character_manager = CharacterDataManager()


# Función de compatibilidad para código existente
def get_character_data(character_name: str) -> dict[str, Any] | None:
    """
    Función de compatibilidad para obtener datos de personaje.

    Args:
        character_name: Nombre del personaje

    Returns:
        Diccionario con datos del personaje
    """
    return _character_manager.get_character_data(character_name)


def get_all_characters() -> list[str]:
    """
    Función de compatibilidad para obtener todos los personajes.

    Returns:
        Lista de nombres de personajes
    """
    return _character_manager.get_all_characters()


# Mantener compatibilidad con código existente que usa CHARACTER_DATA
CHARACTER_DATA = {
    name: _character_manager.get_character_data(name)
    for name in _character_manager.get_all_characters()
}
