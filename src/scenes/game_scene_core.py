"""Game Scene Core - Núcleo de la Escena Principal"""

import os
import random

import pygame

from ..core.scene_manager import Scene
from ..entities.enemy import EnemyManager
from ..entities.player import Player
from ..entities.projectile import Projectile
from ..ui.hud import HUD
from ..utils.animation_manager import IntelligentAnimationManager
from ..utils.asset_manager import AssetManager
from ..utils.camera import Camera
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger
from ..utils.simple_desert_background import SimpleDesertBackground
from ..utils.world_generator import WorldGenerator
from .game_scene_collisions import GameSceneCollisions
from .game_scene_powerups import GameScenePowerups
from .game_scene_render import GameSceneRender
from .game_scene_waves import GameSceneWaves


class GameScene(Scene):
    """Núcleo de la escena principal del juego. Delegación a submódulos."""

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        """Inicializa la escena principal del juego."""
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.scene_manager = None  # Definición explícita del atributo
        self.logger = get_logger("SiK_Game")
        self.logger.info("[GameScene] Escena de nivel inicializada (núcleo)")
        # Inicialización de entidades y managers
        self.asset_manager = AssetManager()
        self.animation_manager = IntelligentAnimationManager(self.asset_manager)
        self.player = None
        self.enemy_manager = EnemyManager(self.animation_manager)
        self.projectiles: list[Projectile] = []
        self.powerups = []
        self.tiles = []
        self.hud = HUD(screen, config, game_state)
        self.camera = Camera(
            screen_width=screen.get_width(),
            screen_height=screen.get_height(),
            world_width=5000,
            world_height=5000,
        )

        # Variables de gameplay
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 2000
        self.max_enemies = 5
        self.wave_number = 1
        self.enemies_per_wave = 10
        self.enemies_spawned_this_wave = 0
        self.wave_completed = False
        self.powerup_spawn_timer = 0
        self.powerup_spawn_delay = 10000
        self.powerup_spawn_chance = 0.3
        self.background = None

        self._generate_world()
        self._load_background()
        self._initialize_player()

        # Integración de submódulos
        self.waves = GameSceneWaves(self)
        self.powerups_manager = GameScenePowerups(self)
        self.collisions = GameSceneCollisions(self)
        self.renderer = GameSceneRender(self)
        self.logger.info(
            "[GameScene] Submódulos integrados: waves, powerups, collisions, render"
        )

    def handle_event(self, event: pygame.event.Event):
        """Maneja eventos de entrada del usuario."""
        self.logger.info("[GameScene] Evento recibido: %s - %s", event.type, event)
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:  # pylint: disable=no-member
                self.logger.info("Juego pausado")
                if hasattr(self, "scene_manager") and self.scene_manager:
                    try:
                        self.scene_manager.change_scene("pause")
                    except AttributeError as e:
                        self.logger.error("Error al cambiar de escena: %s", e)
        if self.player:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            self.player.handle_input(keys, mouse_pos, mouse_buttons)
            if mouse_buttons[0]:
                enemies = getattr(self, "enemies", [])
                results = self.player.attack(mouse_pos, enemies)
                for obj in results:
                    if (
                        hasattr(obj, "entity_type")
                        and obj.entity_type.name == "PROJECTILE"
                    ):
                        self.projectiles.append(obj)

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = 1.0 / 60.0
        if self.background and hasattr(self.background, "update"):
            self.background.update(delta_time)
        elif self.background is None:
            self.logger.warning(
                "No se ha inicializado un fondo válido para actualizar."
            )
        if self.player:
            self.camera.follow_target(self.player.x, self.player.y)
        self.camera.update(delta_time)
        if self.player:
            self.player.update(delta_time)
        player_pos = (self.player.x, self.player.y) if self.player else None
        self.enemy_manager.update(delta_time, player_pos)
        self.waves.check_wave_completion()
        for projectile in self.projectiles[:]:
            projectile.update(delta_time)
        self.powerups_manager.update_powerups(delta_time)
        if (
            current_time - self.powerup_spawn_timer > self.powerup_spawn_delay
            and random.random() < self.powerup_spawn_chance
        ):
            self.powerups_manager.spawn_powerup()
            self.powerup_spawn_timer = current_time
        self.collisions.check_all_collisions()
        self.powerups_manager.apply_powerup_to_player()
        self.hud.update(delta_time)
        if self.player:
            self.game_state.current_player = self.player
        if self.game_state.lives <= 0:
            self.logger.info("Game Over")

    def render(self):
        self.renderer.render_scene()

    def _load_background(self):
        try:
            self.background = SimpleDesertBackground(
                screen_width=self.screen.get_width(),
                screen_height=self.screen.get_height(),
            )
            self.logger.info("Fondo simple de desierto cargado correctamente")
        except ImportError:
            self.logger.error("Error al cargar fondo simple")
            self.background = None

    def _initialize_player(self):
        try:
            character_key = (
                getattr(self.game_state, "selected_character", None) or "guerrero"
            )
            player_x, player_y = 2500, 2500
            sprite_path = f"assets/characters/used/{character_key}/idle"
            if not os.path.exists(sprite_path):
                sprite_path = f"assets/characters/used/{character_key}/Idle"
            if not os.path.exists(sprite_path):
                raise FileNotFoundError(f"Sprites no encontrados en {sprite_path}")
            self.player = Player(
                player_x, player_y, character_key, self.config, self.animation_manager
            )
            self.logger.info("Jugador inicializado con personaje: %s", character_key)
        except (ImportError, FileNotFoundError):
            self.logger.error("Error al inicializar jugador")

    def _generate_world(self):
        print("--- Iniciando _generate_world ---")
        try:
            world_width, world_height = (
                self.screen.get_width() * 4,
                self.screen.get_height() * 4,
            )
            print(f"Dimensiones del mundo: {world_width}x{world_height}")
            world_generator = WorldGenerator(
                world_width=world_width,
                world_height=world_height,
                screen_width=self.screen.get_width(),
                screen_height=self.screen.get_height(),
            )
            print("Generador del mundo creado.")
            self.tiles = world_generator.generate_world()
            print(f"Generados {len(self.tiles)} tiles base.")
            self.tiles.extend(world_generator.generate_desert_oasis(1000, 1000, 300))
            print(f"Añadido oasis. Total tiles: {len(self.tiles)}")
            self.tiles.extend(world_generator.generate_rock_formation(4000, 1000, 250))
            print(f"Añadida formación rocosa. Total tiles: {len(self.tiles)}")
            self.tiles.extend(world_generator.generate_cactus_field(1000, 4000, 200))
            print(f"Añadido campo de cactus. Total tiles: {len(self.tiles)}")
            self.tiles.extend(world_generator.generate_ruins(4000, 4000, 280))
            print(f"Añadidas ruinas. Total tiles: {len(self.tiles)}")
            if self.camera:
                self.camera.world_width, self.camera.world_height = (
                    world_width,
                    world_height,
                )
            self.logger.info(
                "Mundo generado con %d elementos - Tamaño: %dx%d",
                len(self.tiles),
                world_width,
                world_height,
            )
            print("--- _generate_world completado ---")
        except ImportError:
            self.logger.error("Error al generar mundo")
            print("!!! Error al generar mundo !!!")
            self.tiles = []
