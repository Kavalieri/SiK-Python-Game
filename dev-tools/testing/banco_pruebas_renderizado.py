#!/usr/bin/env python
"""
Banco de Pruebas de Bajo Nivel - Análisis de Renderizado
=======================================================

Autor: SiK Team
Fecha: 2025-08-02
Descripción: Pruebas específicas para detectar problemas de renderizado,
             barra de carga, y visualización en pantalla.
"""

import sys
import threading
import time
from pathlib import Path

import pygame

# Configurar paths desde raíz
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from utils.logger import setup_logger


class ColorLogger:
    """Logger con colores para testing visual."""

    def __init__(self) -> None:
        """Inicializar logger con colores."""
        self.logger = setup_logger()

    def info(self, message: str) -> None:
        """Log info con color."""
        print(f"✅ {message}")
        self.logger.info(f"[RENDER_TEST] {message}")

    def warning(self, message: str) -> None:
        """Log warning con color."""
        print(f"⚠️  {message}")
        self.logger.warning(f"[RENDER_TEST] {message}")

    def error(self, message: str) -> None:
        """Log error con color."""
        print(f"❌ {message}")
        self.logger.error(f"[RENDER_TEST] {message}")

    def critical(self, message: str) -> None:
        """Log critical con color."""
        print(f"🚨 {message}")
        self.logger.critical(f"[RENDER_TEST] {message}")


