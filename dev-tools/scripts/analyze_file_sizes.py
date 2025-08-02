#!/usr/bin/env python3
"""
Script para analizar el tamaño de archivos Python en el proyecto.
"""

from pathlib import Path


def analyze_files() -> list[tuple[str, int]]:
    """
    Analiza todos los archivos Python en el proyecto y devuelve los que superan 150 líneas.

    Returns:
        List[Tuple[str, int]]: Lista de archivos con más de 150 líneas y su conteo.
    """
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

        except (OSError, UnicodeDecodeError) as e:
            print(f"Error leyendo {py_file}: {e}")

    # Ordenar por número de líneas
    files_over_150.sort(key=lambda x: x[1], reverse=True)
    all_files.sort(key=lambda x: x[1], reverse=True)

    _print_summary(files_over_150, all_files)

    return files_over_150


def _print_summary(
    files_over_150: list[tuple[str, int]], all_files: list[tuple[str, int]]
):
    """
    Imprime un resumen de los archivos analizados.

    Args:
        files_over_150: Archivos con más de 150 líneas.
        all_files: Todos los archivos analizados.
    """
    print("=== ARCHIVOS CON MÁS DE 150 LÍNEAS ===")
    for file_path, line_count in files_over_150:
        print(f"{file_path}: {line_count} líneas")

    print(f"\nTotal de archivos >150 líneas: {len(files_over_150)}")
    print(f"Total de archivos Python: {len(all_files)}")


if __name__ == "__main__":
    analyze_files()
