# Limpieza y Optimización

## 🧹 **Limpieza Post-Operación**
**RECORDATORIO**: Usar `.\dev-tools\scripts\vscode_cleanup_sendkeys.ps1 -Level "light"` tras operaciones importantes.

- **Método validado**: SendKeys (Ctrl+K U) preserva pestañas pinned
- **Libera**: 272+ MB caché VS Code comprobados
- **Sin efectos secundarios**: No cambia tamaño ventana

### Optimización de Entorno de Trabajo (NUEVO - RECOMENDADO)
- **Script de limpieza**: `.\dev-tools\scripts\workspace_cleanup.ps1` para optimizar VS Code y caché
- **Configuración automática**: `.\dev-tools\scripts\setup_auto_cleanup.ps1` para integrar limpieza
- **Niveles de limpieza**: light (diario), deep (semanal), complete (mensual)
- **Capacidades VS Code**: Cierre automático de pestañas con comandos workbench
- **Limpieza de caché**: Python (__pycache__), Poetry, Git, VS Code workspaceStorage
- **Optimización memoria**: Garbage collection .NET y análisis de uso de memoria
- **Integración commits**: Limpieza automática después de commits exitosos
- **Atajos de teclado**: Ctrl+K Ctrl+L (light), Ctrl+K Ctrl+T (tabs), Ctrl+K Ctrl+D (deep)
- **Documentación**: `docs/OPTIMIZACION_ENTORNO_TRABAJO.md` con guía completa
- **Uso recomendado**: `.\dev-tools\scripts\workspace_cleanup.ps1 -Level "light"` después de cada commit

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
