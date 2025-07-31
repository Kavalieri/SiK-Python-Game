# Script de Limpieza Completa - Referencia Rápida

## 📋 **Comandos Principales**

### Uso Diario (Recomendado)
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "light"
```

### Limpieza Profunda (Semanal)
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "deep"
```

### Limpieza Completa (Mensual/Pre-cierre)
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "complete" -Force
```

### Cierre de Proyecto (Shutdown)
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "shutdown" -PreShutdown
```

## 🔍 **Validación y Pruebas**

### Probar Script
```powershell
.\dev-tools\scripts\test_comprehensive_cleanup.ps1 -Mode test
```

### Validar Sintaxis
```powershell
.\dev-tools\scripts\test_comprehensive_cleanup.ps1 -Mode validate
```

### Ver Cachés Actuales
```powershell
.\dev-tools\scripts\test_comprehensive_cleanup.ps1 -Mode show
```

## 📊 **Qué Limpia Cada Nivel**

### Level: light
- ✅ Cachés Python (src\__pycache__, .pytest_cache)
- ✅ Cachés herramientas (.mypy_cache, .ruff_cache)
- ✅ VS Code SendKeys (si está abierto)

### Level: deep
- ✅ Todo lo de "light"
- ✅ VS Code workspaceStorage y logs
- ✅ Archivos temporales (*.tmp, *.temp, etc.)

### Level: complete
- ✅ Todo lo de "deep"
- ✅ Rotación de logs del proyecto (mantiene últimos 5)
- ✅ Optimización Git (gc, reflog)

### Level: shutdown
- ✅ Todo lo de "complete"
- ✅ Cierre completo de pestañas VS Code
- ✅ Preparación para cierre del proyecto

## 🚨 **Notas Importantes**

### Confirmaciones
- Los niveles `complete` y `shutdown` requieren confirmación
- Usar `-Force` para omitir confirmación
- El script siempre pregunta antes de operaciones destructivas

### Logs
- Cada ejecución genera un log: `logs/cleanup_TIMESTAMP.log`
- Los logs se rotan automáticamente (se mantienen los últimos 5)
- Usar los logs para auditoría y resolución de problemas

### Integración VS Code
- Detecta automáticamente si VS Code está ejecutándose
- Usa vscode_cleanup_sendkeys.ps1 si está disponible
- Preserva pestañas pinned y configuración

### Validación Post-Limpieza
- Verifica cachés eliminados
- Muestra procesos VS Code restantes
- Indica si la limpieza fue exitosa

## 📁 **Estructura de Archivos**

```
dev-tools/scripts/
├── comprehensive_cleanup.ps1      # Script principal
├── test_comprehensive_cleanup.ps1 # Script de prueba
└── vscode_cleanup_sendkeys.ps1   # Script auxiliar VS Code
```

## 🔄 **Integración con Flujo de Trabajo**

### Post-Commit (Automático)
```powershell
# Añadir al final de scripts de commit
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "light"
```

### Pre-Push (Manual)
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "deep"
```

### Fin de Sesión
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "complete" -Force
```

### Cierre de Proyecto
```powershell
.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "shutdown" -PreShutdown
```

---

**Fecha de creación**: 31 de Julio, 2025
**Última actualización**: 31 de Julio, 2025
**Estado**: Implementado y probado
**Reemplaza**: vscode_cleanup_sendkeys.ps1 como script principal
