"""
Enemy Types - Sistema Mixto ConfigDatabase
==========================================

Autor: SiK Team
Fecha: 30 Julio 2025
Descripción: Sistema de tipos de enemigos usando ConfigDatabase (SQLite).
Sistema mixto inteligente: Datos complejos en SQLite, configuración simple en JSON.

MIGRACIÓN COMPLETADA:
- enemies.json → SQLite tabla enemigos
- Eliminado hardcodeo de configuraciones de enemigos
- Implementado sistema mixto inteligente
"""

import logging
import random
from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.utils.config_database import ConfigDatabase
from src.utils.database_manager import DatabaseManager


class EnemyRarity(Enum):
    """Rareza de los enemigos."""

    NORMAL = "normal"
    RARE = "rare"
    ELITE = "elite"
    LEGENDARY = "legendary"


class EnemyBehavior(Enum):
    """Comportamientos de enemigos."""

    CHASE = "chase"
    WANDER = "wander"
    AMBUSH = "ambush"
    SWARM = "swarm"
    BOSS = "boss"


@dataclass
class EnemyConfig:
    """Configuración de un tipo de enemigo."""

    name: str
    rarity: EnemyRarity
    behavior: EnemyBehavior
    health: int
    speed: int
    damage: int
    armor: int
    score_value: int
    color: tuple
    symbol: str
    size: int
    spawn_chance: float


class EnemyTypesManager:
    """
    Gestor de tipos de enemigos usando ConfigDatabase (sistema mixto).
    """

    _instance = None
    _config_db = None

    def __new__(cls):
        """Singleton para evitar múltiples conexiones a la base de datos."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializar el gestor de tipos de enemigos."""
        if self._config_db is None:
            self.logger = logging.getLogger(__name__)
            try:
                db_manager = DatabaseManager()
                self._config_db = ConfigDatabase(db_manager)
                self.logger.info("EnemyTypesManager inicializado con ConfigDatabase")
            except (ConnectionError, OSError) as e:
                self.logger.error("Error inicializando EnemyTypesManager: %s", e)
                self._config_db = None

    def get_enemy_config(self, enemy_type: str) -> EnemyConfig | None:
        """
        Obtener configuración de un tipo de enemigo específico.

        Args:
            enemy_type: Nombre del tipo de enemigo

        Returns:
            EnemyConfig o None si no existe
        """
        if self._config_db:
            try:
                enemy_data = self._config_db.get_enemy_data(enemy_type)
                if enemy_data:
                    return self._convert_to_config(enemy_data)
                return None
            except (ConnectionError, OSError) as e:
                self.logger.error("Error obteniendo config de %s: %s", enemy_type, e)
                return self._get_fallback_config(enemy_type)
        else:
            return self._get_fallback_config(enemy_type)

    def get_all_enemy_types(self) -> list[str]:
        """
        Obtener lista de todos los tipos de enemigos disponibles.

        Returns:
            Lista de nombres de tipos de enemigos
        """
        if self._config_db:
            try:
                all_enemies = self._config_db.get_all_enemies()
                return [enemy.get("tipo", "unknown") for enemy in all_enemies]
            except (ConnectionError, OSError) as e:
                self.logger.error("Error obteniendo tipos de enemigos: %s", e)
                return list(self._get_fallback_data().keys())
        else:
            return list(self._get_fallback_data().keys())

    def get_random_by_rarity(self, rarity: EnemyRarity) -> EnemyConfig | None:
        """Obtiene un enemigo aleatorio de una rareza específica."""
        configs = self.get_by_rarity(rarity)
        if configs:
            total_chance = sum(config.spawn_chance for config in configs)
            rand = random.uniform(0, total_chance)
            current = 0
            for config in configs:
                current += config.spawn_chance
                if rand <= current:
                    return config
        return None

    def get_by_rarity(self, rarity: EnemyRarity) -> list[EnemyConfig]:
        """Obtiene todos los enemigos de una rareza específica."""
        all_types = self.get_all_enemy_types()
        configs = []
        for enemy_type in all_types:
            config = self.get_enemy_config(enemy_type)
            if config and config.rarity == rarity:
                configs.append(config)
        return configs

    def get_random_enemy(self) -> EnemyConfig:
        """Obtiene un enemigo aleatorio basado en probabilidades de rareza."""
        rarity_chances = {
            EnemyRarity.NORMAL: 0.7,  # 70%
            EnemyRarity.RARE: 0.2,  # 20%
            EnemyRarity.ELITE: 0.08,  # 8%
            EnemyRarity.LEGENDARY: 0.02,  # 2%
        }

        rand = random.random()
        current = 0
        for rarity, chance in rarity_chances.items():
            current += chance
            if rand <= current:
                result = self.get_random_by_rarity(rarity)
                if result:
                    return result

        # Fallback al enemigo normal
        return self._get_fallback_config("zombie_male") or self.create_default_config()

    def _convert_to_config(self, enemy_data: dict[str, Any]) -> EnemyConfig:
        """Convierte datos de la base de datos a EnemyConfig."""
        stats = enemy_data.get("stats", {})
        return EnemyConfig(
            name=enemy_data.get("tipo", "unknown"),
            rarity=EnemyRarity.NORMAL,  # Por defecto, puede expandirse
            behavior=EnemyBehavior.CHASE,  # Por defecto, puede expandirse
            health=stats.get("vida", 50),
            speed=stats.get("velocidad", 80),
            damage=stats.get("daño", 15),
            armor=0,  # No está en el JSON actual
            score_value=50,  # Por defecto
            color=(200, 100, 100),  # Rojo por defecto
            symbol="Z",  # Zombie por defecto
            size=32,  # Tamaño por defecto
            spawn_chance=1.0,  # Por defecto
        )

    def _get_fallback_config(self, enemy_type: str) -> EnemyConfig | None:
        """Configuración de fallback temporal."""
        fallback_data = self._get_fallback_data()
        if enemy_type in fallback_data:
            data = fallback_data[enemy_type]
            return EnemyConfig(
                name=enemy_type,
                rarity=EnemyRarity.NORMAL,
                behavior=EnemyBehavior.CHASE,
                health=data["health"],
                speed=data["speed"],
                damage=data["damage"],
                armor=data.get("armor", 0),
                score_value=data.get("score_value", 50),
                color=data.get("color", (200, 100, 100)),
                symbol=data.get("symbol", "Z"),
                size=data.get("size", 32),
                spawn_chance=data.get("spawn_chance", 1.0),
            )
        return None

    def _get_fallback_data(self) -> dict[str, dict[str, Any]]:
        """Datos de fallback temporal hasta completar la migración."""
        return {
            "zombie_male": {
                "health": 50,
                "speed": 80,
                "damage": 15,
                "color": (100, 200, 100),
                "symbol": "Z♂",
                "spawn_chance": 0.8,
            },
            "zombie_female": {
                "health": 40,
                "speed": 90,
                "damage": 12,
                "color": (200, 100, 200),
                "symbol": "Z♀",
                "spawn_chance": 0.7,
            },
        }

    def create_default_config(self) -> EnemyConfig:
        """Crea una configuración por defecto."""
        return EnemyConfig(
            name="zombie_default",
            rarity=EnemyRarity.NORMAL,
            behavior=EnemyBehavior.CHASE,
            health=50,
            speed=80,
            damage=15,
            armor=0,
            score_value=50,
            color=(200, 100, 100),
            symbol="Z",
            size=32,
            spawn_chance=1.0,
        )


