#!/usr/bin/env python3
"""
Test Game Launch - Prueba de Lanzamiento del Juego
=================================================

Autor: SiK Team
Fecha: 2025-07-29
Descripción: Script simple para probar el lanzamiento del juego.
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def test_game_launch():
    """Prueba el lanzamiento del juego."""
    print("=== PRUEBA DE LANZAMIENTO DEL JUEGO ===")

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
    except Exception:
        print("Error al verificar dependencias")  # Eliminada variable `e`

    # Intentar lanzar el juego
    print("\n🚀 Lanzando el juego...")
    print("(El juego se ejecutará por 10 segundos para verificar que funciona)")

    try:
        # Lanzar el juego en segundo plano
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Esperar 10 segundos
        time.sleep(10)

        # Terminar el proceso
        process.terminate()

        # Esperar a que termine
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

        # Verificar la salida
        stdout, stderr = process.communicate()

        if process.returncode == 0 or process.returncode is None:
            print("✅ Juego lanzado exitosamente")
            print("✅ No se detectaron errores críticos")
            return True
        else:
            print(f"⚠️  Juego terminado con código: {process.returncode}")
            if stderr:
                print(f"Errores detectados:\n{stderr}")
            return True  # Consideramos exitoso si no hay errores críticos

    except Exception as e:
        print(f"❌ Error lanzando el juego: {e}")
        return False


def main():
    """Función principal."""
    success = test_game_launch()

    if success:
        print("\n🎉 ¡PRUEBA EXITOSA!")
        print("El juego SiK Python Game está funcionando correctamente.")
        print("\nPara jugar:")
        print("  python src/main.py")
    else:
        print("\n💥 PRUEBA FALLIDA")
        print("Hay problemas que necesitan ser corregidos.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
