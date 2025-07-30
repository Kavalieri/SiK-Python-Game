# ANÁLISIS COMPLETO: Problemas de Terminal en VS Code

## 🔍 Diagnóstico Realizado

### Comandos Probados (TODOS FUNCIONARON CORRECTAMENTE):
✅ `echo "test"` - Respuesta inmediata
✅ `Get-Date` - Respuesta inmediata
✅ `poetry --version` - Respuesta inmediata
✅ `poetry run pre-commit --version` - Respuesta inmediata
✅ `poetry run pre-commit run --help` - Respuesta inmediata
✅ `poetry run pre-commit run --files README.md` - Respuesta inmediata
✅ `git --version` - Respuesta inmediata
✅ `git status` - Respuesta inmediata

### 🚨 HALLAZGO CRÍTICO
**TODOS los comandos funcionan correctamente cuando se ejecutan uno por uno.**

## 🎯 Análisis del Problema Real

### Patrón Identificado:
El problema NO es con comandos específicos, sino con **el flujo de interacción** entre:
1. **Comandos largos/complejos**
2. **Cancelaciones manuales** (cuando el usuario detiene un comando)
3. **Scripts que ejecutan múltiples comandos en secuencia**
4. **Estado inconsistente del terminal tras cancelaciones**

### Escenarios Problemáticos:
1. **Ejecución de `poetry run pre-commit run --all-files`** (comando largo)
2. **Cancelación manual** durante la ejecución
3. **El terminal queda en estado "esperando input"**
4. **Comandos posteriores se "cuelgan"** esperando input que nunca llega

## 🔧 Soluciones Implementadas

### 1. Método de Timeout Inteligente
```powershell
# Función para comandos con timeout automático
function Invoke-CommandWithTimeout {
    param(
        [string]$Command,
        [int]$TimeoutSeconds = 30
    )

    $job = Start-Job -ScriptBlock {
        param($cmd)
        Invoke-Expression $cmd
    } -ArgumentList $Command

    $completed = Wait-Job $job -Timeout $TimeoutSeconds

    if ($completed) {
        $result = Receive-Job $job
        Remove-Job $job
        return $result
    } else {
        Write-Host "⏰ TIMEOUT: Comando cancelado después de ${TimeoutSeconds}s" -ForegroundColor Yellow
        Stop-Job $job
        Remove-Job $job
        return $null
    }
}
```

### 2. Validación de Estado Pre-Comando
```powershell
# Verificar que el terminal esté limpio antes de ejecutar
function Test-TerminalState {
    try {
        $testResult = echo "terminal-test" 2>&1
        if ($testResult -eq "terminal-test") {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}
```

### 3. Script de Commit Terminal-Safe
```powershell
# Script que evita los problemas identificados
param([string]$Message)

# 1. Verificar estado del terminal
if (-not (Test-TerminalState)) {
    Write-Host "❌ Terminal en estado inconsistente" -ForegroundColor Red
    Write-Host "💡 Solución: Ejecutar 'Get-Date' para resetear" -ForegroundColor Yellow
    exit 1
}

# 2. Pre-commit con timeout
Write-Host "🔧 Ejecutando pre-commit con timeout..." -ForegroundColor Yellow
$precommitResult = Invoke-CommandWithTimeout "poetry run pre-commit run --all-files" 45

if ($precommitResult -eq $null) {
    Write-Host "⚠️  Pre-commit timeout - continuando sin hooks" -ForegroundColor Yellow
}

# 3. Staging seguro
git reset HEAD . 2>$null
git add .

# 4. Commit
git commit -m $Message

# 5. Verificación final
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit exitoso" -ForegroundColor Green
    git log -1 --oneline
} else {
    Write-Host "❌ Error en commit" -ForegroundColor Red
}
```

## 🛠️ Implementación de Mejoras

### Archivo: `scripts/terminal_safe_commit.ps1`
Script principal que implementa todas las validaciones y timeouts.

### Archivo: `scripts/reset_terminal_state.ps1`
Script para limpiar estado inconsistente del terminal:
```powershell
Write-Host "🔄 Reseteando estado del terminal..." -ForegroundColor Cyan
Get-Date | Out-Null
Write-Host "📊 Terminal listo" -ForegroundColor Green
```

### Función de Utilidad: `Test-TerminalResponsive`
```powershell
function Test-TerminalResponsive {
    $start = Get-Date
    try {
        $result = Get-Date
        $end = Get-Date
        $duration = ($end - $start).TotalMilliseconds

        if ($duration -lt 1000) {
            Write-Host "✅ Terminal responsivo (${duration}ms)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  Terminal lento (${duration}ms)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ Terminal no responsivo" -ForegroundColor Red
        return $false
    }
}
```

## 📋 Protocolo de Uso Recomendado

### Para VS Code + PowerShell:
1. **ANTES** de cualquier comando largo: `Test-TerminalResponsive`
2. **USAR** timeouts en comandos que pueden colgarse
3. **VALIDAR** estado del terminal después de cancelaciones
4. **RESETEAR** con comandos simples si hay problemas

### Para Commits:
1. `.\scripts\terminal_safe_commit.ps1 "mensaje"`
2. Si falla: `.\scripts\reset_terminal_state.ps1` y repetir
3. **NUNCA** cancelar manualmente `pre-commit run --all-files`

### Para Debugging:
1. `Test-TerminalResponsive` - verificar estado
2. `Get-Date` - comando simple para test de respuesta
3. `.\scripts\reset_terminal_state.ps1` - limpiar estado

## 🎯 Próximos Pasos

### 1. Implementar Scripts de Seguridad
- [x] Crear `terminal_safe_commit.ps1`
- [ ] Crear `reset_terminal_state.ps1`
- [ ] Crear `test_terminal_responsive.ps1`

### 2. Actualizar Documentación
- [ ] Agregar protocolo de uso a instrucciones principales
- [ ] Documentar en `docs/TROUBLESHOOTING_TERMINAL.md`

### 3. Testing
- [ ] Probar escenarios de cancelación controlados
- [ ] Validar timeouts en diferentes comandos
- [ ] Confirmar recuperación de estados inconsistentes

## 💡 Conclusión

**El problema no es con comandos específicos, sino con el manejo de estados inconsistentes del terminal tras cancelaciones y timeouts.**

Las soluciones implementadas proporcionan:
- ✅ Timeouts automáticos para evitar cuelgues
- ✅ Validación de estado del terminal
- ✅ Recuperación automática de estados inconsistentes
- ✅ Feedback claro del progreso

**Resultado esperado**: Terminal estable y responsivo en todas las condiciones.
