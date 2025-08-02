#!/usr/bin/env python3
"""
Script de Empaquetado Universal para Proyectos Python
====================================================

Autor: SiK Team
Fecha: 2024
Descripción: Script universal para empaquetar proyectos Python en ejecutables
             usando PyInstaller. Compatible con cualquier estructura de proyecto.
"""

import json
import logging
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class UniversalPackager:
    """
    Empaquetador universal para proyectos Python.
    """

    def __init__(self, project_root: str = "."):
        """
        Inicializa el empaquetador.

        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root).resolve()
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """
        Carga la configuración del proyecto.

        Returns:
            Configuración del proyecto
        """
        config = {
            "entry_point": "src/main.py",
            "project_name": "SiK-Python-Game",
            "version_file": "VERSION.txt",
            "assets_dir": "assets",
            "config_dir": "config",
            "exclude_dirs": [
                "__pycache__",
                ".git",
                ".pytest_cache",
                "tests",
                "scripts",
                "docs",
                "logs",
                "saves",
                "backups",
            ],
            "exclude_files": [
                ".gitignore",
                "README.md",
                "CHANGELOG.md",
                "requirements.txt",
                "pyproject.toml",
            ],
            "additional_data": [],
            "hidden_imports": [],
            "console": False,
            "onefile": True,
            "icon": None,
        }

        # Intentar cargar configuración específica del proyecto
        config_file = self.project_root / "package_config.json"
        if config_file.exists():
            try:
                with open(config_file, encoding="utf-8") as f:
                    project_config = json.load(f)
                    config.update(project_config)
                logger.info(f"Configuración cargada desde {config_file}")
            except Exception as e:
                logger.warning(f"No se pudo cargar la configuración: {e}")

        return config

    def get_current_version(self) -> str:
        """
        Obtiene la versión actual del proyecto.

        Returns:
            Versión actual
        """
        version_file = self.project_root / self.config["version_file"]

        if not version_file.exists():
            # Intentar obtener versión desde pyproject.toml
            pyproject_file = self.project_root / "pyproject.toml"
            if pyproject_file.exists():
                try:
                    with open(pyproject_file, encoding="utf-8") as f:
                        content = f.read()
                        if 'version = "' in content:
                            start = content.find('version = "') + 10
                            end = content.find('"', start)
                            return content[start:end]
                except Exception:
                    pass

            # Versión por defecto
            return "0.1.0"

        try:
            with open(version_file, encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error al leer versión: {e}")
            return "0.1.0"

    def update_version(self, version_type: str) -> str:
        """
        Actualiza la versión del proyecto.

        Args:
            version_type: Tipo de actualización (major, minor, patch)

        Returns:
            Nueva versión
        """
        current_version = self.get_current_version()
        major, minor, patch = map(int, current_version.split("."))

        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            raise ValueError(
                "Tipo de versión inválido. Use 'major', 'minor' o 'patch'."
            )

        new_version = f"{major}.{minor}.{patch}"

        # Actualizar archivo de versión
        version_file = self.project_root / self.config["version_file"]
        try:
            with open(version_file, "w", encoding="utf-8") as f:
                f.write(new_version)
            logger.info(f"Versión actualizada a {new_version}")
        except Exception as e:
            logger.error(f"Error al actualizar versión: {e}")

        return new_version

    def validate_project_structure(self) -> bool:
        """
        Valida la estructura del proyecto.

        Returns:
            True si la estructura es válida
        """
        entry_point = self.project_root / self.config["entry_point"]

        if not entry_point.exists():
            logger.error(f"Punto de entrada no encontrado: {entry_point}")
            return False

        logger.info(f"Punto de entrada válido: {entry_point}")
        return True

    def build_pyinstaller_command(self, version: str) -> list[str]:
        """
        Construye el comando de PyInstaller.

        Args:
            version: Versión del proyecto

        Returns:
            Lista de argumentos para PyInstaller
        """
        # Separador de datos según plataforma
        data_sep = ";" if sys.platform == "win32" else ":"

        # Rutas absolutas
        entry_point = self.project_root / self.config["entry_point"]
        assets_dir = self.project_root / self.config["assets_dir"]
        config_dir = self.project_root / self.config["config_dir"]

        # Comando base
        command = [
            "pyinstaller",
            str(entry_point),
            "--noconsole" if not self.config["console"] else "--console",
            "--onefile" if self.config["onefile"] else "--onedir",
            f"--name={self.config['project_name']}_v{version}",
            f"--paths={self.project_root / 'src'}",
        ]

        # Añadir datos adicionales
        if assets_dir.exists():
            command.append(
                f"--add-data={assets_dir}{data_sep}{self.config['assets_dir']}"
            )

        if config_dir.exists():
            command.append(
                f"--add-data={config_dir}{data_sep}{self.config['config_dir']}"
            )

        # Añadir datos adicionales configurados
        for data_path in self.config["additional_data"]:
            source_path = self.project_root / data_path["source"]
            dest_path = data_path["dest"]
            if source_path.exists():
                command.append(f"--add-data={source_path}{data_sep}{dest_path}")

        # Añadir imports ocultos
        for hidden_import in self.config["hidden_imports"]:
            command.append(f"--hidden-import={hidden_import}")

        # Añadir icono si existe
        if self.config["icon"]:
            icon_path = self.project_root / self.config["icon"]
            if icon_path.exists():
                command.append(f"--icon={icon_path}")

        return command

    def package_project(self, version: str) -> bool:
        """
        Empaqueta el proyecto.

        Args:
            version: Versión a empaquetar

        Returns:
            True si el empaquetado fue exitoso
        """
        logger.info(f"Empaquetando la versión {version}...")

        # Validar estructura del proyecto
        if not self.validate_project_structure():
            return False

        # Crear directorio de releases
        release_dir = self.project_root / "releases" / f"v{version}"
        release_dir.mkdir(parents=True, exist_ok=True)

        # Limpiar directorios anteriores
        build_dir = release_dir / "build"
        dist_dir = release_dir / "dist"

        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)

        # Construir comando PyInstaller
        pyinstaller_command = self.build_pyinstaller_command(version)

        # Añadir rutas de salida
        pyinstaller_command.extend(
            [
                f"--distpath={dist_dir}",
                f"--workpath={build_dir}",
                f"--specpath={release_dir}",
            ]
        )

        logger.info(f"Ejecutando: {' '.join(pyinstaller_command)}")

        try:
            # Ejecutar PyInstaller
            subprocess.run(
                pyinstaller_command,
                check=True,
            )

            logger.info("PyInstaller completado exitosamente")

            # Crear archivo ZIP
            self._create_zip_package(release_dir, dist_dir, version)

            # Limpiar archivos temporales
            self._cleanup_build_files(release_dir, build_dir)

            logger.info("Proceso de empaquetado completado")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Error durante la ejecución de PyInstaller: {e}")
            logger.error(f"Salida de error: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return False

    def _create_zip_package(self, release_dir: Path, dist_dir: Path, version: str):
        """
        Crea el archivo ZIP del paquete.

        Args:
            release_dir: Directorio de releases
            dist_dir: Directorio de distribución
            version: Versión del proyecto
        """
        zip_filename = release_dir / f"{self.config['project_name']}_v{version}.zip"

        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Añadir ejecutable
            exe_name = (
                f"{self.config['project_name']}_v{version}.exe"
                if sys.platform == "win32"
                else f"{self.config['project_name']}_v{version}"
            )
            exe_path = dist_dir / exe_name

            if exe_path.exists():
                zipf.write(exe_path, exe_path.name)
                logger.info(f"Ejecutable añadido al ZIP: {exe_path.name}")
            else:
                logger.warning(f"Ejecutable no encontrado: {exe_path}")

            # Añadir assets si existen
            assets_dir = self.project_root / self.config["assets_dir"]
            if assets_dir.exists():
                for root, _, files in os.walk(assets_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(self.project_root)
                        zipf.write(file_path, arc_name)
                logger.info("Assets añadidos al ZIP")

            # Añadir configuración si existe
            config_dir = self.project_root / self.config["config_dir"]
            if config_dir.exists():
                for root, _, files in os.walk(config_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(self.project_root)
                        zipf.write(file_path, arc_name)
                logger.info("Configuración añadida al ZIP")

        logger.info(f"Archivo ZIP creado: {zip_filename}")

    def _cleanup_build_files(self, release_dir: Path, build_dir: Path):
        """
        Limpia archivos de compilación temporales.

        Args:
            release_dir: Directorio de releases
            build_dir: Directorio de build
        """
        # Limpiar directorio de build
        if build_dir.exists():
            shutil.rmtree(build_dir)

        # Limpiar archivo .spec
        spec_files = list(release_dir.glob("*.spec"))
        for spec_file in spec_files:
            spec_file.unlink()

        logger.info("Archivos temporales limpiados")


def main():
    """
    Función principal del script.
    """
    if len(sys.argv) != 2:
        print("Uso: python tools/package_improved.py [major|minor|patch]")
        print("Ejemplo: python tools/package_improved.py patch")
        sys.exit(1)

    version_type = sys.argv[1]

    if version_type not in ["major", "minor", "patch"]:
        print("Error: Tipo de versión debe ser 'major', 'minor' o 'patch'")
        sys.exit(1)

    try:
        packager = UniversalPackager()
        new_version = packager.update_version(version_type)

        if packager.package_project(new_version):
            print(f"✅ Empaquetado completado exitosamente - Versión {new_version}")
            print(f"📦 Archivo disponible en: releases/v{new_version}/")
        else:
            print("❌ Error durante el empaquetado")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
