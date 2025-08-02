#!/usr/bin/env python3
"""
Script de commit robusto con manejo automático de formatting y pre-commit hooks.

Soluciona:
- Problemas de ruff-format modificando archivos durante pre-commit
- Commits fallidos por archivos modificados automáticamente
- Necesidad de múltiples iteraciones add/commit
- Procesos bloqueados en terminal
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd: str, timeout: int = 30) -> tuple[bool, str]:
    """Ejecuta comando con timeout para evitar bloqueos."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path.cwd(),
            check=False,
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, f"Comando expiró después de {timeout}s: {cmd}"
    except (subprocess.SubprocessError, OSError) as e:
        return False, f"Error ejecutando comando: {e}"


def format_code():
    """Formatea todo el código antes del commit."""
    print("🔧 Formateando código con ruff...")
    success, output = run_command("poetry run ruff format .")
    if not success:
        print(f"❌ Error formateando: {output}")
        return False

    success, output = run_command("poetry run ruff check --fix .")
    if not success:
        print(f"❌ Error en ruff check: {output}")
        return False

    print("✅ Código formateado correctamente")
    return True


def stage_all_changes():
    """Agrega todos los cambios al staging area."""
    print("📝 Agregando cambios al staging...")
    success, output = run_command("git add -A")
    if not success:
        print(f"❌ Error agregando archivos: {output}")
        return False

    print("✅ Cambios agregados al staging")
    return True


def check_status():
    """Verifica si hay cambios para commitear."""
    success, output = run_command("git status --porcelain")
    if not success:
        return False, "Error verificando estado"

    if not output.strip():
        return False, "No hay cambios para commitear"

    return True, output.strip()


def commit_with_retry(message: str, max_retries: int = 5) -> bool:
    """Intenta hacer commit con reintentos automáticos."""
    print("🚀 Iniciando commit robusto...")
    print(f"📝 Mensaje: {message}")

    for attempt in range(max_retries):
        print(f"\n📦 Intento de commit {attempt + 1}/{max_retries}...")

        # Formatear código
        if not format_code():
            continue

        # Agregar cambios (incluyendo los formateados)
        if not stage_all_changes():
            continue

        # Intentar commit
        success, output = run_command(f'git commit -m "{message}"', timeout=60)

        if success:
            print("🎉 ¡Commit exitoso!")
            return True
        else:
            print(f"⚠️ Intento {attempt + 1} falló")

            # Si pre-commit modificó archivos, continuar el loop
            if "files were modified by this hook" in output:
                print("🔄 Pre-commit modificó archivos, reintentando...")
                continue
            else:
                # Mostrar error completo para otros problemas
                print(f"Error: {output}")

            if attempt < max_retries - 1:
                print("🔄 Reintentando...")
                time.sleep(1)

    print("❌ Commit falló después de todos los intentos")
    return False


def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print("Uso: python scripts/robust_commit.py 'mensaje del commit'")
        sys.exit(1)

    commit_message = " ".join(sys.argv[1:])

    print("🚀 Iniciando commit robusto...")
    print(f"📝 Mensaje: {commit_message}")

    if commit_with_retry(commit_message):
        print("🎉 ¡Commit completado exitosamente!")
        sys.exit(0)
    else:
        print("💥 Commit falló - revisa los errores arriba")
        sys.exit(1)


if __name__ == "__main__":
    main()
