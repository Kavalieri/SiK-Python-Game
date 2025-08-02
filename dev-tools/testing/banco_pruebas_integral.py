#!/usr/bin/env python3
"""
🧪 BANCO DE PRUEBAS INTEGRAL - SiK Python Game
=============================================

Sistema completo de testing automatizado para detectar errores:
- Importaciones
- Sintaxis Python
- Configuración del proyecto
- Dependencias
- Funcionalidad básica del juego
- Logs en tiempo real

Autor: SiK Team
Fecha: 2 Agosto 2025
"""

import ast
import importlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
SRC_DIR = PROJECT_ROOT / "src"

# Asegurar directorios
LOGS_DIR.mkdir(exist_ok=True)


class ColorLogger:
    """Logger con colores para mejor visualización."""

    @staticmethod
    def success(msg: str) -> None:
        print(f"✅ {msg}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"⚠️  {msg}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"❌ {msg}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"🔍 {msg}")

    @staticmethod
    def section(msg: str) -> None:
        print(f"\n{'=' * 60}")
        print(f"🧪 {msg}")
        print("=" * 60)


class BancoPruebas:
    """Banco de pruebas integral para detectar errores."""

    def __init__(self):
        self.logger = ColorLogger()
        self.errores_encontrados: list[dict[str, Any]] = []
        self.warnings_encontrados: list[dict[str, Any]] = []

    def registrar_error(
        self, categoria: str, descripcion: str, detalles: str = ""
    ) -> None:
        """Registra un error encontrado."""
        self.errores_encontrados.append(
            {"categoria": categoria, "descripcion": descripcion, "detalles": detalles}
        )
        self.logger.error(f"[{categoria}] {descripcion}")
        if detalles:
            print(f"   → {detalles}")

    def registrar_warning(
        self, categoria: str, descripcion: str, detalles: str = ""
    ) -> None:
        """Registra un warning encontrado."""
        self.warnings_encontrados.append(
            {"categoria": categoria, "descripcion": descripcion, "detalles": detalles}
        )
        self.logger.warning(f"[{categoria}] {descripcion}")
        if detalles:
            print(f"   → {detalles}")

    def test_estructura_proyecto(self) -> bool:
        """Verifica la estructura básica del proyecto."""
        self.logger.section("VERIFICACIÓN ESTRUCTURA DEL PROYECTO")

        estructura_requerida = [
            "src",
            "src/main.py",
            "src/core",
            "src/entities",
            "src/scenes",
            "src/ui",
            "src/utils",
            "data/game.db",
            "pyproject.toml",
            "config",
        ]

        errores = 0
        for item in estructura_requerida:
            path = PROJECT_ROOT / item
            if not path.exists():
                self.registrar_error("ESTRUCTURA", f"Falta: {item}")
                errores += 1
            else:
                self.logger.success(f"Encontrado: {item}")

        return errores == 0

    def test_sintaxis_python(self) -> bool:
        """Verifica sintaxis de todos los archivos Python."""
        self.logger.section("VERIFICACIÓN SINTAXIS PYTHON")

        archivos_python = list(SRC_DIR.rglob("*.py"))
        errores = 0

        for archivo in archivos_python:
            try:
                with open(archivo, encoding="utf-8") as f:
                    contenido = f.read()

                # Verificar sintaxis compilando AST
                ast.parse(contenido)
                self.logger.success(f"Sintaxis OK: {archivo.relative_to(PROJECT_ROOT)}")

            except SyntaxError as e:
                self.registrar_error(
                    "SINTAXIS",
                    f"Error sintaxis en {archivo.relative_to(PROJECT_ROOT)}",
                    f"Línea {e.lineno}: {e.msg}",
                )
                errores += 1
            except Exception as e:
                self.registrar_error(
                    "LECTURA",
                    f"No se puede leer {archivo.relative_to(PROJECT_ROOT)}",
                    str(e),
                )
                errores += 1

        return errores == 0

    def test_importaciones_criticas(self) -> bool:
        """Verifica que las importaciones críticas funcionen."""
        self.logger.section("VERIFICACIÓN IMPORTACIONES CRÍTICAS")

        modulos_criticos = ["pygame", "sqlite3", "json", "pathlib", "typing"]

        errores = 0
        for modulo in modulos_criticos:
            try:
                importlib.import_module(modulo)
                self.logger.success(f"Importación OK: {modulo}")
            except ImportError as e:
                self.registrar_error("IMPORTACIÓN", f"Falta módulo: {modulo}", str(e))
                errores += 1

        return errores == 0

    def test_poetry_dependencies(self) -> bool:
        """Verifica dependencias de Poetry."""
        self.logger.section("VERIFICACIÓN DEPENDENCIAS POETRY")

        try:
            # Verificar que Poetry funciona
            result = subprocess.run(
                ["poetry", "check"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                self.logger.success("Poetry check: OK")

                # Verificar dependencias instaladas
                result_show = subprocess.run(
                    ["poetry", "show"],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if "pygame-ce" in result_show.stdout:
                    self.logger.success("pygame-ce instalado correctamente")
                else:
                    self.registrar_warning(
                        "DEPENDENCIAS", "pygame-ce no encontrado en poetry show"
                    )

                return True
            else:
                self.registrar_error("POETRY", "Poetry check failed", result.stderr)
                return False

        except Exception as e:
            self.registrar_error("POETRY", "Error ejecutando Poetry", str(e))
            return False

    def test_base_datos(self) -> bool:
        """Verifica la base de datos SQLite."""
        self.logger.section("VERIFICACIÓN BASE DE DATOS")

        db_path = PROJECT_ROOT / "data" / "game.db"

        if not db_path.exists():
            self.registrar_error("DATABASE", "Base de datos no existe")
            return False

        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Verificar tabla personajes
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='personajes'"
            )
            if cursor.fetchone():
                self.logger.success("Tabla 'personajes' existe")

                # Contar personajes
                cursor.execute("SELECT COUNT(*) FROM personajes WHERE activo = 1")
                count = cursor.fetchone()[0]
                if count > 0:
                    self.logger.success(f"{count} personajes activos en BD")
                else:
                    self.registrar_warning("DATABASE", "No hay personajes activos")
            else:
                self.registrar_error("DATABASE", "Tabla 'personajes' no existe")

            conn.close()
            return True

        except Exception as e:
            self.registrar_error("DATABASE", "Error accediendo a base de datos", str(e))
            return False

    def test_configuracion_json(self) -> bool:
        """Verifica archivos de configuración JSON."""
        self.logger.section("VERIFICACIÓN CONFIGURACIÓN JSON")

        archivos_config = [
            "config/display.json",
            "config/audio.json",
            "config/gameplay.json",
            "config/characters.json",
        ]

        errores = 0
        for archivo in archivos_config:
            config_path = PROJECT_ROOT / archivo
            if config_path.exists():
                try:
                    with open(config_path, encoding="utf-8") as f:
                        json.load(f)
                    self.logger.success(f"JSON válido: {archivo}")
                except json.JSONDecodeError as e:
                    self.registrar_error("CONFIG", f"JSON inválido: {archivo}", str(e))
                    errores += 1
            else:
                self.registrar_warning("CONFIG", f"Config no encontrada: {archivo}")

        return errores == 0

    def test_importacion_modulos_juego(self) -> bool:
        """Verifica que los módulos del juego se puedan importar."""
        self.logger.section("VERIFICACIÓN MÓDULOS DEL JUEGO")

        # Añadir src al path temporalmente
        sys.path.insert(0, str(SRC_DIR))

        modulos_juego = [
            "main",
            "core.game_engine",
            "entities.player",
            "scenes.game_scene_core",
            "utils.config_loader",
        ]

        errores = 0
        for modulo in modulos_juego:
            try:
                importlib.import_module(modulo)
                self.logger.success(f"Módulo OK: {modulo}")
            except Exception as e:
                self.registrar_error("MÓDULO", f"Error importando: {modulo}", str(e))
                errores += 1

        # Restaurar path
        sys.path.remove(str(SRC_DIR))

        return errores == 0

    def generar_reporte(self) -> None:
        """Genera reporte final de las pruebas."""
        self.logger.section("REPORTE FINAL")

        total_errores = len(self.errores_encontrados)
        total_warnings = len(self.warnings_encontrados)

        if total_errores == 0 and total_warnings == 0:
            self.logger.success("🎉 TODAS LAS PRUEBAS PASARON - PROYECTO LISTO")
        else:
            if total_errores > 0:
                self.logger.error(f"Se encontraron {total_errores} errores críticos")
                for error in self.errores_encontrados:
                    print(f"   ❌ [{error['categoria']}] {error['descripcion']}")

            if total_warnings > 0:
                self.logger.warning(f"Se encontraron {total_warnings} advertencias")
                for warning in self.warnings_encontrados:
                    print(f"   ⚠️  [{warning['categoria']}] {warning['descripcion']}")

        # Guardar reporte en archivo
        reporte_path = LOGS_DIR / f"reporte_pruebas_{Path(__file__).stem}.json"
        with open(reporte_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "errores": self.errores_encontrados,
                    "warnings": self.warnings_encontrados,
                    "total_errores": total_errores,
                    "total_warnings": total_warnings,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        self.logger.info(f"Reporte guardado en: {reporte_path}")

    def ejecutar_todas_las_pruebas(self) -> bool:
        """Ejecuta todas las pruebas del banco."""
        self.logger.info("🚀 INICIANDO BANCO DE PRUEBAS INTEGRAL")

        pruebas = [
            self.test_estructura_proyecto,
            self.test_sintaxis_python,
            self.test_importaciones_criticas,
            self.test_poetry_dependencies,
            self.test_base_datos,
            self.test_configuracion_json,
            self.test_importacion_modulos_juego,
        ]

        resultados = []
        for prueba in pruebas:
            try:
                resultado = prueba()
                resultados.append(resultado)
            except Exception as e:
                self.registrar_error(
                    "PRUEBA", f"Error ejecutando {prueba.__name__}", str(e)
                )
                resultados.append(False)

        self.generar_reporte()

        return all(resultados) and len(self.errores_encontrados) == 0


def main():
    """Función principal."""
    banco = BancoPruebas()
    exito = banco.ejecutar_todas_las_pruebas()

    if exito:
        print("\n🎯 PROYECTO LISTO PARA DESARROLLO")
        sys.exit(0)
    else:
        print("\n🛑 ERRORES ENCONTRADOS - REVISAR ANTES DE CONTINUAR")
        sys.exit(1)


if __name__ == "__main__":
    main()
