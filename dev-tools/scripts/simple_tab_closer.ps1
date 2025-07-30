# VALIDACION DEFINITIVA: Cerrar pestanas VS Code correctamente
param([switch]$TestOnly)

Write-Host "=== VALIDACION DEFINITIVA ===" -ForegroundColor Yellow

# Configuracion
$VSCodePath = "C:\Users\Kava\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

# Verificar VS Code
if (-not (Test-Path $VSCodePath)) {
    Write-Host "[ERROR] VS Code no encontrado" -ForegroundColor Red
    exit 1
}

# Contar instancias antes
$before = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
Write-Host "[BEFORE] Instancias: $($before.Count)" -ForegroundColor Cyan
if ($before.Count -gt 0) {
    Write-Host "  Titulo: $($before[0].MainWindowTitle)" -ForegroundColor Gray
}

if ($TestOnly) {
    Write-Host "[TEST] Comando: code workbench.action.closeUnmodifiedEditors" -ForegroundColor White
    exit 0
}

# EJECUTAR comando real
Write-Host "[EJECUTANDO] Cerrando pestanas no modificadas..." -ForegroundColor Yellow

try {
    & "$VSCodePath" "workbench.action.closeUnmodifiedEditors"
    Start-Sleep -Seconds 3
    Write-Host "[SUCCESS] Comando ejecutado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Fallo: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Contar instancias despues
$after = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
Write-Host "[AFTER] Instancias: $($after.Count)" -ForegroundColor Cyan
if ($after.Count -gt 0) {
    Write-Host "  Titulo: $($after[0].MainWindowTitle)" -ForegroundColor Gray
}

# Resultado
if ($after.Count -eq $before.Count) {
    Write-Host "[RESULTADO] OK - No nuevas instancias" -ForegroundColor Green

    if ($before.Count -eq 1 -and $after.Count -eq 1) {
        $titleBefore = $before[0].MainWindowTitle
        $titleAfter = $after[0].MainWindowTitle
        if ($titleBefore -ne $titleAfter) {
            Write-Host "[VALIDADO] Pestanas cerradas - titulo cambio" -ForegroundColor Green
        } else {
            Write-Host "[INFO] Titulo sin cambios - verificar manualmente" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "[ERROR] Cambio inesperado de instancias" -ForegroundColor Red
}

Write-Host ""
Write-Host "[VERIFICAR] En VS Code:" -ForegroundColor Cyan
Write-Host "  - Pestanas sin modificar y sin pin: CERRADAS" -ForegroundColor White
Write-Host "  - Pestanas fijadas: ABIERTAS" -ForegroundColor White
Write-Host "  - Pestanas modificadas: ABIERTAS" -ForegroundColor White
