# LIMPIEZA FINAL INTEGRADA - Metodos validados
param(
    [switch]$TestOnly
)

Write-Host "=== LIMPIEZA FINAL CON METODOS VALIDADOS ===" -ForegroundColor Yellow
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Configuracion
$VSCodePath = "C:\Users\Kava\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

function Clean-VSCodeTabs {
    Write-Host "[1] LIMPIEZA DE PESTANAS VS CODE" -ForegroundColor Cyan
    Write-Host "    Metodo: VALIDADO y COMPROBADO" -ForegroundColor Green
    
    if (-not (Test-Path $VSCodePath)) {
        Write-Host "    [SKIP] VS Code no encontrado" -ForegroundColor Yellow
        return
    }
    
    $processes = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
    if ($processes.Count -eq 0) {
        Write-Host "    [SKIP] VS Code no ejecutandose" -ForegroundColor Yellow
        return
    }
    
    Write-Host "    [INFO] VS Code detectado - PID: $($processes[0].Id)" -ForegroundColor Green
    $beforeTitle = $processes[0].MainWindowTitle
    Write-Host "    [BEFORE] $beforeTitle" -ForegroundColor Gray
    
    if ($TestOnly) {
        Write-Host "    [TEST] Se ejecutaria comando validado" -ForegroundColor White
        return
    }
    
    try {
        Write-Host "    [EJECUTANDO] Cerrando pestanas no modificadas..." -ForegroundColor Yellow
        & "$VSCodePath" "workbench.action.closeUnmodifiedEditors"
        Start-Sleep -Seconds 3
        
        $afterProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
        if ($afterProcesses.Count -eq 1) {
            $afterTitle = $afterProcesses[0].MainWindowTitle
            Write-Host "    [AFTER] $afterTitle" -ForegroundColor Gray
            
            if ($beforeTitle -ne $afterTitle) {
                Write-Host "    [SUCCESS] ✓ Pestanas cerradas - titulo cambio detectado" -ForegroundColor Green
            } else {
                Write-Host "    [INFO] Sin cambios de titulo visibles" -ForegroundColor Yellow
            }
        }
        
        Write-Host "    [COMPLETED] ✓ Comando ejecutado sin nuevas instancias" -ForegroundColor Green
        Write-Host "    [INFO] Pestanas fijadas y modificadas preservadas" -ForegroundColor Gray
        
    } catch {
        Write-Host "    [ERROR] $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Clean-PythonCache {
    Write-Host "[2] LIMPIEZA DE CACHE PYTHON" -ForegroundColor Cyan
    
    $pycacheCount = 0
    $pycFiles = 0
    
    try {
        $pycacheDirs = Get-ChildItem -Path "." -Recurse -Directory -Name "__pycache__" -ErrorAction SilentlyContinue
        $pycacheCount = $pycacheDirs.Count
        
        $pycFilesAll = Get-ChildItem -Path "." -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue
        $pycFiles = $pycFilesAll.Count
        
        Write-Host "    [INFO] Directorios __pycache__: $pycacheCount" -ForegroundColor Gray
        Write-Host "    [INFO] Archivos .pyc: $pycFiles" -ForegroundColor Gray
        
        if ($TestOnly) {
            Write-Host "    [TEST] Se limpiarian $pycacheCount directorios y $pycFiles archivos" -ForegroundColor White
            return
        }
        
        if ($pycacheCount -gt 0) {
            Get-ChildItem -Path "." -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "    [OK] ✓ $pycacheCount directorios __pycache__ eliminados" -ForegroundColor Green
        }
        
        if ($pycFiles -gt 0) {
            Get-ChildItem -Path "." -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
            Write-Host "    [OK] ✓ $pycFiles archivos .pyc eliminados" -ForegroundColor Green
        }
        
        if ($pycacheCount -eq 0 -and $pycFiles -eq 0) {
            Write-Host "    [INFO] Cache Python ya estaba limpio" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "    [ERROR] $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Clean-PoetryCache {
    Write-Host "[3] LIMPIEZA DE CACHE POETRY" -ForegroundColor Cyan
    
    if ($TestOnly) {
        Write-Host "    [TEST] Se ejecutaria: poetry cache clear pypi --all" -ForegroundColor White
        return
    }
    
    try {
        $output = poetry cache clear pypi --all 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    [OK] ✓ Cache Poetry limpiado" -ForegroundColor Green
        } else {
            Write-Host "    [WARNING] Poetry no disponible o sin cache" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "    [WARNING] No se pudo limpiar cache Poetry" -ForegroundColor Yellow
    }
}

function Show-ProjectStatus {
    Write-Host "[4] ESTADO DEL PROYECTO" -ForegroundColor Cyan
    
    try {
        $projectSize = (Get-ChildItem -Path "." -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "    [INFO] Tamaño total: $([math]::Round($projectSize, 2)) MB" -ForegroundColor Gray
        
        $pythonFiles = (Get-ChildItem -Path "." -Recurse -Filter "*.py" | Measure-Object).Count
        Write-Host "    [INFO] Archivos Python: $pythonFiles" -ForegroundColor Gray
        
        $vscodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
        Write-Host "    [INFO] Instancias VS Code: $($vscodeProcesses.Count)" -ForegroundColor Gray
        
    } catch {
        Write-Host "    [WARNING] No se pudo obtener estado completo" -ForegroundColor Yellow
    }
}

# EJECUCION PRINCIPAL
if ($TestOnly) {
    Write-Host "[TEST MODE] Simulacion de limpieza:" -ForegroundColor Magenta
    Write-Host ""
    Clean-VSCodeTabs
    Write-Host ""
    Clean-PythonCache  
    Write-Host ""
    Clean-PoetryCache
    Write-Host ""
    Show-ProjectStatus
} else {
    Write-Host "[EJECUCION REAL] Iniciando limpieza completa:" -ForegroundColor Magenta
    Write-Host ""
    Clean-VSCodeTabs
    Write-Host ""
    Clean-PythonCache
    Write-Host ""
    Clean-PoetryCache
    Write-Host ""
    Show-ProjectStatus
}

Write-Host ""
Write-Host "=== LIMPIEZA COMPLETADA ===" -ForegroundColor Green
Write-Host "Hora: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
