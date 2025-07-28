"""
Enemy Types - Tipos de Enemigos
=============================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de tipos de enemigos con diferentes comportamientos y estadísticas.
"""

import pygame
import logging
import random
import math
from typing import Optional, Tuple, List
from enum import Enum
from dataclasses import dataclass

from .entity import Entity, EntityType, EntityStats


class EnemyRarity(Enum):
	"""Rareza de los enemigos."""
	NORMAL = "normal"
	RARE = "rare"
	ELITE = "elite"
	LEGENDARY = "legendary"


class EnemyBehavior(Enum):
	"""Comportamientos de enemigos."""
	CHASE = "chase"           # Persigue al jugador
	WANDER = "wander"         # Vaga aleatoriamente
	AMBUSH = "ambush"         # Se esconde y ataca
	SWARM = "swarm"           # Se mueve en grupo
	BOSS = "boss"             # Comportamiento de jefe


@dataclass
class EnemyConfig:
	"""Configuración de un tipo de enemigo."""
	name: str
	rarity: EnemyRarity
	behavior: EnemyBehavior
	health: float
	speed: float
	damage: float
	armor: float
	score_value: int
	color: Tuple[int, int, int]
	symbol: str
	size: Tuple[int, int]
	spawn_chance: float


class EnemyTypes:
	"""Configuraciones de tipos de enemigos."""
	
	# Zombies básicos
	ZOMBIE_NORMAL = EnemyConfig(
		name="Zombie",
		rarity=EnemyRarity.NORMAL,
		behavior=EnemyBehavior.CHASE,
		health=100.0,
		speed=1.0,
		damage=10.0,
		armor=0.0,
		score_value=100,
		color=(139, 69, 19),  # Marrón
		symbol="🧟",
		size=(50, 50),
		spawn_chance=0.6
	)
	
	ZOMBIE_RARE = EnemyConfig(
		name="Zombie Raro",
		rarity=EnemyRarity.RARE,
		behavior=EnemyBehavior.AMBUSH,
		health=150.0,
		speed=1.5,
		damage=15.0,
		armor=5.0,
		score_value=250,
		color=(160, 82, 45),  # Marrón claro
		symbol="🧟‍♂️",
		size=(55, 55),
		spawn_chance=0.25
	)
	
	ZOMBIE_ELITE = EnemyConfig(
		name="Zombie Elite",
		rarity=EnemyRarity.ELITE,
		behavior=EnemyBehavior.SWARM,
		health=250.0,
		speed=2.0,
		damage=25.0,
		armor=15.0,
		score_value=500,
		color=(205, 133, 63),  # Marrón dorado
		symbol="🧟‍♀️",
		size=(60, 60),
		spawn_chance=0.1
	)
	
	ZOMBIE_LEGENDARY = EnemyConfig(
		name="Zombie Legendario",
		rarity=EnemyRarity.LEGENDARY,
		behavior=EnemyBehavior.BOSS,
		health=500.0,
		speed=1.8,
		damage=40.0,
		armor=30.0,
		score_value=1000,
		color=(255, 215, 0),  # Dorado
		symbol="👑",
		size=(80, 80),
		spawn_chance=0.05
	)
	
	# Zombies femeninos
	ZOMBIE_GIRL_NORMAL = EnemyConfig(
		name="Zombie Girl",
		rarity=EnemyRarity.NORMAL,
		behavior=EnemyBehavior.CHASE,
		health=80.0,
		speed=1.2,
		damage=8.0,
		armor=0.0,
		score_value=80,
		color=(218, 112, 214),  # Violeta
		symbol="🧟‍♀️",
		size=(45, 45),
		spawn_chance=0.6
	)
	
	ZOMBIE_GIRL_RARE = EnemyConfig(
		name="Zombie Girl Rara",
		rarity=EnemyRarity.RARE,
		behavior=EnemyBehavior.WANDER,
		health=120.0,
		speed=1.8,
		damage=12.0,
		armor=3.0,
		score_value=200,
		color=(221, 160, 221),  # Violeta claro
		symbol="🧟‍♀️",
		size=(50, 50),
		spawn_chance=0.25
	)
	
	ZOMBIE_GIRL_ELITE = EnemyConfig(
		name="Zombie Girl Elite",
		rarity=EnemyRarity.ELITE,
		behavior=EnemyBehavior.AMBUSH,
		health=200.0,
		speed=2.2,
		damage=20.0,
		armor=10.0,
		score_value=400,
		color=(255, 182, 193),  # Rosa claro
		symbol="🧟‍♀️",
		size=(55, 55),
		spawn_chance=0.1
	)
	
	ZOMBIE_GIRL_LEGENDARY = EnemyConfig(
		name="Zombie Girl Legendaria",
		rarity=EnemyRarity.LEGENDARY,
		behavior=EnemyBehavior.BOSS,
		health=400.0,
		speed=2.0,
		damage=35.0,
		armor=25.0,
		score_value=800,
		color=(255, 20, 147),  # Rosa intenso
		symbol="👑",
		size=(75, 75),
		spawn_chance=0.05
	)
	
	@classmethod
	def get_all_configs(cls) -> List[EnemyConfig]:
		"""Obtiene todas las configuraciones de enemigos."""
		return [
			cls.ZOMBIE_NORMAL,
			cls.ZOMBIE_RARE,
			cls.ZOMBIE_ELITE,
			cls.ZOMBIE_LEGENDARY,
			cls.ZOMBIE_GIRL_NORMAL,
			cls.ZOMBIE_GIRL_RARE,
			cls.ZOMBIE_GIRL_ELITE,
			cls.ZOMBIE_GIRL_LEGENDARY
		]
	
	@classmethod
	def get_by_rarity(cls, rarity: EnemyRarity) -> List[EnemyConfig]:
		"""Obtiene configuraciones por rareza."""
		return [config for config in cls.get_all_configs() if config.rarity == rarity]
	
	@classmethod
	def get_random_by_rarity(cls, rarity: EnemyRarity) -> Optional[EnemyConfig]:
		"""Obtiene una configuración aleatoria por rareza."""
		configs = cls.get_by_rarity(rarity)
		if configs:
			# Ponderar por spawn_chance
			total_chance = sum(config.spawn_chance for config in configs)
			rand = random.uniform(0, total_chance)
			current = 0
			for config in configs:
				current += config.spawn_chance
				if rand <= current:
					return config
		return None
	
	@classmethod
	def get_random_enemy(cls) -> EnemyConfig:
		"""Obtiene un enemigo aleatorio basado en probabilidades de rareza."""
		# Probabilidades de rareza
		rarity_chances = {
			EnemyRarity.NORMAL: 0.7,    # 70%
			EnemyRarity.RARE: 0.2,      # 20%
			EnemyRarity.ELITE: 0.08,    # 8%
			EnemyRarity.LEGENDARY: 0.02 # 2%
		}
		
		rand = random.random()
		current = 0
		for rarity, chance in rarity_chances.items():
			current += chance
			if rand <= current:
				return cls.get_random_by_rarity(rarity) or cls.ZOMBIE_NORMAL
		
		return cls.ZOMBIE_NORMAL 