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

    Args:
        scene: Referencia al núcleo GameScene.
    """

    def __init__(self, scene):
        """
        Inicializa el gestor de renderizado.

        Args:
            scene: Referencia al núcleo GameScene.
        """
        self.scene = scene  # Referencia al núcleo GameScene

    def render_scene(self):
        """
        Renderiza fondo, entidades, proyectiles, powerups, tiles y HUD.
        """
        scene = self.scene
        # Renderizar fondo
        if scene.background:
            scene.background.render(scene.screen)
        else:
            scene.screen.fill((135, 206, 235))
        # Renderizar entidades
        self._render_entities(scene.enemy_manager, scene.screen, scene.camera)
        self._render_entities(scene.projectiles, scene.screen, scene.camera)
        self._render_entities(scene.powerups, scene.screen, scene.camera)
        self._render_entities(scene.tiles, scene.screen, scene.camera)
        # Renderizar jugador
        if scene.player:
            self._render_entity(scene.player, scene.screen, scene.camera)
        # Renderizar HUD
        scene.hud.render()

    def _render_entities(self, entities, screen, camera):
        """
        Renderiza una lista de entidades visibles en la cámara.

        Args:
            entities: Lista de entidades a renderizar.
            screen: Superficie de la pantalla.
            camera: Cámara del juego.
        """
        for entity in entities:
            self._render_entity(entity, screen, camera)

    def _render_entity(self, entity, screen, camera):
        """
        Renderiza una entidad si es visible en la cámara.

        Args:
            entity: Entidad a renderizar.
            screen: Superficie de la pantalla.
            camera: Cámara del juego.
        """
        if camera.is_visible(entity.x, entity.y, entity.width, entity.height):
            screen_x, screen_y = camera.world_to_screen(entity.x, entity.y)
            entity.render(screen, (screen_x, screen_y))
