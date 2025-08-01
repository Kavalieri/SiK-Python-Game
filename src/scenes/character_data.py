"""
Character Data - Datos de Personajes
===================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que contiene todos los datos de personajes jugables.
"""

from typing import Any


class CharacterData:
    """
    Gestiona todos los datos de personajes jugables.

    Ejemplo de uso:
        >>> datos = CharacterData.get_character_data("guerrero")
        >>> print(datos["nombre"])
    """

    # Datos de personajes disponibles
    CHARACTER_DATA = {
        "guerrero": {
            "nombre": "Guerrero",
            "tipo": "Jugable",
            "descripcion": "Un valiente guerrero con habilidades de combate cuerpo a cuerpo.",
            "stats": {"vida": 100, "velocidad": 5, "daño": 25, "defensa": 15},
            "habilidades": ["Ataque Melee", "Defensa", "Carga"],
        },
        "adventureguirl": {
            "nombre": "Aventurera",
            "tipo": "Jugable",
            "descripcion": "Una aventurera ágil con habilidades de combate a distancia.",
            "stats": {"vida": 80, "velocidad": 7, "daño": 20, "defensa": 10},
            "habilidades": ["Tiro con Arco", "Esquiva", "Sigilo"],
        },
        "robot": {
            "nombre": "Robot",
            "tipo": "Jugable",
            "descripcion": "Un robot avanzado con tecnología futurista.",
            "stats": {"vida": 120, "velocidad": 4, "daño": 30, "defensa": 20},
            "habilidades": ["Láser", "Escudo", "Reparación"],
        },
    }

    @classmethod
    def get_character_data(cls, character_key: str) -> dict[str, Any] | None:
        """
        Obtiene los datos de un personaje específico.

        Args:
            character_key: Clave del personaje

        Returns:
            dict: Datos del personaje o None si no existe

        Ejemplo:
            >>> datos = CharacterData.get_character_data("guerrero")
            >>> print(datos["nombre"])
        """
        return cls.CHARACTER_DATA.get(character_key)

    @classmethod
    def is_valid_character(cls, character_key: str) -> bool:
        """
        Verifica si un personaje es válido.

        Args:
            character_key: Clave del personaje

        Returns:
            bool: True si el personaje existe, False en caso contrario

        Ejemplo:
            >>> valido = CharacterData.is_valid_character("guerrero")
            >>> print(valido)
        """
        return character_key in cls.CHARACTER_DATA

    @classmethod
    def get_character_summary(cls, character_key: str) -> dict[str, Any]:
        """
        Obtiene un resumen completo de un personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            dict: Resumen del personaje con todos sus datos

        Ejemplo:
            >>> resumen = CharacterData.get_character_summary("guerrero")
            >>> print(resumen["nombre"])
        """
        if not cls.is_valid_character(character_key):
            return {}

        return {
            "key": character_key,
            "nombre": cls.get_character_attribute(
                character_key, "nombre", "Desconocido"
            ),
            "tipo": cls.get_character_attribute(character_key, "tipo", "Desconocido"),
            "descripcion": cls.get_character_attribute(
                character_key, "descripcion", ""
            ),
            "stats": cls.get_character_attribute(character_key, "stats", {}),
            "habilidades": cls.get_character_attribute(
                character_key, "habilidades", []
            ),
        }

    @classmethod
    def validate_character_data(cls):
        """
        Valida que los datos de los personajes cumplan con el esquema esperado.

        Raises:
            ValueError: Si algún personaje tiene datos inválidos

        Ejemplo:
            >>> CharacterData.validate_character_data()
        """
        required_keys = {"nombre", "tipo", "descripcion", "stats", "habilidades"}

        for key, data in cls.CHARACTER_DATA.items():
            if not required_keys.issubset(data.keys()):
                raise ValueError(
                    f"El personaje '{key}' tiene datos incompletos: {data}"
                )

    @classmethod
    def get_character_attribute(
        cls, character_key: str, attribute: str, default: Any
    ) -> Any:
        """
        Obtiene un atributo específico de un personaje.

        Args:
            character_key: Clave del personaje
            attribute: Nombre del atributo
            default: Valor por defecto si el atributo no existe

        Returns:
            Valor del atributo o el valor por defecto

        Ejemplo:
            >>> vida = CharacterData.get_character_attribute("guerrero", "stats", {})
        """
        char_data = cls.get_character_data(character_key)
        return char_data.get(attribute, default) if char_data else default
