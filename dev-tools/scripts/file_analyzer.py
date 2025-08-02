#!/usr/bin/env python3
"""
File Analyzer - Análisis rápido de archivos para refactorización.
Proporciona información instantánea sin comandos externos.
"""

from pathlib import Path
from typing import Any


def analyze_file(file_path: str) -> dict[str, Any]:
    """
    Analiza un archivo Python y devuelve métricas importantes.

    Returns:
        Dict con: lines, classes, functions, imports, status
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": "Archivo no encontrado"}

        with open(path, encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        total_lines = len(lines)
        classes = sum(1 for line in lines if line.strip().startswith("class "))
        functions = sum(1 for line in lines if line.strip().startswith("def "))
        imports = sum(
            1 for line in lines if line.strip().startswith(("import ", "from "))
        )

        # Determine status based on line count
        if total_lines <= 150:
            status = "✅ COMPLIANT"
            priority = "LOW"
        elif total_lines <= 250:
            status = "🟡 EXCEEDS (MODERATE)"
            priority = "MEDIUM"
        elif total_lines <= 350:
            status = "🟠 EXCEEDS (HIGH)"
            priority = "HIGH"
        else:
            status = "🔴 CRITICAL"
            priority = "URGENT"

        return {
            "lines": total_lines,
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "status": status,
            "priority": priority,
            "percentage_over": round((total_lines / 150) * 100, 1),
            "needs_division": total_lines > 150,
        }

    except (OSError, UnicodeError) as e:
        return {"error": f"Error leyendo archivo: {e}"}


def analyze_critical_files() -> list[tuple[str, dict]]:
    """Analiza los archivos más críticos identificados."""
    critical_files = [
        "src/entities/entity.py",
        "src/utils/asset_manager.py",
        "src/ui/hud.py",
        "src/entities/player.py",
        "src/entities/player_combat.py",
        "src/utils/desert_background.py",
        "src/entities/enemy.py",
        "src/utils/save_manager.py",
        "src/core/game_engine.py",
        "src/scenes/character_ui.py",
        "src/ui/menu_callbacks.py",
    ]

    results = []
    for file_path in critical_files:
        analysis = analyze_file(file_path)
        results.append((file_path, analysis))

    # Sort by lines (most critical first)
    results.sort(key=lambda x: x[1].get("lines", 0), reverse=True)
    return results


def print_analysis_report():
    """Imprime reporte de análisis de archivos críticos."""
    print("📊 ANÁLISIS RÁPIDO DE ARCHIVOS CRÍTICOS")
    print("=" * 60)

    results = analyze_critical_files()

    for file_path, analysis in results:
        if "error" in analysis:
            print(f"❌ {file_path}: {analysis['error']}")
            continue

        lines = analysis["lines"]
        status = analysis["status"]
        percentage = analysis["percentage_over"]

        print(f"{status} {file_path}")
        print(f"   📏 {lines} líneas ({percentage}% del límite)")
        print(f"   🏗️  {analysis['classes']} clases, {analysis['functions']} funciones")
        print("")


if __name__ == "__main__":
    print_analysis_report()
