"""
Menu Callbacks - Fachada de compatibilidad tras refactorización modular
======================================================================
Delega a: navigation_callbacks, upgrade_callbacks, options_callbacks, save_callbacks
"""

from typing import Any

from core.game_state import GameState
from utils.logger import get_logger
from utils.save_manager import SaveManager

from .navigation_callbacks import NavigationCallbacks
from .options_callbacks import OptionsCallbacks
from .save_callbacks import SaveCallbacks
from .upgrade_callbacks import UpgradeCallbacks


class MenuCallbacks:
    """Fachada de compatibilidad para callbacks de menús del juego."""

    def __init__(self, game_state: GameState, save_manager: SaveManager):
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")
        self.navigation = NavigationCallbacks(game_state, save_manager)
        self.upgrades = UpgradeCallbacks(game_state, save_manager)
        self.options = OptionsCallbacks(game_state, save_manager)
        self.saves = SaveCallbacks(game_state, save_manager)

    # Navigation callbacks
    def on_new_game(self):
        """Inicia un nuevo juego."""
        self.logger.info("[MenuCallbacks] Acción: Nuevo Juego (usuario)")
        self.navigation.on_new_game()

    def on_continue_game(self):
        """Continúa el último juego guardado."""
        self.logger.info("[MenuCallbacks] Acción: Continuar Juego (usuario)")
        self.navigation.on_continue_game()

    def on_load_game(self):
        """Navega a la pantalla de cargar juego."""
        return self.navigation.on_load_game()

    def on_options(self):
        """Navega a la pantalla de opciones."""
        return self.navigation.on_options()

    def on_exit(self):
        """Cierra el juego."""
        return self.navigation.on_exit()

    def on_resume_game(self):
        """Reanuda el juego en pausa."""
        return self.navigation.on_resume_game()

    def on_main_menu(self):
        """Navega al menú principal."""
        return self.navigation.on_main_menu()

    def on_back_to_previous(self):
        """Regresa a la pantalla anterior."""
        return self.navigation.on_back_to_previous()

    def on_character_selected(self, character: str):
        """Selecciona un personaje para jugar."""
        self.logger.info("[MenuCallbacks] Personaje: '%s'", character)
        self.navigation.on_character_selected(character)

    def on_back_to_main(self):
        """Regresa al menú principal."""
        self.logger.info("[MenuCallbacks] Volver al menú principal")
        self.navigation.on_back_to_main()

    # Upgrade callbacks
    def on_upgrade_speed(self):
        """Mejora la velocidad del jugador."""
        return self.upgrades.on_upgrade_speed()

    def on_upgrade_damage(self):
        """Mejora el daño del jugador."""
        return self.upgrades.on_upgrade_damage()

    def on_upgrade_health(self):
        """Mejora la salud del jugador."""
        return self.upgrades.on_upgrade_health()

    def on_upgrade_shield(self):
        """Mejora el escudo del jugador."""
        return self.upgrades.on_upgrade_shield()

    def on_continue_after_upgrade(self):
        """Continúa el juego después de aplicar mejoras."""
        return self.upgrades.on_continue_after_upgrade()

    def on_equip_weapon(self):
        """Equipa un arma al jugador."""
        return self.upgrades.on_equip_weapon()

    def on_equip_armor(self):
        """Equipa armadura al jugador."""
        return self.upgrades.on_equip_armor()

    def on_equip_accessory(self):
        """Equipa un accesorio al jugador."""
        return self.upgrades.on_equip_accessory()

    # Options callbacks
    def on_resolution_change(self, value: Any, resolution: str):
        """Cambia la resolución de pantalla."""
        return self.options.on_resolution_change(value, resolution)

    def on_fullscreen_change(self, value: bool):
        """Activa o desactiva pantalla completa."""
        return self.options.on_fullscreen_change(value)

    def on_music_volume_change(self, value: float):
        """Cambia el volumen de la música."""
        return self.options.on_music_volume_change(value)

    def on_sfx_volume_change(self, value: float):
        """Cambia el volumen de efectos de sonido."""
        return self.options.on_sfx_volume_change(value)

    def on_configure_controls(self):
        """Abre la configuración de controles."""
        return self.options.on_configure_controls()

    def on_save_options(self):
        """Guarda las opciones configuradas."""
        return self.options.on_save_options()

    # Save callbacks
    def on_save_game(self):
        """Guarda el juego actual."""
        return self.saves.on_save_game()

    def on_new_save(self):
        """Crea una nueva partida guardada."""
        return self.saves.on_new_save()

    def on_delete_save(self):
        """Elimina una partida guardada."""
        return self.saves.on_delete_save()

    def on_select_save_file(self, file_number: int):
        """Selecciona un archivo de guardado."""
        return self.saves.on_select_save_file(file_number)

    def on_select_slot(self, slot: int):
        """Selecciona un slot de guardado."""
        self.logger.info("[MenuCallbacks] Slot %d", slot)
        self.saves.on_select_slot(slot)

    def on_clear_slot(self, slot: int):
        """Vacía un slot de guardado específico."""
        self.logger.info("[MenuCallbacks] Vaciar Slot %d", slot)
        self.saves.on_clear_slot(slot)

    def on_back_to_main_from_slots(self):
        """Regresa al menú principal desde la pantalla de slots."""
        self.logger.info("[MenuCallbacks] Volver desde Slots")
        self.saves.on_back_to_main_from_slots()

    def on_continue_slot(self, slot: int):
        """Continúa una partida específica del slot indicado."""
        self.logger.info("[MenuCallbacks] Continuar slot %d", slot)
        self.saves.on_select_save_file(slot)  # Cargar y continuar el slot específico

    def on_new_game_slot(self, slot: int):
        """Inicia nueva partida en el slot indicado."""
        self.logger.info("[MenuCallbacks] Nueva partida en slot %d", slot)
        # Ir directamente a selección de personajes con el slot seleccionado
        self.navigation.on_new_game_with_slot(slot)

    def get_all_callbacks(self) -> dict:
        """Obtiene todos los callbacks disponibles."""
        all_callbacks = {
            # Navegación
            "new_game": self.on_new_game,
            "continue_game": self.on_continue_game,
            "load_game": self.on_load_game,
            "options": self.on_options,
            "exit": self.on_exit,
            "resume_game": self.on_resume_game,
            "main_menu": self.on_main_menu,
            "select_character": self.on_character_selected,
            "back_to_main": self.on_back_to_main,
            "back_to_previous": self.on_back_to_previous,
        }
        all_callbacks.update(self.upgrades.get_upgrade_callbacks())
        all_callbacks.update(self.options.get_options_callbacks())
        all_callbacks.update(self.saves.get_save_callbacks())
        return all_callbacks