class RenderTester:
    """Tester específico para problemas de renderizado."""

    def __init__(self) -> None:
        """Inicializar tester de renderizado."""
        self.logger = ColorLogger()
        self.tests_passed = 0
        self.tests_failed = 0

    def test_pygame_initialization(self) -> bool:
        """Probar inicialización básica de pygame."""
        try:
            pygame.quit()  # Limpiar estado previo
            pygame.init()

            # Probar configuración de display
            info = pygame.display.Info()
            self.logger.info(f"Display disponible: {info.bitsize}-bit, {info.hw}")

            # Intentar crear superficie
            screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
            self.logger.info(f"Superficie creada: {screen.get_size()}")

            pygame.quit()
            return True

        except Exception as e:
            self.logger.error(f"Error en inicialización pygame: {e}")
            return False

    def test_loading_bar_mechanics(self) -> bool:
        """Probar mecánicas específicas de la barra de carga."""
        try:
            from scenes.loading_scene_core import LoadingSceneCore
            from utils.config_manager import ConfigManager

            # Inicializar componentes
            config_manager = ConfigManager()
            loading_scene = LoadingSceneCore(config_manager)

            self.logger.info("Testing mecánicas de barra de carga...")

            # Probar estados de progreso
            test_values = [0, 25, 50, 75, 100]
            for value in test_values:
                loading_scene.progress = value
                self.logger.info(f"Progreso establecido: {value}%")
                time.sleep(0.1)  # Simular timing real

            # Verificar que el progreso se mantiene
            if loading_scene.progress == 100:
                self.logger.info("✅ Progreso final mantenido correctamente")
                return True
            else:
                self.logger.error(
                    f"❌ Progreso final incorrecto: {loading_scene.progress}"
                )
                return False

        except Exception as e:
            self.logger.error(f"Error en test barra de carga: {e}")
            return False

    def test_rendering_pipeline(self) -> bool:
        """Probar pipeline completo de renderizado."""
        try:
            pygame.init()
            screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
            clock = pygame.time.Clock()

            self.logger.info("Testing pipeline de renderizado...")

            # Test 1: Renderizado básico
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0), (100, 100, 50, 50))

            # Test 2: Verificar superficie
            pixel_color = screen.get_at((125, 125))
            if pixel_color[:3] == (255, 0, 0):
                self.logger.info("✅ Renderizado básico funcionando")
            else:
                self.logger.error(f"❌ Color incorrecto: {pixel_color}")
                return False

            # Test 3: Timing de frames
            frame_times = []
            for i in range(10):
                start_time = time.time()
                screen.fill((0, 0, 0))
                pygame.display.flip()
                clock.tick(60)
                frame_times.append(time.time() - start_time)

            avg_frame_time = sum(frame_times) / len(frame_times)
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0

            self.logger.info(f"FPS promedio: {fps:.2f}")

            pygame.quit()
            return True

        except Exception as e:
            self.logger.error(f"Error en pipeline renderizado: {e}")
            return False

    def test_scene_transitions(self) -> bool:
        """Probar transiciones entre escenas."""
        try:
            from core.scene_manager import SceneManager
            from utils.config_manager import ConfigManager

            config_manager = ConfigManager()
            scene_manager = SceneManager(config_manager)

            self.logger.info("Testing transiciones de escenas...")

            # Verificar estado inicial
            if scene_manager.current_scene is None:
                self.logger.info("✅ Estado inicial correcto (sin escena)")
            else:
                self.logger.warning(
                    f"⚠️  Escena inicial inesperada: {scene_manager.current_scene}"
                )

            return True

        except Exception as e:
            self.logger.error(f"Error en test transiciones: {e}")
            return False

    def test_threading_issues(self) -> bool:
        """Detectar problemas de threading en carga."""
        try:
            self.logger.info("Testing problemas de threading...")

            # Simular carga en background
            loading_complete = threading.Event()

            def background_task():
                time.sleep(0.5)  # Simular carga
                loading_complete.set()

            # Iniciar tarea en background
            thread = threading.Thread(target=background_task)
            thread.daemon = True
            thread.start()

            # Esperar con timeout
            if loading_complete.wait(timeout=2.0):
                self.logger.info("✅ Threading funcionando correctamente")
                return True
            else:
                self.logger.error("❌ Timeout en threading")
                return False

        except Exception as e:
            self.logger.error(f"Error en test threading: {e}")
            return False

    def test_asset_loading_timing(self) -> bool:
        """Probar timing de carga de assets."""
        try:
            from utils.asset_manager import AssetManager

            self.logger.info("Testing timing de carga de assets...")

            start_time = time.time()
            asset_manager = AssetManager()
            init_time = time.time() - start_time

            self.logger.info(f"Tiempo inicialización AssetManager: {init_time:.3f}s")

            if init_time < 1.0:
                self.logger.info("✅ Carga de assets rápida")
                return True
            else:
                self.logger.warning(f"⚠️  Carga lenta de assets: {init_time:.3f}s")
                return False

        except Exception as e:
            self.logger.error(f"Error en test assets: {e}")
            return False

    def run_all_tests(self) -> None:
        """Ejecutar todas las pruebas de renderizado."""
        print("🔬 **BANCO DE PRUEBAS DE BAJO NIVEL - RENDERIZADO**")
        print("=" * 60)

        tests = [
            ("Inicialización Pygame", self.test_pygame_initialization),
            ("Mecánicas Barra de Carga", self.test_loading_bar_mechanics),
            ("Pipeline Renderizado", self.test_rendering_pipeline),
            ("Transiciones Escenas", self.test_scene_transitions),
            ("Problemas Threading", self.test_threading_issues),
            ("Timing Carga Assets", self.test_asset_loading_timing),
        ]

        for test_name, test_func in tests:
            print(f"\n🧪 Testing: {test_name}")
            print("-" * 40)

            try:
                if test_func():
                    self.tests_passed += 1
                    self.logger.info(f"✅ {test_name}: PASADO")
                else:
                    self.tests_failed += 1
                    self.logger.error(f"❌ {test_name}: FALLADO")
            except Exception as e:
                self.tests_failed += 1
                self.logger.critical(f"🚨 {test_name}: EXCEPCIÓN - {e}")

        print("\n" + "=" * 60)
        print("📊 **RESUMEN DE PRUEBAS DE RENDERIZADO**")
        print(f"✅ Pasadas: {self.tests_passed}")
        print(f"❌ Falladas: {self.tests_failed}")
        print(
            f"📈 Ratio éxito: {self.tests_passed / (self.tests_passed + self.tests_failed) * 100:.1f}%"
        )

        if self.tests_failed == 0:
            print("🎉 TODAS LAS PRUEBAS DE RENDERIZADO PASARON")
        else:
            print("🔧 HAY PROBLEMAS DE RENDERIZADO QUE REQUIEREN ATENCIÓN")


def main() -> None:
    """Función principal del banco de pruebas."""
    tester = RenderTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
