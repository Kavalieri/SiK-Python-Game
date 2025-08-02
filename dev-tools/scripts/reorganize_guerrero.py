"""
Reorganización de Archivos del Guerrero
======================================

Autor: SiK Team
Fecha: 2024
Descripción: Reorganiza los archivos del guerrero para que tengan la misma estructura que los demás personajes.
"""

import shutil
from pathlib import Path


def reorganize_guerrero():
    """Reorganiza los archivos del guerrero para unificar la estructura."""

    # Directorio base del guerrero
    guerrero_dir = Path("assets/characters/used/guerrero")

    if not guerrero_dir.exists():
        print("Error: No se encontró el directorio del guerrero")
        return

    print("=== REORGANIZANDO ARCHIVOS DEL GUERRERO ===")

    # Mapeo de directorios a nombres de animación
    animation_mapping = {
        "idle": "Idle",
        "run": "Run",
        "walk": "Walk",
        "attack": "Attack",
        "dead": "Dead",
        "jump": "Jump",
        "jumpattack": "JumpAttack",
    }

    # Procesar cada subdirectorio
    for subdir, anim_name in animation_mapping.items():
        subdir_path = guerrero_dir / subdir

        if subdir_path.exists():
            print(f"Procesando {subdir} -> {anim_name}")

            # Buscar todos los archivos PNG en el subdirectorio
            png_files = list(subdir_path.glob("*.png"))

            for png_file in png_files:
                # Extraer el número de frame del nombre del archivo
                filename = png_file.name

                # El formato es: Idle_1_.png, Idle_2_.png, etc.
                if filename.startswith(anim_name) and filename.endswith(".png"):
                    # Mover el archivo al directorio principal del guerrero
                    new_path = guerrero_dir / filename

                    if not new_path.exists():
                        shutil.move(str(png_file), str(new_path))
                        print(f"  Movido: {filename}")
                    else:
                        print(f"  Ya existe: {filename}")

            # Eliminar el subdirectorio vacío
            try:
                subdir_path.rmdir()
                print(f"  Eliminado subdirectorio: {subdir}")
            except OSError:
                print(f"  No se pudo eliminar {subdir} (puede no estar vacío)")

    print("=== REORGANIZACIÓN COMPLETADA ===")


def verify_guerrero_structure():
    """Verifica que la estructura del guerrero sea correcta."""

    guerrero_dir = Path("assets/characters/used/guerrero")

    if not guerrero_dir.exists():
        print("Error: No se encontró el directorio del guerrero")
        return

    print("\n=== VERIFICANDO ESTRUCTURA DEL GUERRERO ===")

    # Buscar todos los archivos PNG
    png_files = list(guerrero_dir.glob("*.png"))

    # Agrupar por tipo de animación
    animations = {}
    for png_file in png_files:
        filename = png_file.name

        # Extraer el tipo de animación (Idle, Run, etc.)
        if "_" in filename:
            anim_type = filename.split("_")[0]
            if anim_type not in animations:
                animations[anim_type] = []
            animations[anim_type].append(filename)

    # Mostrar resultados
    for anim_type, files in animations.items():
        files.sort()  # Ordenar por nombre
        print(f"{anim_type}: {len(files)} archivos")
        for file in files[:5]:  # Mostrar solo los primeros 5
            print(f"  {file}")
        if len(files) > 5:
            print(f"  ... y {len(files) - 5} más")
        print()

    print("=== VERIFICACIÓN COMPLETADA ===")


if __name__ == "__main__":
    reorganize_guerrero()
    verify_guerrero_structure()
