"""
Game Scene Collisions - Colisiones de la Escena Principal
========================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Lógica de detección y resolución de colisiones en la escena principal del juego.
"""

import pygame


class GameSceneCollisions:
    """
    Gestión de colisiones para GameScene.
    Se integra con el núcleo mediante composición o herencia.
    """

    def __init__(self, scene):
        self.scene = scene  # Referencia al núcleo GameScene

    def check_collision(self, entity1, entity2) -> bool:
        """
        Verifica si dos entidades colisionan usando rectángulos.

        Args:
            entity1: Primera entidad con atributos x, y, width, height.
            entity2: Segunda entidad con atributos x, y, width, height.

        Returns:
            bool: True si las entidades colisionan, False en caso contrario.
        """
        if not entity1 or not entity2:
            return False
        rect1 = pygame.Rect(entity1.x, entity1.y, entity1.width, entity1.height)
        rect2 = pygame.Rect(entity2.x, entity2.y, entity2.width, entity2.height)
        return rect1.colliderect(rect2)

    def check_all_collisions(self):
        """
        Detecta y maneja colisiones entre entidades en la escena.

        Incluye colisiones entre:
        - Proyectiles y enemigos.
        - Jugador y enemigos.
        - Jugador y tiles.
        """
        self._handle_projectile_enemy_collisions()
        self._handle_player_enemy_collisions()
        self._handle_player_tile_collisions()

    def _handle_projectile_enemy_collisions(self):
        """Maneja colisiones entre proyectiles y enemigos."""
        for projectile in self.scene.projectiles[:]:
            enemies_in_range = self.scene.enemy_manager.get_enemies_in_range(
                (projectile.x, projectile.y), 30
            )
            for enemy in enemies_in_range:
                if self.check_collision(projectile, enemy):
                    enemy.take_damage(projectile.damage)
                    projectile.alive = False
                    if enemy.is_dead:
                        self.scene.game_state.add_score(10)
                        self.scene.logger.debug(
                            f"Enemigo eliminado. Puntuación: {self.scene.game_state.score}"
                        )
                    break

    def _handle_player_enemy_collisions(self):
        """Maneja colisiones entre el jugador y enemigos."""
        if self.scene.player:
            enemies_in_range = self.scene.enemy_manager.get_enemies_in_range(
                (self.scene.player.x, self.scene.player.y), 50
            )
            for enemy in enemies_in_range:
                if self.check_collision(self.scene.player, enemy):
                    if enemy.is_attack_ready():
                        damage = enemy.damage
                        if self.scene.player.take_damage(damage):
                            self.scene.game_state.lose_life()
                            self.scene.logger.debug(
                                f"Jugador dañado. Vidas: {self.scene.game_state.lives}"
                            )
                        enemy.reset_attack_state()

    def _handle_player_tile_collisions(self):
        """Maneja colisiones entre el jugador y tiles."""
        if self.scene.player:
            for tile in self.scene.tiles:
                if tile.has_collision() and self.check_collision(
                    self.scene.player, tile
                ):
                    self.resolve_tile_collision(self.scene.player, tile)

    def resolve_tile_collision(self, player, tile):
        """
        Resuelve la colisión entre el jugador y un tile.

        Empuja al jugador fuera del tile y lo mantiene dentro de los límites del mundo.

        Args:
            player: El jugador que colisiona.
            tile: El tile con el que colisiona el jugador.
        """
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2
        tile_center_x = tile.x + tile.width // 2
        tile_center_y = tile.y + tile.height // 2
        dx = player_center_x - tile_center_x
        dy = player_center_y - tile_center_y
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 0:
            dx /= distance
            dy /= distance
            push_distance = 5
            player.x += dx * push_distance
            player.y += dy * push_distance
            player.clamp_position()  # Usar un método público en lugar de uno protegido
