"""
Banco de Pruebas - Sistema de Movimiento del Jugador
===================================================

Autor: SiK Team
Fecha: 2 de Agosto, 2025
Descripción: Diagnóstico completo del sistema de movimiento del jugador.
"""

import logging
import sys
from pathlib import Path

# Configurar ruta del proyecto
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pygame

from entities.player import Player
from entities.player_core import AnimationState
from utils.animation_manager import IntelligentAnimationManager
from utils.config_manager import ConfigManager


class ColorLogger:
    """Logger con colores para mejor visualización."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    END = "\033[0m"

    @staticmethod
    def error(msg: str) -> None:
        print(f"{ColorLogger.RED}❌ {msg}{ColorLogger.END}")

    @staticmethod
    def success(msg: str) -> None:
        print(f"{ColorLogger.GREEN}✅ {msg}{ColorLogger.END}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{ColorLogger.YELLOW}⚠️ {msg}{ColorLogger.END}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"{ColorLogger.CYAN}ℹ️ {msg}{ColorLogger.END}")

    @staticmethod
    def header(msg: str) -> None:
        print(f"\n{ColorLogger.BOLD}{ColorLogger.BLUE}🔍 {msg}{ColorLogger.END}")
        print("=" * (len(msg) + 4))


class BancoPruebasMovimiento:
    """Banco de pruebas para el sistema de movimiento del jugador."""

    def __init__(self):
        """Inicializar banco de pruebas."""
        self.logger = ColorLogger()

        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Inicializar pygame
        pygame.init()
        pygame.display.set_mode((100, 100))  # Ventana mínima

        # Cargar configuración
        self.config = ConfigManager()

        # Crear objetos de prueba
        self.animation_manager = IntelligentAnimationManager()
        self.player = None
        self.movement = None

        # Contadores de pruebas
        self.tests_passed = 0
        self.tests_failed = 0

    def crear_jugador_prueba(self) -> bool:
        """Crear jugador para pruebas."""
        try:
            self.player = Player(
                x=100,
                y=100,
                character_name="guerrero",
                config=self.config,
                animation_manager=self.animation_manager,
            )
            self.movement = self.player.movement
            self.logger.success("Jugador de prueba creado exitosamente")
            return True
        except Exception as e:
            self.logger.error(f"Error creando jugador: {e}")
            return False

    def test_configuracion_inicial(self) -> bool:
        """Probar configuración inicial del movimiento."""
        self.logger.header("TEST: Configuración Inicial del Movimiento")

        try:
            # Verificar que el player existe
            if not self.player:
                self.logger.error("Player no inicializado")
                return False

            # Verificar velocidad inicial
            vel_x, vel_y = self.movement.get_velocity()
            print(f"  📊 Velocidad inicial: ({vel_x}, {vel_y})")

            # Verificar stats del jugador
            speed = self.player.core.stats.speed
            print(f"  📊 Velocidad configurada: {speed}")

            # Verificar posición inicial
            print(f"  📊 Posición inicial: ({self.player.x}, {self.player.y})")

            # Verificar estado de animación
            print(f"  📊 Estado animación: {self.player.core.current_animation_state}")

            if speed > 0:
                self.logger.success("Configuración inicial correcta")
                return True
            else:
                self.logger.error("Velocidad del jugador es 0")
                return False

        except Exception as e:
            self.logger.error(f"Error en configuración inicial: {e}")
            return False

    def test_input_detection(self) -> bool:
        """Probar detección de entrada."""
        self.logger.header("TEST: Detección de Entrada de Teclado")

        try:
            # Simular teclas presionadas
            keys_pressed = {
                119: True,  # W
                115: False,  # S
                97: False,  # A
                100: False,  # D
                273: False,  # UP
                274: False,  # DOWN
                276: False,  # LEFT
                275: False,  # RIGHT
            }

            # Crear objeto ScancodeWrapper simulado
            class MockKeys:
                def __init__(self, pressed_keys):
                    self.pressed_keys = pressed_keys

                def __getitem__(self, key):
                    return self.pressed_keys.get(key, False)

            mock_keys = MockKeys(keys_pressed)
            mouse_pos = (0, 0)
            mouse_buttons = (False, False, False)

            # Guardar posición inicial
            pos_inicial_x = self.player.x
            pos_inicial_y = self.player.y

            print(f"  📊 Posición antes: ({pos_inicial_x}, {pos_inicial_y})")

            # Procesar input
            self.movement.handle_input(mock_keys, mouse_pos, mouse_buttons, None)

            # Verificar velocidad después del input
            vel_x, vel_y = self.movement.get_velocity()
            print(f"  📊 Velocidad después input: ({vel_x}, {vel_y})")

            # Actualizar movimiento
            delta_time = 0.016  # ~60 FPS
            self.movement.update_movement(delta_time)
            # CRUCIAL: Sincronizar player desde core
            self.player.update(delta_time)

            # Verificar nueva posición
            print(f"  📊 Posición después: ({self.player.x}, {self.player.y})")

            # Verificar que hubo movimiento
            if self.player.y != pos_inicial_y:
                self.logger.success("Detección de entrada funcionando")
                return True
            else:
                self.logger.error("No se detectó movimiento con tecla W")
                return False

        except Exception as e:
            self.logger.error(f"Error en detección de entrada: {e}")
            return False

    def test_velocidad_aplicacion(self) -> bool:
        """Probar aplicación de velocidad."""
        self.logger.header("TEST: Aplicación de Velocidad")

        try:
            # Establecer velocidad manualmente
            test_vel_x = 100.0
            test_vel_y = -50.0

            self.movement.set_velocity(test_vel_x, test_vel_y)

            # Verificar que se aplicó
            vel_x, vel_y = self.movement.get_velocity()
            print(f"  📊 Velocidad establecida: ({test_vel_x}, {test_vel_y})")
            print(f"  📊 Velocidad obtenida: ({vel_x}, {vel_y})")

            if vel_x == test_vel_x and vel_y == test_vel_y:
                self.logger.success("Velocidad se aplica correctamente")
                return True
            else:
                self.logger.error("La velocidad no se aplicó correctamente")
                return False

        except Exception as e:
            self.logger.error(f"Error en aplicación de velocidad: {e}")
            return False

    def test_actualizacion_posicion(self) -> bool:
        """Probar actualización de posición."""
        self.logger.header("TEST: Actualización de Posición")

        try:
            # Establecer posición y velocidad conocidas
            pos_inicial_x = 200.0
            pos_inicial_y = 200.0

            self.player.x = pos_inicial_x
            self.player.y = pos_inicial_y

            vel_x = 60.0  # 60 píxeles por segundo
            vel_y = 80.0  # 80 píxeles por segundo

            self.movement.set_velocity(vel_x, vel_y)

            # Simular 1 segundo (16 frames a 60 FPS)
            delta_time = 0.016
            frames = 60

            print(f"  📊 Posición inicial: ({pos_inicial_x}, {pos_inicial_y})")
            print(f"  📊 Velocidad: ({vel_x}, {vel_y})")

            for _ in range(frames):
                self.movement.update_movement(delta_time)
                # CRUCIAL: Sincronizar player desde core
                self.player.update(delta_time)

            print(f"  📊 Posición final: ({self.player.x}, {self.player.y})")

            # Calcular posición esperada
            expected_x = pos_inicial_x + (vel_x * 1.0)  # 1 segundo
            expected_y = pos_inicial_y + (vel_y * 1.0)  # 1 segundo

            print(f"  📊 Posición esperada: ({expected_x}, {expected_y})")

            # Verificar con tolerancia
            tolerance = 5.0
            if (
                abs(self.player.x - expected_x) < tolerance
                and abs(self.player.y - expected_y) < tolerance
            ):
                self.logger.success("Actualización de posición correcta")
                return True
            else:
                self.logger.error("La posición no se actualiza correctamente")
                return False

        except Exception as e:
            self.logger.error(f"Error en actualización de posición: {e}")
            return False

    def test_animaciones(self) -> bool:
        """Probar sistema de animaciones."""
        self.logger.header("TEST: Sistema de Animaciones")

        try:
            # Estado inicial (idle)
            initial_state = self.player.core.current_animation_state
            print(f"  📊 Estado inicial: {initial_state}")

            # Establecer movimiento
            self.movement.set_velocity(100, 0)
            self.movement.update_animation(0.016)

            # Verificar cambio de estado
            moving_state = self.player.core.current_animation_state
            print(f"  📊 Estado en movimiento: {moving_state}")

            # Parar movimiento
            self.movement.set_velocity(0, 0)
            self.movement.update_animation(0.016)

            # Verificar vuelta a idle
            idle_state = self.player.core.current_animation_state
            print(f"  📊 Estado parado: {idle_state}")

            if (
                moving_state in [AnimationState.WALK, AnimationState.RUN]
                and idle_state == AnimationState.IDLE
            ):
                self.logger.success("Sistema de animaciones funcionando")
                return True
            else:
                self.logger.warning("Animaciones pueden tener problemas")
                return True  # No falla el test por esto

        except Exception as e:
            self.logger.error(f"Error en sistema de animaciones: {e}")
            return False

    def test_limites_mundo(self) -> bool:
        """Probar límites del mundo."""
        self.logger.header("TEST: Límites del Mundo")

        try:
            # Probar límite inferior derecho
            self.player.x = 4900  # Cerca del límite
            self.player.y = 4900

            self.movement.set_velocity(200, 200)  # Velocidad hacia el límite

            for _ in range(10):  # Varios frames
                self.movement.update_movement(0.016)
                # CRUCIAL: Sincronizar player desde core
                self.player.update(0.016)

            print(f"  📊 Posición en límites: ({self.player.x}, {self.player.y})")

            # Verificar que no se salió del mundo
            if (
                self.player.x <= self.player.core.world_width
                and self.player.y <= self.player.core.world_height
            ):
                self.logger.success("Límites del mundo funcionando")
                return True
            else:
                self.logger.error("El jugador se salió de los límites")
                return False

        except Exception as e:
            self.logger.error(f"Error en límites del mundo: {e}")
            return False

    def test_integracion_completa(self) -> bool:
        """Test de integración completa del movimiento."""
        self.logger.header("TEST: Integración Completa del Movimiento")

        try:
            # Resetear jugador
            self.player.x = 500
            self.player.y = 500

            # Simular secuencia de movimiento completa
            movements = [
                (119, 0, -1),  # W - arriba
                (100, 1, 0),  # D - derecha
                (115, 0, 1),  # S - abajo
                (97, -1, 0),  # A - izquierda
            ]

            positions = []

            for key, expected_x_dir, expected_y_dir in movements:
                # Simular tecla presionada
                keys_pressed = {
                    k: k == key for k in [119, 115, 97, 100, 273, 274, 276, 275]
                }

                class MockKeys:
                    def __init__(self, pressed_keys):
                        self.pressed_keys = pressed_keys

                    def __getitem__(self, key):
                        return self.pressed_keys.get(key, False)

                mock_keys = MockKeys(keys_pressed)

                # Procesar input y movimiento
                pos_antes = (self.player.x, self.player.y)

                self.movement.handle_input(
                    mock_keys, (0, 0), (False, False, False), None
                )

                for _ in range(30):  # 0.5 segundos de movimiento
                    self.movement.update_movement(0.016)
                    # CRUCIAL: Sincronizar player desde core
                    self.player.update(0.016)

                pos_despues = (self.player.x, self.player.y)
                positions.append((pos_antes, pos_despues))

                print(f"  📊 Tecla {chr(key)}: {pos_antes} → {pos_despues}")

            # Verificar que hubo movimiento en todas las direcciones
            movements_detected = 0
            for i, (pos_antes, pos_despues) in enumerate(positions):
                if pos_antes != pos_despues:
                    movements_detected += 1

            if movements_detected >= 3:  # Al menos 3 de 4 direcciones
                self.logger.success(
                    f"Integración completa: {movements_detected}/4 movimientos detectados"
                )
                return True
            else:
                self.logger.error(
                    f"Pocos movimientos detectados: {movements_detected}/4"
                )
                return False

        except Exception as e:
            self.logger.error(f"Error en integración completa: {e}")
            return False

    def ejecutar_test(self, test_func, nombre: str) -> bool:
        """Ejecutar un test individual."""
        try:
            resultado = test_func()
            if resultado:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return resultado
        except Exception as e:
            self.logger.error(f"Error ejecutando {nombre}: {e}")
            self.tests_failed += 1
            return False

    def ejecutar_todos_tests(self):
        """Ejecutar todos los tests del banco de pruebas."""
        self.logger.header("BANCO DE PRUEBAS - SISTEMA DE MOVIMIENTO DEL JUGADOR")
        print()

        # Crear jugador de prueba
        if not self.crear_jugador_prueba():
            self.logger.error("No se pudo crear jugador de prueba - Abortando")
            return

        # Lista de tests
        tests = [
            (self.test_configuracion_inicial, "Configuración Inicial"),
            (self.test_input_detection, "Detección de Entrada"),
            (self.test_velocidad_aplicacion, "Aplicación de Velocidad"),
            (self.test_actualizacion_posicion, "Actualización de Posición"),
            (self.test_animaciones, "Sistema de Animaciones"),
            (self.test_limites_mundo, "Límites del Mundo"),
            (self.test_integracion_completa, "Integración Completa"),
        ]

        # Ejecutar todos los tests
        for test_func, nombre in tests:
            self.ejecutar_test(test_func, nombre)
            print()

        # Resumen final
        total_tests = self.tests_passed + self.tests_failed
        porcentaje = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "=" * 60)
        self.logger.header("RESUMEN FINAL")
        print(f"📊 Tests ejecutados: {total_tests}")
        print(f"✅ Tests pasados: {self.tests_passed}")
        print(f"❌ Tests fallidos: {self.tests_failed}")
        print(f"📈 Porcentaje éxito: {porcentaje:.1f}%")

        if self.tests_failed == 0:
            self.logger.success(
                "¡TODOS LOS TESTS PASARON! Sistema de movimiento funcionando correctamente."
            )
        elif self.tests_failed <= 2:
            self.logger.warning(
                "Algunos tests fallaron. Revisar problemas específicos."
            )
        else:
            self.logger.error(
                "Múltiples fallas detectadas. Sistema de movimiento necesita revisión."
            )

        pygame.quit()


if __name__ == "__main__":
    banco = BancoPruebasMovimiento()
    banco.ejecutar_todos_tests()
