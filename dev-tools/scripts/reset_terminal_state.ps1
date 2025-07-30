# Reset Terminal State Script
# Limpia el estado inconsistente del terminal en VS Code PowerShell

param([switch]$Verbose)

$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"

Write-Host "🔄 Terminal State Reset" -ForegroundColor $ColorInfo
Write-Host "📅 $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor $ColorInfo

if ($Verbose) {
    Write-Host "🔍 Diagnóstico previo..." -ForegroundColor $ColorInfo

    # Test de responsividad
    $start = Get-Date
    try {
        Get-Date | Out-Null
        $end = Get-Date
        $duration = ($end - $start).TotalMilliseconds
        Write-Host "⏱️  Tiempo de respuesta: ${duration}ms" -ForegroundColor $ColorInfo
    } catch {
        Write-Host "❌ Terminal no responde" -ForegroundColor $ColorWarning
    }
}

# Secuencia de limpieza
Write-Host "🧹 Ejecutando secuencia de limpieza..." -ForegroundColor $ColorInfo

# 1. Comando simple para verificar respuesta
Get-Date | Out-Null

# 2. Limpiar variables de entorno temporal
if ($Verbose) {
    Write-Host "   📝 Limpiando variables temporales..." -ForegroundColor $ColorInfo
}
$env:TEMP_VAR = $null

# 3. Forzar garbage collection
if ($Verbose) {
    Write-Host "   🗑️  Garbage collection..." -ForegroundColor $ColorInfo
}
[System.GC]::Collect()

# 4. Sleep breve para permitir reset
Start-Sleep -Milliseconds 200

# 5. Test final
Write-Host "✅ Verificando estado final..." -ForegroundColor $ColorInfo
$finalStart = Get-Date
try {
    Get-Date | Out-Null  # Test simple sin asignación
    $finalEnd = Get-Date
    $finalDuration = ($finalEnd - $finalStart).TotalMilliseconds

    if ($finalDuration -lt 500) {
        Write-Host "✅ Terminal responsivo (${finalDuration}ms)" -ForegroundColor $ColorSuccess
        Write-Host "📊 Reset completado exitosamente" -ForegroundColor $ColorSuccess
        exit 0
    } else {
        Write-Host "⚠️  Terminal lento (${finalDuration}ms)" -ForegroundColor $ColorWarning
        Write-Host "💡 Puede requerir reinicio manual del terminal" -ForegroundColor $ColorWarning
        exit 1
    }
} catch {
    Write-Host "❌ Terminal aún no responsivo" -ForegroundColor $ColorWarning
    Write-Host "💡 Solución: Cerrar y reabrir terminal" -ForegroundColor $ColorWarning
    exit 1
}
