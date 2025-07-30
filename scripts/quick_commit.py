#!/usr/bin/env python3
"""
Quick Commit - Versión optimizada sin esperas innecesarias.
Proporciona información instantánea y commits rápidos.
"""

import subprocess
import sys
from pathlib import Path


def run_cmd_quick(cmd: list) -> bool:
    """Ejecuta comando rápido sin capturar salida innecesaria."""
    try:
        result = subprocess.run(cmd, cwd=Path.cwd(), check=False)
        return result.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False


def get_file_lines(file_path: str) -> int:
    """Obtiene el número de líneas de un archivo rápidamente."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (OSError, UnicodeError):
        return 0


def quick_commit_workflow(message: str) -> bool:
    """Workflow de commit optimizado sin esperas."""

    # 1. Formatear código (rápido, sin salida)
    print("🔧 Formateando código...")
    run_cmd_quick(["poetry", "run", "ruff", "format", "src/", "scripts/"])

    # 2. Agregar todos los cambios
    print("📁 Agregando cambios...")
    if not run_cmd_quick(["git", "add", "."]):
        print("❌ Error agregando cambios")
        return False

    # 3. Commit directo
    print("💾 Realizando commit...")
    if not run_cmd_quick(["git", "commit", "-m", message]):
        print("❌ Error en commit")
        return False

    print("✅ Commit exitoso")
    return True


def main():
    if len(sys.argv) != 2:
        print("Uso: python quick_commit.py 'mensaje del commit'")
        sys.exit(1)

    message = sys.argv[1]
    quick_commit_workflow(message)


if __name__ == "__main__":
    main()
