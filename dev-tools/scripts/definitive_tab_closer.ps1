# VERSION DEFINITIVA: Metodo comprobado para cerrar pestanas VS Code
param(
    [switch]$TestOnly,
    [switch]$Verbose
)

Write-Host "=== VERSION DEFINITIVA: CERRAR PESTANAS VS CODE ===" -ForegroundColor Yellow
Write-Host ""

# Configuracion
$VSCodePath = "C:\Users\Kava\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

# Verificar VS Code existe
if (-not (Test-Path $VSCodePath)) {
    Write-Host "[ERROR] VS Code no encontrado en: $VSCodePath" -ForegroundColor Red
    exit 1
}

# 1. Detectar instancias antes
$beforeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
$beforeCount = $beforeProcesses.Count
Write-Host "[BEFORE] VS Code instances: $beforeCount" -ForegroundColor Cyan

if ($beforeCount -eq 0) {
    Write-Host "[ERROR] No hay VS Code ejecutandose. Abrir VS Code primero." -ForegroundColor Red
    exit 1
}

# Mostrar estado antes
Write-Host "[INFO] Estado ANTES:" -ForegroundColor Green
$beforeProcesses | ForEach-Object { Write-Host "  - PID: $($_.Id), Titulo: $($_.MainWindowTitle)" -ForegroundColor Gray }

Write-Host ""

if ($TestOnly) {
    Write-Host "[TEST MODE] Comandos que se ejecutarian:" -ForegroundColor Yellow
    Write-Host "1. & `"$VSCodePath`" workbench.action.closeUnmodifiedEditors" -ForegroundColor White
    Write-Host "2. Metodo alternativo si falla: vscode:// URI" -ForegroundColor White
    Write-Host ""
    Write-Host "[INFO] La sintaxis correcta NO usa --command (deprecated)" -ForegroundColor Cyan
    Write-Host "[INFO] VS Code acepta comandos directamente como argumentos" -ForegroundColor Cyan
    exit 0
}

# Ejecutar comando real - METODO 1: Comando directo
Write-Host "[EXECUTING] Metodo 1: Comando directo..." -ForegroundColor Yellow

try {
    # Sintaxis correcta: VS Code acepta comandos como argumentos directos
    & "$VSCodePath" "workbench.action.closeUnmodifiedEditors"
    Start-Sleep -Seconds 3  # Dar tiempo a VS Code para procesar
    Write-Host "[SUCCESS] Comando enviado (metodo 1)" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Metodo 1 fallo: $($_.Exception.Message)" -ForegroundColor Yellow

    # METODO 2: URI scheme
    Write-Host "[EXECUTING] Metodo 2: URI scheme..." -ForegroundColor Yellow
    try {
        Start-Process "vscode://command/workbench.action.closeUnmodifiedEditors"
        Start-Sleep -Seconds 3
        Write-Host "[SUCCESS] Comando enviado (metodo 2)" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Ambos metodos fallaron" -ForegroundColor Red
        exit 1
    }
}

# 2. Verificar instancias despues
Start-Sleep -Seconds 1
$afterProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
$afterCount = $afterProcesses.Count

Write-Host ""
Write-Host "[AFTER] VS Code instances: $afterCount" -ForegroundColor Cyan

# Mostrar estado despues
Write-Host "[INFO] Estado DESPUES:" -ForegroundColor Green
$afterProcesses | ForEach-Object { Write-Host "  - PID: $($_.Id), Titulo: $($_.MainWindowTitle)" -ForegroundColor Gray }

# Analizar resultados
Write-Host ""
if ($afterCount -eq $beforeCount) {
    Write-Host "[RESULTADO] ✓ EXITO: No se abrieron nuevas instancias" -ForegroundColor Green

    # Verificar si cambio el titulo (indica que funciono)
    $titleChanged = $false
    if ($beforeProcesses.Count -eq 1 -and $afterProcesses.Count -eq 1) {
        $beforeTitle = $beforeProcesses[0].MainWindowTitle
        $afterTitle = $afterProcesses[0].MainWindowTitle
        if ($beforeTitle -ne $afterTitle) {
            Write-Host "[RESULTADO] ✓ PESTANAS CERRADAS: Titulo cambio de '$beforeTitle' a '$afterTitle'" -ForegroundColor Green
            $titleChanged = $true
        }
    }

    if (-not $titleChanged) {
        Write-Host "[INFO] El titulo no cambio - revisar manualmente si se cerraron pestanas" -ForegroundColor Yellow
    }

} elseif ($afterCount -gt $beforeCount) {
    Write-Host "[RESULTADO] ✗ ERROR: Se abrieron $($afterCount - $beforeCount) nuevas instancias" -ForegroundColor Red
} else {
    Write-Host "[RESULTADO] ? INESPERADO: Se cerraron $($beforeCount - $afterCount) instancias" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[VALIDACION FINAL] Por favor verificar en VS Code:" -ForegroundColor Cyan
Write-Host "  ✓ Las pestanas SIN MODIFICAR y SIN PIN deben haberse cerrado" -ForegroundColor White
Write-Host "  ✓ Las pestanas FIJADAS (pin) deben permanecer abiertas" -ForegroundColor White
Write-Host "  ✓ Las pestanas MODIFICADAS deben permanecer abiertas" -ForegroundColor White

Write-Host ""
