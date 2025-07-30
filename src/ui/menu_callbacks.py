"""
Menu Callbacks - Fachada de compatibilidad tras refactorización modular
======================================================================
Delega a: navigation_callbacks, upgrade_callbacks, options_callbacks, save_callbacks
"""

from typing import Any

from ..core.game_state import GameState
from ..utils.logger import get_logger
from ..utils.save_manager import SaveManager
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
        self.logger.info("[MenuCallbacks] Acción: Nuevo Juego (usuario)")
        self.navigation.on_new_game()

    def on_continue_game(self):
        self.logger.info("[MenuCallbacks] Acción: Continuar Juego (usuario)")
        self.navigation.on_continue_game()

    def on_load_game(self):
        return self.navigation.on_load_game()

    def on_options(self):
        return self.navigation.on_options()

    def on_exit(self):
        return self.navigation.on_exit()

    def on_resume_game(self):
        return self.navigation.on_resume_game()

    def on_main_menu(self):
        return self.navigation.on_main_menu()

    def on_back_to_previous(self):
        return self.navigation.on_back_to_previous()

    def on_character_selected(self, character: str):
        self.logger.info("[MenuCallbacks] Personaje: '%s'", character)
        self.navigation.on_character_selected(character)

    def on_back_to_main(self):
        self.logger.info("[MenuCallbacks] Volver al menú principal")
        self.navigation.on_back_to_main()

    # Upgrade callbacks
    def on_upgrade_speed(self):
        return self.upgrades.on_upgrade_speed()

    def on_upgrade_damage(self):
        return self.upgrades.on_upgrade_damage()

    def on_upgrade_health(self):
        return self.upgrades.on_upgrade_health()

    def on_upgrade_shield(self):
        return self.upgrades.on_upgrade_shield()

    def on_continue_after_upgrade(self):
        return self.upgrades.on_continue_after_upgrade()

    def on_equip_weapon(self):
        return self.upgrades.on_equip_weapon()

    def on_equip_armor(self):
        return self.upgrades.on_equip_armor()

    def on_equip_accessory(self):
        return self.upgrades.on_equip_accessory()

    # Options callbacks
    def on_resolution_change(self, value: Any, resolution: str):
        return self.options.on_resolution_change(value, resolution)

    def on_fullscreen_change(self, value: bool):
        return self.options.on_fullscreen_change(value)

    def on_music_volume_change(self, value: float):
        return self.options.on_music_volume_change(value)

    def on_sfx_volume_change(self, value: float):
        return self.options.on_sfx_volume_change(value)

    def on_configure_controls(self):
        return self.options.on_configure_controls()

    def on_save_options(self):
        return self.options.on_save_options()

    # Save callbacks
    def on_save_game(self):
        return self.saves.on_save_game()

    def on_new_save(self):
        return self.saves.on_new_save()

    def on_delete_save(self):
        return self.saves.on_delete_save()

    def on_select_save_file(self, file_number: int):
        return self.saves.on_select_save_file(file_number)

    def on_select_slot(self, slot: int):
        self.logger.info("[MenuCallbacks] Slot %d", slot)
        self.saves.on_select_slot(slot)

    def on_clear_slot(self, slot: int):
        self.logger.info("[MenuCallbacks] Vaciar Slot %d", slot)
        self.saves.on_clear_slot(slot)

    def on_back_to_main_from_slots(self):
        self.logger.info("[MenuCallbacks] Volver desde Slots")
        self.saves.on_back_to_main_from_slots()

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
