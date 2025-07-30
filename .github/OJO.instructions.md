---
applyTo: '**'
---

# Instrucciones Personalizadas - SiK Python Game

## 🚨 FLUJO POST-OPERACIÓN OBLIGATORIO
**Ejecutar SIEMPRE tras**: commits, pruebas, errores, objetivos completados
```powershell
.\scripts\vscode_cleanup_sendkeys.ps1 -Level "light"
```
- **Método validado**: SendKeys (Ctrl+K U) preserva pestañas pinned
- **Libera**: 272+ MB caché VS Code comprobados
- **Sin efectos secundarios**: No cambia tamaño ventana

## 🎯 Directrices Críticas
- **CONSULTAR PRIMERO**: `docs/refactorizacion_progreso.md` antes de CUALQUIER cambio
- **LÍMITE ABSOLUTO**: 150 líneas por archivo - dividir INMEDIATAMENTE si se excede
- **ACTUALIZAR SIEMPRE**: `docs/FUNCIONES_DOCUMENTADAS.md` con cada función nueva
- **Commits**: Solo `.\scripts\simple_commit.ps1 "mensaje"` (método unificado)

## 🛠️ Stack y Preferencias
- **Español completo**: Código, comentarios, variables, documentación
- **GitHub CLI prioritario**: `gh` > git tradicional para operaciones repo
- **PowerShell**: Shell predeterminado (NO `&&`, usar `;`)
- **Calidad**: 0 errores Ruff + 0 warnings MyPy + 100% cobertura tests

## 📋 Responsabilidades Automáticas
- **Mantener consistencia** con arquitectura modular SiK Python Game
- **Documentar decisiones** importantes en archivos correspondientes
- **Actualizar automáticamente** documentación tras cambios significativos
- **Priorizar robustez** y mantenibilidad sobre velocidad desarrollo
- Seguir metodología incremental
- **Usar scripts automatizados** cuando estén disponibles (`commit_profesional.ps1`)
