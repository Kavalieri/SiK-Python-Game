"""
Callbacks de mejoras/upgrades del jugador.
Módulo especializado extraído de MenuCallbacks para mantener límite de 150 líneas.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.game_state import GameState
    from src.utils.save_manager import SaveManager

logger = logging.getLogger(__name__)


class UpgradeCallbacks:
    """
    Gestiona los callbacks de mejoras y upgrades del jugador.
    """

    def __init__(self, game_state: "GameState", save_manager: "SaveManager"):
        """
        Inicializa el gestor de callbacks de upgrades.

        Args:
            game_state: Estado del juego
            save_manager: Gestor de archivos de guardado
        """
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = logger

    def on_upgrade_speed(self):
        """Callback para mejorar velocidad."""
        try:
            self.logger.info("Mejorando velocidad")
            if self.game_state.current_player:
                success = self.game_state.current_player.upgrade_stat("speed", 1)
                if success:
                    self.logger.info("Velocidad mejorada")
                else:
                    self.logger.warning("No hay suficientes puntos de mejora")
            else:
                self.logger.warning("No hay jugador disponible para mejorar")
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error mejorando velocidad: %s", str(e))

    def on_upgrade_damage(self):
        """Callback para mejorar daño."""
        try:
            self.logger.info("Mejorando daño")
            if self.game_state.current_player:
                success = self.game_state.current_player.upgrade_stat("damage", 1)
                if success:
                    self.logger.info("Daño mejorado")
                else:
                    self.logger.warning("No hay suficientes puntos de mejora")
            else:
                self.logger.warning("No hay jugador disponible para mejorar")
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error mejorando daño: %s", str(e))

    def on_upgrade_health(self):
        """Callback para mejorar vida."""
        try:
            self.logger.info("Mejorando vida")
            if self.game_state.current_player:
                success = self.game_state.current_player.upgrade_stat("health", 1)
                if success:
                    self.logger.info("Vida mejorada")
                else:
                    self.logger.warning("No hay suficientes puntos de mejora")
            else:
                self.logger.warning("No hay jugador disponible para mejorar")
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error mejorando vida: %s", str(e))

    def on_upgrade_shield(self):
        """Callback para mejorar escudo."""
        try:
            self.logger.info("Mejorando escudo")
            if self.game_state.current_player:
                success = self.game_state.current_player.upgrade_stat("shield", 1)
                if success:
                    self.logger.info("Escudo mejorado")
                else:
                    self.logger.warning("No hay suficientes puntos de mejora")
            else:
                self.logger.warning("No hay jugador disponible para mejorar")
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error mejorando escudo: %s", str(e))

    def on_continue_after_upgrade(self):
        """Callback para continuar después de mejoras."""
        try:
            self.logger.info("Continuando después de mejoras")
            self.game_state.set_scene("game")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error continuando después de mejoras: %s", str(e))

    def on_equip_weapon(self):
        """Callback para equipar arma."""
        try:
            self.logger.info("Equipando arma")
            # TODO: Implementar sistema de equipación
            self.logger.warning("Sistema de equipación no implementado")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error equipando arma: %s", str(e))

    def on_equip_armor(self):
        """Callback para equipar armadura."""
        try:
            self.logger.info("Equipando armadura")
            # TODO: Implementar sistema de equipación
            self.logger.warning("Sistema de equipación no implementado")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error equipando armadura: %s", str(e))

    def on_equip_accessory(self):
        """Callback para equipar accesorio."""
        try:
            self.logger.info("Equipando accesorio")
            # TODO: Implementar sistema de equipación
            self.logger.warning("Sistema de equipación no implementado")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error equipando accesorio: %s", str(e))

    def get_upgrade_callbacks(self) -> dict:
        """
        Obtiene todos los callbacks de upgrades disponibles.

        Returns:
            Diccionario con callbacks de upgrades
        """
        return {
            "upgrade_speed": self.on_upgrade_speed,
            "upgrade_damage": self.on_upgrade_damage,
            "upgrade_health": self.on_upgrade_health,
            "upgrade_shield": self.on_upgrade_shield,
            "continue_after_upgrade": self.on_continue_after_upgrade,
            "equip_weapon": self.on_equip_weapon,
            "equip_armor": self.on_equip_armor,
            "equip_accessory": self.on_equip_accessory,
        }
