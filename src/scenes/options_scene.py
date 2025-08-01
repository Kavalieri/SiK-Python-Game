"""
Options Scene - Escena de Opciones
=================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Escena para configurar opciones del juego.
"""

import pygame
import pygame_gui

from ..core.scene_manager import Scene
from ..ui.menu_manager import MenuManager
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger


class OptionsScene(Scene):
    """
    Escena de opciones del juego.
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

        self._inicializar_menu()
        self._setup_pygame_gui_elements()
        self.logger.info("[OptionsScene] Escena de opciones inicializada")

    def _setup_pygame_gui_elements(self):
        """
        Configura los elementos de pygame-gui para las opciones.
        """
        screen_width, screen_height = self.screen.get_size()

        # Panel central de opciones
        panel_width, panel_height = 500, 600
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        # Título
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (panel_x + panel_width // 2 - 75, panel_y + 20), (150, 50)
            ),
            text="OPCIONES",
            manager=self.ui_manager,
        )

        # Sliders de volumen
        self.volumen_maestro_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x + 20, panel_y + 100), (200, 30)),
            text="Volumen Maestro:",
            manager=self.ui_manager,
        )

        self.volumen_maestro_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((panel_x + 20, panel_y + 140), (300, 30)),
            start_value=int(self.config.get("audio", "master_volume", 0.8) * 100),
            value_range=(0, 100),
            manager=self.ui_manager,
        )

        self.volumen_sfx_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x + 20, panel_y + 200), (200, 30)),
            text="Volumen SFX:",
            manager=self.ui_manager,
        )

        self.volumen_sfx_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((panel_x + 20, panel_y + 240), (300, 30)),
            start_value=int(self.config.get("audio", "sfx_volume", 0.7) * 100),
            value_range=(0, 100),
            manager=self.ui_manager,
        )

        # Botón de pantalla completa
        fullscreen_state = (
            "ON" if self.config.get("display", "fullscreen", False) else "OFF"
        )
        self.fullscreen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x + 20, panel_y + 320), (300, 50)),
            text=f"Pantalla Completa: {fullscreen_state}",
            manager=self.ui_manager,
        )

        # Botones de acción
        self.aplicar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x + 20, panel_y + 450), (120, 50)),
            text="Aplicar",
            manager=self.ui_manager,
        )

        self.restaurar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x + 160, panel_y + 450), (120, 50)),
            text="Restaurar",
            manager=self.ui_manager,
        )

        self.volver_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x + 300, panel_y + 450), (120, 50)),
            text="Volver",
            manager=self.ui_manager,
        )

    def _inicializar_menu(self):
        """
        Inicializa el menú de opciones.
        """
        try:
            self.menu_manager = MenuManager(
                self.screen, self.config, self.game_state, self.save_manager
            )
        except Exception as e:
            self.logger.error("Error al inicializar el menú de opciones: %s", e)
            raise

    def _setup_pygame_gui_elements(self):
        """
        Configura los elementos de pygame-gui para la escena de opciones.
        """
        screen_width, screen_height = self.screen.get_size()

        # Título de la pantalla de opciones
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 50), (200, 50)),
            text="OPCIONES",
            manager=self.ui_manager,
        )

        # Sección de audio
        self.audio_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 80, 150), (160, 30)),
            text="AUDIO",
            manager=self.ui_manager,
        )

        # Slider de volumen maestro
        self.volumen_maestro_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 200, 200), (150, 30)),
            text="Volumen Maestro:",
            manager=self.ui_manager,
        )

        self.volumen_maestro_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((screen_width // 2 - 40, 200), (200, 30)),
            start_value=int(self.config.get("audio", "master_volume", 0.8) * 100),
            value_range=(0, 100),
            manager=self.ui_manager,
        )

        # Slider de efectos de sonido
        self.volumen_sfx_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 200, 250), (150, 30)),
            text="Efectos de Sonido:",
            manager=self.ui_manager,
        )

        self.volumen_sfx_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((screen_width // 2 - 40, 250), (200, 30)),
            start_value=int(self.config.get("audio", "sfx_volume", 0.7) * 100),
            value_range=(0, 100),
            manager=self.ui_manager,
        )

        # Sección de video
        self.video_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 80, 320), (160, 30)),
            text="VIDEO",
            manager=self.ui_manager,
        )

        # Botón de pantalla completa
        self.fullscreen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 100, 370), (200, 40)),
            text="Pantalla Completa: OFF",
            manager=self.ui_manager,
        )

        # Botones de navegación
        self.aplicar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 220, screen_height - 80), (100, 40)
            ),
            text="Aplicar",
            manager=self.ui_manager,
        )

        self.restaurar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 110, screen_height - 80), (100, 40)
            ),
            text="Restaurar",
            manager=self.ui_manager,
        )

        self.volver_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 + 120, screen_height - 80), (100, 40)
            ),
            text="Volver",
            manager=self.ui_manager,
        )

    def enter(self):
        super().enter()
        self.menu_manager.show_menu("options")
        self.logger.info("[OptionsScene] Entrando en escena de opciones")

    def exit(self):
        super().exit()
        self.menu_manager.hide_current_menu()
        self.logger.info("[OptionsScene] Saliendo de escena de opciones")

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Maneja eventos de la escena de opciones.

        Args:
            event: Evento de Pygame a procesar.

        Returns:
            bool: True si el evento fue manejado, False en caso contrario.
        """
        # Procesar eventos de pygame-gui primero
        self.ui_manager.process_events(event)

        # Eventos específicos de pygame-gui
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.aplicar_button:
                self._aplicar_configuraciones()
                return True
            elif event.ui_element == self.restaurar_button:
                self._restaurar_configuraciones()
                return True
            elif event.ui_element == self.volver_button:
                self.game_state.scene_manager.change_scene("main_menu")
                return True
            elif event.ui_element == self.fullscreen_button:
                self._toggle_fullscreen()
                return True

        # Eventos de sliders
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.volumen_maestro_slider:
                self._actualizar_volumen_maestro(event.value)
                return True
            elif event.ui_element == self.volumen_sfx_slider:
                self._actualizar_volumen_sfx(event.value)
                return True

        # Procesar eventos del menú original
        self.menu_manager.update([event])

        if event.type == pygame.constants.KEYDOWN:  # pylint: disable=c-extension-no-member
            if event.key == pygame.constants.K_ESCAPE:  # pylint: disable=c-extension-no-member
                self.logger.info(
                    "[OptionsScene] ESC presionado - volviendo al menú principal"
                )
                self.game_state.scene_manager.change_scene("main_menu")
                return True
        return False

    def update(self):
        """
        Actualiza la lógica de la escena de opciones.
        """
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        self.ui_manager.update(time_delta)
        self.menu_manager.update([])

    def render(self):
        """
        Renderiza la escena de opciones.
        """
        self.screen.fill((0, 0, 0))
        # Comentar el menú original para evitar superposición
        # self.menu_manager.render()

        # Solo renderizar UI de pygame-gui
        self.ui_manager.draw_ui(self.screen)

    def _aplicar_configuraciones(self):
        """
        Aplica las configuraciones actuales.
        """
        # Aquí se aplicarían las configuraciones
        self.logger.info("[OptionsScene] Configuraciones aplicadas")

    def _restaurar_configuraciones(self):
        """
        Restaura las configuraciones por defecto.
        """
        # Restaurar valores por defecto
        self.volumen_maestro_slider.set_current_value(80)
        self.volumen_sfx_slider.set_current_value(70)
        self.fullscreen_button.set_text("Pantalla Completa: OFF")
        self.logger.info("[OptionsScene] Configuraciones restauradas")

    def _toggle_fullscreen(self):
        """
        Alterna entre pantalla completa y ventana.
        """
        # Aquí se implementaría el toggle de pantalla completa
        current_text = self.fullscreen_button.text
        if "OFF" in current_text:
            self.fullscreen_button.set_text("Pantalla Completa: ON")
        else:
            self.fullscreen_button.set_text("Pantalla Completa: OFF")
        self.logger.info("[OptionsScene] Pantalla completa alternada")

    def _actualizar_volumen_maestro(self, valor):
        """
        Actualiza el volumen maestro.

        Args:
            valor: Nuevo valor del volumen (0-100)
        """
        # Aquí se actualizaría el volumen maestro
        self.logger.debug(f"[OptionsScene] Volumen maestro: {valor}")

    def _actualizar_volumen_sfx(self, valor):
        """
        Actualiza el volumen de efectos de sonido.

        Args:
            valor: Nuevo valor del volumen (0-100)
        """
        # Aquí se actualizaría el volumen de SFX
        self.logger.debug(f"[OptionsScene] Volumen SFX: {valor}")
