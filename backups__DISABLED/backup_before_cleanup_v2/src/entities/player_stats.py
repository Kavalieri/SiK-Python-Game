"""
Player Stats - Estadísticas del Jugador
======================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que maneja las estadísticas específicas del jugador.
"""

from dataclasses import dataclass
from typing import Dict, Any
from .entity import EntityStats


@dataclass
class PlayerStats(EntityStats):
    """Estadísticas específicas del jugador."""

    shoot_speed: float = 0.2  # Tiempo entre disparos
    bullet_speed: float = 500.0  # Velocidad de los proyectiles
    bullet_damage: float = 25.0  # Daño de los proyectiles
    shield: float = 0.0  # Escudo actual
    max_shield: float = 100.0  # Escudo máximo
    upgrade_points: int = 0  # Puntos de mejora
    combo: int = 0  # Combo actual
    max_combo: int = 0  # Combo máximo

    def to_dict(self) -> Dict[str, Any]:
        """Convierte las estadísticas a diccionario para guardado."""
        base_dict = super().to_dict()
        player_dict = {
            "shoot_speed": self.shoot_speed,
            "bullet_speed": self.bullet_speed,
            "bullet_damage": self.bullet_damage,
            "shield": self.shield,
            "max_shield": self.max_shield,
            "upgrade_points": self.upgrade_points,
            "combo": self.combo,
            "max_combo": self.max_combo,
        }
        base_dict.update(player_dict)
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerStats":
        """Crea estadísticas desde diccionario."""
        base_stats = EntityStats.from_dict(data)
        return cls(
            health=base_stats.health,
            max_health=base_stats.max_health,
            speed=base_stats.speed,
            damage=base_stats.damage,
            shoot_speed=data.get("shoot_speed", 0.2),
            bullet_speed=data.get("bullet_speed", 500.0),
            bullet_damage=data.get("bullet_damage", 25.0),
            shield=data.get("shield", 0.0),
            max_shield=data.get("max_shield", 100.0),
            upgrade_points=data.get("upgrade_points", 0),
            combo=data.get("combo", 0),
            max_combo=data.get("max_combo", 0),
        )

    def upgrade_stat(self, stat_name: str, cost: int) -> bool:
        """
        Mejora una estadística específica.

        Args:
            stat_name: Nombre de la estadística a mejorar
            cost: Costo en puntos de mejora

        Returns:
            True si la mejora fue exitosa, False en caso contrario
        """
        if self.upgrade_points < cost:
            return False

        upgrade_amounts = {
            "health": 20,
            "speed": 10,
            "damage": 5,
            "shoot_speed": -0.02,  # Reducir tiempo entre disparos
            "bullet_speed": 25,
            "bullet_damage": 5,
            "shield": 10,
        }

        if stat_name not in upgrade_amounts:
            return False

        # Aplicar mejora
        if stat_name == "health":
            self.max_health += upgrade_amounts[stat_name]
            self.health = min(self.health + upgrade_amounts[stat_name], self.max_health)
        elif stat_name == "speed":
            self.speed += upgrade_amounts[stat_name]
        elif stat_name == "damage":
            self.damage += upgrade_amounts[stat_name]
        elif stat_name == "shoot_speed":
            self.shoot_speed = max(0.05, self.shoot_speed + upgrade_amounts[stat_name])
        elif stat_name == "bullet_speed":
            self.bullet_speed += upgrade_amounts[stat_name]
        elif stat_name == "bullet_damage":
            self.bullet_damage += upgrade_amounts[stat_name]
        elif stat_name == "shield":
            self.max_shield += upgrade_amounts[stat_name]
            self.shield = min(self.shield + upgrade_amounts[stat_name], self.max_shield)

        self.upgrade_points -= cost
        return True

    def add_combo(self, amount: int = 1):
        """Añade puntos de combo."""
        self.combo += amount
        if self.combo > self.max_combo:
            self.max_combo = self.combo

    def reset_combo(self):
        """Reinicia el combo actual."""
        self.combo = 0

    def add_upgrade_points(self, amount: int):
        """Añade puntos de mejora."""
        self.upgrade_points += amount

    def heal(self, amount: float):
        """Cura al jugador."""
        self.health = min(self.health + amount, self.max_health)

    def add_shield(self, amount: float):
        """Añade escudo al jugador."""
        self.shield = min(self.shield + amount, self.max_shield)

    def take_shield_damage(self, damage: float) -> float:
        """
        Aplica daño al escudo primero.

        Returns:
            Daño restante que debe aplicarse a la vida
        """
        if self.shield > 0:
            if self.shield >= damage:
                self.shield -= damage
                return 0.0
            else:
                remaining_damage = damage - self.shield
                self.shield = 0
                return remaining_damage
        return damage
