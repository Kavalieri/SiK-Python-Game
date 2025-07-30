#!/usr/bin/env python3
"""
Smart Commit - Sistema inteligente que maneja pre-commit hooks.
Ejecuta hooks manualmente y hace commit solo cuando todo está correcto.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, capture_output: bool = True) -> tuple[bool, str, str]:
    """Ejecuta comando y retorna (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=Path.cwd(),
            capture_output=capture_output,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return (
            result.returncode == 0,
            result.stdout.strip() if result.stdout else "",
            result.stderr.strip() if result.stderr else "",
        )
    except Exception as e:
        return False, "", str(e)


def run_pre_commit_manually() -> bool:
    """Ejecuta pre-commit hooks manualmente hasta que pasen."""
    print("🔧 Ejecutando pre-commit hooks manualmente...")

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        print(f"  Intento {attempt}/{max_attempts}")

        # Ejecutar pre-commit
        success, stdout, stderr = run_command(["pre-commit", "run", "--all-files"])

        if success:
            print("  ✅ Todos los hooks pasaron")
            return True
        else:
            print("  ⚠️  Hooks fallaron, aplicando correcciones automáticas...")
            # Los hooks ya corrigieron archivos, agregar cambios
            run_command(["git", "add", "."])

    print("  ❌ No se pudieron corregir todos los problemas automáticamente")
    return False


def smart_commit(message: str) -> bool:
    """Commit inteligente con manejo de hooks."""
    print("🚀 SMART COMMIT - Manejo inteligente de pre-commit hooks")
    print("=" * 60)

    # 1. Agregar cambios iniciales
    print("📁 Agregando cambios...")
    success, _, _ = run_command(["git", "add", "."])
    if not success:
        print("❌ Error agregando cambios")
        return False

    # 2. Verificar si hay cambios
    success, status, _ = run_command(["git", "status", "--porcelain"])
    if not success or not status.strip():
        print("⚠️  No hay cambios para commitear")
        return True

    # 3. Ejecutar pre-commit hooks manualmente
    if not run_pre_commit_manually():
        print("❌ Pre-commit hooks fallaron")
        return False

    # 4. Commit final (sin hooks, ya se ejecutaron)
    print("💾 Ejecutando commit final...")
    success, _, stderr = run_command(["git", "commit", "--no-verify", "-m", message])

    if not success:
        print(f"❌ Error en commit: {stderr}")
        return False

    # 5. Obtener hash del commit
    success, commit_hash, _ = run_command(["git", "rev-parse", "HEAD"])
    if success and commit_hash:
        print(f"✅ Commit exitoso: {commit_hash[:8]}")

    return True


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("❌ Error: Se requiere un mensaje de commit")
        print("Uso: python scripts/smart_commit.py 'mensaje del commit'")
        sys.exit(1)

    commit_message = sys.argv[1]
    success = smart_commit(commit_message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
