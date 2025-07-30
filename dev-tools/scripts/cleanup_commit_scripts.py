"""
Script de Limpieza - Scripts de Commit Redundantes
==================================================

Elimina scripts de commit obsoletos tras implementación del método unificado.
Conserva únicamente unified_commit.ps1 y simple_commit.ps1.

Referencia: docs/METODO_COMMIT_UNIFICADO.md
"""

import shutil
from pathlib import Path


def main():
    # Scripts de commit obsoletos a eliminar
    scripts_to_remove = [
        # Scripts Python obsoletos
        "scripts/intelligent_commit.py",
        "scripts/professional_commit.py",
        "scripts/quick_commit.py",
        "scripts/robust_commit.py",
        "scripts/smart_commit_system.py",
        "scripts/smart_commit.py",
        "scripts/pre_commit_check.py",
        # Scripts PowerShell obsoletos
        "scripts/professional_commit.ps1",
        "scripts/ultra_fast_commit.ps1",
        "scripts/quick_commit.ps1",
        "scripts/intelligent_commit.ps1",
        "scripts/commit_profesional.ps1",
    ]

    # Scripts a conservar
    scripts_to_keep = [
        "scripts/unified_commit.ps1",  # Script completo
        "scripts/simple_commit.ps1",  # Script simplificado
    ]

    print("🧹 LIMPIEZA DE SCRIPTS DE COMMIT REDUNDANTES")
    print("=" * 50)

    removed_count = 0
    errors = []

    for script_path in scripts_to_remove:
        file_path = Path(script_path)

        if file_path.exists():
            try:
                # Crear backup en backups__DISABLED antes de eliminar
                backup_dir = Path("backups__DISABLED/commit_scripts_backup")
                backup_dir.mkdir(parents=True, exist_ok=True)

                backup_path = backup_dir / file_path.name

                # Mover a backup
                shutil.move(str(file_path), str(backup_path))

                print(f"✅ Movido a backup: {script_path}")
                removed_count += 1

            except (OSError, shutil.Error) as e:
                error_msg = f"❌ Error moviendo {script_path}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
        else:
            print(f"⚠️  No encontrado: {script_path}")

    print("\n📊 RESUMEN:")
    print(f"  • Scripts movidos a backup: {removed_count}")
    print(f"  • Errores: {len(errors)}")

    print("\n✅ SCRIPTS CONSERVADOS:")
    for script in scripts_to_keep:
        if Path(script).exists():
            print(f"  • {script} ✓")
        else:
            print(f"  • {script} ❌ (NO ENCONTRADO)")

    if errors:
        print("\n❌ ERRORES ENCONTRADOS:")
        for error in errors:
            print(f"  • {error}")

    print("\n🎉 Limpieza completada. Usar únicamente:")
    print("  • scripts/simple_commit.ps1 para uso diario")
    print("  • scripts/unified_commit.ps1 para casos avanzados")


if __name__ == "__main__":
    main()
