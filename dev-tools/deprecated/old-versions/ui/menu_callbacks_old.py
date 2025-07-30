"""
Menu Callbacks - Callbacks de Menús
==================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que contiene todos los callbacks de los menús del juego.
"""

from typing import Any
from ..core.game_state import GameState
from ..utils.save_manager import SaveManager
from ..utils.logger import get_logger


class MenuCallbacks:
    """
    Gestiona todos los callbacks de los menús del juego.
    """

    def __init__(self, game_state: GameState, save_manager: SaveManager):
        """
        Inicializa los callbacks de menú.

        Args:
            game_state: Estado del juego
            save_manager: Gestor de guardado
        """
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")

    # Callbacks de navegación principal
    def on_new_game(self):
        """Callback para iniciar un nuevo juego."""
        self.logger.info("[MenuCallbacks] Acción: Nuevo Juego (usuario)")
        self.game_state.set_scene("character_select")

    def on_continue_game(self):
        """Callback para continuar el último juego guardado."""
        self.logger.info("[MenuCallbacks] Acción: Continuar Juego (usuario)")
        try:
            if self.save_manager.has_save_file():
                self.save_manager.load_latest_save()
                self.game_state.set_scene("game")
            else:
                self.logger.warning("No hay partida guardada para continuar")
        except Exception as e:
            self.logger.error(f"Error cargando partida: {e}")

    def on_load_game(self):
        """Callback para cargar un juego específico."""
        self.logger.info("[MenuCallbacks] Acción: Cargar Juego (usuario)")
        self.game_state.set_scene("save_menu")

    def on_options(self):
        self.logger.info("[MenuCallbacks] Acción: Opciones (usuario)")
        self.logger.warning("[MenuCallbacks] Acción: Opciones - NO IMPLEMENTADO")
        # No cambiar de escena

    def on_exit(self):
        """Callback para salir del juego (botón Salir del menú principal)."""
        self.logger.info(
            "[MenuCallbacks] Acción: Salir (usuario) - Botón Salir pulsado"
        )
        # Aquí no se cierra la ventana directamente, sino que se delega al engine para diferenciar logs
        if hasattr(self.game_state, "scene_manager") and self.game_state.scene_manager:
            if hasattr(self.game_state.scene_manager, "game_engine"):
                self.game_state.scene_manager.game_engine._log_and_quit_menu()

    # Callbacks de menú de pausa
    def on_resume_game(self):
        """Callback para reanudar el juego."""
        self.logger.info("Reanudando juego")
        self.game_state.set_scene("game")

    def on_save_game(self):
        self.logger.warning("[MenuCallbacks] Acción: Guardar Juego - NO IMPLEMENTADO")
        # No cambiar de escena

    def on_main_menu(self):
        """Callback para volver al menú principal."""
        self.logger.info("Volviendo al menú principal")
        self.game_state.set_scene("main_menu")

    # Callbacks de menú de mejoras
    def on_upgrade_speed(self):
        """Callback para mejorar velocidad."""
        self.logger.info("Mejorando velocidad")
        if self.game_state.player:
            success = self.game_state.player.upgrade_stat("speed", 1)
            if success:
                self.logger.info("Velocidad mejorada")
            else:
                self.logger.warning("No hay suficientes puntos de mejora")

    def on_upgrade_damage(self):
        """Callback para mejorar daño."""
        self.logger.info("Mejorando daño")
        if self.game_state.player:
            success = self.game_state.player.upgrade_stat("damage", 1)
            if success:
                self.logger.info("Daño mejorado")
            else:
                self.logger.warning("No hay suficientes puntos de mejora")

    def on_upgrade_health(self):
        """Callback para mejorar vida."""
        self.logger.info("Mejorando vida")
        if self.game_state.player:
            success = self.game_state.player.upgrade_stat("health", 1)
            if success:
                self.logger.info("Vida mejorada")
            else:
                self.logger.warning("No hay suficientes puntos de mejora")

    def on_upgrade_shield(self):
        """Callback para mejorar escudo."""
        self.logger.info("Mejorando escudo")
        if self.game_state.player:
            success = self.game_state.player.upgrade_stat("shield", 1)
            if success:
                self.logger.info("Escudo mejorado")
            else:
                self.logger.warning("No hay suficientes puntos de mejora")

    def on_continue_after_upgrade(self):
        """Callback para continuar después de mejoras."""
        self.logger.info("Continuando después de mejoras")
        self.game_state.set_scene("game")

    # Callback para selección de slot
    def on_select_slot(self, slot: int):
        """Callback para seleccionar un slot de guardado."""
        self.logger.info(f"[MenuCallbacks] Acción: Seleccionar Slot {slot} (usuario)")
        if hasattr(self.game_state, "scene_manager") and self.game_state.scene_manager:
            if hasattr(self.game_state.scene_manager, "game_engine"):
                self.game_state.scene_manager.game_engine._handle_slot_selection(slot)

    # Callback para vaciar slot
    def on_clear_slot(self, slot: int):
        """Callback para vaciar un slot de guardado."""
        self.logger.info(f"[MenuCallbacks] Acción: Vaciar Slot {slot} (usuario)")
        if hasattr(self.game_state, "scene_manager") and self.game_state.scene_manager:
            if hasattr(self.game_state.scene_manager, "game_engine"):
                self.game_state.scene_manager.game_engine._handle_clear_slot(slot)

    # Callback para volver al menú principal desde selección de slots
    def on_back_to_main_from_slots(self):
        self.logger.info(
            "[MenuCallbacks] Acción: Volver al Menú Principal desde Slots (usuario)"
        )
        if hasattr(self.game_state, "scene_manager") and self.game_state.scene_manager:
            self.game_state.scene_manager.change_scene("main_menu")

    # Callback para selección de personaje
    def on_character_selected(self, character: str):
        self.logger.info(
            f"[MenuCallbacks] Acción: Personaje Seleccionado '{character}' (usuario)"
        )
        if hasattr(self.game_state, "scene_manager") and self.game_state.scene_manager:
            if hasattr(self.game_state.scene_manager, "game_engine"):
                self.game_state.scene_manager.game_engine._handle_character_selection(
                    character
                )

    def on_back_to_main(self):
        """Callback para volver al menú principal desde selección de personaje."""
        self.logger.info("[MenuCallbacks] Acción: Volver al menú principal (usuario)")
        self.game_state.set_scene("main_menu")

    def on_back_to_previous(self):
        """Callback para volver al menú anterior."""
        self.logger.info("Volviendo al menú anterior")
        self.game_state.go_back()

    # Callbacks de opciones
    def on_resolution_change(self, value: Any, resolution: str):
        """Callback para cambiar resolución."""
        self.logger.info(f"Cambiando resolución a: {resolution}")
        try:
            width, height = map(int, resolution.split("x"))
            self.game_state.config.set_resolution(width, height)
            self.logger.info(f"Resolución cambiada a {width}x{height}")
        except Exception as e:
            self.logger.error(f"Error cambiando resolución: {e}")

    def on_fullscreen_change(self, value: bool):
        """Callback para cambiar modo pantalla completa."""
        self.logger.info(f"Cambiando modo pantalla completa: {value}")
        try:
            self.game_state.config.set_fullscreen(value)
            self.logger.info(f"Modo pantalla completa: {value}")
        except Exception as e:
            self.logger.error(f"Error cambiando modo pantalla completa: {e}")

    def on_music_volume_change(self, value: float):
        """Callback para cambiar volumen de música."""
        self.logger.info(f"Cambiando volumen de música: {value}")
        try:
            self.game_state.config.set_music_volume(value)
            self.logger.info(f"Volumen de música: {value}")
        except Exception as e:
            self.logger.error(f"Error cambiando volumen de música: {e}")

    def on_sfx_volume_change(self, value: float):
        """Callback para cambiar volumen de efectos de sonido."""
        self.logger.info(f"Cambiando volumen de SFX: {value}")
        try:
            self.game_state.config.set_sfx_volume(value)
            self.logger.info(f"Volumen de SFX: {value}")
        except Exception as e:
            self.logger.error(f"Error cambiando volumen de SFX: {e}")

    def on_configure_controls(self):
        """Callback para configurar controles."""
        self.logger.info("Abriendo configuración de controles")
        # TODO: Implementar configuración de controles
        self.logger.warning("Configuración de controles no implementada")

    def on_save_options(self):
        """Callback para guardar opciones."""
        self.logger.info("Guardando opciones")
        try:
            self.game_state.config.save_config()
            self.logger.info("Opciones guardadas exitosamente")
        except Exception as e:
            self.logger.error(f"Error guardando opciones: {e}")

    # Callbacks de inventario
    def on_equip_weapon(self):
        """Callback para equipar arma."""
        self.logger.info("Equipando arma")
        # TODO: Implementar sistema de equipación
        self.logger.warning("Sistema de equipación no implementado")

    def on_equip_armor(self):
        """Callback para equipar armadura."""
        self.logger.info("Equipando armadura")
        # TODO: Implementar sistema de equipación
        self.logger.warning("Sistema de equipación no implementado")

    def on_equip_accessory(self):
        """Callback para equipar accesorio."""
        self.logger.info("Equipando accesorio")
        # TODO: Implementar sistema de equipación
        self.logger.warning("Sistema de equipación no implementado")

    # Callbacks de guardado
    def on_select_save_file(self, file_number: int):
        """Callback para seleccionar archivo de guardado."""
        self.logger.info(f"Seleccionando archivo de guardado: {file_number}")
        try:
            info = self.save_manager.get_save_files_info()[file_number - 1]
            if not info["exists"]:
                self._show_save_menu_feedback("Slot vacío. No se puede continuar.")
                self.logger.warning("Slot vacío. No se puede continuar.")
                self._refresh_save_menu()
                return
            self.save_manager.load_save(file_number)
            self.game_state.set_scene("game")
            self.logger.info(f"Archivo de guardado {file_number} cargado")
            self._show_save_menu_feedback("")
            self._refresh_save_menu()
        except Exception as e:
            self._show_save_menu_feedback(f"Error cargando slot: {e}")
            self.logger.error(f"Error cargando archivo de guardado {file_number}: {e}")
            self._refresh_save_menu()

    def on_new_save(self):
        """Callback para crear nuevo archivo de guardado."""
        self.logger.info("Creando nuevo archivo de guardado")
        try:
            # Buscar primer slot vacío
            for i, info in enumerate(self.save_manager.get_save_files_info(), 1):
                if not info["exists"]:
                    self.save_manager.create_new_save(i)
                    self._show_save_menu_feedback(f"Nuevo guardado creado en slot {i}")
                    self.logger.info(f"Nuevo archivo de guardado creado en slot {i}")
                    self._refresh_save_menu()
                    return
            self._show_save_menu_feedback("No hay slots vacíos disponibles.")
            self.logger.warning("No hay slots vacíos disponibles.")
            self._refresh_save_menu()
        except Exception as e:
            self._show_save_menu_feedback(f"Error creando guardado: {e}")
            self.logger.error(f"Error creando nuevo archivo de guardado: {e}")
            self._refresh_save_menu()

    def on_delete_save(self):
        """Callback para eliminar archivo de guardado."""
        self.logger.info("Eliminando archivo de guardado")
        try:
            # Eliminar el slot seleccionado (por simplicidad, eliminar el primero ocupado)
            for i, info in enumerate(self.save_manager.get_save_files_info(), 1):
                if info["exists"]:
                    self.save_manager.delete_save(i)
                    self._show_save_menu_feedback(f"Guardado eliminado en slot {i}")
                    self.logger.info(f"Guardado eliminado en slot {i}")
                    self._refresh_save_menu()
                    return
            self._show_save_menu_feedback("No hay guardados para eliminar.")
            self.logger.warning("No hay guardados para eliminar.")
            self._refresh_save_menu()
        except Exception as e:
            self._show_save_menu_feedback(f"Error eliminando guardado: {e}")
            self.logger.error(f"Error eliminando archivo de guardado: {e}")
            self._refresh_save_menu()

    def _show_save_menu_feedback(self, msg: str):
        # Busca el menú de guardado y actualiza un label de feedback
        from .menu_manager import MenuManager

        menu_manager = None
        for obj in globals().values():
            if isinstance(obj, MenuManager):
                menu_manager = obj
                break
        if menu_manager and "save" in menu_manager.menus:
            menu = menu_manager.menus["save"]
            if hasattr(menu, "_feedback_label"):
                menu._feedback_label.set_title(msg)

    def _refresh_save_menu(self):
        from .menu_manager import MenuManager

        menu_manager = None
        for obj in globals().values():
            if isinstance(obj, MenuManager):
                menu_manager = obj
                break
        if menu_manager:
            menu_manager.menus["save"] = menu_manager.factory.create_save_menu()
            menu_manager.show_menu("save")

    def get_all_callbacks(self) -> dict:
        """
        Obtiene todos los callbacks disponibles.

        Returns:
            Diccionario con todos los callbacks
        """
        return {
            # Navegación principal
            "new_game": self.on_new_game,
            "continue_game": self.on_continue_game,
            "load_game": self.on_load_game,
            "options": self.on_options,
            "exit": self.on_exit,
            # Menú de pausa
            "resume_game": self.on_resume_game,
            "save_game": self.on_save_game,
            "main_menu": self.on_main_menu,
            # Mejoras
            "upgrade_speed": self.on_upgrade_speed,
            "upgrade_damage": self.on_upgrade_damage,
            "upgrade_health": self.on_upgrade_health,
            "upgrade_shield": self.on_upgrade_shield,
            "continue_after_upgrade": self.on_continue_after_upgrade,
            # Selección de personaje
            "select_character": self.on_character_selected,
            "back_to_main": self.on_back_to_main,
            "back_to_previous": self.on_back_to_previous,
            # Opciones
            "resolution_change": self.on_resolution_change,
            "fullscreen_change": self.on_fullscreen_change,
            "music_volume_change": self.on_music_volume_change,
            "sfx_volume_change": self.on_sfx_volume_change,
            "configure_controls": self.on_configure_controls,
            "save_options": self.on_save_options,
            # Inventario
            "equip_weapon": self.on_equip_weapon,
            "equip_armor": self.on_equip_armor,
            "equip_accessory": self.on_equip_accessory,
            # Guardado
            "select_save_file": self.on_select_save_file,
            "new_save": self.on_new_save,
            "delete_save": self.on_delete_save,
        }
