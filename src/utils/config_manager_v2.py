"""
Config Manager V2 - Gestor de Configuración Mejorado
==================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Gestor de configuración que carga y gestiona todos los archivos de configuración del juego.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManagerV2:
    """
    Gestor de configuración mejorado que maneja múltiples archivos de configuración.
    """
    
    def __init__(self):
        """Inicializa el gestor de configuración V2."""
        self.logger = logging.getLogger(__name__)
        
        # Directorio de configuración
        self.config_dir = Path(__file__).parent.parent.parent / "config"
        
        # Configuraciones cargadas
        self.configs = {}
        
        # Cargar todas las configuraciones
        self._load_all_configs()
    
    def _load_all_configs(self):
        """Carga todos los archivos de configuración."""
        try:
            config_files = [
                "characters.json",
                "gameplay.json", 
                "enemies.json",
                "powerups.json",
                "ui.json",
                "audio.json"
            ]
            
            for config_file in config_files:
                config_path = self.config_dir / config_file
                if config_path.exists():
                    self._load_config(config_file, config_path)
                else:
                    self.logger.warning(f"Archivo de configuración no encontrado: {config_file}")
            
            self.logger.info(f"Configuraciones cargadas: {len(self.configs)} archivos")
            
        except Exception as e:
            self.logger.error(f"Error cargando configuraciones: {e}")
    
    def _load_config(self, config_name: str, config_path: Path):
        """
        Carga un archivo de configuración específico.
        
        Args:
            config_name: Nombre del archivo de configuración
            config_path: Ruta al archivo de configuración
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Extraer el nombre base del archivo (sin extensión)
            config_key = config_path.stem
            self.configs[config_key] = config_data
            
            self.logger.debug(f"Configuración cargada: {config_key}")
            
        except Exception as e:
            self.logger.error(f"Error cargando {config_name}: {e}")
    
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """
        Obtiene una configuración específica.
        
        Args:
            config_name: Nombre de la configuración
            
        Returns:
            Datos de la configuración o diccionario vacío si no existe
        """
        return self.configs.get(config_name, {})
    
    def get_character_data(self, character_key: str) -> Dict[str, Any]:
        """
        Obtiene los datos de un personaje específico.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Datos del personaje o diccionario vacío si no existe
        """
        characters_config = self.get_config("characters")
        return characters_config.get("characters", {}).get(character_key, {})
    
    def get_character_stats(self, character_key: str) -> Dict[str, Any]:
        """
        Obtiene las estadísticas de un personaje.
        
        Args:
            character_key: Clave del personaje
            
        Returns:
            Estadísticas del personaje o diccionario vacío si no existe
        """
        char_data = self.get_character_data(character_key)
        return char_data.get("stats", {})
    
    def get_character_stat(self, character_key: str, stat_name: str, default: Any = 0) -> Any:
        """
        Obtiene una estadística específica de un personaje.
        
        Args:
            character_key: Clave del personaje
            stat_name: Nombre de la estadística
            default: Valor por defecto si no existe
            
        Returns:
            Valor de la estadística
        """
        stats = self.get_character_stats(character_key)
        return stats.get(stat_name, default)
    
    def get_enemy_data(self, enemy_type: str) -> Dict[str, Any]:
        """
        Obtiene los datos de un tipo de enemigo.
        
        Args:
            enemy_type: Tipo de enemigo
            
        Returns:
            Datos del enemigo o diccionario vacío si no existe
        """
        enemies_config = self.get_config("enemies")
        return enemies_config.get("tipos_enemigos", {}).get(enemy_type, {})
    
    def get_enemy_variant(self, variant_type: str) -> Dict[str, Any]:
        """
        Obtiene los datos de una variante de enemigo.
        
        Args:
            variant_type: Tipo de variante
            
        Returns:
            Datos de la variante o diccionario vacío si no existe
        """
        enemies_config = self.get_config("enemies")
        return enemies_config.get("variantes", {}).get(variant_type, {})
    
    def get_powerup_data(self, powerup_type: str) -> Dict[str, Any]:
        """
        Obtiene los datos de un tipo de powerup.
        
        Args:
            powerup_type: Tipo de powerup
            
        Returns:
            Datos del powerup o diccionario vacío si no existe
        """
        powerups_config = self.get_config("powerups")
        return powerups_config.get("tipos_powerups", {}).get(powerup_type, {})
    
    def get_gameplay_value(self, category: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de la configuración de gameplay.
        
        Args:
            category: Categoría (niveles, combate, powerups, puntuación)
            key: Clave del valor
            default: Valor por defecto
            
        Returns:
            Valor de la configuración
        """
        gameplay_config = self.get_config("gameplay")
        return gameplay_config.get(category, {}).get(key, default)
    
    def get_ui_color(self, color_name: str) -> tuple:
        """
        Obtiene un color de la configuración de UI.
        
        Args:
            color_name: Nombre del color
            
        Returns:
            Tupla RGB del color o (255, 255, 255) si no existe
        """
        ui_config = self.get_config("ui")
        color_data = ui_config.get("colores", {}).get(color_name, [255, 255, 255])
        return tuple(color_data)
    
    def get_ui_font_size(self, font_name: str) -> int:
        """
        Obtiene el tamaño de una fuente de la configuración de UI.
        
        Args:
            font_name: Nombre de la fuente
            
        Returns:
            Tamaño de la fuente o 24 si no existe
        """
        ui_config = self.get_config("ui")
        return ui_config.get("fuentes", {}).get(font_name, 24)
    
    def get_ui_dimension(self, dimension_name: str) -> int:
        """
        Obtiene una dimensión de la configuración de UI.
        
        Args:
            dimension_name: Nombre de la dimensión
            
        Returns:
            Valor de la dimensión o 0 si no existe
        """
        ui_config = self.get_config("ui")
        return ui_config.get("dimensiones", {}).get(dimension_name, 0)
    
    def get_audio_volume(self, volume_type: str) -> float:
        """
        Obtiene el volumen de un tipo de audio.
        
        Args:
            volume_type: Tipo de volumen
            
        Returns:
            Volumen (0.0 - 1.0) o 0.5 si no existe
        """
        audio_config = self.get_config("audio")
        return audio_config.get("volúmenes", {}).get(volume_type, 0.5)
    
    def get_audio_file(self, category: str, sound_name: str) -> str:
        """
        Obtiene la ruta de un archivo de audio.
        
        Args:
            category: Categoría (música, efectos)
            sound_name: Nombre del sonido
            
        Returns:
            Ruta del archivo de audio o cadena vacía si no existe
        """
        audio_config = self.get_config("audio")
        return audio_config.get("archivos_audio", {}).get(category, {}).get(sound_name, "")
    
    def get_upgrade_data(self, upgrade_type: str) -> Dict[str, Any]:
        """
        Obtiene los datos de una mejora.
        
        Args:
            upgrade_type: Tipo de mejora
            
        Returns:
            Datos de la mejora o diccionario vacío si no existe
        """
        characters_config = self.get_config("characters")
        return characters_config.get("upgrades", {}).get(upgrade_type, {})
    
    def reload_configs(self):
        """Recarga todas las configuraciones."""
        self.logger.info("Recargando configuraciones...")
        self.configs.clear()
        self._load_all_configs()
    
    def save_config(self, config_name: str, config_data: Dict[str, Any]):
        """
        Guarda una configuración en su archivo correspondiente.
        
        Args:
            config_name: Nombre de la configuración
            config_data: Datos a guardar
        """
        try:
            config_path = self.config_dir / f"{config_name}.json"
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Actualizar en memoria
            self.configs[config_name] = config_data
            
            self.logger.info(f"Configuración guardada: {config_name}")
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración {config_name}: {e}")
    
    def get_all_characters(self) -> list:
        """
        Obtiene la lista de todos los personajes disponibles.
        
        Returns:
            Lista de claves de personajes
        """
        characters_config = self.get_config("characters")
        return list(characters_config.get("characters", {}).keys())
    
    def get_all_enemy_types(self) -> list:
        """
        Obtiene la lista de todos los tipos de enemigos.
        
        Returns:
            Lista de tipos de enemigos
        """
        enemies_config = self.get_config("enemies")
        return list(enemies_config.get("tipos_enemigos", {}).keys())
    
    def get_all_powerup_types(self) -> list:
        """
        Obtiene la lista de todos los tipos de powerups.
        
        Returns:
            Lista de tipos de powerups
        """
        powerups_config = self.get_config("powerups")
        return list(powerups_config.get("tipos_powerups", {}).keys())
    
    def validate_configs(self) -> bool:
        """
        Valida que todas las configuraciones estén correctas.
        
        Returns:
            True si todas las configuraciones son válidas, False en caso contrario
        """
        try:
            # Validar que existan las configuraciones básicas
            required_configs = ["characters", "gameplay", "enemies", "powerups", "ui", "audio"]
            
            for config_name in required_configs:
                if config_name not in self.configs:
                    self.logger.error(f"Configuración requerida faltante: {config_name}")
                    return False
            
            # Validar que existan personajes
            characters = self.get_all_characters()
            if not characters:
                self.logger.error("No se encontraron personajes en la configuración")
                return False
            
            # Validar que existan enemigos
            enemies = self.get_all_enemy_types()
            if not enemies:
                self.logger.error("No se encontraron enemigos en la configuración")
                return False
            
            self.logger.info("Todas las configuraciones son válidas")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando configuraciones: {e}")
            return False 