#!/usr/bin/env python3
"""
Script de Validación del Sistema de Documentación Integrado
Verifica que todas las referencias cruzadas estén correctas y accesibles.
"""

import os
import re


def validar_referencias_cruzadas():
    """Valida que todas las referencias entre documentos existan"""

    documentos_principales = [
        "docs/refactorizacion_progreso.md",
        "docs/PLAN_MIGRACION_SQLITE.md",
        "docs/FUNCIONES_DOCUMENTADAS.md",
        "docs/INDICE_MIGRACION_SQLITE.md",
        ".github/copilot-instructions.md",
    ]

    referencias_encontradas = []
    referencias_rotas = []

    for doc in documentos_principales:
        if not os.path.exists(doc):
            referencias_rotas.append(f"Documento faltante: {doc}")
            continue

        with open(doc, encoding="utf-8") as f:
            contenido = f.read()

        # Buscar enlaces markdown [](./)
        enlaces = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", contenido)

        for _, ruta in enlaces:
            if ruta.startswith("./") or ruta.startswith("../"):
                # Es una referencia local
                # Separar archivo de ancla (#seccion)
                if "#" in ruta:
                    archivo, _ = ruta.split("#", 1)
                else:
                    archivo = ruta

                ruta_absoluta = os.path.normpath(
                    os.path.join(os.path.dirname(doc), archivo)
                )
                if os.path.exists(ruta_absoluta):
                    referencias_encontradas.append(f"✅ {doc} → {ruta}")
                else:
                    referencias_rotas.append(f"❌ {doc} → {ruta} (NO EXISTE)")

    print("🔗 VALIDACIÓN DEL SISTEMA DE DOCUMENTACIÓN INTEGRADO")
    print("=" * 60)

    print(f"\n✅ Referencias válidas encontradas: {len(referencias_encontradas)}")
    for ref in referencias_encontradas[:5]:  # Mostrar solo las primeras 5
        print(f"  {ref}")
    if len(referencias_encontradas) > 5:
        print(f"  ... y {len(referencias_encontradas) - 5} más")

    if referencias_rotas:
        print(f"\n❌ Referencias rotas encontradas: {len(referencias_rotas)}")
        for ref in referencias_rotas:
            print(f"  {ref}")
        return False
    else:
        print("\n🎉 TODAS LAS REFERENCIAS ESTÁN CORRECTAS")
        return True


def verificar_estructura_documentos():
    """Verifica que los documentos tengan la estructura esperada"""

    verificaciones = {
        "docs/refactorizacion_progreso.md": [
            "Sistema de Documentación Integrado",
            "FASE 1 - URGENTE",
            "FASE 2 - ALTA PRIORIDAD",
            "FASE 3 - CRÍTICA",
        ],
        "docs/PLAN_MIGRACION_SQLITE.md": [
            "Referencias Cruzadas",
            "FASE 1: Preparación e Infraestructura",
            "FASE 2: Migración del ConfigManager",
            "FASE 3: Migración del SaveManager",
        ],
        ".github/copilot-instructions.md": [
            "Sistema de Documentación Integrado",
            "Protocolo de Trabajo OBLIGATORIO",
            "Migración SQLite Integrada",
        ],
    }

    print("\n📋 VERIFICANDO ESTRUCTURA DE DOCUMENTOS")
    print("=" * 40)

    todo_correcto = True

    for doc, secciones_requeridas in verificaciones.items():
        if not os.path.exists(doc):
            print(f"❌ {doc} - NO EXISTE")
            todo_correcto = False
            continue

        with open(doc, encoding="utf-8") as f:
            contenido = f.read()

        secciones_faltantes = []
        for seccion in secciones_requeridas:
            if seccion not in contenido:
                secciones_faltantes.append(seccion)

        if secciones_faltantes:
            print(f"❌ {doc} - Secciones faltantes: {secciones_faltantes}")
            todo_correcto = False
        else:
            print(f"✅ {doc} - Estructura correcta")

    return todo_correcto


if __name__ == "__main__":
    referencias_ok = validar_referencias_cruzadas()
    estructura_ok = verificar_estructura_documentos()

    if referencias_ok and estructura_ok:
        print("\n🎯 SISTEMA DE DOCUMENTACIÓN INTEGRADO: VALIDADO CORRECTAMENTE")
        print("El sistema está listo para la refactorización con migración SQLite")
    else:
        print("\n⚠️  PROBLEMAS DETECTADOS EN EL SISTEMA DE DOCUMENTACIÓN")
        print("Revisar y corregir antes de proceder con la refactorización")
