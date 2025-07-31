# Limpieza y Optimización

# Limpieza y Optimización

## 🧹 **Limpieza Post-Operación**
**ACTUALIZADO**: Usar `.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "light"` tras operaciones importantes.

- **Script mejorado**: comprehensive_cleanup.ps1 (reemplaza vscode_cleanup_sendkeys.ps1)
- **Limpieza completa**: Python caches, VS Code, herramientas dev, logs, git optimization
- **4 niveles**: light (diario), deep (semanal), complete (mensual), shutdown (cierre proyecto)
- **Sin efectos secundarios**: Preserva pestañas pinned, configuración VS Code
- **Validación integrada**: Script de prueba disponible para verificar funcionalidad

### 🔒 **Sistema de Cierre de Sesión** (NUEVO - CRÍTICO)
- **Activación automática**: Cuando usuario indique cierre de sesión ("cerrar sesión", "terminar trabajo", "shutdown", etc.)
- **Comando**: `.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "shutdown" -Force`
- **Funcionalidad**: Cierre agresivo VS Code + eliminación archivos no rastreados + limpieza completa
- **Problema resuelto**: Evita reapertura de pestañas no deseadas y regeneración de archivos eliminados
- **Documentación completa**: `docs/SISTEMA_CIERRE_SESION.md`
- **Validado**: ✅ 31 Julio 2025 - Funcional completamente

### Script de Limpieza Completa (NUEVO - RECOMENDADO)
- **Script principal**: `.\dev-tools\scripts\comprehensive_cleanup.ps1`
- **Script de prueba**: `.\dev-tools\scripts\test_comprehensive_cleanup.ps1`
- **Niveles disponibles**:
  - `light`: Cachés Python y herramientas básicas
  - `deep`: + VS Code caches y archivos temporales
  - `complete`: + optimización Git y logs antiguos
  - `shutdown`: + cierre completo VS Code (para cierre proyecto)
- **Uso diario**: `.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "light"`
- **Uso forzado**: `.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "complete" -Force`
- **Pre-shutdown**: `.\dev-tools\scripts\comprehensive_cleanup.ps1 -Level "shutdown" -PreShutdown`
- **Validación**: `.\dev-tools\scripts\test_comprehensive_cleanup.ps1 -Mode test`

### Capacidades del Script Completo
- **Limpieza Python**: __pycache__, .pytest_cache recursivos
- **Herramientas dev**: .mypy_cache, .ruff_cache, .coverage, htmlcov
- **VS Code**: .vscode\workspaceStorage, .vscode\logs
- **Archivos temporales**: *.tmp, *.temp, *~, .DS_Store, Thumbs.db
- **Optimización Git**: gc --prune, reflog expire
- **Logs del proyecto**: Rotación automática (mantiene últimos 5)
- **Integración SendKeys**: Usa vscode_cleanup_sendkeys.ps1 si VS Code está abierto
- **Logging completo**: logs/cleanup_TIMESTAMP.log para auditoría
- **Resumen final**: Estado post-limpieza y validaciones

### Configuración Terminal VS Code (CRÍTICO)
- **Terminal optimizado**: Ver `docs/CONFIGURACION_TERMINAL_OPTIMIZADA.md` para configuración completa
- **Usar terminal existente** cuando esté disponible en lugar de crear nuevos
- **Scripts PowerShell ASCII-only**: **PROHIBIDOS emojis, Unicode y caracteres especiales**
- **Timeouts automáticos**: Todos los comandos largos deben tener timeout (30-45s máximo)
- **Detección de output**: Usar `isBackground=false` para comandos que requieren respuesta inmediata
- **Scripts terminal-safe**: OBLIGATORIO usar `.\dev-tools\scripts\terminal_safe_commit.ps1` para commits
- **Recuperación automática**: Si hay problemas, usar `.\dev-tools\scripts\reset_terminal_state.ps1`
- **Validación pre-comando**: Verificar responsividad con `.\dev-tools\scripts\test_ascii_safe.ps1`
- **Estado validado**: Terminal completamente funcional (30 jul 2025) - ver documentación

### Reglas PowerShell Scripts (OBLIGATORIO)
- **NUNCA usar emojis** (🚀, ✅, ❌, etc.) - causan problemas encoding
- **NUNCA usar Unicode** - solo caracteres ASCII básicos
- **Usar [OK], [ERROR], [WARN]** en lugar de símbolos
- **Usar Write-Host con -ForegroundColor** para colores
- **Incluir timeouts** en todos los comandos que pueden colgarse
- **Validar estado terminal** antes de operaciones complejas
