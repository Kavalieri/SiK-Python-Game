"""
Core - Motor principal del juego
===============================

Este paquete contiene el motor principal del juego y los componentes fundamentales.
"""

from .game_engine import GameEngine
from .game_state import GameState
from .scene_manager import SceneManager

__all__ = ["GameEngine", "GameState", "SceneManager"]
