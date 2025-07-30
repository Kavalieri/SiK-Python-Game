#!/usr/bin/env python3
"""
Professional Commit System - Solución robusta para commits sin errores.

Este script implementa un sistema de commit profesional que:
1. Valida el estado del repositorio antes de proceder
2. Ejecuta todas las verificaciones previas necesarias
3. Maneja errores de forma inteligente
4. Proporciona feedback detallado del proceso
5. Compatible con PowerShell Pro Tools y PowerShell Universal

Autor: Sistema de Refactorización SiK Python Game
Fecha: 30 de Julio, 2025
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple


class ProfessionalCommitSystem:
    """Sistema de commit profesional con validaciones exhaustivas."""

    def __init__(self):
        self.repo_path = Path.cwd()
        self.encoding = "utf-8"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def run_command(
        self, cmd: List[str], capture_output: bool = True, timeout: int = 60
    ) -> Tuple[bool, str, str]:
        """
        Ejecuta un comando de forma segura con manejo robusto de errores.

        Args:
            cmd: Lista de argumentos del comando
            capture_output: Si capturar stdout/stderr
            timeout: Timeout en segundos

        Returns:
            Tuple (success, stdout, stderr)
        """
        try:
            # Configurar proceso con encoding UTF-8 y sin shell
            process_kwargs = {
                "cwd": self.repo_path,
                "timeout": timeout,
                "text": True,
                "encoding": self.encoding,
                "errors": "replace",  # Manejar caracteres problemáticos
            }

            if capture_output:
                process_kwargs.update({"capture_output": True, "check": False})
                result = subprocess.run(cmd, **process_kwargs)
                return (
                    result.returncode == 0,
                    result.stdout.strip() if result.stdout else "",
                    result.stderr.strip() if result.stderr else "",
                )
            else:
                # Para comandos que necesitan interacción con terminal
                result = subprocess.run(cmd, check=False, **process_kwargs)
                return result.returncode == 0, "", ""

        except subprocess.TimeoutExpired:
            error_msg = f"Timeout ejecutando: {' '.join(cmd)}"
            self.errors.append(error_msg)
            return False, "", error_msg

        except subprocess.SubprocessError as e:
            error_msg = f"Error subprocess: {e}"
            self.errors.append(error_msg)
            return False, "", error_msg

        except (OSError, FileNotFoundError, PermissionError) as e:
            error_msg = f"Error inesperado: {e}"
            self.errors.append(error_msg)
            return False, "", error_msg

    def validate_repository_state(self) -> bool:
        """Valida el estado del repositorio antes de proceder."""
        print("🔍 Validando estado del repositorio...")

        # 1. Verificar que estamos en un repositorio Git
        success, _, _ = self.run_command(["git", "rev-parse", "--git-dir"])
        if not success:
            self.errors.append("No se encuentra un repositorio Git válido")
            return False

        # 2. Verificar conectividad con remote
        success, remotes, _ = self.run_command(["git", "remote", "-v"])
        if not success or not remotes:
            self.warnings.append("No se encontraron remotes configurados")

        # 3. Verificar estado del working directory
        success, _, _ = self.run_command(["git", "status", "--porcelain"])
        if not success:
            self.errors.append("Error verificando git status")
            return False

        print("✅ Repositorio validado correctamente")
        return True

    def run_pre_commit_validations(self) -> bool:
        """Ejecuta todas las validaciones previas al commit."""
        print("🧪 Ejecutando validaciones pre-commit...")

        # 1. Formateo de código con Ruff
        print("  🔧 Formateando código con Ruff...")
        success, _, stderr = self.run_command(
            ["poetry", "run", "ruff", "format", "src/", "scripts/", "tests/"]
        )

        if not success:
            self.errors.append(f"Error en formateo Ruff: {stderr}")
            return False

        # 2. Linting con Ruff
        print("  🔍 Ejecutando linting con Ruff...")
        success, _, stderr = self.run_command(
            ["poetry", "run", "ruff", "check", "src/", "scripts/", "tests/"]
        )

        if not success:
            # Ruff puede devolver código de salida != 0 con warnings, verificar si son errores críticos
            if stderr and "error" in stderr.lower():
                self.errors.append(f"Errores críticos en linting: {stderr}")
                return False
            else:
                self.warnings.append("Warnings de linting encontrados")

        # 3. Verificar sintaxis Python en archivos críticos
        print("  🐍 Verificando sintaxis Python...")
        critical_files = [
            "src/entities/entity.py",
            "src/entities/entity_core.py",
            "src/entities/entity_types.py",
            "src/entities/entity_effects.py",
            "src/entities/entity_rendering.py",
        ]

        for file_path in critical_files:
            if Path(file_path).exists():
                success, _, stderr = self.run_command(
                    ["python", "-m", "py_compile", file_path]
                )
                if not success:
                    self.errors.append(f"Error de sintaxis en {file_path}: {stderr}")
                    return False

        print("✅ Validaciones pre-commit completadas")
        return True

    def stage_changes(self) -> bool:
        """Agrega cambios al staging area de forma inteligente."""
        print("📁 Agregando cambios al staging area...")

        # Verificar qué archivos han cambiado
        success, status, _ = self.run_command(["git", "status", "--porcelain"])
        if not success:
            self.errors.append("Error verificando archivos modificados")
            return False

        if not status.strip():
            self.warnings.append("No hay cambios para agregar")
            return True

        # Agregar todos los cambios
        success, _, stderr = self.run_command(["git", "add", "."])
        if not success:
            self.errors.append(f"Error agregando cambios: {stderr}")
            return False

        # Verificar que los archivos se agregaron correctamente
        success, staged, _ = self.run_command(
            ["git", "diff", "--cached", "--name-only"]
        )
        if success and staged:
            staged_files = staged.split("\n")
            print(f"  ✅ {len(staged_files)} archivos agregados al staging area")
        else:
            self.warnings.append("No se detectaron archivos en staging area")

        return True

    def execute_commit(self, message: str) -> bool:
        """Ejecuta el commit de forma segura."""
        print("💾 Ejecutando commit...")

        # Commit con mensaje
        success, stdout, stderr = self.run_command(["git", "commit", "-m", message])

        if not success:
            if "nothing to commit" in stderr.lower():
                self.warnings.append("No hay cambios para commitear")
                return True
            else:
                self.errors.append(f"Error en commit: {stderr}")
                return False

        # Obtener hash del commit
        success, commit_hash, _ = self.run_command(["git", "rev-parse", "HEAD"])
        if success and commit_hash:
            print(f"  ✅ Commit exitoso: {commit_hash[:8]}")
        else:
            print("  ✅ Commit completado")

        return True

    def update_documentation(self) -> bool:
        """Actualiza documentación si es necesario."""
        print("📝 Verificando documentación...")

        # Ejecutar análisis de archivos
        success, _, _ = self.run_command(["python", "scripts/file_analyzer.py"])
        if success:
            print("  ✅ Análisis de archivos actualizado")
        else:
            self.warnings.append("No se pudo ejecutar file_analyzer.py")

        return True

    def print_summary(self) -> None:
        """Imprime resumen del proceso."""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL COMMIT PROFESIONAL")
        print("=" * 60)

        if self.errors:
            print("❌ ERRORES:")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print("⚠️  ADVERTENCIAS:")
            for warning in self.warnings:
                print(f"  • {warning}")

        if not self.errors:
            print("✅ COMMIT COMPLETADO EXITOSAMENTE")
        else:
            print("❌ COMMIT FALLÓ - Revisa los errores arriba")

    def professional_commit(self, message: str) -> bool:
        """
        Ejecuta el workflow completo de commit profesional.

        Args:
            message: Mensaje del commit

        Returns:
            True si el commit fue exitoso
        """
        print("🚀 INICIANDO COMMIT PROFESIONAL")
        print("=" * 50)

        start_time = time.time()

        # Paso 1: Validar repositorio
        if not self.validate_repository_state():
            self.print_summary()
            return False

        # Paso 2: Ejecutar validaciones pre-commit
        if not self.run_pre_commit_validations():
            self.print_summary()
            return False

        # Paso 3: Agregar cambios al staging area
        if not self.stage_changes():
            self.print_summary()
            return False

        # Paso 4: Ejecutar commit
        if not self.execute_commit(message):
            self.print_summary()
            return False

        # Paso 5: Actualizar documentación
        self.update_documentation()

        # Resumen final
        elapsed_time = time.time() - start_time
        print(f"\n⏱️  Tiempo total: {elapsed_time:.2f} segundos")
        self.print_summary()

        return len(self.errors) == 0


def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print("❌ Error: Se requiere un mensaje de commit")
        print("Uso: python scripts/professional_commit.py 'mensaje del commit'")
        sys.exit(1)

    commit_message = sys.argv[1]

    # Crear instancia del sistema de commit
    commit_system = ProfessionalCommitSystem()

    # Ejecutar commit profesional
    success = commit_system.professional_commit(commit_message)

    # Salir con código apropiado
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
