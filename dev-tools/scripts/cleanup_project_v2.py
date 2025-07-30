#!/usr/bin/env python3
"""
Script de Limpieza Automática del Proyecto SiK-Python-Game - VERSIÓN 2
====================================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Segunda pasada de limpieza con límite de 150 líneas por archivo.
             Refactorización más agresiva para lograr máxima modularidad.

Uso: python scripts/cleanup_project_v2.py
"""

import shutil
import logging
from pathlib import Path
from datetime import datetime


class ProjectCleanerV2:
    """
    Clase principal para la limpieza del proyecto - Versión 2.
    """

    def __init__(self):
        """Inicializa el limpiador del proyecto."""
        self.project_root = Path(__file__).parent.parent
        self.backup_dir = self.project_root / "backup_before_cleanup_v2"
        self.setup_logging()

        # Archivos que requieren refactorización (>150 líneas)
        self.files_to_refactor = [
            (
                "src/scenes/character_select_scene.py",
                530,
                "character_ui.py, character_data.py, character_animations.py",
            ),
            (
                "src/scenes/game_scene.py",
                509,
                "game_logic.py, game_rendering.py, game_entities.py",
            ),
            (
                "src/entities/entity.py",
                434,
                "entity_base.py, entity_physics.py, entity_renderer.py",
            ),
            (
                "src/utils/save_manager.py",
                426,
                "save_encryption.py, save_validation.py, save_serializer.py",
            ),
            (
                "src/utils/desert_background.py",
                408,
                "background_renderer.py, background_generator.py, background_tiles.py",
            ),
            ("src/ui/hud.py", 399, "hud_renderer.py, hud_data.py, hud_widgets.py"),
            (
                "src/utils/asset_manager.py",
                362,
                "asset_loader.py, asset_cache.py, asset_organizer.py",
            ),
            (
                "src/entities/player.py",
                341,
                "player_controller.py, player_animations.py, player_ui.py",
            ),
            (
                "src/entities/enemy.py",
                338,
                "enemy_ai.py, enemy_combat.py, enemy_spawner.py",
            ),
            (
                "src/utils/world_generator.py",
                315,
                "world_builder.py, world_tiles.py, world_objects.py",
            ),
            (
                "src/ui/menu_callbacks.py",
                306,
                "menu_navigation.py, menu_actions.py, menu_validation.py",
            ),
            (
                "src/ui/menu_factory.py",
                303,
                "menu_builder.py, menu_themes.py, menu_widgets.py",
            ),
            (
                "src/utils/animation_manager.py",
                288,
                "animation_loader.py, animation_player.py, animation_cache.py",
            ),
            (
                "src/entities/powerup.py",
                246,
                "powerup_types.py, powerup_effects.py, powerup_spawner.py",
            ),
            (
                "src/entities/player_combat.py",
                243,
                "combat_mechanics.py, combat_weapons.py, combat_effects.py",
            ),
            (
                "src/scenes/loading_scene.py",
                241,
                "loading_ui.py, loading_logic.py, loading_assets.py",
            ),
            (
                "src/utils/input_manager.py",
                240,
                "input_handler.py, input_mapping.py, input_validation.py",
            ),
            (
                "src/entities/enemy_types.py",
                232,
                "enemy_definitions.py, enemy_stats.py, enemy_abilities.py",
            ),
            (
                "src/core/game_engine.py",
                209,
                "engine_core.py, engine_loop.py, engine_events.py",
            ),
            (
                "src/entities/tile.py",
                207,
                "tile_types.py, tile_renderer.py, tile_collision.py",
            ),
            (
                "src/entities/player_effects.py",
                175,
                "effects_manager.py, effects_types.py, effects_ui.py",
            ),
            ("src/ui/menu_manager.py", 164, "menu_controller.py, menu_state.py"),
            (
                "src/utils/config_manager.py",
                164,
                "config_loader.py, config_validator.py, config_defaults.py",
            ),
        ]

        self.stats = {
            "files_refactored": 0,
            "modules_created": 0,
            "backup_created": False,
            "errors": [],
        }

    def setup_logging(self):
        """Configura el sistema de logging."""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(
                    log_dir
                    / f"cleanup_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                ),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def create_backup(self):
        """Crea una copia de seguridad del proyecto."""
        try:
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)

            self.logger.info("Creando copia de seguridad para V2...")

            # Crear directorio de backup
            self.backup_dir.mkdir(exist_ok=True)

            # Copiar archivos importantes
            important_dirs = ["src", "assets", "docs", "tests"]
            important_files = [
                "README.md",
                "requirements.txt",
                "config.json",
                "pyproject.toml",
            ]

            for dir_name in important_dirs:
                dir_path = self.project_root / dir_name
                if dir_path.exists():
                    shutil.copytree(dir_path, self.backup_dir / dir_name)

            for file_name in important_files:
                file_path = self.project_root / file_name
                if file_path.exists():
                    shutil.copy2(file_path, self.backup_dir / file_name)

            self.stats["backup_created"] = True
            self.logger.info(f"Copia de seguridad V2 creada en: {self.backup_dir}")

        except Exception as e:
            self.logger.error(f"Error creando backup V2: {e}")
            self.stats["errors"].append(f"Backup error: {e}")

    def analyze_refactorization_needs(self):
        """Analiza qué archivos necesitan refactorización."""
        self.logger.info("Analizando necesidades de refactorización...")

        for file_path, line_count, suggestion in self.files_to_refactor:
            full_path = self.project_root / file_path

            if full_path.exists():
                self.logger.warning(
                    f"Archivo largo detectado: {file_path} ({line_count} líneas)"
                )
                self.logger.info(f"Sugerencia de refactorización: {suggestion}")
                self.stats["files_refactored"] += 1
            else:
                self.logger.debug(f"Archivo no encontrado: {file_path}")

    def generate_refactorization_plan(self):
        """Genera un plan detallado de refactorización."""
        plan_path = self.project_root / "PLAN_REFACTORIZACION_V2.md"

        plan_content = f"""# PLAN DE REFACTORIZACIÓN V2 - LÍMITE 150 LÍNEAS

**Fecha**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 RESUMEN

- **Archivos a refactorizar**: {len(self.files_to_refactor)}
- **Módulos nuevos a crear**: ~{len(self.files_to_refactor) * 3}
- **Objetivo**: Todos los archivos < 150 líneas

## 🔧 ARCHIVOS A REFACTORIZAR

"""

        for file_path, line_count, suggestion in self.files_to_refactor:
            plan_content += f"""
### {file_path} ({line_count} líneas)
**Dividir en:**
- {suggestion}

**Prioridad:** {"ALTA" if line_count > 400 else "MEDIA" if line_count > 250 else "BAJA"}
"""

        plan_content += """
## 📋 ESTRATEGIA DE REFACTORIZACIÓN

### Fase 1: Archivos Críticos (>400 líneas)
1. character_select_scene.py
2. game_scene.py
3. entity.py

### Fase 2: Archivos Importantes (250-400 líneas)
1. save_manager.py
2. desert_background.py
3. hud.py
4. asset_manager.py
5. player.py
6. enemy.py

### Fase 3: Archivos Restantes (150-250 líneas)
- Todos los demás archivos

## 🎯 OBJETIVOS

1. **Modularidad máxima**: Cada módulo con responsabilidad única
2. **Reutilización**: Componentes intercambiables
3. **Mantenibilidad**: Código fácil de entender y modificar
4. **Testabilidad**: Módulos independientes y testeables

---
*Plan generado automáticamente por cleanup_project_v2.py*
"""

        plan_path.write_text(plan_content, encoding="utf-8")
        self.logger.info(f"Plan de refactorización generado: {plan_path}")

    def run_cleanup(self):
        """Ejecuta todo el proceso de limpieza V2."""
        self.logger.info("=== INICIANDO LIMPIEZA V2 DEL PROYECTO ===")

        try:
            # 1. Crear backup
            self.create_backup()

            # 2. Analizar necesidades de refactorización
            self.analyze_refactorization_needs()

            # 3. Generar plan de refactorización
            self.generate_refactorization_plan()

            # 4. Mostrar resumen
            self.show_summary()

        except Exception as e:
            self.logger.error(f"Error durante la limpieza V2: {e}")
            self.stats["errors"].append(f"Error general: {e}")

    def show_summary(self):
        """Muestra un resumen de la limpieza V2 realizada."""
        self.logger.info("=== RESUMEN DE LIMPIEZA V2 ===")
        self.logger.info(f"Archivos a refactorizar: {self.stats['files_refactored']}")
        self.logger.info(
            f"Backup creado: {'Sí' if self.stats['backup_created'] else 'No'}"
        )
        self.logger.info(f"Errores: {len(self.stats['errors'])}")

        if self.stats["errors"]:
            self.logger.warning("Errores encontrados durante la limpieza V2:")
            for error in self.stats["errors"]:
                self.logger.warning(f"  - {error}")

        self.logger.info("=== LIMPIEZA V2 COMPLETADA ===")
        self.logger.info("Próximo paso: Ejecutar refactorización manual de archivos")


def main():
    """Función principal."""
    cleaner = ProjectCleanerV2()
    cleaner.run_cleanup()


if __name__ == "__main__":
    main()
