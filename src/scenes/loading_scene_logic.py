"""
Loading Scene Logic - Lógica de carga y threading
==================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Manejo de la lógica de carga en segundo plano.
"""

import threading
import time
from typing import TYPE_CHECKING

from utils.logger import get_logger

if TYPE_CHECKING:
    from .loading_scene_core import LoadingSceneCore


class LoadingSceneLogic:
    """
    Lógica de carga en segundo plano para la escena de carga.
    """

    def __init__(self, core: "LoadingSceneCore"):
        """
        Inicializa la lógica de carga.

        Args:
            core: Núcleo de la escena de carga
        """
        self.core = core
        self.logger = get_logger("SiK_Game")
        self.loading_thread = None

    def start_background_loading(self):
        """Inicia la carga en segundo plano."""
        if self.loading_thread and self.loading_thread.is_alive():
            self.logger.warning("Hilo de carga ya está en ejecución")
            return

        self.loading_thread = threading.Thread(target=self._background_loading_task)
        self.loading_thread.daemon = True
        self.loading_thread.start()
        self.logger.info("Hilo de carga en segundo plano iniciado")

    def _background_loading_task(self):
        """Tarea de carga en segundo plano con configuración de progreso."""
        try:
            # Obtener configuración de carga
            loading_config = self.core.config.get_section("loading_screen")
            progress_config = loading_config.get("progress", {})

            # Configuración de tiempo
            total_duration = (
                progress_config.get("duration", 5000) / 1000.0
            )  # Convertir a segundos
            total_steps = progress_config.get("steps", len(self.core.loading_messages))
            step_duration = total_duration / total_steps if total_steps > 0 else 0.5

            self.logger.info(
                f"Iniciando carga: {total_duration:.1f}s total, {step_duration:.2f}s por paso"
            )

            for i in range(total_steps):
                # Tiempo de carga realista por paso
                time.sleep(step_duration)

                # Actualizar progreso
                progress = (i + 1) / total_steps
                message_index = min(i + 1, len(self.core.loading_messages) - 1)

                self.core.update_loading_progress(progress, message_index)
                self.logger.debug(
                    "Progreso de carga: %.1f%% - %s",
                    progress * 100,
                    self.core.loading_messages[message_index]
                    if message_index < len(self.core.loading_messages)
                    else "Completando...",
                )

            # Carga completada - pausa final para mostrar 100%
            time.sleep(0.3)
            self.core.update_loading_progress(1.0, len(self.core.loading_messages) - 1)
            self.logger.info("Carga completada exitosamente en %.1fs", total_duration)

        except (RuntimeError, OSError) as e:
            self.logger.error("Error durante la carga: %s", e)
            # Marcar como completado incluso si hay error
            self.core.update_loading_progress(1.0, len(self.core.loading_messages) - 1)

    def is_loading_active(self) -> bool:
        """
        Verifica si la carga está activa.

        Returns:
            True si la carga está en progreso
        """
        return (
            self.loading_thread is not None
            and self.loading_thread.is_alive()
            and not self.core.loading_complete
        )

    def stop_loading(self):
        """Detiene la carga si está en progreso."""
        if self.loading_thread and self.loading_thread.is_alive():
            # Marcar como completado para finalizar el hilo
            self.core.update_loading_progress(1.0, len(self.core.loading_messages) - 1)
            self.logger.info("Carga detenida manualmente")

    def get_loading_info(self) -> dict:
        """
        Obtiene información del estado de carga.

        Returns:
            Información del estado de carga
        """
        return {
            "thread_active": self.is_loading_active(),
            "thread_alive": self.loading_thread.is_alive()
            if self.loading_thread
            else False,
            "loading_state": self.core.get_loading_state(),
        }

    def validate_loading_state(self) -> bool:
        """
        Valida que el estado de carga sea consistente.

        Returns:
            True si el estado es válido
        """
        state = self.core.get_loading_state()

        # Validaciones básicas
        if not 0.0 <= state["progress"] <= 1.0:
            self.logger.error("Progreso de carga fuera de rango: %f", state["progress"])
            return False

        if state["message_index"] < 0 or state["message_index"] >= len(
            self.core.loading_messages
        ):
            self.logger.error("Índice de mensaje inválido: %d", state["message_index"])
            return False

        # Si está completo, el progreso debe ser 1.0
        if state["complete"] and state["progress"] < 1.0:
            self.logger.warning("Carga marcada como completa pero progreso < 1.0")

        return True
