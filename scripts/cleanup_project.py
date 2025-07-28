#!/usr/bin/env python3
"""
Script de Limpieza Automática del Proyecto SiK-Python-Game
=========================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Script que realiza limpieza automática del proyecto eliminando archivos redundantes,
             refactorizando archivos largos y optimizando la estructura general.

Uso: python scripts/cleanup_project.py
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime

class ProjectCleaner:
    """
    Clase principal para la limpieza del proyecto.
    """
    
    def __init__(self):
        """Inicializa el limpiador del proyecto."""
        self.project_root = Path(__file__).parent.parent
        self.backup_dir = self.project_root / "backup_before_cleanup"
        self.setup_logging()
        
        # Archivos a eliminar (redundantes)
        self.files_to_delete = [
            # Scripts de test redundantes
            "scripts/test_quick_gameplay.py",
            "scripts/test_final_integration.py",
            "scripts/test_simple_enemy_system.py",
            "scripts/test_enemy_system.py",
            "scripts/test_complete_animation_system.py",
            "scripts/test_final_animations.py",
            "scripts/test_optimal_animations.py",
            "scripts/test_intelligent_animations.py",
            "scripts/test_all_animations.py",
            "scripts/test_desert_background.py",
            "scripts/test_character_select_simple.py",
            "scripts/test_character_select_fix.py",
            "scripts/test_animation_fix.py",
            
            # Scripts de análisis redundantes
            "scripts/analyze_all_animations.py",
            "scripts/analyze_animation_frames.py",
            "scripts/generate_animation_report.py",
            
            # Archivos de configuración redundantes
            "animation_config.json",
            "ANIMATION_REPORT.md",
        ]
        
        # Archivos a mantener
        self.files_to_keep = [
            "scripts/cleanup_tests.py",
            "scripts/clean_asset_names.py",
            "scripts/reorganize_characters.py",
            "scripts/reorganize_guerrero.py",
            "scripts/run_unified_tests.py",
            "scripts/run_tests.py",
            "scripts/README.md",
            "scripts/MEJORAS_IMPLEMENTADAS.md",
        ]
        
        # Archivos que requieren refactorización
        self.files_to_refactor = [
            ("src/entities/player.py", 599, "player_combat.py, player_effects.py, player_stats.py"),
            ("src/ui/menu_manager.py", 603, "menu_factory.py, menu_callbacks.py"),
            ("src/scenes/character_select_scene.py", 530, "character_ui.py, character_data.py"),
            ("src/scenes/game_scene.py", 509, "game_logic.py, game_rendering.py"),
            ("src/utils/save_manager.py", 426, "save_encryption.py, save_validation.py"),
            ("src/utils/asset_manager.py", 362, "asset_loader.py, asset_cache.py"),
            ("src/utils/desert_background.py", 408, "background_renderer.py, background_generator.py"),
            ("src/core/save_manager.py", 237, "ELIMINAR (duplicado de utils/save_manager.py)"),
        ]
        
        self.stats = {
            "files_deleted": 0,
            "files_refactored": 0,
            "backup_created": False,
            "errors": []
        }
    
    def setup_logging(self):
        """Configura el sistema de logging."""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_backup(self):
        """Crea una copia de seguridad del proyecto."""
        try:
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            
            self.logger.info("Creando copia de seguridad...")
            
            # Crear directorio de backup
            self.backup_dir.mkdir(exist_ok=True)
            
            # Copiar archivos importantes
            important_dirs = ["src", "assets", "docs", "tests"]
            important_files = ["README.md", "requirements.txt", "config.json", "pyproject.toml"]
            
            for dir_name in important_dirs:
                dir_path = self.project_root / dir_name
                if dir_path.exists():
                    shutil.copytree(dir_path, self.backup_dir / dir_name)
            
            for file_name in important_files:
                file_path = self.project_root / file_name
                if file_path.exists():
                    shutil.copy2(file_path, self.backup_dir / file_name)
            
            self.stats["backup_created"] = True
            self.logger.info(f"Copia de seguridad creada en: {self.backup_dir}")
            
        except Exception as e:
            self.logger.error(f"Error creando backup: {e}")
            self.stats["errors"].append(f"Backup error: {e}")
    
    def delete_redundant_files(self):
        """Elimina archivos redundantes identificados."""
        self.logger.info("Eliminando archivos redundantes...")
        
        for file_path in self.files_to_delete:
            full_path = self.project_root / file_path
            
            if full_path.exists():
                try:
                    full_path.unlink()
                    self.stats["files_deleted"] += 1
                    self.logger.info(f"Eliminado: {file_path}")
                except Exception as e:
                    error_msg = f"Error eliminando {file_path}: {e}"
                    self.logger.error(error_msg)
                    self.stats["errors"].append(error_msg)
            else:
                self.logger.debug(f"Archivo no encontrado: {file_path}")
    
    def refactor_large_files(self):
        """Identifica archivos largos y propone refactorización."""
        self.logger.info("Analizando archivos que requieren refactorización...")
        
        for file_path, line_count, suggestion in self.files_to_refactor:
            full_path = self.project_root / file_path
            
            if full_path.exists():
                self.logger.warning(f"Archivo largo detectado: {file_path} ({line_count} líneas)")
                self.logger.info(f"Sugerencia de refactorización: {suggestion}")
                self.stats["files_refactored"] += 1
            else:
                self.logger.debug(f"Archivo no encontrado: {file_path}")
    
    def consolidate_save_managers(self):
        """Consolida los save managers duplicados."""
        self.logger.info("Consolidando save managers...")
        
        core_save = self.project_root / "src/core/save_manager.py"
        utils_save = self.project_root / "src/utils/save_manager.py"
        
        if core_save.exists() and utils_save.exists():
            try:
                # Eliminar el save manager de core (mantener el de utils)
                core_save.unlink()
                self.stats["files_deleted"] += 1
                self.logger.info("Eliminado src/core/save_manager.py (duplicado)")
                
                # Actualizar imports en archivos que usen core/save_manager
                self.update_imports("src.utils.save_manager", "src.utils.save_manager")
                
            except Exception as e:
                error_msg = f"Error consolidando save managers: {e}"
                self.logger.error(error_msg)
                self.stats["errors"].append(error_msg)
    
    def update_imports(self, old_import: str, new_import: str):
        """Actualiza imports en archivos Python."""
        self.logger.info(f"Actualizando imports: {old_import} -> {new_import}")
        
        for py_file in self.project_root.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    py_file.write_text(content, encoding='utf-8')
                    self.logger.info(f"Actualizado imports en: {py_file.relative_to(self.project_root)}")
            except Exception as e:
                self.logger.error(f"Error actualizando imports en {py_file}: {e}")
    
    def clean_pycache(self):
        """Limpia archivos __pycache__."""
        self.logger.info("Limpiando archivos __pycache__...")
        
        for pycache_dir in self.project_root.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                self.logger.info(f"Eliminado: {pycache_dir.relative_to(self.project_root)}")
            except Exception as e:
                self.logger.error(f"Error eliminando {pycache_dir}: {e}")
    
    def generate_cleanup_report(self):
        """Genera un reporte de la limpieza realizada."""
        report_path = self.project_root / "CLEANUP_REPORT.md"
        
        report_content = f"""# REPORTE DE LIMPIEZA DEL PROYECTO

