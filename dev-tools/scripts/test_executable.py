#!/usr/bin/env python3
"""
Script de Prueba del Ejecutable
===============================

Autor: SiK Team
Fecha: 2024
Descripción: Script para probar el ejecutable generado y verificar su funcionamiento.
"""

import logging
import subprocess
import sys
import time
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def find_latest_executable():
    """
    Encuentra el ejecutable más reciente en el directorio releases.

    Returns:
        Path del ejecutable más reciente o None si no se encuentra
    """
    releases_dir = Path("releases")

    if not releases_dir.exists():
        logger.error("Directorio releases no encontrado")
        return None

    # Buscar la versión más reciente
    version_dirs = [
        d for d in releases_dir.iterdir() if d.is_dir() and d.name.startswith("v")
    ]

    if not version_dirs:
        logger.error("No se encontraron directorios de versiones")
        return None

    # Ordenar por nombre (versión) y tomar la más reciente
    latest_version = sorted(version_dirs)[-1]
    dist_dir = latest_version / "dist"

    if not dist_dir.exists():
        logger.error(f"Directorio dist no encontrado en {latest_version}")
        return None

    # Buscar el ejecutable
    exe_files = list(dist_dir.glob("*.exe"))

    if not exe_files:
        logger.error(f"No se encontraron ejecutables en {dist_dir}")
        return None

    return exe_files[0]


def test_executable_basic(exe_path):
    """
    Prueba básica del ejecutable.

    Args:
        exe_path: Ruta del ejecutable

    Returns:
        True si la prueba es exitosa
    """
    logger.info(f"Probando ejecutable: {exe_path}")

    try:
        # Verificar que el archivo existe y es ejecutable
        if not exe_path.exists():
            logger.error(f"El ejecutable no existe: {exe_path}")
            return False

        file_size = exe_path.stat().st_size
        logger.info(f"Tamaño del ejecutable: {file_size / (1024 * 1024):.1f} MB")

        # Verificar que el archivo no está corrupto
        if file_size < 1024 * 1024:  # Menos de 1MB
            logger.warning(
                "El ejecutable parece ser muy pequeño, podría estar corrupto"
            )

        return True

    except Exception as e:
        logger.error(f"Error al verificar el ejecutable: {e}")
        return False


def test_executable_launch(exe_path, timeout=30):
    """
    Prueba el lanzamiento del ejecutable.

    Args:
        exe_path: Ruta del ejecutable
        timeout: Tiempo máximo de espera en segundos

    Returns:
        True si el lanzamiento es exitoso
    """
    logger.info(f"Probando lanzamiento del ejecutable (timeout: {timeout}s)")

    try:
        # Lanzar el ejecutable en segundo plano
        process = subprocess.Popen(
            [str(exe_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Esperar un tiempo para que se inicialice
        time.sleep(5)

        # Verificar si el proceso sigue ejecutándose
        if process.poll() is None:
            logger.info("✅ Ejecutable lanzado correctamente y sigue ejecutándose")

            # Terminar el proceso después de un tiempo
            time.sleep(10)
            process.terminate()

            try:
                process.wait(timeout=5)
                logger.info("✅ Proceso terminado correctamente")
                return True
            except subprocess.TimeoutExpired:
                logger.warning(
                    "⚠️ El proceso no terminó en 5 segundos, forzando terminación"
                )
                process.kill()
                return True
        else:
            # El proceso terminó prematuramente
            stdout, stderr = process.communicate()
            logger.error("❌ El ejecutable terminó prematuramente")
            logger.error(f"Salida estándar: {stdout}")
            logger.error(f"Error estándar: {stderr}")
            return False

    except Exception as e:
        logger.error(f"❌ Error al lanzar el ejecutable: {e}")
        return False


def test_executable_zip():
    """
    Prueba el archivo ZIP generado.

    Returns:
        True si la prueba es exitosa
    """
    releases_dir = Path("releases")

    if not releases_dir.exists():
        logger.error("Directorio releases no encontrado")
        return False

    # Buscar el ZIP más reciente
    version_dirs = [
        d for d in releases_dir.iterdir() if d.is_dir() and d.name.startswith("v")
    ]

    if not version_dirs:
        logger.error("No se encontraron directorios de versiones")
        return False

    latest_version = sorted(version_dirs)[-1]
    zip_files = list(latest_version.glob("*.zip"))

    if not zip_files:
        logger.error(f"No se encontraron archivos ZIP en {latest_version}")
        return False

    zip_path = zip_files[0]

    try:
        import zipfile

        with zipfile.ZipFile(zip_path, "r") as zipf:
            file_list = zipf.namelist()

            logger.info(f"📦 Archivo ZIP: {zip_path.name}")
            logger.info(f"📦 Tamaño: {zip_path.stat().st_size / (1024 * 1024):.1f} MB")
            logger.info(f"📦 Archivos contenidos: {len(file_list)}")

            # Verificar que contiene el ejecutable
            exe_files = [f for f in file_list if f.endswith(".exe")]
            if exe_files:
                logger.info(f"✅ ZIP contiene ejecutable: {exe_files[0]}")
            else:
                logger.error("❌ ZIP no contiene ejecutable")
                return False

            # Verificar que contiene assets
            asset_files = [f for f in file_list if f.startswith("assets/")]
            if asset_files:
                logger.info(f"✅ ZIP contiene {len(asset_files)} archivos de assets")
            else:
                logger.warning("⚠️ ZIP no contiene archivos de assets")

            return True

    except Exception as e:
        logger.error(f"❌ Error al verificar el ZIP: {e}")
        return False


def main():
    """
    Función principal del script de prueba.
    """
    logger.info("🧪 Iniciando pruebas del ejecutable...")

    # Encontrar el ejecutable más reciente
    exe_path = find_latest_executable()

    if not exe_path:
        logger.error("❌ No se pudo encontrar el ejecutable")
        return False

    logger.info(f"📁 Ejecutable encontrado: {exe_path}")

    # Ejecutar pruebas
    tests_passed = 0
    total_tests = 3

    # Prueba 1: Verificación básica
    logger.info("\n🔍 Prueba 1: Verificación básica del ejecutable")
    if test_executable_basic(exe_path):
        tests_passed += 1
        logger.info("✅ Prueba 1 pasada")
    else:
        logger.error("❌ Prueba 1 falló")

    # Prueba 2: Lanzamiento del ejecutable
    logger.info("\n🚀 Prueba 2: Lanzamiento del ejecutable")
    if test_executable_launch(exe_path):
        tests_passed += 1
        logger.info("✅ Prueba 2 pasada")
    else:
        logger.error("❌ Prueba 2 falló")

    # Prueba 3: Verificación del ZIP
    logger.info("\n📦 Prueba 3: Verificación del archivo ZIP")
    if test_executable_zip():
        tests_passed += 1
        logger.info("✅ Prueba 3 pasada")
    else:
        logger.error("❌ Prueba 3 falló")

    # Resumen de resultados
    logger.info("\n📊 Resumen de pruebas:")
    logger.info(f"   Pruebas pasadas: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        logger.info(
            "🎉 ¡Todas las pruebas pasaron! El ejecutable está listo para distribución."
        )
        return True
    else:
        logger.error(
            f"⚠️ {total_tests - tests_passed} prueba(s) fallaron. Revisar el ejecutable."
        )
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
