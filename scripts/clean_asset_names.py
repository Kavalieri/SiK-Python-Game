"""
Clean Asset Names - Limpiar Nombres de Assets
===========================================

Autor: SiK Team
Fecha: 2024
Descripción: Script para eliminar espacios en nombres de archivos de assets.
"""

import os
import shutil
import re
from pathlib import Path

def clean_filename(filename):
    """Elimina espacios y caracteres problemáticos del nombre del archivo."""
    # Eliminar espacios y reemplazar con guiones bajos
    cleaned = filename.replace(' ', '_')
    # Eliminar paréntesis y reemplazar con guiones bajos
    cleaned = re.sub(r'[()]', '_', cleaned)
    # Eliminar múltiples guiones bajos consecutivos
    cleaned = re.sub(r'_+', '_', cleaned)
    # Eliminar guiones bajos al final
    cleaned = cleaned.rstrip('_')
    return cleaned

def process_directory(directory_path):
    """Procesa un directorio y renombra todos los archivos."""
    directory = Path(directory_path)
    if not directory.exists():
        print(f"❌ Directorio no encontrado: {directory_path}")
        return
    
    print(f"📁 Procesando directorio: {directory_path}")
    
    # Obtener todos los archivos en el directorio
    files = list(directory.rglob('*'))
    
    renamed_files = []
    
    for file_path in files:
        if file_path.is_file():
            old_name = file_path.name
            new_name = clean_filename(old_name)
            
            if old_name != new_name:
                new_path = file_path.parent / new_name
                
                try:
                    # Renombrar archivo
                    file_path.rename(new_path)
                    renamed_files.append((str(file_path), str(new_path)))
                    print(f"  ✅ {old_name} → {new_name}")
                except Exception as e:
                    print(f"  ❌ Error renombrando {old_name}: {e}")
    
    return renamed_files

def update_references_in_file(file_path, renamed_files):
    """Actualiza referencias a archivos renombrados en un archivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Actualizar cada referencia
        for old_path, new_path in renamed_files:
            old_name = os.path.basename(old_path)
            new_name = os.path.basename(new_path)
            
            # Reemplazar referencias en el contenido
            content = content.replace(old_name, new_name)
        
        # Si el contenido cambió, escribir el archivo
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Actualizado: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error actualizando {file_path}: {e}")
        return False

def main():
    """Función principal del script."""
    print("🧹 Iniciando limpieza de nombres de assets...")
    print("=" * 50)
    
    # Directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    assets_dir = project_root / "assets"
    
    if not assets_dir.exists():
        print("❌ Directorio assets no encontrado")
        return
    
    # Procesar directorio de personajes
    characters_dir = assets_dir / "characters"
    if characters_dir.exists():
        print("\n🎭 Procesando personajes...")
        renamed_files = process_directory(characters_dir)
        
        if renamed_files:
            print(f"\n📝 Actualizando referencias en código...")
            
            # Archivos que pueden contener referencias
            code_files = [
                project_root / "src" / "entities" / "character_data.py",
                project_root / "src" / "utils" / "asset_manager.py",
                project_root / "src" / "utils" / "animation_manager.py",
            ]
            
            for code_file in code_files:
                if code_file.exists():
                    update_references_in_file(code_file, renamed_files)
        else:
            print("✅ No se encontraron archivos para renombrar")
    else:
        print("❌ Directorio de personajes no encontrado")
    
    print("\n🎉 Limpieza de assets completada")

if __name__ == "__main__":
    main() 