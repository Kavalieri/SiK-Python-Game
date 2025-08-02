"""
Game Scene Powerups - Gestión de Powerups
=========================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Lógica de generación, recogida y efectos de powerups en la escena principal del juego.
"""

import random

from entities.powerup import Powerup


class GameScenePowerups:
    """
    Gestión de powerups para GameScene.
    Se integra con el núcleo mediante composición o herencia.

    Args:
        scene: Referencia al núcleo GameScene.
    """

    def __init__(self, scene):
        """
        Inicializa el gestor de powerups.

        Args:
            scene: Referencia al núcleo GameScene.
        """
        self.scene = scene  # Referencia al núcleo GameScene

    def spawn_powerup(self):
        """
        Genera un powerup aleatorio en el mundo.
        """
        try:
            x = random.randint(100, 4900)
            y = random.randint(100, 4900)
            powerup = Powerup.create_random(x, y)
            self.scene.powerups.append(powerup)
            # Corregir acceso a atributo - asegurar que powerup_type existe
            powerup_name = getattr(
                powerup.powerup_type, "value", str(powerup.powerup_type)
            )
            self.scene.logger.debug(
                "Powerup %s generado en (%s, %s)", powerup_name, x, y
            )
        except AttributeError as e:
            self.scene.logger.error(f"Error al generar powerup: {e}")

    def update_powerups(self, delta_time):
        """
        Actualiza y elimina powerups fuera de rango.

        Args:
            delta_time: Tiempo transcurrido desde el último frame.
        """
        for powerup in self.scene.powerups[:]:
            powerup.update(delta_time)
            if self._is_out_of_bounds(powerup):
                self.scene.powerups.remove(powerup)

    def apply_powerup_to_player(self):
        """
        Detecta colisión y aplica powerup al jugador.
        """
        player = self.scene.player
        if player:
            for powerup in self.scene.powerups[:]:
                if self.scene.collisions.check_collision(player, powerup):
                    powerup_effect = powerup.get_effect()
                    player.apply_powerup(powerup_effect)
                    self.scene.powerups.remove(powerup)
                    # Corregir acceso a atributo - usar lazy logging
                    effect_name = getattr(
                        powerup_effect.type, "value", str(powerup_effect.type)
                    )
                    self.scene.logger.debug("Powerup %s recolectado", effect_name)

    def _is_out_of_bounds(self, powerup):
        """
        Verifica si un powerup está fuera de los límites del mundo.

        Args:
            powerup: Objeto Powerup a verificar.

        Returns:
            bool: True si el powerup está fuera de los límites, False en caso contrario.
        """
        return (
            powerup.x < -100 or powerup.x > 5100 or powerup.y < -100 or powerup.y > 5100
        )

    def render(self, screen, camera):
        """
        Renderiza todos los powerups visibles en pantalla.

        Args:
            screen: Superficie de pantalla donde renderizar
            camera: Cámara para conversión de coordenadas
        """
        if hasattr(self.scene, "powerups") and self.scene.powerups:
            for powerup in self.scene.powerups:
                # Verificar si está visible
                if camera.is_visible(
                    powerup.x, powerup.y, powerup.width, powerup.height
                ):
                    # Convertir a coordenadas de pantalla
                    screen_x, screen_y = camera.world_to_screen(powerup.x, powerup.y)
                    # Obtener frame del powerup
                    frame = powerup.get_current_frame()
                    if frame:
                        screen.blit(frame, (screen_x, screen_y))
