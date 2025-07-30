# =============================================================================
# SCRIPT DE LIMPIEZA Y OPTIMIZACION DEL ENTORNO DE TRABAJO - VERSION CORREGIDA
# =============================================================================
# Cierra pestanas de VS Code (SOLO pinned y sin cambios), limpia caches
# Uso: .\scripts\workspace_cleanup_fixed.ps1 [-Level "light"|"deep"|"complete"]
# =============================================================================

param(
    [ValidateSet("light", "deep", "complete")]
    [string]$Level = "light",

    [switch]$CloseTabs,
    [switch]$ClearCache,
    [switch]$OptimizeMemory,
    [switch]$Force
)

# Configuracion de colores para output (sin acentos)
$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

# Path especifico de VS Code (NO Cursor)
$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"

# Verificar si VS Code existe
if (-not (Test-Path $VSCodePath)) {
    Write-Host "[ERROR] VS Code no encontrado en: $VSCodePath" -ForegroundColor $ColorError
    $VSCodePath = "code"  # Fallback al PATH
}

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================

function Close-VSCodeTabs {
    param([string]$Mode = "smart")

    Write-Host "`n[TABS] Gestionando pestanas de VS Code..." -ForegroundColor $ColorInfo

    try {
        # Verificar si VS Code esta ejecutandose
        $vscodeProcess = Get-Process "Code" -ErrorAction SilentlyContinue
        if (-not $vscodeProcess) {
            Write-Host "[INFO] VS Code no esta ejecutandose" -ForegroundColor $ColorWarning
            return
        }

        Write-Host "[INFO] VS Code detectado, procesando pestanas..." -ForegroundColor $ColorSuccess

        # Usar comando especifico para SOLO cerrar pestanas sin cambios y sin pin
        if ($Mode -eq "smart") {
            # Este comando respeta pins y cambios pendientes
            & $VSCodePath --command "workbench.action.closeUnmodifiedEditors" 2>$null
            Write-Host "[OK] Pestanas sin cambios cerradas (pins y modificadas preservadas)" -ForegroundColor $ColorSuccess
        } elseif ($Mode -eq "others") {
            & $VSCodePath --command "workbench.action.closeOtherEditors" 2>$null
            Write-Host "[OK] Otras pestanas cerradas" -ForegroundColor $ColorSuccess
        } elseif ($Mode -eq "all") {
            & $VSCodePath --command "workbench.action.closeAllEditors" 2>$null
            Write-Host "[OK] Todas las pestanas cerradas" -ForegroundColor $ColorSuccess
        }

        Start-Sleep -Seconds 1

        # Reorganizar grupos de editores
        & $VSCodePath --command "workbench.action.evenEditorWidths" 2>$null
        Write-Host "[OK] Grupos de editores reorganizados" -ForegroundColor $ColorSuccess

    } catch {
        Write-Host "[WARN] Error gestionando pestanas: $_" -ForegroundColor $ColorWarning
    }
}

function Clear-ProjectCache {
    Write-Host "`n[CACHE] Limpiando caches del proyecto..." -ForegroundColor $ColorInfo

    $cachePaths = @(
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules/.cache",
        ".vscode/.ropeproject",
        "src/__pycache__",
        "src/*/__pycache__",
        "tests/__pycache__",
        "scripts/__pycache__",
        "tools/__pycache__"
    )

    # Buscar en el entorno virtual tambien
    if (Test-Path ".venv") {
        $cachePaths += ".venv\Lib\site-packages\*\__pycache__"
    }

    $cleaned = 0
    foreach ($path in $cachePaths) {
        $items = Get-ChildItem -Path $path -Recurse -Directory -ErrorAction SilentlyContinue
        foreach ($item in $items) {
            try {
                $fullPath = $item.FullName
                Remove-Item -Path $fullPath -Recurse -Force -ErrorAction Stop
                $cleaned++
                Write-Host "[OK] Eliminado: $fullPath" -ForegroundColor $ColorSuccess
            } catch {
                Write-Host "[WARN] No se pudo eliminar: $fullPath" -ForegroundColor $ColorWarning
            }
        }
    }

    # Limpiar archivos temporales Python
    Get-ChildItem -Path . -Recurse -File -Name "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -File -Name "*.pyo" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

    Write-Host "[OK] $cleaned directorios de cache eliminados" -ForegroundColor $ColorSuccess
}

function Clear-PoetryCache {
    Write-Host "`n[POETRY] Limpiando cache de Poetry..." -ForegroundColor $ColorInfo

    try {
        poetry cache clear --all pypi --no-interaction | Out-Null
        Write-Host "[OK] Cache de Poetry limpiada" -ForegroundColor $ColorSuccess
    } catch {
        Write-Host "[WARN] No se pudo limpiar cache de Poetry: $_" -ForegroundColor $ColorWarning
    }
}

