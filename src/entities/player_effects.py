"""
Player Effects - Efectos y Powerups del Jugador
==============================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que maneja los efectos activos y powerups del jugador.
"""

import logging

from entities.powerup import PowerupEffect, PowerupType


class PlayerEffects:
    """
    Gestiona los efectos activos y powerups del jugador.
    """

    def __init__(self):
        """Inicializa el gestor de efectos."""
        self.active_effects: dict[
            PowerupType, tuple[float, float]
        ] = {}  # {PowerupType: (end_time, value)}
        self.logger = logging.getLogger(__name__)

    def apply_powerup(self, powerup_effect: PowerupEffect, current_time: float):
        """
        Aplica un powerup al jugador.

        Args:
            powerup_effect: Efecto del powerup a aplicar
            current_time: Tiempo actual del juego
        """
        effect_type = (
            powerup_effect.type
        )  # Corregido: usar 'type' en lugar de 'effect_type'
        duration = powerup_effect.duration
        value = powerup_effect.value

        # Si ya existe el efecto, extender su duración
        if effect_type in self.active_effects:
            existing_end_time, existing_value = self.active_effects[effect_type]
            # Tomar el valor más alto si es el mismo tipo de efecto
            new_value = max(existing_value, value)
            new_end_time = max(existing_end_time, current_time + duration)
            self.active_effects[effect_type] = (new_end_time, new_value)
            self.logger.debug("Efecto %s extendido hasta %s", effect_type, new_end_time)
        else:
            # Nuevo efecto
            end_time = current_time + duration
            self.active_effects[effect_type] = (end_time, value)
            self.logger.debug(
                "Nuevo efecto %s aplicado hasta %s", effect_type, end_time
            )

    def update_effects(self, current_time: float) -> dict[PowerupType, float]:
        """
        Actualiza los efectos activos y elimina los expirados.

        Args:
            current_time: Tiempo actual del juego

        Returns:
            Diccionario con los efectos activos y sus valores
        """
        expired_effects = []
        active_values = {}

        for effect_type, (end_time, value) in self.active_effects.items():
            if current_time >= end_time:
                expired_effects.append(effect_type)
                self.logger.debug("Efecto %s expirado", effect_type)
            else:
                active_values[effect_type] = value

        # Eliminar efectos expirados
        for effect_type in expired_effects:
            del self.active_effects[effect_type]

        return active_values

    def has_effect(self, effect_type: PowerupType) -> bool:
        """
        Verifica si el jugador tiene un efecto activo.

        Args:
            effect_type: Tipo de efecto a verificar

        Returns:
            True si el efecto está activo
        """
        return effect_type in self.active_effects

    def get_effect_value(self, effect_type: PowerupType) -> float:
        """
        Obtiene el valor de un efecto activo.

        Args:
            effect_type: Tipo de efecto

        Returns:
            Valor del efecto o 0.0 si no está activo
        """
        if effect_type in self.active_effects:
            return self.active_effects[effect_type][1]
        return 0.0

    def get_effect_remaining_time(
        self, effect_type: PowerupType, current_time: float
    ) -> float:
        """
        Obtiene el tiempo restante de un efecto.

        Args:
            effect_type: Tipo de efecto
            current_time: Tiempo actual del juego

        Returns:
            Tiempo restante en segundos, 0.0 si no está activo
        """
        if effect_type in self.active_effects:
            end_time = self.active_effects[effect_type][0]
            remaining = end_time - current_time
            return max(0.0, remaining)
        return 0.0

    def get_active_effects(self) -> dict[PowerupType, tuple[float, float]]:
        """
        Obtiene todos los efectos activos.

        Returns:
            Diccionario con todos los efectos activos
        """
        return self.active_effects.copy()

    def clear_all_effects(self):
        """Elimina todos los efectos activos."""
        self.active_effects.clear()
        self.logger.debug("Todos los efectos eliminados")

    def get_effect_description(self, effect_type: PowerupType) -> str:
        """
        Obtiene la descripción de un tipo de efecto.

        Args:
            effect_type: Tipo de efecto

        Returns:
            Descripción del efecto
        """
        descriptions = {
            PowerupType.SPEED: "Velocidad aumentada",
            PowerupType.RAPID_FIRE: "Velocidad de disparo aumentada",
            PowerupType.DAMAGE: "Daño aumentado",
            PowerupType.SHIELD: "Escudo temporal",
            PowerupType.DOUBLE_SHOT: "Disparo doble",
            PowerupType.SPREAD: "Disparo disperso",
            PowerupType.EXPLOSIVE: "Proyectiles explosivos",
            PowerupType.SHRAPNEL: "Metralla",
        }
        return descriptions.get(effect_type, "Efecto desconocido")

    def get_effects_summary(self, current_time: float) -> str:
        """
        Obtiene un resumen de todos los efectos activos.

        Args:
            current_time: Tiempo actual del juego

        Returns:
            Resumen de efectos activos
        """
        if not self.active_effects:
            return "Sin efectos activos"

        summary_parts = []
        for effect_type, (end_time, _) in self.active_effects.items():
            remaining_time = max(0.0, end_time - current_time)
            description = self.get_effect_description(effect_type)
            summary_parts.append(f"{description}: {remaining_time:.1f}s")

        return ", ".join(summary_parts)
