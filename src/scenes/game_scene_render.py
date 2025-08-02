"""
Módulo de renderizado para GameScene.
Maneja el renderizado de todos los elementos del juego.
"""

import logging
from typing import TYPE_CHECKING

import pygame

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
            # Renderizar fondo procedural y bordes
            self._render_procedural_background()
            self._render_world_borders()

            # Renderizar fondo de escena (si existe)
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

    def _render_procedural_background(self) -> None:
        """
        Renderiza un fondo procedural con grid y detalles aleatorios.
        """
        try:
            # Usar valores por defecto para el fondo
            base_color = (32, 48, 32)
            line_color = (48, 64, 48)
            cell_size = 100
            line_thickness = 2

            # Llenar fondo base
            self.screen.fill(base_color)

            # Obtener área visible de la cámara
            camera_rect = self.camera.get_visible_rect()

            # Calcular grid visible
            start_x = int(camera_rect.x // cell_size) * cell_size
            end_x = start_x + camera_rect.width + cell_size
            start_y = int(camera_rect.y // cell_size) * cell_size
            end_y = start_y + camera_rect.height + cell_size

            # Dibujar líneas verticales
            for x in range(start_x, end_x, cell_size):
                screen_x, screen_y = self.camera.world_to_screen(x, camera_rect.y)
                if 0 <= screen_x <= self.screen.get_width():
                    pygame.draw.line(
                        self.screen,
                        line_color,
                        (screen_x, 0),
                        (screen_x, self.screen.get_height()),
                        line_thickness,
                    )

            # Dibujar líneas horizontales
            for y in range(start_y, end_y, cell_size):
                screen_x, screen_y = self.camera.world_to_screen(camera_rect.x, y)
                if 0 <= screen_y <= self.screen.get_height():
                    pygame.draw.line(
                        self.screen,
                        line_color,
                        (0, screen_y),
                        (self.screen.get_width(), screen_y),
                        line_thickness,
                    )

        except Exception as e:
            self.logger.error("Error renderizando fondo procedural: %s", e)

    def _render_world_borders(self) -> None:
        """
        Renderiza los bordes del mundo del escenario de forma más visible.
        """
        try:
            if (
                not hasattr(self.scene, "borders_enabled")
                or not self.scene.borders_enabled
            ):
                return

            # Usar configuración unificada del mundo
            thickness = getattr(self.scene, "border_thickness", 50)
            border_color = getattr(self.scene, "border_color", (200, 200, 200))
            # Calcular color interior como versión más oscura del color principal
            inner_color = tuple(max(0, c - 70) for c in border_color)
            warning_color = (255, 255, 0)  # Amarillo para las líneas de advertencia

            world_width = getattr(self.scene, "world_width", 5120)
            world_height = getattr(self.scene, "world_height", 2880)

            # Bordes del mundo (exterior) - Más gruesos y visibles
            borders = [
                # Borde superior
                pygame.Rect(0, 0, world_width, thickness),
                # Borde inferior
                pygame.Rect(0, world_height - thickness, world_width, thickness),
                # Borde izquierdo
                pygame.Rect(0, 0, thickness, world_height),
                # Borde derecho
                pygame.Rect(world_width - thickness, 0, thickness, world_height),
            ]

            for border in borders:
                # Verificar si el borde está visible
                if self.camera.is_visible(
                    border.x, border.y, border.width, border.height
                ):
                    # Convertir a coordenadas de pantalla
                    screen_x, screen_y = self.camera.world_to_screen(border.x, border.y)
                    screen_rect = pygame.Rect(
                        screen_x, screen_y, border.width, border.height
                    )

                    # Recortar a la pantalla
                    screen_rect = screen_rect.clip(self.screen.get_rect())

                    if screen_rect.width > 0 and screen_rect.height > 0:
                        # Renderizar borde exterior (rojo visible)
                        pygame.draw.rect(self.screen, border_color, screen_rect)

                        # Renderizar borde interior (más oscuro)
                        inner_thickness = max(5, thickness // 3)
                        inner_rect = screen_rect.inflate(
                            -inner_thickness * 2, -inner_thickness * 2
                        )
                        if inner_rect.width > 0 and inner_rect.height > 0:
                            pygame.draw.rect(self.screen, inner_color, inner_rect)

                        # Línea de advertencia amarilla en el borde interior
                        warning_thickness = 2
                        warning_rect = screen_rect.inflate(
                            -warning_thickness * 4, -warning_thickness * 4
                        )
                        if warning_rect.width > 0 and warning_rect.height > 0:
                            pygame.draw.rect(
                                self.screen,
                                warning_color,
                                warning_rect,
                                warning_thickness,
                            )

        except Exception as e:
            self.logger.error("Error renderizando bordes del mundo: %s", e)
