"""Game Scene Core - Núcleo de la Escena Principal"""

import os
import random

import pygame

from core.scene_manager import Scene
from entities.enemy import EnemyManager
from entities.player import Player
from entities.projectile import Projectile
from ui.hud import HUD
from utils.animation_manager import IntelligentAnimationManager
from utils.asset_manager import AssetManager
from utils.camera import Camera
from utils.config_manager import ConfigManager
from utils.logger import get_logger
from utils.simple_desert_background import SimpleDesertBackground
from utils.world_generator import WorldGenerator

from .game_scene_collisions import GameSceneCollisions
from .game_scene_powerups import GameScenePowerups
from .game_scene_render import GameSceneRenderer
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
        self.is_paused = False  # Estado de pausa
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

        # Configuración del mundo desde gameplay.json
        # Usar valores por defecto ya que la configuración específica no está disponible
        self.world_width = 5000
        self.world_height = 5000

        self.camera = Camera(
            screen_width=screen.get_width(),
            screen_height=screen.get_height(),
            world_width=self.world_width,
            world_height=self.world_height,
        )

        # Configuración de bordes del escenario
        self.border_thickness = 50
        self.border_color = (128, 128, 128)
        self.border_inner_color = (64, 64, 64)
        self.borders_enabled = True

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
        self.renderer = GameSceneRenderer(self, screen, self.camera)
        self.logger.info(
            "[GameScene] Submódulos integrados: waves, powerups, collisions, render"
        )

    @property
    def enemies(self):
        """Delega acceso a la lista de enemigos del enemy_manager."""
        return self.enemy_manager.enemies

    def handle_event(self, event):
        """Maneja los eventos de la escena del juego."""
        # Sistema de pausa mejorado con múltiples teclas
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                self._toggle_pause()

        # Solo loggear eventos importantes, no movimiento de mouse
        if event.type not in [pygame.MOUSEMOTION]:
            self.logger.debug("[GameScene] Evento recibido: %s", event.type)

    def _toggle_pause(self):
        """Alterna el estado de pausa del juego."""
        if not hasattr(self, "scene_manager") or not self.scene_manager:
            # Fallback: usar game_state si scene_manager no está disponible
            if hasattr(self.game_state, "scene_manager"):
                self.scene_manager = self.game_state.scene_manager
            else:
                self.logger.error("No se puede acceder al scene_manager para pausar")
                return

        if self.is_paused:
            # Reanudar juego
            self.is_paused = False
            self.logger.info("Juego reanudado")
        else:
            # Pausar juego y cambiar a escena de pausa
            self.is_paused = True
            self.logger.info("Juego pausado - cambiando a escena de pausa")
            self.scene_manager.change_scene("pause")

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = 1.0 / 60.0

        # **CRÍTICO: Procesar input del jugador**
        if self.player:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            # Player effects desde integration
            player_effects = getattr(self.player.integration, "player_effects", None)
            self.player.movement.handle_input(
                keys, mouse_pos, mouse_buttons, player_effects
            )

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
            # Aplicar colisiones con bordes del escenario
            self._enforce_world_boundaries()
        player_pos = (self.player.x, self.player.y) if self.player else None
        self.enemy_manager.update(delta_time, player_pos)
        self.waves.check_wave_completion()
        for projectile in self.projectiles[:]:
            projectile.update(delta_time)
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
            # Obtener personaje seleccionado (priorizar game_state)
            character_key = "guerrero"  # Valor por defecto

            if (
                hasattr(self.game_state, "selected_character")
                and self.game_state.selected_character
            ):
                character_key = self.game_state.selected_character
                self.logger.info("Personaje desde game_state: %s", character_key)
            elif (
                hasattr(self.game_state, "current_character")
                and self.game_state.current_character
            ):
                character_key = self.game_state.current_character
                self.logger.info("Personaje desde current_character: %s", character_key)
            else:
                self.logger.warning(
                    "No se encontró personaje seleccionado, usando: %s", character_key
                )

            # Mapeo de fallbacks para personajes alternativos
            character_fallbacks = {
                "adventureguirl": ["adventureguirl", "guerrero"],
                "robot": ["robot", "guerrero"],
                "guerrero": ["guerrero"],
            }

            # Si el personaje no está en el mapeo, usar guerrero como fallback
            if character_key not in character_fallbacks:
                self.logger.warning(
                    "Personaje %s no reconocido, usando guerrero", character_key
                )
                character_key = "guerrero"

            player_x, player_y = 2500, 2500

            # Verificar múltiples rutas posibles para los sprites
            sprite_paths = [
                f"assets/characters/used/{character_key}/idle",
                f"assets/characters/used/{character_key}/Idle",
                f"assets/characters/{character_key}/idle",
                f"assets/characters/{character_key}/Idle",
            ]

            sprite_path = None
            for path in sprite_paths:
                if os.path.exists(path):
                    sprite_path = path
                    break

            if not sprite_path:
                self.logger.error(
                    "No se encontraron sprites para %s en ninguna ruta", character_key
                )
                # Fallback al guerrero si el personaje no existe
                character_key = "guerrero"
                sprite_path = "assets/characters/used/guerrero/idle"
                if not os.path.exists(sprite_path):
                    sprite_path = "assets/characters/used/guerrero/Idle"

            self.player = Player(
                player_x, player_y, character_key, self.config, self.animation_manager
            )
            self.logger.info(
                "✅ Jugador inicializado con personaje: %s (ruta: %s)",
                character_key,
                sprite_path,
            )

        except (ImportError, FileNotFoundError) as e:
            self.logger.error("Error al inicializar jugador: %s", e)

    def _enforce_world_boundaries(self):
        """
        Mantiene al jugador dentro de los límites del mundo del escenario.
        Evita que el jugador salga del área visible y que la cámara se desoriente.
        """
        if not self.player or not self.borders_enabled:
            return

        # Definir límites del mundo (considerando el grosor de los bordes)
        # Añadir un margen extra para el tamaño del sprite del jugador
        player_size = 32  # Tamaño aproximado del sprite del jugador
        margin = self.border_thickness + player_size // 2

        min_x = margin
        min_y = margin
        max_x = self.world_width - margin
        max_y = self.world_height - margin

        # Aplicar límites al jugador con feedback visual
        player_moved = False

        if self.player.x < min_x:
            self.player.x = min_x
            player_moved = True
        elif self.player.x > max_x:
            self.player.x = max_x
            player_moved = True

        if self.player.y < min_y:
            self.player.y = min_y
            player_moved = True
        elif self.player.y > max_y:
            self.player.y = max_y
            player_moved = True

        # Log para debug cuando el jugador toca los bordes
        if player_moved:
            self.logger.debug(
                "Jugador limitado por bordes del mundo en (%d, %d)",
                self.player.x,
                self.player.y,
            )

        # Asegurar que la cámara también respete los límites
        if hasattr(self.camera, "clamp_to_world"):
            self.camera.clamp_to_world()

    def _generate_world(self):
        try:
            world_width, world_height = (
                self.screen.get_width() * 4,
                self.screen.get_height() * 4,
            )
            world_generator = WorldGenerator(
                world_width=world_width,
                world_height=world_height,
                screen_width=self.screen.get_width(),
                screen_height=self.screen.get_height(),
            )
            self.tiles = world_generator.generate_world()
            self.tiles.extend(world_generator.generate_desert_oasis(1000, 1000, 300))
            self.tiles.extend(world_generator.generate_rock_formation(4000, 1000, 250))
            self.tiles.extend(world_generator.generate_cactus_field(1000, 4000, 200))
            self.tiles.extend(world_generator.generate_ruins(4000, 4000, 280))
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
        except ImportError:
            self.logger.error("Error al generar mundo")
            self.tiles = []