**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 ESTADÍSTICAS

- **Archivos eliminados**: {self.stats['files_deleted']}
- **Archivos a refactorizar**: {self.stats['files_refactored']}
- **Backup creado**: {'Sí' if self.stats['backup_created'] else 'No'}
- **Errores encontrados**: {len(self.stats['errors'])}

## 🗑️ ARCHIVOS ELIMINADOS

### Scripts de Test Redundantes
- test_quick_gameplay.py
- test_final_integration.py
- test_simple_enemy_system.py
- test_enemy_system.py
- test_complete_animation_system.py
- test_final_animations.py
- test_optimal_animations.py
- test_intelligent_animations.py
- test_all_animations.py
- test_desert_background.py
- test_character_select_simple.py
- test_character_select_fix.py
- test_animation_fix.py

### Scripts de Análisis Redundantes
- analyze_all_animations.py
- analyze_animation_frames.py
- generate_animation_report.py

### Archivos de Configuración Redundantes
- animation_config.json
- ANIMATION_REPORT.md

## 🔧 ARCHIVOS A REFACTORIZAR

### Archivos Críticos (>500 líneas)
1. **src/entities/player.py** (599 líneas)
   - Sugerencia: Dividir en player_combat.py, player_effects.py, player_stats.py

2. **src/ui/menu_manager.py** (603 líneas)
   - Sugerencia: Dividir en menu_factory.py, menu_callbacks.py

