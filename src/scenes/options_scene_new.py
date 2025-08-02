"""
Options Scene - Escena de Opciones (Refactorizada)
==================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Escena para configurar opciones del juego.
REFACTORIZADA: Ahora utiliza paneles especializados para mejor organización.
"""

import pygame
import pygame_gui

from core.scene_manager import Scene
from ui.menu_manager import MenuManager
from utils.config_manager import ConfigManager
from utils.logger import get_logger

from .options_audio_panel import OptionsAudioPanel
from .options_display_panel import OptionsDisplayPanel


class OptionsScene(Scene):
    """
    Escena de opciones del juego.
    Utiliza paneles especializados para mejor organización.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        """
        Inicializa la escena de opciones.

        Args:
            screen: Superficie de Pygame donde renderizar
            config: Configuración del juego
            game_state: Estado del juego
            save_manager: Gestor de guardado
        """
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")

        # Configurar pygame-gui
        self.ui_manager = pygame_gui.UIManager(
            (self.screen.get_width(), self.screen.get_height()),
            theme_path="assets/ui/theme.json",
        )

        # Inicializar paneles especializados
        self.audio_panel = OptionsAudioPanel(
            self.ui_manager,
            self.config,
            self.screen.get_width(),
            self.screen.get_height(),
        )

        self.display_panel = OptionsDisplayPanel(
            self.ui_manager,
            self.config,
            self.screen.get_width(),
            self.screen.get_height(),
        )

        self._inicializar_menu()
        self._setup_common_elements()
        self.logger.info(
            "[OptionsScene] Escena de opciones inicializada con paneles especializados"
        )

    def _setup_common_elements(self):
        """Configura elementos comunes de la UI (título, botones de acción)."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Panel central de opciones
        self.panel_opciones = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(50, 50, screen_width - 100, screen_height - 100),
            manager=self.ui_manager,
        )

        # Título
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 80), (200, 50)),
            text="OPCIONES",
            manager=self.ui_manager,
        )

        # Botones de acción
        self.guardar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 150, screen_height - 150), (100, 40)
            ),
            text="Guardar",
            manager=self.ui_manager,
        )

        self.cancelar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 40, screen_height - 150), (100, 40)
            ),
            text="Cancelar",
            manager=self.ui_manager,
        )

        self.volver_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 + 70, screen_height - 150), (100, 40)
            ),
            text="Volver",
            manager=self.ui_manager,
        )

    def _inicializar_menu(self):
        """
        Inicializa el menú de opciones usando MenuManager.
        Mantiene compatibilidad con sistema existente.
        """
        try:
            menu_manager = MenuManager(self.config)
            self.menu = menu_manager.crear_menu_opciones()
            self.logger.debug("[OptionsScene] Menú de opciones creado exitosamente")
        except Exception as e:
            self.logger.error("[OptionsScene] Error creando menú de opciones: %s", e)
            self.menu = None

    def handle_event(self, event):
        """
        Maneja eventos de la escena.

        Args:
            event: Evento de pygame

        Returns:
            str: Nombre de la próxima escena o None
        """
        # Delegar eventos a paneles especializados
        self.audio_panel.handle_event(event)
        display_action = self.display_panel.handle_event(event)

        # Manejar acciones de paneles
        if display_action == "toggle_fullscreen":
            self._handle_fullscreen_toggle()

        # Manejar eventos de botones principales
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.guardar_button:
                return self._handle_save_options()
            elif event.ui_element == self.cancelar_button:
                return self._handle_cancel_options()
            elif event.ui_element == self.volver_button:
                return "main_menu"

        # Procesar eventos con pygame_gui
        self.ui_manager.process_events(event)

        # Procesar eventos con menu si existe
        if self.menu:
            try:
                if self.menu.is_enabled():
                    self.menu.update([event])
            except (AttributeError, TypeError) as e:
                self.logger.warning(
                    "[OptionsScene] Error procesando evento en menú: %s", e
                )

        return None

    def _handle_fullscreen_toggle(self):
        """Maneja el cambio de pantalla completa."""
        try:
            # Aplicar cambio de pantalla completa
            if self.config.get_fullscreen():
                pygame.display.set_mode(
                    (self.config.get_width(), self.config.get_height()),
                    pygame.FULLSCREEN,
                )
            else:
                pygame.display.set_mode(
                    (self.config.get_width(), self.config.get_height())
                )

            self.logger.info("Modo de pantalla actualizado")
        except Exception as e:
            self.logger.error("Error cambiando modo de pantalla: %s", e)

    def _handle_save_options(self) -> str:
        """
        Guarda las opciones configuradas.

        Returns:
            str: Próxima escena
        """
        try:
            self.config.save_config()
            self.logger.info("[OptionsScene] Opciones guardadas exitosamente")
            return "main_menu"
        except Exception as e:
            self.logger.error("[OptionsScene] Error guardando opciones: %s", e)
            return None

    def _handle_cancel_options(self) -> str:
        """
        Cancela los cambios y vuelve al menú principal.

        Returns:
            str: Próxima escena
        """
        try:
            self.config.reload_config()
            self.logger.info(
                "[OptionsScene] Cambios cancelados, configuración recargada"
            )
            return "main_menu"
        except Exception as e:
            self.logger.error("[OptionsScene] Error cancelando opciones: %s", e)
            return "main_menu"

    def update(self, dt):
        """
        Actualiza la escena.

        Args:
            dt: Delta time desde la última actualización
        """
        # Actualizar pygame_gui
        self.ui_manager.update(dt)

        # Actualizar menú si existe
        if self.menu:
            try:
                if self.menu.is_enabled():
                    self.menu.update([])
            except (AttributeError, TypeError) as e:
                self.logger.warning("[OptionsScene] Error actualizando menú: %s", e)

    def render(self):
        """Renderiza la escena."""
        # Limpiar pantalla
        self.screen.fill((50, 50, 50))

        # Renderizar pygame_gui
        self.ui_manager.draw_ui(self.screen)

        # Renderizar menú si existe
        if self.menu:
            try:
                if self.menu.is_enabled():
                    self.menu.draw(self.screen)
            except (AttributeError, TypeError) as e:
                self.logger.warning("[OptionsScene] Error renderizando menú: %s", e)
