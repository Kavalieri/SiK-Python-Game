"""
Game Scene (Legacy Wrapper) - Transición a núcleo modularizado
=============================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Wrapper temporal para mantener compatibilidad mientras se migra a la versión modularizada.
"""

from .game_scene_core import GameScene
# El resto de la lógica se encuentra ahora en los submódulos especializados.
# Este archivo se mantendrá como punto de entrada para la escena principal hasta completar la migración y refactorización total. 