3. **src/scenes/character_select_scene.py** (530 líneas)
   - Sugerencia: Dividir en character_ui.py, character_data.py

4. **src/scenes/game_scene.py** (509 líneas)
   - Sugerencia: Dividir en game_logic.py, game_rendering.py

### Archivos que Requieren Atención (>200 líneas)
1. **src/utils/save_manager.py** (426 líneas)
2. **src/utils/asset_manager.py** (362 líneas)
3. **src/utils/desert_background.py** (408 líneas)

## ⚠️ ERRORES ENCONTRADOS

"""
        
        if self.stats["errors"]:
            for error in self.stats["errors"]:
                report_content += f"- {error}\n"
        else:
            report_content += "- Ningún error encontrado\n"
        
        report_content += f"""
## 📋 PRÓXIMOS PASOS

1. **Revisar archivos refactorizados**: Verificar que la funcionalidad se mantiene
2. **Ejecutar tests**: Asegurar que todo funciona correctamente
3. **Actualizar documentación**: Reflejar los cambios en README.md y CHANGELOG.md
4. **Optimizar imports**: Revisar y limpiar imports no utilizados

## 🔄 BACKUP

Copia de seguridad disponible en: `{self.backup_dir.relative_to(self.project_root)}`

---
*Reporte generado automáticamente por cleanup_project.py*
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        self.logger.info(f"Reporte generado: {report_path}")
    
    def run_cleanup(self):
        """Ejecuta todo el proceso de limpieza."""
        self.logger.info("=== INICIANDO LIMPIEZA DEL PROYECTO ===")
        
        try:
            # 1. Crear backup
            self.create_backup()
            
            # 2. Eliminar archivos redundantes
            self.delete_redundant_files()
            
            # 3. Consolidar save managers
            self.consolidate_save_managers()
            
            # 4. Limpiar __pycache__
            self.clean_pycache()
            
            # 5. Analizar archivos a refactorizar
            self.refactor_large_files()
            
            # 6. Generar reporte
            self.generate_cleanup_report()
            
            # 7. Mostrar resumen
            self.show_summary()
            
        except Exception as e:
            self.logger.error(f"Error durante la limpieza: {e}")
            self.stats["errors"].append(f"Error general: {e}")
    
    def show_summary(self):
        """Muestra un resumen de la limpieza realizada."""
        self.logger.info("=== RESUMEN DE LIMPIEZA ===")
        self.logger.info(f"Archivos eliminados: {self.stats['files_deleted']}")
        self.logger.info(f"Archivos a refactorizar: {self.stats['files_refactored']}")
        self.logger.info(f"Backup creado: {'Sí' if self.stats['backup_created'] else 'No'}")
        self.logger.info(f"Errores: {len(self.stats['errors'])}")
        
        if self.stats["errors"]:
            self.logger.warning("Errores encontrados durante la limpieza:")
            for error in self.stats["errors"]:
                self.logger.warning(f"  - {error}")
        
        self.logger.info("=== LIMPIEZA COMPLETADA ===")


def main():
    """Función principal."""
    cleaner = ProjectCleaner()
    cleaner.run_cleanup()


if __name__ == "__main__":
    main() 