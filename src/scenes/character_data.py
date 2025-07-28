"""
Character Data - Datos de Personajes
===================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que contiene todos los datos de personajes jugables.
"""

from typing import Dict, Any, List
from ..utils.config_manager_v2 import ConfigManagerV2


class CharacterData:
    """
    Gestiona todos los datos de personajes jugables.
    """
    
    def __init__(self):
        """Inicializa el gestor de datos de personajes."""
        self.config_manager = ConfigManagerV2()
    
    @classmethod
    def get_character_data(cls, character_key: str) -> Dict[str, Any]:
        """
        Obtiene los datos de un personaje específico.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Datos del personaje o diccionario vacío si no existe
        """
        config_manager = ConfigManagerV2()
        return config_manager.get_character_data(character_key)
    
    @classmethod
    def get_all_characters(cls) -> List[str]:
        """
        Obtiene la lista de todos los personajes disponibles.
        
        Returns:
            Lista de claves de personajes
        """
        config_manager = ConfigManagerV2()
        return config_manager.get_all_characters()
    
    @classmethod
    def get_character_data(cls, character_key: str) -> Dict[str, Any]:
        """
        Obtiene los datos de un personaje específico.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Datos del personaje o None si no existe
        """
        return cls.CHARACTER_DATA.get(character_key)
    
    @classmethod
    def get_all_characters(cls) -> List[str]:
        """
        Obtiene la lista de todos los personajes disponibles.
        
        Returns:
            Lista de claves de personajes
        """
        return list(cls.CHARACTER_DATA.keys())
    
    @classmethod
    def get_character_name(cls, character_key: str) -> str:
        """
        Obtiene el nombre de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Nombre del personaje o "Desconocido" si no existe
        """
        char_data = cls.get_character_data(character_key)
        return char_data.get("nombre", "Desconocido") if char_data else "Desconocido"
    
    @classmethod
    def get_character_type(cls, character_key: str) -> str:
        """
        Obtiene el tipo de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Tipo del personaje o "Desconocido" si no existe
        """
        char_data = cls.get_character_data(character_key)
        return char_data.get("tipo", "Desconocido") if char_data else "Desconocido"
    
    @classmethod
    def get_character_description(cls, character_key: str) -> str:
        """
        Obtiene la descripción de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Descripción del personaje o cadena vacía si no existe
        """
        char_data = cls.get_character_data(character_key)
        return char_data.get("descripcion", "") if char_data else ""
    
    @classmethod
    def get_character_stats(cls, character_key: str) -> Dict[str, int]:
        """
        Obtiene las estadísticas de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Estadísticas del personaje o diccionario vacío si no existe
        """
        char_data = cls.get_character_data(character_key)
        return char_data.get("stats", {}) if char_data else {}
    
    @classmethod
    def get_character_skills(cls, character_key: str) -> List[str]:
        """
        Obtiene las habilidades de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Lista de habilidades del personaje o lista vacía si no existe
        """
        char_data = cls.get_character_data(character_key)
        return char_data.get("habilidades", []) if char_data else []
    
    @classmethod
    def get_character_stat(cls, character_key: str, stat_name: str) -> int:
        """
        Obtiene una estadística específica de un personaje.
        
        Args:
            character_key: Clave del personaje
            stat_name: Nombre de la estadística
            
        Returns:
            Valor de la estadística o 0 si no existe
        """
        stats = cls.get_character_stats(character_key)
        return stats.get(stat_name, 0)
    
    @classmethod
    def is_valid_character(cls, character_key: str) -> bool:
        """
        Verifica si un personaje es válido.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            True si el personaje existe, False en caso contrario
        """
        return character_key in cls.CHARACTER_DATA
    
    @classmethod
    def get_character_summary(cls, character_key: str) -> Dict[str, Any]:
        """
        Obtiene un resumen completo de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Resumen del personaje con todos sus datos
        """
        if not cls.is_valid_character(character_key):
            return {}
        
        return {
            "key": character_key,
            "nombre": cls.get_character_name(character_key),
            "tipo": cls.get_character_type(character_key),
            "descripcion": cls.get_character_description(character_key),
            "stats": cls.get_character_stats(character_key),
            "habilidades": cls.get_character_skills(character_key)
        } 