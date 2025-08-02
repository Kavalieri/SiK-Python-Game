# PRUEBA FINAL: Script de limpieza integrado con metodo comprobado
param(
    [switch]$TestOnly
)

Write-Host "=== PRUEBA FINAL: LIMPIEZA INTEGRADA ===" -ForegroundColor Yellow
Write-Host ""

# Configuracion
$VSCodePath = "C:\Users\Kava\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

function Test-VSCodeTabClosure {
    Write-Host "[1] PESTANAS VS CODE:" -ForegroundColor Cyan

    if (-not (Test-Path $VSCodePath)) {
        Write-Host "  [SKIP] VS Code no encontrado" -ForegroundColor Yellow
        return
    }

    $processes = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
    if ($processes.Count -eq 0) {
        Write-Host "  [SKIP] VS Code no ejecutandose" -ForegroundColor Yellow
        return
    }

    Write-Host "  [INFO] VS Code detectado ($($processes.Count) instancia)" -ForegroundColor Green
    $beforeTitle = $processes[0].MainWindowTitle
    Write-Host "  [BEFORE] $beforeTitle" -ForegroundColor Gray

    if ($TestOnly) {
        Write-Host "  [TEST] Se ejecutaria: code workbench.action.closeUnmodifiedEditors" -ForegroundColor White
        return
    }

    try {
        & "$VSCodePath" "workbench.action.closeUnmodifiedEditors"
        Start-Sleep -Seconds 3

        $afterProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
        if ($afterProcesses.Count -eq 1) {
            $afterTitle = $afterProcesses[0].MainWindowTitle
            Write-Host "  [AFTER] $afterTitle" -ForegroundColor Gray

            if ($beforeTitle -ne $afterTitle) {
                Write-Host "  [SUCCESS] ✓ Pestanas cerradas (titulo cambio)" -ForegroundColor Green
            } else {
                Write-Host "  [INFO] Sin cambios de titulo" -ForegroundColor Yellow
            }
        }

        Write-Host "  [OK] Comando ejecutado correctamente" -ForegroundColor Green

    } catch {
        Write-Host "  [ERROR] Fallo: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Test-CacheCleanup {
    Write-Host "[2] LIMPIEZA DE CACHE:" -ForegroundColor Cyan

    # Python cache
    $pycacheFiles = Get-ChildItem -Path "." -Recurse -Directory -Name "__pycache__" -ErrorAction SilentlyContinue
    Write-Host "  [INFO] Directorios __pycache__: $($pycacheFiles.Count)" -ForegroundColor Gray

    if ($TestOnly) {
        Write-Host "  [TEST] Se limpiarian $($pycacheFiles.Count) directorios de cache Python" -ForegroundColor White
        return
    }

    # Limpiar Python cache
    if ($pycacheFiles.Count -gt 0) {
        Get-ChildItem -Path "." -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  [OK] Cache Python limpiado" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] No hay cache Python para limpiar" -ForegroundColor Yellow
    }
}

# Ejecutar pruebas
if ($TestOnly) {
    Write-Host "[TEST MODE] Mostrando que se ejecutaria:" -ForegroundColor Yellow
    Write-Host ""
    Test-VSCodeTabClosure
    Write-Host ""
    Test-CacheCleanup
} else {
    Write-Host "[EJECUTANDO] Limpieza real:" -ForegroundColor Yellow
    Write-Host ""
    Test-VSCodeTabClosure
    Write-Host ""
    Test-CacheCleanup
}

Write-Host ""
Write-Host "[COMPLETED] Prueba final completada" -ForegroundColor Green
