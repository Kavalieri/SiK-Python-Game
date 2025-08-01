"""Character Select Scene - Selección de Personaje (Refactorizada V2)"""

import pygame
import pygame_gui

from ..core.scene_manager import Scene
from ..ui.menu_manager import MenuManager
from ..utils.logger import get_logger
from .character_animations import CharacterAnimations
from .character_data import CharacterData
from .character_ui import CharacterUI


class CharacterSelectScene(Scene):
    """Escena de selección de personaje jugable (Refactorizada V2)."""

    def __init__(self, screen, config, game_state, save_manager):
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.character_data = CharacterData()
        self.character_animations = CharacterAnimations()
        self.character_ui = CharacterUI(self.screen_width, self.screen_height, config)
        self.character_keys = list(CharacterData.CHARACTER_DATA.keys())
        self.current_character_index = 0
        self.selected_key = self.character_keys[0] if self.character_keys else None
        self.mouse_pos = (0, 0)
        self.logger = get_logger("SiK_Game")

        # Configurar pygame-gui
        self.ui_manager = pygame_gui.UIManager(
            (self.screen_width, self.screen_height), theme_path="assets/ui/theme.json"
        )

        # Inicializar menú (requerido por game_engine_scenes)
        self.menu_manager = MenuManager(screen, config, game_state, save_manager)

        # Configurar elementos pygame-gui
        self._setup_pygame_gui_elements()

    def _setup_pygame_gui_elements(self):
        """Configura los elementos de pygame-gui para la selección de personajes."""

        # Título
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width // 2 - 150, 20), (300, 50)),
            text="SELECCIONAR PERSONAJE",
            manager=self.ui_manager,
        )

        # Información del personaje seleccionado
        self.character_info_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width // 2 - 200, 350), (400, 30)),
            text="",
            manager=self.ui_manager,
        )

        # Botones de navegación
        self.prev_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, self.screen_height // 2 - 25), (80, 50)),
            text="< Anterior",
            manager=self.ui_manager,
        )

        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.screen_width - 130, self.screen_height // 2 - 25), (80, 50)
            ),
            text="Siguiente >",
            manager=self.ui_manager,
        )

        # Botones de acción
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, self.screen_height - 80), (120, 50)),
            text="Volver",
            manager=self.ui_manager,
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.screen_width - 170, self.screen_height - 80), (120, 50)
            ),
            text="Iniciar",
            manager=self.ui_manager,
        )

        # Actualizar información inicial
        self._update_character_info()

    def update(self):
        """Actualiza la escena."""
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        self.ui_manager.update(time_delta)
        self.character_animations.update(0.016)
        self.mouse_pos = pygame.mouse.get_pos()

    def render(self):
        """Renderiza la escena."""
        self.screen.fill((20, 20, 40))
        # Comentar UI original para evitar superposición
        # self.character_ui.render_title(self.screen)
        if self.selected_key:
            self._render_selected_character()
        # self.character_ui.render_buttons(self.screen, self.mouse_pos)
        # self.character_ui.render_navigation_indicator(
        #     self.screen, self.current_character_index, len(self.character_keys)
        # )
        # Renderizar UI de pygame-gui
        self.ui_manager.draw_ui(self.screen)

    def _navigate_character(self, direction: int):
        """Navega entre los personajes disponibles."""
        if len(self.character_keys) > 1:
            self.current_character_index = (
                self.current_character_index + direction
            ) % len(self.character_keys)
            self.selected_key = self.character_keys[self.current_character_index]
            self._update_character_info()

    def _update_character_info(self):
        """Actualiza la información del personaje seleccionado."""
        if self.selected_key:
            char_data = CharacterData.get_character_data(self.selected_key)
            if char_data:
                info_text = f"Personaje: {char_data.get('name', 'Sin nombre')} | Clase: {char_data.get('class', 'Guerrero')}"
                self.character_info_label.set_text(info_text)

    def _render_selected_character(self):
        """Renderiza el personaje seleccionado."""
        if not self.selected_key:
            return
        char_key = self.selected_key
        char_data = CharacterData.get_character_data(char_key)
        if not char_data:
            return

        self._draw_character_card(char_key)
        stats_x = (self.screen_width - 600) // 2 + 30
        skills_x = stats_x + 300
        content_y = 460
        self.character_ui.render_character_stats(
            self.screen, char_key, stats_x, content_y
        )
        self.character_ui.render_character_skills(
            self.screen, char_key, skills_x, content_y
        )

    def _draw_character_card(self, char_key: str):
        """Dibuja la tarjeta del personaje seleccionado."""
        card_width, card_height = 600, 600
        x = (self.screen_width - card_width) // 2
        y = 100

        card_rect = pygame.Rect(x, y, card_width, card_height)
        pygame.draw.rect(self.screen, (40, 40, 80), card_rect)
        pygame.draw.rect(self.screen, (80, 80, 120), card_rect, 3)

        image_size = 250
        image_x = x + (card_width - image_size) // 2
        image_y = y + 90
        character_image = self.character_animations.get_character_image(char_key)
        if character_image:
            self._render_character_image(character_image, image_x, image_y, image_size)

    def _render_character_image(self, image: pygame.Surface, x: int, y: int, size: int):
        """Renderiza la imagen del personaje."""
        mouse_x, _ = self.mouse_pos
        sprite_center_x = x + size // 2
        flip = mouse_x < sprite_center_x
        if flip:
            image = pygame.transform.flip(image, True, False)
        scaled_image = pygame.transform.scale(image, (size, size))
        image_rect = scaled_image.get_rect(center=(x + size // 2, y + size // 2))
        self.screen.blit(scaled_image, image_rect)

    def _on_character_selected(self, character_key: str):
        """Maneja la selección de un personaje."""
        self.selected_key = character_key
        self.logger.info("Personaje seleccionado: %s", character_key)

    def _on_back_clicked(self):
        """Maneja el click en el botón Atrás."""
        self.game_state.set_scene("main_menu")
        self.logger.info("Volviendo al menú principal")

    def _on_start_clicked(self):
        """Maneja el click en el botón Iniciar."""
        if self.selected_key:
            self.game_state.selected_character = self.selected_key
            self.game_state.set_scene("game")
            self.logger.info("Iniciando juego con personaje: %s", self.selected_key)

    def handle_event(self, event):
        """Maneja eventos de la escena."""
        # Procesar eventos de pygame-gui primero
        self.ui_manager.process_events(event)

        # Eventos específicos de pygame-gui
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.prev_button:
                self._navigate_character(-1)
                return True
            elif event.ui_element == self.next_button:
                self._navigate_character(1)
                return True
            elif event.ui_element == self.back_button:
                self._on_back_clicked()
                return True
            elif event.ui_element == self.start_button:
                self._on_start_clicked()
                return True

        # Eventos de teclado
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if event.key in [pygame.K_LEFT, pygame.K_a]:  # pylint: disable=no-member
                self._navigate_character(-1)
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:  # pylint: disable=no-member
                self._navigate_character(1)
            elif event.key == pygame.K_RETURN:  # pylint: disable=no-member
                self._on_start_clicked()
            elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                self._on_back_clicked()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
            if event.button == 1:
                self._handle_click(event.pos)

    def _handle_click(self, pos):
        """Maneja clicks del mouse."""
        clicked_button = self.character_ui.get_clicked_button(pos)
        if clicked_button == "back":
            self._on_back_clicked()
        elif clicked_button == "start":
            self._on_start_clicked()
        elif clicked_button == "prev":
            self._navigate_character(-1)
        elif clicked_button == "next":
            self._navigate_character(1)