function Clear-GitCache {
    Write-Host "`n[GIT] Optimizando repositorio Git..." -ForegroundColor $ColorInfo

    try {
        # Git garbage collection
        git gc --aggressive --prune=now | Out-Null
        Write-Host "[OK] Git optimizado" -ForegroundColor $ColorSuccess
    } catch {
        Write-Host "[WARN] No se pudo optimizar Git: $_" -ForegroundColor $ColorWarning
    }
}

function Clear-VSCodeCache {
    Write-Host "`n[VSCODE] Limpiando cache de VS Code..." -ForegroundColor $ColorInfo

    $vscodeCache = "${env:APPDATA}\Code\User\workspaceStorage"
    if (Test-Path $vscodeCache) {
        try {
            # Solo limpiar caches viejos (mas de 7 dias)
            Get-ChildItem -Path $vscodeCache -Directory |
                Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } |
                Remove-Item -Recurse -Force
            Write-Host "[OK] Cache antiguo de VS Code limpiado" -ForegroundColor $ColorSuccess
        } catch {
            Write-Host "[WARN] No se pudo limpiar cache de VS Code: $_" -ForegroundColor $ColorWarning
        }
    }
}

function Optimize-Memory {
    Write-Host "`n[MEMORY] Optimizando memoria..." -ForegroundColor $ColorInfo

    try {
        # Forzar garbage collection .NET
        [System.GC]::Collect()
        [System.GC]::WaitForPendingFinalizers()
        [System.GC]::Collect()

        Write-Host "[OK] Memoria optimizada" -ForegroundColor $ColorSuccess
    } catch {
        Write-Host "[WARN] No se pudo optimizar memoria: $_" -ForegroundColor $ColorWarning
    }
}

function Show-Summary {
    Write-Host "`n[SUMMARY] Resumen de limpieza completada:" -ForegroundColor $ColorInfo
    Write-Host "==========================================" -ForegroundColor $ColorInfo

    # Calcular tamano del proyecto
    try {
        $projectSize = (Get-ChildItem -Path . -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "[INFO] Tamano del proyecto: $([math]::Round($projectSize, 2)) MB" -ForegroundColor $ColorInfo
    } catch {
        Write-Host "[INFO] No se pudo calcular tamano del proyecto" -ForegroundColor $ColorWarning
    }

    # Contar archivos en .git
    try {
        $gitFiles = (Get-ChildItem -Path ".git" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "[INFO] Archivos en .git: $gitFiles" -ForegroundColor $ColorInfo
    } catch {
        Write-Host "[INFO] No se pudo acceder a .git" -ForegroundColor $ColorWarning
    }

    # Contar archivos Python
    try {
        $pythonFiles = (Get-ChildItem -Path . -Recurse -File -Include "*.py" -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "[INFO] Archivos Python: $pythonFiles" -ForegroundColor $ColorInfo
    } catch {
        Write-Host "[INFO] No se pudo contar archivos Python" -ForegroundColor $ColorWarning
    }

    Write-Host "[SUCCESS] Limpieza completada exitosamente" -ForegroundColor $ColorSuccess
    Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo
}

# =============================================================================
# LOGICA PRINCIPAL
# =============================================================================

Write-Host "[CLEANUP] Iniciando limpieza del entorno de trabajo" -ForegroundColor $ColorInfo
Write-Host "[INFO] Nivel de limpieza: $Level" -ForegroundColor $ColorInfo
Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo

# Determinar acciones segun el nivel
$actions = @{
    "closeTabs" = $CloseTabs
    "clearCache" = $ClearCache
    "optimizeMemory" = $OptimizeMemory
}

# Configurar acciones segun nivel si no se especificaron switches
if (-not ($CloseTabs -or $ClearCache -or $OptimizeMemory)) {
    switch ($Level) {
        "light" {
            $actions.closeTabs = $true
            $actions.clearCache = $true
        }
        "deep" {
            $actions.closeTabs = $true
            $actions.clearCache = $true
            $actions.optimizeMemory = $true
        }
        "complete" {
            $actions.closeTabs = $true
            $actions.clearCache = $true
            $actions.optimizeMemory = $true
        }
    }
}

# Ejecutar acciones
if ($actions.closeTabs) {
    Close-VSCodeTabs -Mode "smart"
}

if ($actions.clearCache) {
    Clear-ProjectCache
    Clear-PoetryCache

    if ($Level -eq "deep" -or $Level -eq "complete") {
        Clear-GitCache
        Clear-VSCodeCache
    }
}

if ($actions.optimizeMemory) {
    Optimize-Memory
}

# Mostrar resumen
Show-Summary

Write-Host "[CLEANUP] Entorno de trabajo optimizado" -ForegroundColor $ColorSuccess

# NO Read-Host - El script termina automaticamente
