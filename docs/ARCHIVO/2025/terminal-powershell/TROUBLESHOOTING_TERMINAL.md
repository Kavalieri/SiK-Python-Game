# Troubleshooting Terminal - SiK Python Game

## 🚨 Problemas Identificados y Soluciones

### Problema Principal: Terminal "Colgado" en VS Code PowerShell
**Síntomas:**
- Comandos que se ejecutan pero no devuelven control al terminal
- Agent esperando respuesta indefinidamente
- Necesidad de presionar "Enter" manualmente para continuar
- Scripts que se "cuelgan" en ciertos comandos

**Causas Identificadas:**
1. **Estado inconsistente** del terminal tras cancelaciones manuales
2. **Comandos largos** que timeout sin notificación clara
3. **Pipe buffers** que no se vacían correctamente
4. **Job processes** que no terminan limpiamente

## 🛠️ Soluciones Implementadas

### 1. Script Terminal-Safe Commit
**Archivo:** `scripts/terminal_safe_commit.ps1`

**Características:**
- ✅ Timeouts automáticos para todos los comandos
- ✅ Validación de estado del terminal antes de ejecutar
- ✅ Recuperación automática de estados inconsistentes
- ✅ Feedback claro del progreso en cada fase
- ✅ Manejo de errores robusto

**Uso:**
```powershell
# Commit básico
.\scripts\terminal_safe_commit.ps1 "fix: resolver problema de terminal"

# Commit con tipo y scope
.\scripts\terminal_safe_commit.ps1 "resolver timeout terminal" -Type "fix" -Scope "scripts"

# Commit con push automático
.\scripts\terminal_safe_commit.ps1 "nueva funcionalidad" -Type "feat" -Push
```

### 2. Script de Reset de Terminal
**Archivo:** `scripts/reset_terminal_state.ps1`

**Función:** Limpia estados inconsistentes del terminal

**Uso:**
```powershell
# Reset básico
.\scripts\reset_terminal_state.ps1

# Reset con diagnóstico completo
.\scripts\reset_terminal_state.ps1 -Verbose
```

### 3. Script de Test de Responsividad
**Archivo:** `scripts/test_terminal_responsive.ps1`

**Función:** Verifica que todas las herramientas respondan correctamente

**Uso:**
```powershell
.\scripts\test_terminal_responsive.ps1
```

## 📋 Protocolo de Uso Recomendado

### Antes de Cualquier Operación Importante:
1. **Verificar responsividad:**
   ```powershell
   .\scripts\test_terminal_responsive.ps1
   ```

2. **Si hay problemas, resetear:**
   ```powershell
   .\scripts\reset_terminal_state.ps1
   ```

3. **Usar scripts terminal-safe:**
   ```powershell
   .\scripts\terminal_safe_commit.ps1 "mensaje"
   ```

### Para Commits Diarios:
**USAR SIEMPRE:**
```powershell
.\scripts\terminal_safe_commit.ps1 "descripción del cambio"
```

**NO USAR:**
```powershell
# EVITAR - puede causar timeouts
poetry run pre-commit run --all-files
git add .
git commit -m "mensaje"
```

### Si el Terminal se "Cuelga":
1. **NO cancelar manualmente** (Ctrl+C)
2. **Esperar timeout automático** (30-45 segundos)
3. **Ejecutar reset:**
   ```powershell
   .\scripts\reset_terminal_state.ps1 -Verbose
   ```
4. **Verificar estado:**
   ```powershell
   .\scripts\test_terminal_responsive.ps1
   ```

## 🔧 Funciones de Timeout Integradas

### Invoke-CommandWithTimeout
```powershell
function Invoke-CommandWithTimeout {
    param(
        [string]$Command,
        [int]$TimeoutSeconds = 30,
        [string]$Description = "Comando"
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
        # TIMEOUT AUTOMÁTICO
        Stop-Job $job
        Remove-Job $job
        return $null
    }
}
```

### Test-TerminalResponsive
```powershell
function Test-TerminalResponsive {
    $start = Get-Date
    try {
        Get-Date | Out-Null
        $end = Get-Date
        $duration = ($end - $start).TotalMilliseconds

        return ($duration -lt 1000)
    } catch {
        return $false
    }
}
```

## 📊 Timeouts Configurados

| Comando | Timeout | Justificación |
|---------|---------|---------------|
| `poetry --version` | 5s | Comando simple |
| `git --version` | 5s | Comando simple |
| `git add .` | 15s | Puede ser lento con muchos archivos |
| `git commit` | 15s | Generalmente rápido |
| `git push` | 30s | Depende de red |
| `pre-commit run --all-files` | 45s | Puede ser muy lento |

## 🚨 Señales de Alerta

### Terminal Necesita Reset:
- ⏰ Comandos simples toman >1 segundo
- 🔄 Get-Date tarda en responder
- 📝 Variables no se asignan correctamente
- 🛑 Scripts se detienen sin error

### Terminal Necesita Reinicio Completo:
- ❌ Reset script falla
- 🔴 Test responsive falla consistentemente
- 💥 Errores de "access denied" o "process in use"

## 💡 Mejores Prácticas

### DO (Hacer):
- ✅ Usar scripts terminal-safe para todas las operaciones
- ✅ Verificar responsividad antes de operaciones largas
- ✅ Esperar timeouts automáticos
- ✅ Resetear estado tras problemas

### DON'T (No Hacer):
- ❌ Cancelar comandos manualmente (Ctrl+C)
- ❌ Ejecutar `pre-commit run --all-files` directamente
- ❌ Ignorar warnings de terminal lento
- ❌ Usar múltiples comandos en secuencia sin validación

## 🔄 Procedimiento de Escalación

### Nivel 1: Reset Automático
```powershell
.\scripts\reset_terminal_state.ps1
```

### Nivel 2: Reset con Diagnóstico
```powershell
.\scripts\reset_terminal_state.ps1 -Verbose
```

### Nivel 3: Reinicio de Terminal
1. Cerrar terminal actual en VS Code
2. Abrir nuevo terminal PowerShell
3. Verificar con `.\scripts\test_terminal_responsive.ps1`

### Nivel 4: Reinicio de VS Code
1. Cerrar VS Code completamente
2. Reabrir proyecto
3. Verificar funcionamiento con scripts de test

## 📈 Monitoreo y Métricas

### Indicadores de Salud del Terminal:
- **Tiempo de respuesta Get-Date:** <500ms (bueno), <1000ms (aceptable), >1000ms (problema)
- **Tasa de éxito de timeouts:** >95% (bueno), >90% (aceptable), <90% (problema)
- **Frecuencia de resets necesarios:** <1/día (bueno), <3/día (aceptable), >3/día (problema)

---

**Resumen:** Con estos scripts y procedimientos, el terminal debe mantenerse estable y responsivo en todas las condiciones de uso del proyecto.
