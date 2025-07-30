"""
Test Unificado del Sistema
=========================

Autor: SiK Team
Fecha: 2024
Descripción: Test unificado que combina todas las funcionalidades principales del sistema.
"""

import sys
import os
import pygame
import logging
from typing import Dict

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/test_unified.log"),
            logging.StreamHandler(),
        ],
    )


class UnifiedTestSystem:
    """Sistema unificado de pruebas para todas las funcionalidades."""

    def __init__(self):
        """Inicializa el sistema de pruebas unificado."""
        self.logger = logging.getLogger(__name__)
        self.screen = None
        self.clock = None
        self.running = False

        # Configuración de la ventana
        self.screen_width = 1600
        self.screen_height = 1000

        # Estados de prueba
        self.current_test = 0
        self.test_results = {}

        # Lista de pruebas disponibles
        self.tests = [
            ("Sistema de Personajes", self.test_character_system),
            ("Sistema de Animación", self.test_animation_system),
            ("Sistema de Powerups", self.test_powerup_system),
            ("Sistema de Botones UI", self.test_ui_button_system),
            ("Sistema de Navegación", self.test_navigation_system),
            ("Sistema de Configuración", self.test_config_system),
            ("Sistema de Asset Manager", self.test_asset_manager_system),
        ]

        # Datos de personajes
        self.character_data = {
            "guerrero": {
                "nombre": "Kava",
                "tipo": "Melee",
                "stats": {
                    "vida": 200,
                    "velocidad": 180,
                    "daño": 50,
                    "escudo": 20,
                    "rango_ataque": 80,
                },
                "habilidades": [
                    "Ataque de espada",
                    "Escudo protector",
                    "Mayor resistencia",
                    "Combo de ataques",
                ],
            },
            "adventureguirl": {
                "nombre": "Sara",
                "tipo": "Ranged",
                "stats": {
                    "vida": 120,
                    "velocidad": 220,
                    "daño": 25,
                    "escudo": 5,
                    "rango_ataque": 300,
                },
                "habilidades": [
                    "Flechas mágicas",
                    "Disparo rápido",
                    "Alta movilidad",
                    "Evasión mejorada",
                ],
            },
            "robot": {
                "nombre": "Guiral",
                "tipo": "Tech",
                "stats": {
                    "vida": 150,
                    "velocidad": 160,
                    "daño": 35,
                    "escudo": 15,
                    "rango_ataque": 250,
                },
                "habilidades": [
                    "Proyectiles de energía",
                    "Misiles explosivos",
                    "Daño en área",
                    "Blindaje mejorado",
                ],
            },
            "zombiemale": {
                "nombre": "Zombie",
                "tipo": "Undead",
                "stats": {
                    "vida": 180,
                    "velocidad": 140,
                    "daño": 40,
                    "escudo": 10,
                    "rango_ataque": 120,
                },
                "habilidades": [
                    "Resistencia a veneno",
                    "Regeneración lenta",
                    "Ataque de mordida",
                    "Infección",
                ],
            },
            "zombieguirl": {
                "nombre": "Zombie Girl",
                "tipo": "Undead",
                "stats": {
                    "vida": 160,
                    "velocidad": 150,
                    "daño": 35,
                    "escudo": 8,
                    "rango_ataque": 100,
                },
                "habilidades": [
                    "Agilidad zombie",
                    "Ataque rápido",
                    "Resistencia física",
                    "Grito aterrador",
                ],
            },
        }

        # Powerups disponibles
        self.powerups = [
            "potion",
            "shield",
            "sword",
            "coin",
            "heart",
            "star",
            "crystal",
            "ring",
            "scroll",
            "key",
        ]

        # Botones UI disponibles
        self.ui_buttons = [
            ("bleft", "Botón Izquierda"),
            ("bright", "Botón Derecha"),
            ("btnmid", "Botón Medio"),
            ("btnlong", "Botón Largo"),
            ("blank", "Botón Vacío"),
            ("circle", "Botón Circular"),
            ("star", "Botón Estrella"),
            ("heart", "Botón Corazón"),
        ]

        # Colores
        self.colors = {
            "background": (20, 20, 40),
            "panel": (40, 40, 80),
            "panel_border": (80, 80, 120),
            "text": (255, 255, 255),
            "text_highlight": (255, 255, 0),
            "text_secondary": (200, 200, 200),
            "success": (0, 255, 0),
            "error": (255, 0, 0),
            "warning": (255, 165, 0),
        }

        # Fuentes
        self.fonts = {}

        # Asset manager
        self.asset_manager = None

        # Estado de animación
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = 150

        # Navegación
        self.selected_character = 0
        self.character_keys = list(self.character_data.keys())

        self.logger.info("Sistema de pruebas unificado inicializado")

    def initialize_pygame(self):
        """Inicializa pygame y componentes básicos."""
        try:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height)
            )
            pygame.display.set_caption("Test Unificado - SiK Python Game")
            self.clock = pygame.time.Clock()

            # Inicializar fuentes
            self.fonts = {
                "title": pygame.font.Font(None, 48),
                "subtitle": pygame.font.Font(None, 32),
                "normal": pygame.font.Font(None, 24),
                "small": pygame.font.Font(None, 18),
            }

            # Importar asset manager
            from utils.asset_manager import AssetManager

            self.asset_manager = AssetManager()

            self.logger.info("Pygame inicializado correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error al inicializar pygame: {e}")
            return False

    def test_character_system(self) -> Dict:
        """Prueba el sistema de personajes."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            # Probar carga de personajes
            for char_key in self.character_keys:
                sprite = self.asset_manager.get_character_sprite(char_key, "idle", 1)
                if sprite:
                    self.logger.info(f"✓ Personaje {char_key} cargado correctamente")
                else:
                    results["warnings"].append(f"Personaje {char_key} no encontrado")

            # Probar animaciones
            for char_key in self.character_keys:
                frames = self.asset_manager.get_character_animation_frames(
                    char_key, "idle"
                )
                if frames and len(frames) > 0:
                    self.logger.info(f"✓ Animación de {char_key}: {len(frames)} frames")
                else:
                    results["warnings"].append(f"Sin animación para {char_key}")

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en sistema de personajes: {e}")

        return results

    def test_animation_system(self) -> Dict:
        """Prueba el sistema de animación."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            # Probar diferentes animaciones
            animations = ["idle", "walk", "run", "attack"]

            for char_key in self.character_keys[:2]:  # Solo primeros 2 para no saturar
                for anim in animations:
                    frames = self.asset_manager.get_character_animation_frames(
                        char_key, anim
                    )
                    if frames:
                        self.logger.info(f"✓ {char_key} - {anim}: {len(frames)} frames")
                    else:
                        results["warnings"].append(
                            f"{char_key} - {anim}: no disponible"
                        )

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en sistema de animación: {e}")

        return results

    def test_powerup_system(self) -> Dict:
        """Prueba el sistema de powerups."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            for powerup in self.powerups:
                sprite = self.asset_manager.get_powerup_sprite(powerup)
                if sprite:
                    self.logger.info(f"✓ Powerup {powerup} cargado")
                else:
                    results["warnings"].append(f"Powerup {powerup} no encontrado")

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en sistema de powerups: {e}")

        return results

    def test_ui_button_system(self) -> Dict:
        """Prueba el sistema de botones UI."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            states = ["n", "h", "p", "l"]

            for button_name, button_desc in self.ui_buttons:
                for state in states:
                    sprite = self.asset_manager.get_ui_button(button_name, state)
                    if sprite:
                        self.logger.info(f"✓ Botón {button_name}_{state} cargado")
                    else:
                        results["warnings"].append(
                            f"Botón {button_name}_{state} no encontrado"
                        )

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en sistema de botones UI: {e}")

        return results

    def test_navigation_system(self) -> Dict:
        """Prueba el sistema de navegación."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            # Probar navegación entre personajes
            for i in range(len(self.character_keys)):
                self.selected_character = i
                char_key = self.character_keys[i]
                self.logger.info(f"✓ Navegación a {char_key}")

            # Resetear selección
            self.selected_character = 0

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en sistema de navegación: {e}")

        return results

    def test_config_system(self) -> Dict:
        """Prueba el sistema de configuración."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            # Probar carga de configuración
            from utils.config_manager import ConfigManager

            config = ConfigManager()

            # Verificar configuración básica
            if config.get("display", "width"):
                self.logger.info("✓ Configuración cargada correctamente")
            else:
                results["warnings"].append("Configuración incompleta")

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en sistema de configuración: {e}")

        return results

    def test_asset_manager_system(self) -> Dict:
        """Prueba el sistema de asset manager."""
        results = {"success": True, "errors": [], "warnings": []}

        try:
            # Probar métodos básicos
            if self.asset_manager:
                self.logger.info("✓ Asset Manager inicializado")

                # Probar caché
                cache_size = len(self.asset_manager.cache)
                self.logger.info(f"✓ Caché de imágenes: {cache_size} elementos")

            else:
                results["errors"].append("Asset Manager no inicializado")

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Error en Asset Manager: {e}")

        return results

    def run_all_tests(self):
        """Ejecuta todas las pruebas."""
        self.logger.info("=== INICIANDO PRUEBAS UNIFICADAS ===")

        for test_name, test_func in self.tests:
            self.logger.info(f"\n--- Ejecutando: {test_name} ---")
            try:
                result = test_func()
                self.test_results[test_name] = result

                if result["success"]:
                    self.logger.info(f"✓ {test_name}: EXITOSO")
                else:
                    self.logger.error(f"✗ {test_name}: FALLIDO")

                # Mostrar warnings
                for warning in result["warnings"]:
                    self.logger.warning(f"⚠ {warning}")

                # Mostrar errores
                for error in result["errors"]:
                    self.logger.error(f"✗ {error}")

            except Exception as e:
                self.logger.error(f"Error ejecutando {test_name}: {e}")
                self.test_results[test_name] = {
                    "success": False,
                    "errors": [str(e)],
                    "warnings": [],
                }

        self.logger.info("\n=== RESUMEN DE PRUEBAS ===")
        successful_tests = sum(
            1 for result in self.test_results.values() if result["success"]
        )
        total_tests = len(self.test_results)

        self.logger.info(f"Pruebas exitosas: {successful_tests}/{total_tests}")

        for test_name, result in self.test_results.items():
            status = "✓" if result["success"] else "✗"
            self.logger.info(f"{status} {test_name}")

    def render_test_interface(self):
        """Renderiza la interfaz de pruebas."""
        if not self.screen:
            return

        # Limpiar pantalla
        self.screen.fill(self.colors["background"])

        # Título principal
        title_text = self.fonts["title"].render(
            "Sistema Unificado de Pruebas", True, self.colors["text_highlight"]
        )
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 30))
        self.screen.blit(title_text, title_rect)

        # Subtítulo
        subtitle_text = self.fonts["subtitle"].render(
            "SiK Python Game - Test Completo", True, self.colors["text_secondary"]
        )
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 60))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Mostrar resultados de pruebas
        y_offset = 100
        for test_name, result in self.test_results.items():
            status_color = (
                self.colors["success"] if result["success"] else self.colors["error"]
            )
            status_symbol = "✓" if result["success"] else "✗"

            # Nombre de la prueba
            test_text = self.fonts["normal"].render(
                f"{status_symbol} {test_name}", True, status_color
            )
            self.screen.blit(test_text, (20, y_offset))

            # Contador de errores y warnings
            error_count = len(result["errors"])
            warning_count = len(result["warnings"])

            if error_count > 0 or warning_count > 0:
                count_text = self.fonts["small"].render(
                    f"Errores: {error_count}, Warnings: {warning_count}",
                    True,
                    self.colors["warning"],
                )
                self.screen.blit(count_text, (400, y_offset))

            y_offset += 30

        # Mostrar personaje actual
        if self.character_keys:
            char_key = self.character_keys[self.selected_character]
            char_data = self.character_data[char_key]

            # Panel de personaje
            char_panel_rect = pygame.Rect(20, y_offset + 20, 300, 200)
            pygame.draw.rect(self.screen, self.colors["panel"], char_panel_rect)
            pygame.draw.rect(
                self.screen, self.colors["panel_border"], char_panel_rect, 2
            )

            # Nombre del personaje
            char_name_text = self.fonts["subtitle"].render(
                char_data["nombre"], True, self.colors["text_highlight"]
            )
            self.screen.blit(char_name_text, (30, y_offset + 30))

            # Tipo
            char_type_text = self.fonts["normal"].render(
                char_data["tipo"], True, self.colors["text_secondary"]
            )
            self.screen.blit(char_type_text, (30, y_offset + 60))

            # Sprite del personaje
            sprite = self.asset_manager.get_character_sprite(char_key, "idle", 1)
            if sprite:
                sprite_rect = sprite.get_rect(topleft=(30, y_offset + 90))
                self.screen.blit(sprite, sprite_rect)

        # Mostrar powerups
        powerup_y = y_offset + 240
        powerup_text = self.fonts["subtitle"].render(
            "Powerups:", True, self.colors["text_highlight"]
        )
        self.screen.blit(powerup_text, (20, powerup_y))

        powerup_x = 20
        for powerup in self.powerups[:8]:  # Mostrar solo los primeros 8
            sprite = self.asset_manager.load_image(f"objects/varios/{powerup}.png")
            if sprite:
                sprite_rect = sprite.get_rect(topleft=(powerup_x, powerup_y + 40))
                self.screen.blit(sprite, sprite_rect)

                # Nombre del powerup
                name_text = self.fonts["small"].render(
                    powerup, True, self.colors["text"]
                )
                self.screen.blit(name_text, (powerup_x, powerup_y + 70))

            powerup_x += 80

        # Instrucciones
        instructions = "ESPACIO: Siguiente prueba • ENTER: Ejecutar todas • ESC: Salir"
        inst_text = self.fonts["small"].render(
            instructions, True, self.colors["text_secondary"]
        )
        inst_rect = inst_text.get_rect(
            center=(self.screen_width // 2, self.screen_height - 30)
        )
        self.screen.blit(inst_text, inst_rect)

        # Actualizar pantalla
        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos de pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Siguiente prueba
                    self.current_test = (self.current_test + 1) % len(self.tests)
                    test_name, test_func = self.tests[self.current_test]
                    self.logger.info(f"Ejecutando: {test_name}")
                    self.test_results[test_name] = test_func()
                elif event.key == pygame.K_RETURN:
                    # Ejecutar todas las pruebas
                    self.run_all_tests()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # Personaje anterior
                    self.selected_character = (self.selected_character - 1) % len(
                        self.character_keys
                    )
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # Personaje siguiente
                    self.selected_character = (self.selected_character + 1) % len(
                        self.character_keys
                    )

    def run(self):
        """Ejecuta el sistema de pruebas unificado."""
        if not self.initialize_pygame():
            return

        self.running = True

        # Ejecutar todas las pruebas al inicio
        self.run_all_tests()

        while self.running:
            self.handle_events()
            self.render_test_interface()
            self.clock.tick(60)

        pygame.quit()
        self.logger.info("Sistema de pruebas unificado finalizado")


def main():
    """Función principal."""
    print("=== SISTEMA UNIFICADO DE PRUEBAS ===")

    # Configurar logging
    setup_logging()

    # Crear y ejecutar el sistema de pruebas
    test_system = UnifiedTestSystem()
    test_system.run()


if __name__ == "__main__":
    main()
