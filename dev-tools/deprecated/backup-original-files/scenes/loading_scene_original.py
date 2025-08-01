"""
Loading Scene - Escena de Carga
=============================

Autor: SiK Team
Fecha: 2024
Descripción: Escena de carga con progreso visual y carga en segundo plano.
"""

import json
import random
import threading
import time
from collections.abc import Callable

import pygame

from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger


class LoadingScene(Scene):
    """
    Escena de carga que muestra el progreso mientras se cargan los recursos.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        config: ConfigManager,
        game_state,
        save_manager,
        on_loading_complete: Callable = None,
    ):
        """
        Inicializa la escena de carga.

        Args:
                screen: Superficie de pantalla
                config: Configuración del juego
                game_state: Estado del juego
                save_manager: Gestor de guardado
                on_loading_complete: Callback cuando termine la carga
        """
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")
        self.logger.info("[LoadingScene] Escena de carga inicializada")

        # Estado de carga
        self.loading_progress = 0.0
        self.loading_complete = False
        self.loading_messages = [
            "Inicializando motor del juego...",
            "Cargando configuración...",
            "Preparando recursos gráficos...",
            "Generando mundo...",
            "Cargando personajes...",
            "Preparando enemigos...",
            "Configurando controles...",
            "¡Listo para jugar!",
        ]
        self.current_message_index = 0
        self.message_timer = 0
        self.message_duration = 1.0  # 1 segundo por mensaje

        # Callback de finalización
        self.on_loading_complete = on_loading_complete

        # Iniciar carga en segundo plano
        self.loading_thread = None
        self.start_background_loading()

        self._has_advanced = False  # Para evitar múltiples llamadas
        # Cargar configuración de pantalla de carga
        self.loading_screen_config = self._load_loading_screen_config()
        self.tips = self.loading_screen_config.get(
            "tips",
            [
                "Rompe las cajas para encontrar valiosas recompensas.",
                "Prioriza la supervivencia: cuanto más avances, más puntos obtienes.",
                "Los cactus dañan al contacto, ¡evítalos!",
            ],
        )
        self.title = self.loading_screen_config.get("title", "SiK Python Game")
        self.subtitle = self.loading_screen_config.get("subtitle", "Cargando...")
        self.version = self.loading_screen_config.get("version", "v1.0.0")
        self.current_tip = random.choice(self.tips)

        self.logger.info("Escena de carga inicializada")

    def start_background_loading(self):
        """Inicia la carga en segundo plano."""
        self.loading_thread = threading.Thread(target=self._background_loading_task)
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def _background_loading_task(self):
        """Tarea de carga en segundo plano."""
        try:
            # Simular carga de recursos
            total_steps = len(self.loading_messages) - 1

            for i in range(total_steps):
                # Simular tiempo de carga
                time.sleep(0.5)  # 0.5 segundos por paso

                # Actualizar progreso
                self.loading_progress = (i + 1) / total_steps
                self.current_message_index = i + 1

                self.logger.debug(f"Progreso de carga: {self.loading_progress:.1%}")

            # Carga completada
            time.sleep(0.5)
            self.loading_complete = True
            self.loading_progress = 1.0
            self.current_message_index = len(self.loading_messages) - 1

            self.logger.info("Carga completada")

        except Exception as e:
            self.logger.error(f"Error durante la carga: {e}")
            self.loading_complete = True

    def handle_event(self, event: pygame.event.Event):
        """Maneja eventos de la escena de carga."""
        self.logger.info(f"[LoadingScene] Evento recibido: {event.type} - {event}")
        # En la escena de carga, solo permitir cerrar la ventana o continuar tras la carga
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if self.loading_complete and not self._has_advanced:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self._has_advanced = True
                if self.on_loading_complete:
                    self.on_loading_complete()

    def update(self):
        """Actualiza la lógica de la escena de carga."""
        # Actualizar timer de mensajes
        self.message_timer += 1.0 / 60.0  # Asumiendo 60 FPS
        # Ya no cambiamos de escena automáticamente tras la carga

    def render(self):
        """Renderiza la escena de carga."""
        # Fondo con gradiente
        self._render_background()

        # Título
        self._render_title()

        # Barra de progreso
        self._render_progress_bar()

        # Mensaje actual
        self._render_current_message()

        # Indicador de carga animado
        self._render_loading_indicator()

        # Información adicional
        self._render_additional_info()

    def _render_background(self):
        """Renderiza el fondo con gradiente."""
        # Crear gradiente de fondo
        height = self.screen.get_height()
        for y in range(height):
            # Gradiente de azul oscuro a azul claro
            ratio = y / height
            color = (
                int(20 + ratio * 30),  # R
                int(40 + ratio * 60),  # G
                int(80 + ratio * 100),  # B
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))

    def _render_title(self):
        """Renderiza el título del juego."""
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)

        # Título principal configurable
        title_text = font_large.render(self.title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Subtítulo configurable
        subtitle_text = font_small.render(self.subtitle, True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(
            center=(self.screen.get_width() // 2, 200)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

    def _render_progress_bar(self):
        """Renderiza la barra de progreso."""
        bar_width = 600
        bar_height = 30
        bar_x = (self.screen.get_width() - bar_width) // 2
        bar_y = 300

        # Fondo de la barra
        pygame.draw.rect(
            self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height)
        )
        pygame.draw.rect(
            self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2
        )

        # Barra de progreso
        progress_width = int(bar_width * self.loading_progress)
        if progress_width > 0:
            # Gradiente de color según el progreso
            if self.loading_progress < 0.5:
                color = (255, 100, 100)  # Rojo
            elif self.loading_progress < 0.8:
                color = (255, 255, 100)  # Amarillo
            else:
                color = (100, 255, 100)  # Verde

            pygame.draw.rect(
                self.screen, color, (bar_x, bar_y, progress_width, bar_height)
            )

        # Texto de progreso
        font = pygame.font.Font(None, 24)
        progress_text = font.render(
            f"{self.loading_progress:.1%}", True, (255, 255, 255)
        )
        progress_rect = progress_text.get_rect(
            center=(self.screen.get_width() // 2, bar_y + bar_height + 20)
        )
        self.screen.blit(progress_text, progress_rect)

    def _render_current_message(self):
        """Renderiza el mensaje actual de carga."""
        if self.current_message_index < len(self.loading_messages):
            font = pygame.font.Font(None, 28)
            message = self.loading_messages[self.current_message_index]
            message_text = font.render(message, True, (220, 220, 220))
            message_rect = message_text.get_rect(
                center=(self.screen.get_width() // 2, 400)
            )
            self.screen.blit(message_text, message_rect)

    def _render_loading_indicator(self):
        """
        Renderiza un indicador de carga animado.

        Ejemplo:
            >>> self._render_loading_indicator()
        """
        dot_count = 3
        dot_spacing = 20
        animation_speed = 0.3
        dot_offset = int((time.time() * animation_speed) % dot_count)

        start_x = self.screen.get_width() // 2 - (dot_count * dot_spacing) // 2
        y = 450

        for i in range(dot_count):
            x = start_x + i * dot_spacing
            alpha = 255 if i == dot_offset else 100
            color = (255, 255, 255, alpha)

            # Crear superficie con alpha
            dot_surface = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(dot_surface, color, (4, 4), 4)
            self.screen.blit(dot_surface, (x, y))

    def _render_additional_info(self):
        """Renderiza información adicional."""
        font = pygame.font.Font(None, 20)

        # Versión configurable
        version_text = font.render(self.version, True, (150, 150, 150))
        version_rect = version_text.get_rect(
            bottomright=(self.screen.get_width() - 20, self.screen.get_height() - 20)
        )
        self.screen.blit(version_text, version_rect)

        # Consejo aleatorio
        tip_text = font.render(f"Consejo: {self.current_tip}", True, (180, 220, 255))
        tip_rect = tip_text.get_rect(center=(self.screen.get_width() // 2, 500))
        self.screen.blit(tip_text, tip_rect)

        # Instrucciones
        if self.loading_complete:
            instruction_text = font.render(
                "Presiona cualquier tecla para continuar", True, (200, 200, 200)
            )
            instruction_rect = instruction_text.get_rect(
                center=(self.screen.get_width() // 2, 550)
            )
            self.screen.blit(instruction_text, instruction_rect)

    def _load_loading_screen_config(self):
        """
        Carga la configuración de la pantalla de carga desde un archivo JSON.

        Returns:
            dict: Configuración de la pantalla de carga.

        Ejemplo:
            >>> config = self._load_loading_screen_config()
            >>> print(config.get("title"))
        """
        try:
            with open("config/loading_screen.json", encoding="utf-8") as f:
                config = json.load(f)
                self.logger.info(
                    "Configuración de pantalla de carga cargada correctamente."
                )
                return config
        except FileNotFoundError:
            self.logger.warning(
                "Archivo de configuración de pantalla de carga no encontrado. Usando valores por defecto."
            )
        except json.JSONDecodeError as e:
            self.logger.error(f"Error al decodificar JSON: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado al cargar configuración: {e}")
        return {}