# Instancia global del gestor
_enemy_manager = EnemyTypesManager()


# Funciones de compatibilidad para código existente
def get_enemy_config(enemy_type: str) -> EnemyConfig | None:
    """Función de compatibilidad para obtener configuración de enemigo."""
    return _enemy_manager.get_enemy_config(enemy_type)


def get_random_enemy() -> EnemyConfig:
    """Función de compatibilidad para obtener enemigo aleatorio."""
    return _enemy_manager.get_random_enemy()


def get_random_by_rarity(rarity: EnemyRarity) -> EnemyConfig | None:
    """Función de compatibilidad para obtener enemigo por rareza."""
    return _enemy_manager.get_random_by_rarity(rarity)


# Clase de compatibilidad para código existente que use EnemyTypes
class EnemyTypes:
    """Clase de compatibilidad para el código existente."""

    @classmethod
    def get_random_enemy(cls) -> EnemyConfig:
        """Obtiene un enemigo aleatorio."""
        return _enemy_manager.get_random_enemy()

    @classmethod
    def get_random_by_rarity(cls, rarity: EnemyRarity) -> EnemyConfig | None:
        """Obtiene un enemigo aleatorio de una rareza específica."""
        return _enemy_manager.get_random_by_rarity(rarity)

    # Configuraciones estáticas para compatibilidad inmediata
    ZOMBIE_NORMAL = _enemy_manager.create_default_config()
