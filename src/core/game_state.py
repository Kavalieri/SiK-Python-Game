"""
Game State - Estado global del juego
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona el estado global del juego, puntuaciones, vidas, etc.
"""

import logging
from enum import Enum
from typing import Dict, Any


class GameStatus(Enum):
	"""Estados posibles del juego."""
	MENU = "menu"
	PLAYING = "playing"
	PAUSED = "paused"
	GAME_OVER = "game_over"
	VICTORY = "victory"


class GameState:
	"""
	Gestiona el estado global del juego.
	"""
	
	def __init__(self):
		"""Inicializa el estado del juego."""
		self.logger = logging.getLogger(__name__)
		self.status = GameStatus.MENU
		self.score = 0
		self.lives = 3
		self.level = 1
		self.high_score = 0
		self.player_name = "Player"
		self.selected_character = None
		self.current_player = None  # Referencia al jugador actual para el HUD
		
		# Configuración del juego
		self.settings = {
			'sound_enabled': True,
			'music_enabled': True,
			'difficulty': 'normal'
		}
		
		self.logger.info("Estado del juego inicializado")
	
	def reset_game(self):
		"""Reinicia el estado del juego para una nueva partida."""
		self.score = 0
		self.lives = 3
		self.level = 1
		self.status = GameStatus.PLAYING
		self.logger.info("Estado del juego reiniciado")
	
	def add_score(self, points: int):
		"""
		Añade puntos al score actual.
		
		Args:
			points: Puntos a añadir
		"""
		self.score += points
		if self.score > self.high_score:
			self.high_score = self.score
			self.logger.info(f"Nuevo récord: {self.high_score}")
	
	def lose_life(self):
		"""Reduce una vida del jugador."""
		self.lives -= 1
		self.logger.info(f"Vida perdida. Vidas restantes: {self.lives}")
		
		if self.lives <= 0:
			self.status = GameStatus.GAME_OVER
			self.logger.info("Game Over")
	
	def next_level(self):
		"""Avanza al siguiente nivel."""
		self.level += 1
		self.logger.info(f"Nivel {self.level} iniciado")
	
	def set_status(self, status: GameStatus):
		"""
		Establece el estado del juego.
		
		Args:
			status: Nuevo estado del juego
		"""
		self.status = status
		self.logger.info(f"Estado del juego cambiado a: {status.value}")
	
	def get_state_dict(self) -> Dict[str, Any]:
		"""
		Obtiene el estado actual como diccionario.
		
		Returns:
			Diccionario con el estado actual del juego
		"""
		return {
			'status': self.status.value,
			'score': self.score,
			'lives': self.lives,
			'level': self.level,
			'high_score': self.high_score,
			'player_name': self.player_name,
			'settings': self.settings.copy()
		}
	
	def load_state(self, state_dict: Dict[str, Any]):
		"""
		Carga el estado desde un diccionario.
		
		Args:
			state_dict: Diccionario con el estado a cargar
		"""
		self.status = GameStatus(state_dict.get('status', 'menu'))
		self.score = state_dict.get('score', 0)
		self.lives = state_dict.get('lives', 3)
		self.level = state_dict.get('level', 1)
		self.high_score = state_dict.get('high_score', 0)
		self.player_name = state_dict.get('player_name', 'Player')
		self.settings = state_dict.get('settings', self.settings)
		
		self.logger.info("Estado del juego cargado") 