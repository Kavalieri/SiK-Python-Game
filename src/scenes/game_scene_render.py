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
        """Renderiza todos los elementos de la escena del juego."""
        print("--- Iniciando render_scene ---")
        # Renderizar el fondo
        if self.scene.background:
            self.scene.background.render(self.scene.screen, self.scene.camera)
            print("Fondo renderizado.")

        # Renderizar entidades
        self._render_entities(self.scene.tiles, self.scene.screen, self.scene.camera)
        self._render_entities(self.scene.enemy_manager.enemies, self.scene.screen, self.scene.camera)
        self._render_entities(self.scene.projectiles, self.scene.screen, self.scene.camera)
        self._render_entities(self.scene.powerups, self.scene.screen, self.scene.camera)

        # Renderizar jugador
        if self.scene.player:
            self._render_entity(self.scene.player, self.scene.screen, self.scene.camera)

        # Renderizar HUD
        if self.scene.hud:
            self.scene.hud.render(self.scene.screen)
            print("HUD renderizado.")
        
        print(f"Posición de la cámara: {self.scene.camera.x}, {self.scene.camera.y}")
        print("--- render_scene completado ---")

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
