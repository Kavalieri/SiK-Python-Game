"""
Módulo de renderizado para GameScene.
Maneja el renderizado de todos los elementos del juego.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scenes.game_scene_core import GameScene


class GameSceneRenderer:
    """Renderizador para la escena del juego."""

    def __init__(self, scene: "GameScene", screen, camera):
        """
        Inicializa el renderizador.

        Args:
            scene: Escena del juego
            screen: Superficie de pygame
            camera: Sistema de cámara
        """
        self.scene = scene
        self.screen = screen
        self.camera = camera
        self.logger = logging.getLogger("render_loops")

    def render_scene(self) -> None:
        """Renderiza todos los elementos de la escena."""
        try:
            # Renderizar fondo
            self._render_background()

            # Renderizar enemigos
            self._render_enemies()

            # Renderizar tiles del mundo
            self._render_world_tiles()

            # Renderizar jugador
            self._render_player()

            # Renderizar proyectiles
            self._render_projectiles()

            # Renderizar powerups
            self._render_powerups()

            # Renderizar HUD
            self._render_hud()

        except Exception as e:
            self.logger.error("Error crítico en render_scene: %s", e)

    def _render_background(self) -> None:
        """Renderiza el fondo de la escena."""
        if hasattr(self.scene, "background") and self.scene.background:
            self.scene.background.render(self.screen, self.camera)

    def _render_enemies(self) -> None:
        """Renderiza todos los enemigos en pantalla."""
        try:
            if (
                hasattr(self.scene, "enemy_manager")
                and self.scene.enemy_manager.enemies
            ):
                for enemy in self.scene.enemy_manager.enemies:
                    self.camera.render_entity(self.screen, enemy)
        except Exception as e:
            self.logger.error("Error renderizando enemigos: %s", e)

    def _render_world_tiles(self) -> None:
        """Renderiza los tiles del mundo."""
        if hasattr(self.scene, "tiles") and self.scene.tiles:
            for tile in self.scene.tiles:
                if self.camera.is_in_view(tile.x, tile.y, tile.width, tile.height):
                    self.camera.render_entity(self.screen, tile)

    def _render_player(self) -> None:
        """Renderiza el jugador."""
        try:
            if self.scene.player:
                self.camera.render_entity(self.screen, self.scene.player)
        except Exception as e:
            self.logger.error("Error renderizando jugador: %s", e)

    def _render_projectiles(self) -> None:
        """Renderiza los proyectiles."""
        if hasattr(self.scene, "projectiles") and self.scene.projectiles:
            for projectile in self.scene.projectiles:
                self.camera.render_entity(self.screen, projectile)

    def _render_powerups(self) -> None:
        """Renderiza los powerups."""
        if hasattr(self.scene, "powerups_manager") and self.scene.powerups_manager:
            self.scene.powerups_manager.render(self.screen, self.camera)

    def _render_hud(self) -> None:
        """Renderiza la interfaz de usuario."""
        if hasattr(self.scene, "hud") and self.scene.hud:
            self.scene.hud.render(self.screen)
