"""
Game Scene Render - Renderizado de la Escena Principal
=====================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Lógica de renderizado de la escena principal y sus entidades.
"""


class GameSceneRender:
    """
    Renderizado de la escena principal del juego.
    Se integra con el núcleo mediante composición o herencia.
    """

    def __init__(self, scene):
        self.scene = scene  # Referencia al núcleo GameScene

    def render_scene(self):
        """Renderiza fondo, entidades, proyectiles, powerups, tiles y HUD."""
        scene = self.scene
        # Renderizar fondo
        if scene.background:
            scene.background.render(scene.screen)
        else:
            scene.screen.fill((135, 206, 235))
        # Renderizar enemigos
        camera_offset = (scene.camera.x, scene.camera.y)
        scene.enemy_manager.render(scene.screen, camera_offset)
        # Renderizar proyectiles
        for projectile in scene.projectiles:
            if scene.camera.is_visible(
                projectile.x, projectile.y, projectile.width, projectile.height
            ):
                screen_x, screen_y = scene.camera.world_to_screen(
                    projectile.x, projectile.y
                )
                projectile.render(scene.screen, (screen_x, screen_y))
        # Renderizar powerups
        for powerup in scene.powerups:
            if scene.camera.is_visible(
                powerup.x, powerup.y, powerup.width, powerup.height
            ):
                screen_x, screen_y = scene.camera.world_to_screen(powerup.x, powerup.y)
                powerup.render(scene.screen, (screen_x, screen_y))
        # Renderizar tiles
        for tile in scene.tiles:
            if scene.camera.is_visible(tile.x, tile.y, tile.width, tile.height):
                screen_x, screen_y = scene.camera.world_to_screen(tile.x, tile.y)
                tile.render(scene.screen, (screen_x, screen_y))
        # Renderizar jugador
        if scene.player:
            if scene.camera.is_visible(
                scene.player.x, scene.player.y, scene.player.width, scene.player.height
            ):
                screen_x, screen_y = scene.camera.world_to_screen(
                    scene.player.x, scene.player.y
                )
                scene.player.render(scene.screen, (screen_x, screen_y))
        # Renderizar HUD
        scene.hud.render()
