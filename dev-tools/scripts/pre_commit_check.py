#!/usr/bin/env python3
"""
Script de verificación pre-commit para detectar problemas antes del commit.

Verifica:
- Estado del repositorio
- Archivos modificados que podrían causar problemas
- Formato del código
- Tests básicos
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str) -> tuple[bool, str]:
    """Ejecuta comando y devuelve resultado."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=Path.cwd(), check=False
        )
        return result.returncode == 0, result.stdout + result.stderr
    except (subprocess.SubprocessError, OSError) as e:
        return False, f"Error: {e}"


def check_git_status():
    """Verifica el estado de git."""
    print("📋 Verificando estado de git...")
    cmd_success, output = run_command("git status --porcelain")

    if not cmd_success:
        print("❌ Error verificando git status")
        return False

    if not output.strip():
        print("ℹ️ No hay cambios pendientes")
        return True

    print("📝 Archivos modificados:")
    for line in output.strip().split("\n"):
        print(f"  {line}")

    return True


def check_formatting():
    """Verifica si el código está bien formateado."""
    print("\n🔧 Verificando formato del código...")

    # Verificar formato sin modificar archivos
    format_success, output = run_command("poetry run ruff format --check .")
    if not format_success:
        print("⚠️ Archivos necesitan formateo:")
        print(output)
        return False

    # Verificar reglas de linting
    lint_success, output = run_command("poetry run ruff check .")
    if not lint_success:
        print("⚠️ Problemas de linting encontrados:")
        print(output)
        return False

    print("✅ Código bien formateado")
    return True


def check_critical_files():
    """Verifica archivos críticos que podrían causar problemas."""
    print("\n🔍 Verificando archivos críticos...")

    critical_patterns = [
        "src/utils/database_*.py",
        "src/utils/schema_*.py",
        "scripts/*.py",
        "docs/*.md",
    ]

    issues = []

    for pattern in critical_patterns:
        files = list(Path(".").glob(pattern))
        for file in files:
            if file.exists():
                lines = len(file.read_text(encoding="utf-8").splitlines())
                if "src/utils/" in str(file) and lines > 150:
                    issues.append(f"{file}: {lines} líneas (excede límite de 150)")

    if issues:
        print("⚠️ Problemas encontrados:")
        for issue in issues:
            print(f"  {issue}")
        return False

    print("✅ Archivos críticos OK")
    return True


def check_sqlite_system():
    """Verifica que el sistema SQLite funcione."""
    print("\n🗄️ Verificando sistema SQLite...")

    sqlite_success, output = run_command("python scripts/test_simple_sqlite.py")
    if not sqlite_success:
        print("❌ Sistema SQLite tiene problemas:")
        print(output[-500:])  # Últimas 500 chars para ver el error
        return False

    if "¡Prueba simple exitosa!" in output:
        print("✅ Sistema SQLite funcionando")
        return True
    else:
        print("⚠️ Sistema SQLite con advertencias")
        return True  # No es crítico


def main():
    """Función principal."""
    print("🔍 Verificación pre-commit iniciada...\n")

    checks = [
        ("Git Status", check_git_status),
        ("Formateo", check_formatting),
        ("Archivos Críticos", check_critical_files),
        ("Sistema SQLite", check_sqlite_system),
    ]

    passed = 0
    total = len(checks)

    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
            print()  # Línea en blanco entre checks
        except (subprocess.SubprocessError, OSError, FileNotFoundError) as e:
            print(f"❌ Error en {name}: {e}\n")

    print(f"📊 Resultado: {passed}/{total} verificaciones pasaron")

    if passed == total:
        print("🎉 ¡Todo listo para commit!")
        return True
    else:
        print("⚠️ Hay problemas que resolver antes del commit")
        return False


if __name__ == "__main__":
    exit_success = main()
    sys.exit(0 if exit_success else 1)
