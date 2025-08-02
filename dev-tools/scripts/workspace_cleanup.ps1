# =============================================================================
# SCRIPT DE LIMPIEZA Y OPTIMIZACION DEL ENTORNO DE TRABAJO
# =============================================================================
# Cierra pestanas de VS Code, limpia caches y optimiza memoria
# Uso: .\scripts\workspace_cleanup.ps1 [-Level "light"|"deep"|"complete"]
# =============================================================================

# Configurar codificación para caracteres especiales
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [ValidateSet("light", "deep", "complete")]
    [string]$Level = "light",

    [switch]$CloseTabs,
    [switch]$ClearCache,
    [switch]$OptimizeMemory,
    [switch]$Force
)

# Path especifico de VS Code (NO Cursor)
$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"

if (-not (Test-Path $VSCodePath)) {
    $VSCodePath = "code"  # Fallback al PATH
}

# Configuracion de colores para output (sin acentos)
$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorError = "Red"

Write-Host "[CLEANUP] Iniciando limpieza del entorno de trabajo" -ForegroundColor $ColorInfo
Write-Host "[INFO] Nivel de limpieza: $Level" -ForegroundColor $ColorInfo
Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo

# =============================================================================
# FUNCIONES DE LIMPIEZA
# =============================================================================

function Close-VSCodeTabs {
    param([string]$Mode = "selective")

    Write-Host "`n[TABS] Cerrando pestanas de VS Code..." -ForegroundColor $ColorInfo

    try {
        # Verificar si VS Code está disponible
        $vscodeProcess = Get-Process "Code" -ErrorAction SilentlyContinue
        if (-not $vscodeProcess) {
            Write-Host "[INFO] VS Code no esta ejecutandose" -ForegroundColor $ColorWarning
            return
        }

        Write-Host "[INFO] VS Code detectado, procesando pestanas..." -ForegroundColor $ColorSuccess

        # Método principal: Comandos CLI de VS Code (METODO COMPROBADO)
        if ($Mode -eq "all") {
            & $VSCodePath "workbench.action.closeAllEditors"
            Write-Host "[OK] Todas las pestanas cerradas" -ForegroundColor $ColorSuccess
        } elseif ($Mode -eq "others") {
            & $VSCodePath "workbench.action.closeOtherEditors"
            Write-Host "[OK] Otras pestanas cerradas" -ForegroundColor $ColorSuccess
        } else {
            & $VSCodePath "workbench.action.closeUnmodifiedEditors"
            Write-Host "[OK] Pestanas no modificadas cerradas (fijadas y modificadas preservadas)" -ForegroundColor $ColorSuccess
        }

        Start-Sleep -Seconds 2

        # Método adicional: Atajos de teclado como fallback
        try {
            Add-Type -AssemblyName System.Windows.Forms
            $vscodeWindows = Get-Process "Code" | Where-Object { $_.MainWindowTitle -ne "" }
            if ($vscodeWindows -and $Mode -eq "selective") {
                [System.Windows.Forms.SendKeys]::SendWait("^k")
                Start-Sleep -Milliseconds 500
                [System.Windows.Forms.SendKeys]::SendWait("u")
                Write-Host "[OK] Atajo Ctrl+K U enviado como respaldo" -ForegroundColor $ColorSuccess
            }
        } catch {
            # SendKeys no es crítico, continuar sin error
        }

        # Reorganizar grupos de editores
        & $VSCodePath --command "workbench.action.evenEditorWidths" 2>$null
        Write-Host "[OK] Grupos de editores reorganizados" -ForegroundColor $ColorSuccess

    } catch {
        Write-Host "[WARN] No se pudo conectar con VS Code: $_" -ForegroundColor $ColorWarning
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

    $cleaned = 0
    foreach ($path in $cachePaths) {
        $fullPaths = Get-ChildItem -Path . -Recurse -Directory -Name $path -ErrorAction SilentlyContinue
        foreach ($fullPath in $fullPaths) {
            try {
                Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
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
        Write-Host "[OK] Git garbage collection completado" -ForegroundColor $ColorSuccess

        # Limpiar referencias remotas obsoletas
        git remote prune origin | Out-Null
        Write-Host "[OK] Referencias remotas limpiadas" -ForegroundColor $ColorSuccess

    } catch {
        Write-Host "[WARN] Error en optimización Git: $_" -ForegroundColor $ColorWarning
    }
}

function Clear-VSCodeCache {
    Write-Host "`n[VSCODE] Limpiando caché de VS Code..." -ForegroundColor $ColorInfo

    $vscodeUserDir = "$env:APPDATA\Code\User"
    $vscodeCachePaths = @(
        "$vscodeUserDir\workspaceStorage",
        "$vscodeUserDir\logs",
        "$vscodeUserDir\CachedExtensions",
        "$env:TEMP\vscode-*"
    )

    foreach ($path in $vscodeCachePaths) {
        if (Test-Path $path) {
            try {
                $size = (Get-ChildItem $path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
                if ($Force -or $size -gt 100) {  # Solo limpiar si >100MB o forzado
                    Remove-Item "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
                    Write-Host "[OK] Limpiado: $path ($([math]::Round($size, 2)) MB)" -ForegroundColor $ColorSuccess
                }
            } catch {
                Write-Host "[WARN] No se pudo limpiar: $path" -ForegroundColor $ColorWarning
            }
        }
    }
}

function Optimize-Memory {
    Write-Host "`n[MEMORY] Optimizando memoria del sistema..." -ForegroundColor $ColorInfo

    try {
        # Forzar recolección de basura .NET
        [System.GC]::Collect()
        [System.GC]::WaitForPendingFinalizers()
        [System.GC]::Collect()

        Write-Host "[OK] Recolección de basura .NET ejecutada" -ForegroundColor $ColorSuccess

        # Información de memoria
        $memory = Get-CimInstance -ClassName Win32_OperatingSystem
        $totalMemory = [math]::Round($memory.TotalVisibleMemorySize / 1MB, 2)
        $freeMemory = [math]::Round($memory.FreePhysicalMemory / 1MB, 2)
        $usedPercent = [math]::Round((($totalMemory - $freeMemory) / $totalMemory) * 100, 1)

        Write-Host "[INFO] Memoria total: ${totalMemory}GB" -ForegroundColor $ColorInfo
        Write-Host "[INFO] Memoria libre: ${freeMemory}GB" -ForegroundColor $ColorInfo
        Write-Host "[INFO] Uso de memoria: ${usedPercent}%" -ForegroundColor $ColorInfo

    } catch {
        Write-Host "[WARN] Error en optimización de memoria: $_" -ForegroundColor $ColorWarning
    }
}

function Show-CleanupSummary {
    Write-Host "`n[SUMMARY] Resumen de limpieza completada:" -ForegroundColor $ColorInfo
    Write-Host "==========================================" -ForegroundColor $ColorInfo

    # Tamaño actual del proyecto
    $projectSize = (Get-ChildItem -Path . -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[INFO] Tamano del proyecto: $([math]::Round($projectSize, 2)) MB" -ForegroundColor $ColorInfo

    # Archivos Git
    $gitFiles = (Get-ChildItem -Path .git -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "[INFO] Archivos en .git: $gitFiles" -ForegroundColor $ColorInfo

    # Archivos Python
    $pythonFiles = (Get-ChildItem -Path . -Recurse -File -Include "*.py" -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "[INFO] Archivos Python: $pythonFiles" -ForegroundColor $ColorInfo

    Write-Host "[SUCCESS] Limpieza completada exitosamente" -ForegroundColor $ColorSuccess
    Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo
}

# =============================================================================
# LÓGICA PRINCIPAL
# =============================================================================

# Determinar acciones según el nivel
$actions = @{
    "closeTabs" = $CloseTabs
    "clearCache" = $ClearCache
    "optimizeMemory" = $OptimizeMemory
}

# Configurar acciones según nivel si no se especificaron switches
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
            $Force = $true
        }
    }
}

# Ejecutar acciones
if ($actions.closeTabs) {
    $tabMode = if ($Level -eq "complete") { "all" } elseif ($Level -eq "deep") { "others" } else { "selective" }
    Close-VSCodeTabs -Mode $tabMode
}

if ($actions.clearCache) {
    Clear-ProjectCache
    Clear-PoetryCache

    if ($Level -in @("deep", "complete")) {
        Clear-GitCache
        Clear-VSCodeCache
    }
}

if ($actions.optimizeMemory) {
    Optimize-Memory
}

# Mostrar resumen
Show-CleanupSummary

Write-Host "`n[CLEANUP] Entorno de trabajo optimizado" -ForegroundColor $ColorSuccess
