# VERSION SIMPLE Y FUNCIONAL
param([switch]$TestOnly)

Write-Host "=== METODO URI SIMPLE ===" -ForegroundColor Yellow

$before = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if (-not $before) {
    Write-Host "[ERROR] VS Code no ejecutandose" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] VS Code: $($before.MainWindowTitle)" -ForegroundColor Green

if ($TestOnly) {
    Write-Host "[TEST] Start-Process vscode://command/workbench.action.closeUnmodifiedEditors" -ForegroundColor White
    exit 0
}

Write-Host "[EJECUTANDO] URI method..." -ForegroundColor Yellow
Start-Process "vscode://command/workbench.action.closeUnmodifiedEditors"
Start-Sleep -Seconds 3

$after = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if ($after) {
    Write-Host "[ANTES] $($before.MainWindowTitle)" -ForegroundColor Gray
    Write-Host "[DESPUES] $($after.MainWindowTitle)" -ForegroundColor Gray

    if ($before.MainWindowTitle -ne $after.MainWindowTitle) {
        Write-Host "[SUCCESS] Pestanas cerradas" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Sin cambios visibles" -ForegroundColor Yellow
    }
}

Write-Host "[DONE] Verificar VS Code manualmente" -ForegroundColor Cyan
