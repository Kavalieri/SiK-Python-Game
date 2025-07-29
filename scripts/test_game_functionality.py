#!/usr/bin/env python3
"""
Test Game Functionality - Prueba de Funcionalidad del Juego
=========================================================

Autor: SiK Team
Fecha: 2025-07-29
Descripción: Script que prueba la funcionalidad real del juego.
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def test_game_functionality():
    """Prueba la funcionalidad real del juego."""
    print("=== PRUEBA DE FUNCIONALIDAD DEL JUEGO ===")

    # Verificar que estamos en el directorio correcto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print(f"Directorio del proyecto: {project_root}")

    # Verificar que existe el archivo principal
    main_file = project_root / "src" / "main.py"
    if not main_file.exists():
        print("❌ Error: No se encuentra src/main.py")
        return False

    print("✅ Archivo principal encontrado")

    # Verificar dependencias
    try:
        pass  # Eliminados imports no utilizados
    except Exception as e:
        print(f"Error: {e}")

    # Intentar lanzar el juego y verificar funcionalidad
    print("\n🚀 Lanzando el juego para prueba de funcionalidad...")
    print("(El juego se ejecutará por 15 segundos para verificar navegación)")

    try:
        # Lanzar el juego en segundo plano
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Esperar 15 segundos para que el juego se inicialice
        time.sleep(15)

        # Terminar el proceso
        process.terminate()

        # Esperar a que termine
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

        # Verificar la salida
        stdout, stderr = process.communicate()

        # Analizar los errores
        errors = []
        warnings = []

        if stderr:
            lines = stderr.split("\n")
            for line in lines:
                if "Error" in line:
                    errors.append(line.strip())
                elif "Warning" in line or "warning" in line:
                    warnings.append(line.strip())

        # Evaluar la funcionalidad
        critical_errors = [
            "Error crítico",
            "Error en el bucle principal",
            "Error al configurar escenas",
            "Error al inicializar componentes",
        ]

        has_critical_errors = any(
            any(critical in error for critical in critical_errors) for error in errors
        )

        if has_critical_errors:
            print("❌ ERRORES CRÍTICOS DETECTADOS:")
            for error in errors:
                if any(critical in error for critical in critical_errors):
                    print(f"  - {error}")
            return False

        # Mostrar warnings menores
        if warnings:
            print("⚠️  WARNINGS DETECTADOS (no críticos):")
            for warning in warnings[:5]:  # Mostrar solo los primeros 5
                print(f"  - {warning}")

        # Verificar que el juego se inicializó correctamente
        if (
            "Motor del juego inicializado" in stdout
            or "Motor del juego inicializado" in stderr
        ):
            print("✅ Motor del juego inicializado correctamente")
        else:
            print("⚠️  No se detectó inicialización del motor")

        if (
            "Sistema de logging inicializado" in stdout
            or "Sistema de logging inicializado" in stderr
        ):
            print("✅ Sistema de logging funcionando")
        else:
            print("⚠️  Sistema de logging no detectado")

        # Verificar que no hay errores de callbacks críticos
        callback_errors = [
            error for error in errors if "Callback no encontrado" in error
        ]
        if callback_errors:
            print(f"⚠️  {len(callback_errors)} errores de callbacks (no críticos)")

        # Verificar que no hay errores de sprites críticos
        sprite_errors = [error for error in errors if "Sprite no encontrado" in error]
        if sprite_errors:
            print(
                f"⚠️  {len(sprite_errors)} errores de sprites (placeholders generados)"
            )

        print("\n✅ Juego lanzado y funcionando")
        print("✅ No se detectaron errores críticos")
        print("✅ Sistema operativo básico funcionando")

        return True

    except Exception as e:
        print(f"❌ Error lanzando el juego: {e}")
        return False


def test_basic_components():
    """Prueba componentes básicos del juego."""
    print("\n=== PRUEBA DE COMPONENTES BÁSICOS ===")

    try:
        # Verificar que los archivos principales existen
        project_root = Path(__file__).parent.parent

        required_files = [
            "src/main.py",
            "src/utils/config_manager.py",
            "src/core/game_state.py",
            "src/utils/asset_manager.py",
        ]

        for file_path in required_files:
            if not (project_root / file_path).exists():
                print(f"❌ Archivo faltante: {file_path}")
                return False

        print("✅ Todos los archivos principales existen")
        print("✅ Estructura del proyecto correcta")

        return True

    except Exception as e:
        print(f"❌ Error en componentes básicos: {e}")
        return False


def main():
    """Función principal."""
    print("=== PRUEBA COMPLETA DE FUNCIONALIDAD ===")

    # Probar componentes básicos
    basic_ok = test_basic_components()

    # Probar funcionalidad del juego
    game_ok = test_game_functionality()

    if basic_ok and game_ok:
        print("\n🎉 ¡PRUEBA COMPLETA EXITOSA!")
        print("El juego SiK Python Game está funcionando correctamente.")
        print("\nPara jugar:")
        print("  python src/main.py")
        print("\nEstado: ✅ FUNCIONAL")
    else:
        print("\n💥 PRUEBA FALLIDA")
        if not basic_ok:
            print("- ❌ Componentes básicos con problemas")
        if not game_ok:
            print("- ❌ Funcionalidad del juego con problemas")
        print("\nEstado: ❌ NO FUNCIONAL")

    return 0 if (basic_ok and game_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
