"""
Game Scene - Escena Principal del Juego
=====================================

Autor: SiK Team
Fecha: 2024
Descripción: Escena principal donde se desarrolla la acción del juego.
"""

import pygame
import logging
from typing import Optional, List
import random

from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..utils.asset_manager import AssetManager
from ..utils.animation_manager import AnimationManager
from ..entities.player import Player
from ..entities.enemy import Enemy
from ..ui.hud import HUD
from ..entities.projectile import Projectile
from ..entities.powerup import Powerup, PowerupType
from ..entities.tile import Tile, TileType
from ..entities.enemy_types import EnemyTypes, EnemyRarity
from ..utils.camera import Camera
from ..utils.world_generator import WorldGenerator
from ..utils.desert_background import DesertBackground


class GameScene(Scene):
	"""
	Escena principal del juego donde se desarrolla la acción.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager):
		"""
		Inicializa la escena del juego.
		
		Args:
			screen: Superficie de Pygame donde renderizar
			config: Configuración del juego
			game_state: Estado del juego
			save_manager: Gestor de guardado
		"""
		super().__init__(screen, config)
		self.game_state = game_state
		self.save_manager = save_manager
		self.logger = logging.getLogger(__name__)
		
		# Inicializar gestores
		self.asset_manager = AssetManager()
		self.animation_manager = AnimationManager(config, self.asset_manager)
		
		# Entidades del juego
		self.player = None
		self.enemies: List[Enemy] = []
		self.projectiles: List[Projectile] = []
		self.powerups = []
		self.tiles = []
		
		# HUD
		self.hud = HUD(screen, config, game_state)
		
		# Sistema de cámara
		self.camera = Camera(
			screen_width=self.screen.get_width(),
			screen_height=self.screen.get_height(),
			world_width=5000,
			world_height=5000
		)
		
		# Configuración del juego
		self.enemy_spawn_timer = 0
		self.enemy_spawn_delay = 2000  # 2 segundos
		self.max_enemies = 5
		self.wave_number = 1
		self.enemies_per_wave = 10
		self.enemies_spawned_this_wave = 0
		self.wave_completed = False
		
		# Configuración de powerups
		self.powerup_spawn_timer = 0
		self.powerup_spawn_delay = 10000  # 10 segundos
		self.powerup_spawn_chance = 0.3  # 30% de probabilidad
		
		# Generar mundo con nuevo generador
		self._generate_world()
		
		# Fondo
		self.background = None
		self._load_background()
		
		# Inicializar jugador
		self._initialize_player()
		
		self.logger.info("Escena del juego inicializada")
	
	def _load_background(self):
		"""Carga el fondo simple de desierto."""
		try:
			# Crear fondo simple de desierto
			from ..utils.simple_desert_background import SimpleDesertBackground
			self.background = SimpleDesertBackground(
				screen_width=self.screen.get_width(),
				screen_height=self.screen.get_height()
			)
			self.logger.info("Fondo simple de desierto cargado correctamente")
		except Exception as e:
			self.logger.error(f"Error al cargar fondo simple: {e}")
			# Crear fondo por defecto
			self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
			self.background.fill((135, 206, 235))  # Azul cielo
	
	def _initialize_player(self):
		"""Inicializa el jugador."""
		try:
			# Usar el personaje seleccionado en el GameState, o 'guerrero' por defecto
			character_key = getattr(self.game_state, 'selected_character', None) or 'guerrero'
			player_x = 2500  # Centro del mundo
			player_y = 2500
			self.player = Player(player_x, player_y, character_key, self.config, self.animation_manager)
			self.logger.info(f"Jugador inicializado con personaje: {character_key}")
		except Exception as e:
			self.logger.error(f"Error al inicializar jugador: {e}")
	
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
				# Pausar juego
				self.logger.info("Juego pausado")
				# Cambiar a la escena de pausa
				if hasattr(self, 'scene_manager') and self.scene_manager:
					self.scene_manager.change_scene('pause')
		
		# Pasar eventos al jugador usando handle_input
		if self.player:
			keys = pygame.key.get_pressed()
			mouse_pos = pygame.mouse.get_pos()
			mouse_buttons = pygame.mouse.get_pressed()
			self.player.handle_input(keys, mouse_pos, mouse_buttons)
			
			# Disparar con clic izquierdo
			if mouse_buttons[0]:  # Clic izquierdo
				projectile = self.player.shoot(mouse_pos)
				if projectile:
					self.projectiles.append(projectile)
	
	def update(self):
		"""Actualiza la lógica del juego."""
		current_time = pygame.time.get_ticks()
		delta_time = 1.0 / 60.0  # Asumiendo 60 FPS
		
		# Actualizar fondo de desierto
		if self.background:
			self.background.update(delta_time)
		
		# Actualizar cámara para seguir al jugador
		if self.player:
			self.camera.follow_target(self.player.x, self.player.y)
		self.camera.update(delta_time)
		
		# Actualizar jugador
		if self.player:
			self.player.update(delta_time)
		
		# Generar enemigos
		if (current_time - self.enemy_spawn_timer > self.enemy_spawn_delay and 
			len(self.enemies) < self.max_enemies and 
			self.enemies_spawned_this_wave < self.enemies_per_wave):
			self._spawn_enemy()
			self.enemy_spawn_timer = current_time
		
		# Verificar completación de oleada
		self._check_wave_completion()
		
		# Actualizar enemigos
		for enemy in self.enemies[:]:
			enemy.update(delta_time)
			
			# Eliminar enemigos que salen del mundo
			if enemy.x < -100 or enemy.x > 5100 or enemy.y < -100 or enemy.y > 5100:
				self.enemies.remove(enemy)
				self.game_state.lose_life()
		
		# Actualizar proyectiles
		for projectile in self.projectiles[:]:
			projectile.update(delta_time)
			
			# Eliminar proyectiles que salen de pantalla o impactan
			if not projectile.alive:
				self.projectiles.remove(projectile)
		
		# Actualizar powerups
		for powerup in self.powerups[:]:
			powerup.update(delta_time)
			
			# Eliminar powerups que han estado demasiado tiempo
			if powerup.x < -100 or powerup.x > 5100 or powerup.y < -100 or powerup.y > 5100:
				self.powerups.remove(powerup)
		
		# Generar powerups
		if (current_time - self.powerup_spawn_timer > self.powerup_spawn_delay and 
			random.random() < self.powerup_spawn_chance):
			self._spawn_powerup()
			self.powerup_spawn_timer = current_time
		
		# Detectar colisiones
		self._check_collisions()
		
		# Actualizar HUD
		self.hud.update()
		
		# Conectar jugador actual al HUD para efectos
		if self.player:
			self.game_state.current_player = self.player
		
		# Verificar game over
		if self.game_state.lives <= 0:
			self.logger.info("Game Over")
			# Aquí se cambiaría a la escena de game over
	
	def render(self):
		"""Renderiza la escena del juego."""
		# Renderizar fondo simple de desierto
		if self.background:
			# Para el fondo simple, no necesitamos offset de cámara
			self.background.render(self.screen)
		else:
			self.screen.fill((135, 206, 235))  # Azul cielo
		
		# Renderizar entidades usando coordenadas de pantalla
		for enemy in self.enemies:
			if self.camera.is_visible(enemy.x, enemy.y, enemy.width, enemy.height):
				screen_x, screen_y = self.camera.world_to_screen(enemy.x, enemy.y)
				enemy.render(self.screen, (screen_x, screen_y))
		
		for projectile in self.projectiles:
			if self.camera.is_visible(projectile.x, projectile.y, projectile.width, projectile.height):
				screen_x, screen_y = self.camera.world_to_screen(projectile.x, projectile.y)
				projectile.render(self.screen, (screen_x, screen_y))
		
		# Renderizar powerups
		for powerup in self.powerups:
			if self.camera.is_visible(powerup.x, powerup.y, powerup.width, powerup.height):
				screen_x, screen_y = self.camera.world_to_screen(powerup.x, powerup.y)
				powerup.render(self.screen, (screen_x, screen_y))
		
		# Renderizar tiles (solo los visibles)
		for tile in self.tiles:
			if self.camera.is_visible(tile.x, tile.y, tile.width, tile.height):
				screen_x, screen_y = self.camera.world_to_screen(tile.x, tile.y)
				tile.render(self.screen, (screen_x, screen_y))
		
		if self.player:
			if self.camera.is_visible(self.player.x, self.player.y, self.player.width, self.player.height):
				screen_x, screen_y = self.camera.world_to_screen(self.player.x, self.player.y)
				self.player.render(self.screen, (screen_x, screen_y))
		
		# Renderizar HUD
		self.hud.render()
	
	def _spawn_enemy(self):
		"""Genera un nuevo enemigo."""
		try:
			# Generar enemigo en los bordes del mundo visible
			spawn_side = random.randint(0, 3)  # 0: arriba, 1: derecha, 2: abajo, 3: izquierda
			
			if spawn_side == 0:  # Arriba
				x = random.randint(0, 5000)
				y = -50
			elif spawn_side == 1:  # Derecha
				x = 5050
				y = random.randint(0, 5000)
			elif spawn_side == 2:  # Abajo
				x = random.randint(0, 5000)
				y = 5050
			else:  # Izquierda
				x = -50
				y = random.randint(0, 5000)
			
			# Seleccionar tipo de enemigo basado en la oleada
			enemy_config = self._select_enemy_for_wave()
			
			# Crear enemigo con configuración específica
			enemy = Enemy(x, y, self.asset_manager, self.animation_manager, self.config, self.player, enemy_config)
			
			self.enemies.append(enemy)
			self.enemies_spawned_this_wave += 1
			self.logger.debug(f"Enemigo {enemy_config.name} generado en ({x}, {y}) - Oleada {self.wave_number}")
		except Exception as e:
			self.logger.error(f"Error al generar enemigo: {e}")
	
	def _select_enemy_for_wave(self):
		"""Selecciona el tipo de enemigo basado en la oleada actual."""
		# Ajustar probabilidades según la oleada
		if self.wave_number <= 3:
			# Oleadas 1-3: Solo enemigos normales
			return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
		elif self.wave_number <= 6:
			# Oleadas 4-6: Enemigos normales y raros
			rand = random.random()
			if rand < 0.8:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
			else:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.RARE) or EnemyTypes.ZOMBIE_RARE
		elif self.wave_number <= 10:
			# Oleadas 7-10: Enemigos normales, raros y elite
			rand = random.random()
			if rand < 0.6:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
			elif rand < 0.9:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.RARE) or EnemyTypes.ZOMBIE_RARE
			else:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.ELITE) or EnemyTypes.ZOMBIE_ELITE
		else:
			# Oleadas 11+: Todos los tipos, incluyendo legendarios
			rand = random.random()
			if rand < 0.5:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
			elif rand < 0.8:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.RARE) or EnemyTypes.ZOMBIE_RARE
			elif rand < 0.95:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.ELITE) or EnemyTypes.ZOMBIE_ELITE
			else:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.LEGENDARY) or EnemyTypes.ZOMBIE_LEGENDARY
	
	def _check_wave_completion(self):
		"""Verifica si la oleada actual está completada."""
		if (self.enemies_spawned_this_wave >= self.enemies_per_wave and 
			len(self.enemies) == 0 and 
			not self.wave_completed):
			
			self.wave_completed = True
			self.wave_number += 1
			self.enemies_spawned_this_wave = 0
			self.enemies_per_wave = min(10 + self.wave_number * 2, 50)  # Máximo 50 enemigos por oleada
			
			self.logger.info(f"¡Oleada {self.wave_number - 1} completada! Iniciando oleada {self.wave_number}")
			
			# Dar tiempo entre oleadas
			self.enemy_spawn_timer = pygame.time.get_ticks() + 3000  # 3 segundos de pausa
	
	def _spawn_powerup(self):
		"""Genera un powerup aleatorio."""
		try:
			# Generar powerup en posición aleatoria del mundo
			x = random.randint(100, 4900)
			y = random.randint(100, 4900)
			
			# Crear powerup aleatorio
			powerup = Powerup.create_random(x, y)
			
			self.powerups.append(powerup)
			self.logger.debug(f"Powerup {powerup.powerup_type.value} generado en ({x}, {y})")
		except Exception as e:
			self.logger.error(f"Error al generar powerup: {e}")
	
	def _generate_world(self):
		"""Genera el mundo con elementos distribuidos."""
		try:
			# Calcular tamaño del mundo (3-4 veces la pantalla)
			world_width = self.screen.get_width() * 4
			world_height = self.screen.get_height() * 4
			
			# Crear generador de mundo con nuevo constructor
			world_generator = WorldGenerator(
				world_width=world_width,
				world_height=world_height,
				screen_width=self.screen.get_width(),
				screen_height=self.screen.get_height()
			)
			
			# Generar elementos básicos distribuidos
			self.tiles = world_generator.generate_world()
			
			# Generar áreas especiales del desierto
			oasis_elements = world_generator.generate_desert_oasis(1000, 1000, 300)
			rock_formation = world_generator.generate_rock_formation(4000, 1000, 250)
			cactus_field = world_generator.generate_cactus_field(1000, 4000, 200)
			ruins = world_generator.generate_ruins(4000, 4000, 280)
			
			# Añadir elementos especiales
			self.tiles.extend(oasis_elements)
			self.tiles.extend(rock_formation)
			self.tiles.extend(cactus_field)
			self.tiles.extend(ruins)
			
			# Actualizar configuración del mundo para el jugador y cámara
			if self.player:
				self.player.world_width = world_width
				self.player.world_height = world_height
			
			if self.camera:
				self.camera.world_width = world_width
				self.camera.world_height = world_height
			
			self.logger.info(f"Mundo generado con {len(self.tiles)} elementos - Tamaño: {world_width}x{world_height}")
		except Exception as e:
			self.logger.error(f"Error al generar mundo: {e}")
			self.tiles = []
	
	def _check_collision(self, entity1, entity2) -> bool:
		"""
		Verifica si dos entidades colisionan.
		
		Args:
			entity1: Primera entidad
			entity2: Segunda entidad
			
		Returns:
			True si colisionan
		"""
		if not entity1 or not entity2:
			return False
		
		# Verificar colisión usando rectángulos
		rect1 = pygame.Rect(entity1.x, entity1.y, entity1.width, entity1.height)
		rect2 = pygame.Rect(entity2.x, entity2.y, entity2.width, entity2.height)
		
		return rect1.colliderect(rect2)
	
	def _check_collisions(self):
		"""Detecta y maneja colisiones entre entidades."""
		# Colisiones proyectil-enemigo
		for projectile in self.projectiles[:]:
			for enemy in self.enemies[:]:
				if self._check_collision(projectile, enemy):
					# Aplicar daño al enemigo
					enemy.take_damage(projectile.damage)
					projectile.alive = False
					
					# Eliminar enemigo si muere
					if enemy.stats.health <= 0:
						self.enemies.remove(enemy)
						self.game_state.add_score(enemy.score_value)
						self.logger.debug(f"Enemigo eliminado. Puntuación: {self.game_state.score}")
					
					break
		
		# Colisiones jugador-enemigo
		if self.player:
			for enemy in self.enemies[:]:
				if self._check_collision(self.player, enemy):
					# Aplicar daño al jugador
					damage = enemy.stats.damage
					if self.player.take_damage(damage):
						self.game_state.lose_life()
						self.logger.debug(f"Jugador dañado. Vidas: {self.game_state.lives}")
					
					# Eliminar enemigo
					self.enemies.remove(enemy)
		
		# Colisiones jugador-powerup
		if self.player:
			for powerup in self.powerups[:]:
				if self._check_collision(self.player, powerup):
					# Aplicar powerup al jugador
					powerup_effect = powerup.get_effect()
					self.player.apply_powerup(powerup_effect)
					
					# Eliminar powerup
					self.powerups.remove(powerup)
					self.logger.debug(f"Powerup {powerup_effect.type.value} recolectado")
		
		# Colisiones jugador-tiles (solo tiles con colisión)
		if self.player:
			for tile in self.tiles:
				if tile.has_collision() and self._check_collision(self.player, tile):
					# Empujar al jugador fuera del tile
					self._resolve_tile_collision(self.player, tile)
	
	def _resolve_tile_collision(self, player, tile):
		"""
		Resuelve la colisión entre el jugador y un tile.
		
		Args:
			player: Jugador
			tile: Tile con el que colisiona
		"""
		# Calcular dirección de empuje
		player_center_x = player.x + player.width // 2
		player_center_y = player.y + player.height // 2
		tile_center_x = tile.x + tile.width // 2
		tile_center_y = tile.y + tile.height // 2
		
		# Vector de dirección
		dx = player_center_x - tile_center_x
		dy = player_center_y - tile_center_y
		
		# Normalizar
		distance = (dx*dx + dy*dy)**0.5
		if distance > 0:
			dx /= distance
			dy /= distance
			
			# Empujar al jugador
			push_distance = 5
			player.x += dx * push_distance
			player.y += dy * push_distance
			
			# Mantener dentro de límites del mundo
			player._clamp_position() 