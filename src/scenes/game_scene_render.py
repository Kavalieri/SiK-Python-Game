"""
Módulo de renderizado para GameScene.
Maneja el renderizado de todos los elementos del juego.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenes.game_scene_core import GameScene


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
                    # Verificar si está visible
                    if self.camera.is_visible(
                        enemy.x, enemy.y, enemy.width, enemy.height
                    ):
                        # Convertir a coordenadas de pantalla
                        screen_x, screen_y = self.camera.world_to_screen(
                            enemy.x, enemy.y
                        )
                        # Obtener frame actual del enemigo
                        frame = enemy.get_current_frame()
                        if frame:
                            self.screen.blit(frame, (screen_x, screen_y))
        except Exception as e:
            self.logger.error("Error renderizando enemigos: %s", e)

    def _render_world_tiles(self) -> None:
        """Renderiza los tiles del mundo."""
        if hasattr(self.scene, "tiles") and self.scene.tiles:
            rendered_count = 0
            total_tiles = len(self.scene.tiles)

            for tile in self.scene.tiles:
                if self.camera.is_visible(tile.x, tile.y, tile.width, tile.height):
                    # Convertir a coordenadas de pantalla
                    screen_x, screen_y = self.camera.world_to_screen(tile.x, tile.y)
                    # Renderizar tile usando sprite (no image)
                    if hasattr(tile, "sprite") and tile.sprite:
                        self.screen.blit(tile.sprite, (screen_x, screen_y))
                        rendered_count += 1

            # Log cada 60 frames (aprox. 1 segundo a 60 FPS)
            if hasattr(self, "_tile_debug_counter"):
                self._tile_debug_counter += 1
            else:
                self._tile_debug_counter = 1

            if self._tile_debug_counter % 60 == 0:
                self.logger.debug(f"Tiles renderizados: {rendered_count}/{total_tiles}")
        else:
            if hasattr(self, "_no_tiles_logged"):
                pass  # Ya loggeado
            else:
                self._no_tiles_logged = True
                self.logger.warning(
                    "No hay tiles para renderizar o scene.tiles no existe"
                )

    def _render_player(self) -> None:
        """Renderiza el jugador."""
        try:
            if self.scene.player:
                # Verificar si está visible
                if self.camera.is_visible(
                    self.scene.player.x,
                    self.scene.player.y,
                    self.scene.player.width,
                    self.scene.player.height,
                ):
                    # Convertir a coordenadas de pantalla
                    screen_x, screen_y = self.camera.world_to_screen(
                        self.scene.player.x, self.scene.player.y
                    )
                    # Obtener frame actual del jugador
                    frame = self.scene.player.get_current_frame()
                    if frame:
                        self.screen.blit(frame, (screen_x, screen_y))
        except Exception as e:
            self.logger.error("Error renderizando jugador: %s", e)

    def _render_projectiles(self) -> None:
        """Renderiza los proyectiles."""
        if hasattr(self.scene, "projectiles") and self.scene.projectiles:
            for projectile in self.scene.projectiles:
                # Verificar si está visible
                if self.camera.is_visible(
                    projectile.x, projectile.y, projectile.width, projectile.height
                ):
                    # Convertir a coordenadas de pantalla
                    screen_x, screen_y = self.camera.world_to_screen(
                        projectile.x, projectile.y
                    )
                    # Obtener frame del proyectil
                    frame = projectile.get_current_frame()
                    if frame:
                        self.screen.blit(frame, (screen_x, screen_y))

    def _render_powerups(self) -> None:
        """Renderiza los powerups."""
        if hasattr(self.scene, "powerups_manager") and self.scene.powerups_manager:
            self.scene.powerups_manager.render(self.screen, self.camera)

    def _render_hud(self) -> None:
        """Renderiza la interfaz de usuario."""
        if hasattr(self.scene, "hud") and self.scene.hud:
            self.scene.hud.render(self.screen)
