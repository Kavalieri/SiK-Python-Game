"""
Game Scene Waves - Oleadas y Enemigos
=====================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Lógica de oleadas y gestión de enemigos para la escena principal del juego.
"""

import random
import pygame
from ..entities.enemy_types import EnemyTypes, EnemyRarity

class GameSceneWaves:
	"""
	Gestión de oleadas y enemigos para GameScene.
	Se integra con el núcleo mediante composición o herencia.
	"""
	def __init__(self, scene):
		self.scene = scene  # Referencia al núcleo GameScene

	def spawn_enemy(self):
		"""Genera un nuevo enemigo en el borde del mundo visible."""
		try:
			spawn_side = random.randint(0, 3)
			if spawn_side == 0:
				x = random.randint(0, 5000)
				y = -50
			elif spawn_side == 1:
				x = 5050
				y = random.randint(0, 5000)
			elif spawn_side == 2:
				x = random.randint(0, 5000)
				y = 5050
			else:
				x = -50
				y = random.randint(0, 5000)
			enemy_config = self.select_enemy_for_wave()
			enemy = self.scene.enemy_manager.create_enemy(x, y, enemy_config)
			self.scene.enemies.append(enemy)
			self.scene.enemies_spawned_this_wave += 1
			self.scene.logger.debug(f"Enemigo {enemy_config.name} generado en ({x}, {y}) - Oleada {self.scene.wave_number}")
		except Exception as e:
			self.scene.logger.error(f"Error al generar enemigo: {e}")

	def select_enemy_for_wave(self):
		"""Selecciona el tipo de enemigo basado en la oleada actual."""
		wave = self.scene.wave_number
		if wave <= 3:
			return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
		elif wave <= 6:
			rand = random.random()
			if rand < 0.8:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
			else:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.RARE) or EnemyTypes.ZOMBIE_RARE
		elif wave <= 10:
			rand = random.random()
			if rand < 0.6:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
			elif rand < 0.9:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.RARE) or EnemyTypes.ZOMBIE_RARE
			else:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.ELITE) or EnemyTypes.ZOMBIE_ELITE
		else:
			rand = random.random()
			if rand < 0.5:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.NORMAL) or EnemyTypes.ZOMBIE_NORMAL
			elif rand < 0.8:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.RARE) or EnemyTypes.ZOMBIE_RARE
			elif rand < 0.95:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.ELITE) or EnemyTypes.ZOMBIE_ELITE
			else:
				return EnemyTypes.get_random_by_rarity(EnemyRarity.LEGENDARY) or EnemyTypes.ZOMBIE_LEGENDARY

	def check_wave_completion(self):
		"""Verifica si la oleada actual está completada y gestiona upgrades."""
		scene = self.scene
		if (scene.enemies_spawned_this_wave >= scene.enemies_per_wave and \
			len(scene.enemies) == 0 and not scene.wave_completed):
			scene.wave_completed = True
			scene.wave_number += 1
			scene.enemies_spawned_this_wave = 0
			scene.enemies_per_wave = min(10 + scene.wave_number * 2, 50)
			scene.logger.info(f"¡Oleada {scene.wave_number - 1} completada! Mostrando menú de mejoras")
			if hasattr(scene, 'hud') and hasattr(scene.hud, 'menu_manager'):
				scene.hud.menu_manager.show_menu('upgrade')
				scene.hud.menu_manager.update_upgrade_menu(scene.player.stats.upgrade_points)
				scene.hud.menu_manager.add_callback('continue_after_upgrade', self.on_continue_after_upgrade)
				scene.hud.menu_manager.add_callback('upgrade_speed', lambda: scene.player.upgrade_stat('speed', 10))
				scene.hud.menu_manager.add_callback('upgrade_damage', lambda: scene.player.upgrade_stat('damage', 15))
				scene.hud.menu_manager.add_callback('upgrade_health', lambda: scene.player.upgrade_stat('health', 20))
				scene.hud.menu_manager.add_callback('upgrade_shield', lambda: scene.player.upgrade_stat('shield', 25))
				scene.logger.info("Menú de mejoras mostrado")
			scene.paused_for_upgrade = True
			scene.enemy_spawn_timer = pygame.time.get_ticks() + 3000

	def on_continue_after_upgrade(self):
		"""Callback para continuar el juego tras el menú de mejoras."""
		scene = self.scene
		scene.logger.info("Continuando juego tras mejoras")
		scene.wave_completed = False
		scene.paused_for_upgrade = False
		scene.enemy_spawn_timer = pygame.time.get_ticks() + 1000 