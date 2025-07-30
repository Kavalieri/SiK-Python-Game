# Script de prueba para cerrar pestañas de VS Code
# Uso: .\scripts\test_vscode_tabs.ps1

# Path especifico de VS Code (NO Cursor)
$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"

if (-not (Test-Path $VSCodePath)) {
    $VSCodePath = "code"  # Fallback al PATH
}

Write-Host "[TEST] Probando cierre de pestanas de VS Code..." -ForegroundColor Cyan

try {
    # Verificar si VS Code está ejecutándose
    $vscodeProcess = Get-Process "Code" -ErrorAction SilentlyContinue
    if (-not $vscodeProcess) {
        Write-Host "[WARN] VS Code no esta ejecutandose" -ForegroundColor Yellow
        Write-Host "[INFO] Inicia VS Code y abre algunas pestanas, luego ejecuta este script" -ForegroundColor Cyan
        exit 1
    }

    Write-Host "[INFO] VS Code detectado (PID: $($vscodeProcess.Id))" -ForegroundColor Green

    # Intentar diferentes métodos de cierre de pestañas
    Write-Host "`n[TEST 1] Cerrando pestanas no modificadas..." -ForegroundColor Cyan
    & $VSCodePath --command "workbench.action.closeUnmodifiedEditors" 2>$null
    Start-Sleep -Seconds 2

    Write-Host "[TEST 2] Reorganizando editores..." -ForegroundColor Cyan
    & $VSCodePath --command "workbench.action.evenEditorWidths" 2>$null
    Start-Sleep -Seconds 1

    # Mostrar información de pestañas activas (si es posible)
    Write-Host "`n[INFO] Si las pestanas no se cerraron, prueba manualmente:" -ForegroundColor Yellow
    Write-Host "  1. Ctrl+K U (cerrar no modificadas)" -ForegroundColor White
    Write-Host "  2. Ctrl+K Ctrl+W (cerrar todas)" -ForegroundColor White
    Write-Host "  3. Ctrl+W (cerrar activa)" -ForegroundColor White

    Write-Host "`n[SUCCESS] Test completado" -ForegroundColor Green

} catch {
    Write-Host "[ERROR] Error durante el test: $_" -ForegroundColor Red
}

Write-Host "`n[INFO] Presiona Enter para continuar..." -ForegroundColor Cyan
Read-Host
