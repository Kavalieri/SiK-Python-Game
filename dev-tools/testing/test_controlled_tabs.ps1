# Test controlado de cierre de pestanas - SIN abrir nuevas instancias
# Solo trabaja con la instancia existente de VS Code

param(
    [switch]$TestOnly = $false
)

Write-Host "=== TEST CONTROLADO DE PESTANAS ===" -ForegroundColor Yellow
Write-Host ""

# Path EXACTO de VS Code (evita Cursor)
$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"

Write-Host "[INFO] Usando VS Code en: $VSCodePath" -ForegroundColor Cyan
Write-Host "[INFO] Existe: $(Test-Path $VSCodePath)" -ForegroundColor Cyan

# Verificar instancia existente
$vscodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
if (-not $vscodeProcesses) {
    Write-Host "[ERROR] No hay instancia de VS Code con ventana activa" -ForegroundColor Red
    Write-Host "[INFO] Abre VS Code primero y ejecuta este script de nuevo" -ForegroundColor Yellow
    exit 1
}

Write-Host "[INFO] Instancia VS Code encontrada: PID $($vscodeProcesses[0].Id)" -ForegroundColor Green
Write-Host "[INFO] Ventana: '$($vscodeProcesses[0].MainWindowTitle)'" -ForegroundColor Green

Write-Host ""

if ($TestOnly) {
    Write-Host "[TEST-ONLY] Modo de prueba - NO se ejecutaran comandos" -ForegroundColor Magenta
    Write-Host "[SIMULACION] Se ejecutaria:" -ForegroundColor Cyan
    Write-Host "  & `"$VSCodePath`" --reuse-window --command workbench.action.closeUnmodifiedEditors" -ForegroundColor Gray
    Write-Host ""
    Write-Host "[INFO] Para ejecutar realmente, usa sin -TestOnly" -ForegroundColor Yellow
    exit 0
}

Write-Host "[ACCION] Cerrando pestanas SIN cambios (preserva PIN y modificadas)..." -ForegroundColor Cyan

try {
    # Usar --reuse-window para usar instancia existente
    $result = & $VSCodePath --reuse-window --command "workbench.action.closeUnmodifiedEditors" 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Comando ejecutado exitosamente" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Comando retorno codigo: $LASTEXITCODE" -ForegroundColor Yellow
        Write-Host "[DEBUG] Output: $result" -ForegroundColor Gray
    }

    Start-Sleep -Seconds 2

    Write-Host "[INFO] Verificando si se abrieron nuevas instancias..." -ForegroundColor Cyan
    $newProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }

    if ($newProcesses.Count -gt $vscodeProcesses.Count) {
        Write-Host "[PROBLEMA] Se abrio nueva instancia de VS Code!" -ForegroundColor Red
        Write-Host "[INFO] Instancias antes: $($vscodeProcesses.Count), ahora: $($newProcesses.Count)" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] NO se abrieron nuevas instancias" -ForegroundColor Green
    }

} catch {
    Write-Host "[ERROR] Error ejecutando comando: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "[INFO] Verifica manualmente si se cerraron pestanas sin cambios" -ForegroundColor Cyan
Write-Host "[INFO] Las pestanas con PIN deberian seguir abiertas" -ForegroundColor Cyan
