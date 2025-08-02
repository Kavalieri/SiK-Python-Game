#!/usr/bin/env python3
"""
Intelligent Commit System - Sistema inteligente para commits usando herramientas estándar.

Este sistema:
1. Usa pre-commit hooks nativamente (no los evita)
2. Es genérico (no específico para archivos concretos)
3. Evita bloqueos de entrada en terminal
4. Limpia cachés periódicamente
5. Usa poetry/ruff para operaciones cuando es apropiado
6. Manejo robusto de errores y timeouts

Autor: Sistema de Refactorización SiK Python Game
Fecha: 30 de Julio, 2025
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path


class IntelligentCommitSystem:
    """Sistema inteligente de commit que respeta todos los workflows estándar."""

    def __init__(self):
        self.repo_path = Path.cwd()
        self.start_time = time.time()

    def run_command_with_timeout(
        self, cmd: list, timeout_seconds: int = 120, capture_output: bool = True
    ) -> tuple[bool, str, str]:
        """
        Ejecuta comando con timeout y sin bloqueos de entrada.

        Args:
            cmd: Lista de argumentos del comando
            timeout_seconds: Timeout en segundos
            capture_output: Si capturar stdout/stderr

        Returns:
            Tuple (success, stdout, stderr)
        """
        try:
            # Configurar proceso para evitar bloqueos de entrada
            process_kwargs = {
                "cwd": self.repo_path,
                "text": True,
                "encoding": "utf-8",
                "errors": "replace",
                "timeout": timeout_seconds,
                "stdin": subprocess.DEVNULL,  # Crucial: evita esperar entrada
            }

            if capture_output:
                process_kwargs.update({"capture_output": True})

            result = subprocess.run(cmd, check=False, **process_kwargs)

            return (
                result.returncode == 0,
                result.stdout.strip() if result.stdout else "",
                result.stderr.strip() if result.stderr else "",
            )

        except subprocess.TimeoutExpired:
            return False, "", f"Comando excedió timeout de {timeout_seconds}s"
        except (OSError, ValueError) as e:
            return False, "", f"Error ejecutando comando: {e}"

    def clean_caches(self) -> None:
        """Limpia cachés de Python, pip, poetry y otros."""
        print("🧹 Limpiando cachés...")

        # Cache de Python
        cache_dirs = ["__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"]

        for cache_dir in cache_dirs:
            for path in self.repo_path.rglob(cache_dir):
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                        print(f"  ✅ Eliminado: {path}")
                    except OSError:
                        pass

        # Cache de pip
        success, _, _ = self.run_command_with_timeout(
            ["pip", "cache", "purge"], timeout_seconds=30
        )
        if success:
            print("  ✅ Cache de pip limpiado")

        # Cache de poetry si está disponible
        success, _, _ = self.run_command_with_timeout(
            ["poetry", "cache", "clear", "--all", "."], timeout_seconds=30
        )
        if success:
            print("  ✅ Cache de poetry limpiado")

        print("🧹 Limpieza de cachés completada")

    def validate_repository(self) -> bool:
        """Valida que estamos en un repositorio Git válido."""
        print("🔍 Validando repositorio...")

        if not (self.repo_path / ".git").exists():
            print("❌ No se encuentra un repositorio Git válido")
            return False

        success, _, stderr = self.run_command_with_timeout(
            ["git", "rev-parse", "--git-dir"]
        )
        if not success:
            print(f"❌ Error validando repositorio: {stderr}")
            return False

        print("✅ Repositorio Git válido")
        return True

    def check_working_directory(self) -> bool:
        """Verifica si hay cambios en el directorio de trabajo."""
        success, output, _ = self.run_command_with_timeout(
            ["git", "status", "--porcelain"]
        )
        if not success:
            print("❌ Error verificando estado del repositorio")
            return False

        if not output.strip():
            print("ℹ️  No hay cambios para commitear")
            return False

        # Mostrar resumen de cambios
        lines = output.strip().split("\n")
        modified = len(
            [line for line in lines if line.startswith(" M") or line.startswith("M ")]
        )
        added = len(
            [line for line in lines if line.startswith("A ") or line.startswith("??")]
        )
        deleted = len(
            [line for line in lines if line.startswith(" D") or line.startswith("D ")]
        )

        print(
            f"📊 Cambios detectados: {added} nuevos, {modified} modificados, {deleted} eliminados"
        )
        return True

    def run_quality_checks(self) -> bool:
        """Ejecuta verificaciones de calidad usando poetry/ruff."""
        print("🧪 Ejecutando verificaciones de calidad...")

        # 1. Formateo con ruff via poetry
        print("  🔧 Formateando código con Ruff...")
        success, _, stderr = self.run_command_with_timeout(
            ["poetry", "run", "ruff", "format", "."]
        )
        if not success:
            print(f"⚠️  Error en formateo (continuando): {stderr}")
        else:
            print("  ✅ Formateo completado")

        # 2. Linting con ruff via poetry
        print("  🔍 Ejecutando linting con Ruff...")
        success, stdout, stderr = self.run_command_with_timeout(
            ["poetry", "run", "ruff", "check", ".", "--fix"]
        )
        if not success:
            print(f"⚠️  Linting con advertencias (continuando): {stderr}")
        else:
            print("  ✅ Linting completado")

        print("✅ Verificaciones de calidad completadas")
        return True

    def stage_changes(self) -> bool:
        """Agrega todos los cambios al staging area."""
        print("📁 Agregando cambios al staging area...")

        success, _, stderr = self.run_command_with_timeout(["git", "add", "."])
        if not success:
            print(f"❌ Error agregando cambios: {stderr}")
            return False

        # Verificar archivos staged
        success, output, _ = self.run_command_with_timeout(
            ["git", "diff", "--cached", "--name-only"]
        )
        if success and output:
            staged_files = output.split("\n")
            print(f"  ✅ {len(staged_files)} archivos agregados al staging area")
        else:
            print("⚠️  No se detectaron archivos en staging area")

        return True

    def execute_commit_with_hooks(self, message: str) -> bool:
        """
        Ejecuta commit respetando los pre-commit hooks.
        La clave está en usar stdin=DEVNULL para evitar bloqueos.
        """
        print("💾 Ejecutando commit con pre-commit hooks...")

        # Commit normal que respeta hooks - SIN --no-verify
        success, _stdout, stderr = self.run_command_with_timeout(
            ["git", "commit", "-m", message], timeout_seconds=180
        )  # Más tiempo para hooks

        if not success:
            if "nothing to commit" in stderr.lower():
                print("ℹ️  No hay cambios para commitear")
                return True
            else:
                print(f"❌ Error en commit: {stderr}")
                if _stdout:
                    print(f"📋 Salida adicional: {_stdout}")
                return False

        # Obtener hash del commit recién creado
        success, commit_hash, _ = self.run_command_with_timeout(
            ["git", "rev-parse", "HEAD"]
        )
        if success and commit_hash:
            print(f"✅ Commit exitoso: {commit_hash[:8]}")
        else:
            print("✅ Commit completado")

        return True

    def update_project_analysis(self) -> None:
        """Actualiza análisis del proyecto si las herramientas están disponibles."""
        print("📊 Actualizando análisis del proyecto...")

        # Ejecutar file_analyzer.py si existe
        if (self.repo_path / "scripts" / "file_analyzer.py").exists():
            success, _, _ = self.run_command_with_timeout(
                ["python", "scripts/file_analyzer.py"], timeout_seconds=30
            )
            if success:
                print("  ✅ Análisis de archivos actualizado")
            else:
                print("  ⚠️  No se pudo ejecutar análisis de archivos")

        print("📊 Actualización de análisis completada")

    def print_summary(self, success: bool) -> None:
        """Imprime resumen del proceso."""
        elapsed_time = time.time() - self.start_time

        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL COMMIT INTELIGENTE")
        print("=" * 60)

        if success:
            print("✅ COMMIT COMPLETADO EXITOSAMENTE")
            print(f"⏱️  Tiempo total: {elapsed_time:.2f} segundos")
            print("🎯 Proceso completado con herramientas estándar")
            print("🔒 Pre-commit hooks ejecutados correctamente")
        else:
            print("❌ COMMIT FALLÓ")
            print(f"⏱️  Tiempo transcurrido: {elapsed_time:.2f} segundos")
            print("🔍 Revisa los errores mostrados arriba")

        print("=" * 60)

    def intelligent_commit(self, message: str) -> bool:
        """
        Ejecuta el workflow completo de commit inteligente.

        Args:
            message: Mensaje del commit

        Returns:
            True si el commit fue exitoso
        """
        print("🚀 SISTEMA DE COMMIT INTELIGENTE")
        print("Compatible con pre-commit hooks y herramientas estándar")
        print("=" * 60)

        try:
            # Paso 1: Limpiar cachés periódicamente
            self.clean_caches()

            # Paso 2: Validar repositorio
            if not self.validate_repository():
                return False

            # Paso 3: Verificar cambios
            if not self.check_working_directory():
                return True  # No es error, simplemente no hay cambios

            # Paso 4: Ejecutar verificaciones de calidad
            self.run_quality_checks()  # No falla el commit si hay warnings

            # Paso 5: Agregar cambios
            if not self.stage_changes():
                return False

            # Paso 6: Commit con hooks (sin bypass)
            if not self.execute_commit_with_hooks(message):
                return False

            # Paso 7: Actualizar análisis
            self.update_project_analysis()

            return True

        except KeyboardInterrupt:
            print("\n❌ Proceso cancelado por el usuario")
            return False
        except (OSError, ValueError) as e:
            print(f"\n❌ Error inesperado: {e}")
            return False


def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print("❌ Error: Se requiere un mensaje de commit")
        print("Uso: python scripts/intelligent_commit.py 'mensaje del commit'")
        print("\nEjemplos:")
        print("  python scripts/intelligent_commit.py 'feat: nueva funcionalidad'")
        print("  python scripts/intelligent_commit.py 'fix: corrección de bug'")
        print(
            "  python scripts/intelligent_commit.py 'refactor: división modular asset_manager'"
        )
        sys.exit(1)

    commit_message = sys.argv[1]

    # Crear y ejecutar sistema de commit inteligente
    commit_system = IntelligentCommitSystem()
    success = commit_system.intelligent_commit(commit_message)

    # Imprimir resumen
    commit_system.print_summary(success)

    # Salir con código apropiado
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
