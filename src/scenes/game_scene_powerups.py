"""
Game Scene Powerups - Gestión de Powerups
=========================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Lógica de generación, recogida y efectos de powerups en la escena principal del juego.
"""

import random
from ..entities.powerup import Powerup


class GameScenePowerups:
    """
    Gestión de powerups para GameScene.
    Se integra con el núcleo mediante composición o herencia.
    """

    def __init__(self, scene):
        self.scene = scene  # Referencia al núcleo GameScene

    def spawn_powerup(self):
        """Genera un powerup aleatorio en el mundo."""
        try:
            x = random.randint(100, 4900)
            y = random.randint(100, 4900)
            powerup = Powerup.create_random(x, y)
            self.scene.powerups.append(powerup)
            self.scene.logger.debug(
                f"Powerup {powerup.powerup_type.value} generado en ({x}, {y})"
            )
        except Exception as e:
            self.scene.logger.error(f"Error al generar powerup: {e}")

    def update_powerups(self, delta_time):
        """Actualiza y elimina powerups fuera de rango."""
        for powerup in self.scene.powerups[:]:
            powerup.update(delta_time)
            if (
                powerup.x < -100
                or powerup.x > 5100
                or powerup.y < -100
                or powerup.y > 5100
            ):
                self.scene.powerups.remove(powerup)

    def apply_powerup_to_player(self):
        """Detecta colisión y aplica powerup al jugador."""
        player = self.scene.player
        if player:
            for powerup in self.scene.powerups[:]:
                if self.scene.collisions.check_collision(player, powerup):
                    powerup_effect = powerup.get_effect()
                    player.apply_powerup(powerup_effect)
                    self.scene.powerups.remove(powerup)
                    self.scene.logger.debug(
                        f"Powerup {powerup_effect.type.value} recolectado"
                    )
