"""
Reorganización de Directorios de Personajes
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Reorganiza los directorios de personajes separando los que usamos de los que no.
"""

import shutil
from pathlib import Path


def reorganize_characters():
    """Reorganiza los directorios de personajes."""

    # Definir personajes que usamos
    characters_used = [
        "guerrero",
        "adventureguirl",
        "robot",
        "zombiemale",
        "zombieguirl",
    ]

    # Rutas
    assets_path = Path("assets/characters")
    used_path = assets_path / "used"
    unused_path = assets_path / "unused"

    print("=== Reorganización de Directorios de Personajes ===")

    # Crear directorios si no existen
    used_path.mkdir(exist_ok=True)
    unused_path.mkdir(exist_ok=True)

    # Obtener todos los directorios de personajes
    character_dirs = [
        d
        for d in assets_path.iterdir()
        if d.is_dir() and d.name not in ["used", "unused"]
    ]

    print(f"Encontrados {len(character_dirs)} directorios de personajes")

    for char_dir in character_dirs:
        char_name = char_dir.name

        if char_name in characters_used:
            # Mover a directorio "used"
            target_path = used_path / char_name
            if not target_path.exists():
                shutil.move(str(char_dir), str(target_path))
                print(f"✓ Movido '{char_name}' a 'used'")
            else:
                print(f"⚠ '{char_name}' ya existe en 'used'")
        else:
            # Mover a directorio "unused"
            target_path = unused_path / char_name
            if not target_path.exists():
                shutil.move(str(char_dir), str(target_path))
                print(f"✓ Movido '{char_name}' a 'unused'")
            else:
                print(f"⚠ '{char_name}' ya existe en 'unused'")

    print("\n=== Resumen ===")
    print(f"Personajes usados: {len(list(used_path.iterdir()))}")
    print(f"Personajes no usados: {len(list(unused_path.iterdir()))}")

    # Mostrar contenido
    print("\nPersonajes usados:")
    for char_dir in used_path.iterdir():
        if char_dir.is_dir():
            print(f"  - {char_dir.name}")

    print("\nPersonajes no usados:")
    for char_dir in unused_path.iterdir():
        if char_dir.is_dir():
            print(f"  - {char_dir.name}")


if __name__ == "__main__":
    reorganize_characters()
