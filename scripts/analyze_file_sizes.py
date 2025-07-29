#!/usr/bin/env python3
"""
Script para analizar el tamaño de archivos Python en el proyecto
"""

from pathlib import Path


def analyze_files():
    """Analiza todos los archivos Python en el proyecto."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    files_over_150 = []
    all_files = []

    # Recorrer todos los archivos Python en src
    for py_file in src_dir.rglob("*.py"):
        try:
            line_count = len(py_file.read_text(encoding="utf-8").splitlines())
            relative_path = py_file.relative_to(project_root)

            all_files.append((str(relative_path), line_count))

            if line_count > 150:
                files_over_150.append((str(relative_path), line_count))

        except Exception as e:
            print(f"Error leyendo {py_file}: {e}")

    # Ordenar por número de líneas
    files_over_150.sort(key=lambda x: x[1], reverse=True)
    all_files.sort(key=lambda x: x[1], reverse=True)

    print("=== ARCHIVOS CON MÁS DE 150 LÍNEAS ===")
    for file_path, line_count in files_over_150:
        print(f"{file_path}: {line_count} líneas")

    print(f"\nTotal de archivos >150 líneas: {len(files_over_150)}")
    print(f"Total de archivos Python: {len(all_files)}")

    return files_over_150


if __name__ == "__main__":
    analyze_files()
