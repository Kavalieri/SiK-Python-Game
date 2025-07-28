#!/usr/bin/env python3
"""
Test Config Simple - Prueba Simple del Sistema de Configuración
============================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Script simple para probar el sistema de configuración V2.
"""

import json
import sys
from pathlib import Path


def test_config_files():
    """Prueba que los archivos de configuración existan y sean JSON válidos."""
    print("=== PRUEBA DE ARCHIVOS DE CONFIGURACIÓN ===")
    
    config_dir = Path(__file__).parent.parent / "config"
    config_files = [
        "characters.json",
        "gameplay.json", 
        "enemies.json",
        "powerups.json",
        "ui.json",
        "audio.json"
    ]
    
    success_count = 0
    
    for config_file in config_files:
        config_path = config_dir / config_file
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"✅ {config_file}: Válido ({len(data)} claves principales)")
                success_count += 1
                
            except json.JSONDecodeError as e:
                print(f"❌ {config_file}: Error JSON - {e}")
            except Exception as e:
                print(f"❌ {config_file}: Error - {e}")
        else:
            print(f"❌ {config_file}: No encontrado")
    
    print(f"\nArchivos válidos: {success_count}/{len(config_files)}")
    return success_count == len(config_files)


def test_characters_config():
    """Prueba específicamente la configuración de personajes."""
    print("\n=== PRUEBA DE CONFIGURACIÓN DE PERSONAJES ===")
    
    config_path = Path(__file__).parent.parent / "config" / "characters.json"
    
    if not config_path.exists():
        print("❌ Archivo characters.json no encontrado")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        characters = data.get("characters", {})
        print(f"Personajes encontrados: {len(characters)}")
        
        for char_key, char_data in characters.items():
            nombre = char_data.get("nombre", "N/A")
            stats = char_data.get("stats", {})
            vida = stats.get("vida", 0)
            print(f"  {char_key}: {nombre} - Vida: {vida}")
        
        # Verificar upgrades
        upgrades = data.get("upgrades", {})
        print(f"Tipos de mejoras: {len(upgrades)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo characters.json: {e}")
        return False


def test_gameplay_config():
    """Prueba específicamente la configuración de gameplay."""
    print("\n=== PRUEBA DE CONFIGURACIÓN DE GAMEPLAY ===")
    
    config_path = Path(__file__).parent.parent / "config" / "gameplay.json"
    
    if not config_path.exists():
        print("❌ Archivo gameplay.json no encontrado")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar niveles
        niveles = data.get("niveles", {})
        duracion_ronda = niveles.get("duración_ronda", 0)
        print(f"Duración de ronda: {duracion_ronda} segundos")
        
        # Verificar combate
        combate = data.get("combate", {})
        daño_colision = combate.get("daño_colisión_enemigo", 0)
        print(f"Daño por colisión: {daño_colision}")
        
        # Verificar powerups
        powerups = data.get("powerups", {})
        duracion_estandar = powerups.get("duración_estándar", 0)
        print(f"Duración estándar powerups: {duracion_estandar} segundos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo gameplay.json: {e}")
        return False


def test_ui_config():
    """Prueba específicamente la configuración de UI."""
    print("\n=== PRUEBA DE CONFIGURACIÓN DE UI ===")
    
    config_path = Path(__file__).parent.parent / "config" / "ui.json"
    
    if not config_path.exists():
        print("❌ Archivo ui.json no encontrado")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar colores
        colores = data.get("colores", {})
        print(f"Colores definidos: {len(colores)}")
        
        # Verificar fuentes
        fuentes = data.get("fuentes", {})
        print(f"Tamaños de fuente definidos: {len(fuentes)}")
        
        # Verificar dimensiones
        dimensiones = data.get("dimensiones", {})
        print(f"Dimensiones definidas: {len(dimensiones)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo ui.json: {e}")
        return False


def main():
    """Función principal."""
    print("Iniciando pruebas del sistema de configuración...")
    
    # Probar archivos de configuración
    config_files_ok = test_config_files()
    
    # Probar configuración de personajes
    characters_ok = test_characters_config()
    
    # Probar configuración de gameplay
    gameplay_ok = test_gameplay_config()
    
    # Probar configuración de UI
    ui_ok = test_ui_config()
    
    # Resumen
    print("\n=== RESUMEN ===")
    print(f"Archivos de configuración: {'✅ EXITOSO' if config_files_ok else '❌ FALLIDO'}")
    print(f"Configuración de personajes: {'✅ EXITOSO' if characters_ok else '❌ FALLIDO'}")
    print(f"Configuración de gameplay: {'✅ EXITOSO' if gameplay_ok else '❌ FALLIDO'}")
    print(f"Configuración de UI: {'✅ EXITOSO' if ui_ok else '❌ FALLIDO'}")
    
    all_success = config_files_ok and characters_ok and gameplay_ok and ui_ok
    
    if all_success:
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("✅ El sistema de configuración está listo para usar")
        return 0
    else:
        print("\n💥 ALGUNAS PRUEBAS FALLARON")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 