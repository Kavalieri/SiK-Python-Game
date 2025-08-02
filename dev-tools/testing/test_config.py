"""
Test Config - Configuración Común para Tests
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Configuración común para todos los scripts de test.
"""

import os
import sys


def setup_test_environment():
    """Configura el entorno para los tests."""
    # Obtener el directorio raíz del proyecto (dos niveles arriba de scripts/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Añadir el directorio src al path
    src_path = os.path.join(project_root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Añadir el directorio raíz al path también
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    return project_root, src_path
