"""
Player Integration - Integración del jugador con sistemas existentes
====================================================================

Autor: SiK Team
Fecha: 30 de Julio, 2025
Descripción: Integración del jugador con stats, effects, combat y otros sistemas.
"""

import logging
import time
from typing import Any, Dict, List, Tuple

import pygame
import pygame.mixer

from ..entities.powerup import PowerupEffect
from .attack_configuration import AttackConfig
from .entity import EntityState
from .player_combat import PlayerCombat
from .player_core import AnimationState, PlayerCore
from .player_effects import PlayerEffects
from .player_stats import PlayerStats


class PlayerIntegration:
    """
    Integración del jugador con sistemas existentes.
    Maneja la integración con stats, effects, combat y otros sistemas del juego.
    """

    def __init__(self, player_core: PlayerCore, config):
        """
        Inicializa la integración del jugador.

        Args:
            player_core: Núcleo del jugador
            config: Configuración del juego
        """
        self.player_core = player_core
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Inicializar sistemas modulares
        self.effects = PlayerEffects()

        # Cargar ataques desde config
        char_data = config.get_character_data(player_core.character_name)
        self.attack_configs = [AttackConfig(a) for a in char_data.get("ataques", [])]
        self.combat = PlayerCombat(player_core.stats, self.effects, self.attack_configs)

    def attack(self, target_pos: Tuple[int, int], enemies: List[Any]):
        """
        Ejecuta el ataque actual según el tipo (melee, ranged, area).
        Reproduce animación y sonido si están definidos en el ataque.

        Args:
            target_pos: Posición objetivo del ataque
            enemies: Lista de enemigos en el área

        Returns:
            Lista de resultados del ataque
        """
        current_time = time.time()

        # Obtener ataque activo
        if not self.attack_configs:
            return []

        attack_cfg = self.attack_configs[self.combat.current_attack_index]

        # Animación
        if (
            hasattr(self.player_core, "current_animation_state")
            and attack_cfg.animacion
        ):
            self.player_core.current_animation_state = (
                getattr(
                    AnimationState, attack_cfg.animacion.upper(), AnimationState.ATTACK
                )
                if hasattr(AnimationState, attack_cfg.animacion.upper())
                else AnimationState.ATTACK
            )

        # Sonido
        if attack_cfg.sonido:
            try:
                pygame.mixer.Sound(f"assets/sounds/{attack_cfg.sonido}").play()
            except (FileNotFoundError, RuntimeError) as e:
                self.logger.warning(
                    "No se pudo reproducir el sonido de ataque: %s (%s)",
                    attack_cfg.sonido,
                    e,
                )

        return self.combat.attack(self.player_core, target_pos, current_time, enemies)

    def take_damage(self, damage: float, source=None) -> bool:
        """
        Aplica daño al jugador.

        Args:
            damage: Cantidad de daño
            source: Fuente del daño

        Returns:
            True si el jugador murió
        """
        if self.combat.take_damage(damage, source):
            self.player_core.state = EntityState.DEAD
            return True
        return False

    def heal(self, amount: float):
        """Cura al jugador."""
        self.combat.heal(amount)

    def add_shield(self, amount: float):
        """Añade escudo al jugador."""
        self.combat.add_shield(amount)

    def add_combo(self, amount: int = 1):
        """Añade puntos de combo."""
        self.combat.add_combo(amount)

    def add_upgrade_points(self, amount: int):
        """Añade puntos de mejora."""
        self.player_core.stats.add_upgrade_points(amount)

    def upgrade_stat(self, stat_name: str, cost: int) -> bool:
        """Mejora una estadística."""
        return self.player_core.stats.upgrade_stat(stat_name, cost)

    def apply_powerup(self, powerup_effect: PowerupEffect):
        """
        Aplica un powerup al jugador.

        Args:
            powerup_effect: Efecto del powerup
        """
        current_time = time.time()
        self.effects.apply_powerup(powerup_effect, current_time)

    def has_effect(self, effect_type) -> bool:
        """Verifica si tiene un efecto activo."""
        return self.effects.has_effect(effect_type)

    def get_effect_remaining_time(self, effect_type) -> float:
        """Obtiene el tiempo restante de un efecto."""
        current_time = time.time()
        return self.effects.get_effect_remaining_time(effect_type, current_time)

    def get_active_effects(self) -> dict:
        """Obtiene todos los efectos activos."""
        return self.effects.get_active_effects()

    def update_effects(self, _delta_time: float):
        """
        Actualiza los efectos activos.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        current_time = time.time()
        self.effects.update_effects(current_time)

    def get_integration_data(self) -> Dict[str, Any]:
        """Obtiene datos de integración para guardado."""
        return {
            "effects": self.effects.get_active_effects(),
            "combo": self.player_core.stats.combo,
            "max_combo": self.player_core.stats.max_combo,
            "stats": self.player_core.stats.to_dict(),
        }

    def load_integration_data(self, data: Dict[str, Any]):
        """Carga datos de integración desde guardado."""
        # Cargar estadísticas
        if "stats" in data:
            self.player_core.stats = PlayerStats.from_dict(data["stats"])
        # Cargar efectos
        if "effects" in data:
            self.effects.active_effects = data["effects"]
        # Cargar combo
        if "combo" in data:
            self.player_core.stats.combo = data["combo"]
        if "max_combo" in data:
            self.player_core.stats.max_combo = data["max_combo"]
