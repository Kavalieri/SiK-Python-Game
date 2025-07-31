# Script de Limpieza Completa del Proyecto
# Basado en sesión del 31 de Julio, 2025
# Incluye todas las operaciones de limpieza identificadas

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("light", "deep", "complete", "shutdown")]
    [string]$Level = "light",

    [Parameter(Mandatory=$false)]
    [switch]$Force,

    [Parameter(Mandatory=$false)]
    [switch]$PreShutdown
)

# Configuración
$LogFile = "logs/cleanup_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Función de logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Level] $Message"
    Write-Host $LogMessage -ForegroundColor $(
        switch($Level) {
            "INFO" { "White" }
            "WARN" { "Yellow" }
            "ERROR" { "Red" }
            "SUCCESS" { "Green" }
            default { "White" }
        }
    )
    # Crear directorio de logs si no existe
    $LogDir = Split-Path $LogFile -Parent
    if (!(Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    }
    Add-Content -Path $LogFile -Value $LogMessage
}

# Función para verificar VS Code
function Test-VSCodeRunning {
    $VSCodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue
    return ($VSCodeProcesses.Count -gt 0)
}

# Función de limpieza de cachés Python
function Clear-PythonCaches {
    Write-Log "Iniciando limpieza de cachés Python..." "INFO"

    $CacheDirs = @(
        "src\__pycache__",
        "src\*\__pycache__",
        "tests\__pycache__",
        ".pytest_cache"
    )

    foreach ($CacheDir in $CacheDirs) {
        if (Test-Path $CacheDir) {
            try {
                Remove-Item -Recurse -Force $CacheDir -ErrorAction SilentlyContinue
                Write-Log "Eliminado: $CacheDir" "SUCCESS"
            } catch {
                Write-Log "Error eliminando $CacheDir : $($_.Exception.Message)" "WARN"
            }
        }
    }

    # Buscar cachés adicionales recursivamente
    try {
        Get-ChildItem -Path "src" -Recurse -Name "__pycache__" -Directory -ErrorAction SilentlyContinue |
            ForEach-Object {
                $FullPath = Join-Path "src" $_
                Remove-Item -Recurse -Force $FullPath -ErrorAction SilentlyContinue
                Write-Log "Caché Python eliminado: $FullPath" "SUCCESS"
            }
    } catch {
        Write-Log "Error en búsqueda recursiva de cachés Python: $($_.Exception.Message)" "WARN"
    }
}

# Función de limpieza de herramientas de desarrollo
function Clear-DevToolCaches {
    Write-Log "Iniciando limpieza de cachés de herramientas..." "INFO"

    $ToolCaches = @(
        ".mypy_cache",
        ".ruff_cache",
        ".coverage",
        "htmlcov"
    )

    foreach ($Cache in $ToolCaches) {
        if (Test-Path $Cache) {
            try {
                Remove-Item -Recurse -Force $Cache -ErrorAction SilentlyContinue
                Write-Log "Eliminado: $Cache" "SUCCESS"
            } catch {
                Write-Log "Error eliminando $Cache : $($_.Exception.Message)" "WARN"
            }
        }
    }
}

# Función de limpieza de VS Code
function Clear-VSCodeCaches {
    Write-Log "Iniciando limpieza de cachés VS Code..." "INFO"

    $VSCodeCaches = @(
        ".vscode\workspaceStorage",
        ".vscode\logs"
    )

    foreach ($Cache in $VSCodeCaches) {
        if (Test-Path $Cache) {
            try {
                Remove-Item -Recurse -Force $Cache -ErrorAction SilentlyContinue
                Write-Log "Eliminado: $Cache" "SUCCESS"
            } catch {
                Write-Log "Error eliminando $Cache : $($_.Exception.Message)" "WARN"
            }
        }
    }
}

# Función de limpieza avanzada de logs
function Clear-ProjectLogs {
    param([string]$LogLevel = "light")

    Write-Log "Iniciando limpieza de logs del proyecto..." "INFO"

    if ($LogLevel -eq "complete") {
        # Limpiar logs antiguos (mantener los últimos 5)
        if (Test-Path "logs") {
            $LogFiles = Get-ChildItem "logs\*.log" | Sort-Object LastWriteTime -Descending
            if ($LogFiles.Count -gt 5) {
                $FilesToDelete = $LogFiles | Select-Object -Skip 5
                foreach ($File in $FilesToDelete) {
                    try {
                        Remove-Item $File.FullName -Force
                        Write-Log "Log antiguo eliminado: $($File.Name)" "SUCCESS"
                    } catch {
                        Write-Log "Error eliminando log $($File.Name): $($_.Exception.Message)" "WARN"
                    }
                }
            }
        }
    }
}

# Función de limpieza de VS Code con SendKeys
function Invoke-VSCodeCleanup {
    param([string]$CleanupLevel = "light")

    if (Test-VSCodeRunning) {
        Write-Log "VS Code detectado ejecutándose" "INFO"

        # Verificar si existe el script de SendKeys
        $SendKeysScript = ".\dev-tools\scripts\vscode_cleanup_sendkeys.ps1"
        if (Test-Path $SendKeysScript) {
            try {
                Write-Log "Ejecutando limpieza de VS Code con SendKeys..." "INFO"
                & $SendKeysScript -Level $CleanupLevel
                Write-Log "Limpieza de VS Code completada" "SUCCESS"
            } catch {
                Write-Log "Error ejecutando limpieza de VS Code: $($_.Exception.Message)" "ERROR"
            }
        } else {
            Write-Log "Script SendKeys no encontrado, omitiendo limpieza de pestañas" "WARN"
        }
    } else {
        Write-Log "VS Code no está ejecutándose" "INFO"
    }
}

# Función de limpieza de archivos temporales
function Clear-TempFiles {
    Write-Log "Iniciando limpieza de archivos temporales..." "INFO"

    $TempPatterns = @(
        "*.tmp",
        "*.temp",
        "*~",
        ".DS_Store",
        "Thumbs.db"
    )

    foreach ($Pattern in $TempPatterns) {
        try {
            Get-ChildItem -Path "." -Recurse -Name $Pattern -ErrorAction SilentlyContinue |
                ForEach-Object {
                    Remove-Item $_ -Force -ErrorAction SilentlyContinue
                    Write-Log "Archivo temporal eliminado: $_" "SUCCESS"
                }
        } catch {
            Write-Log "Error eliminando archivos temporales $Pattern : $($_.Exception.Message)" "WARN"
        }
    }
}

# Función de optimización Git
function Optimize-GitRepository {
    Write-Log "Iniciando optimización del repositorio Git..." "INFO"

    try {
        # Git garbage collection
        git gc --prune=now 2>$null
        Write-Log "Git garbage collection completado" "SUCCESS"

        # Limpiar logs de reflog antiguos
        git reflog expire --expire=30.days.ago --all 2>$null
        Write-Log "Reflogs antiguos limpiados" "SUCCESS"

    } catch {
        Write-Log "Error en optimización Git: $($_.Exception.Message)" "WARN"
    }
}

# Función principal de limpieza
function Invoke-ComprehensiveCleanup {
    param([string]$Level)

    Write-Log "=== INICIANDO LIMPIEZA COMPLETA DEL PROYECTO ===" "INFO"
    Write-Log "Nivel de limpieza: $Level" "INFO"
    Write-Log "Directorio de trabajo: $(Get-Location)" "INFO"

    # Verificar que estamos en el directorio correcto
    if (!(Test-Path "src") -or !(Test-Path "pyproject.toml")) {
        Write-Log "ERROR: No se detecta estructura del proyecto Python. Verificar directorio." "ERROR"
        return $false
    }

    $StartTime = Get-Date

    try {
        # Limpieza básica (todos los niveles)
        Clear-PythonCaches
        Clear-DevToolCaches

        if ($Level -in @("deep", "complete", "shutdown")) {
            Clear-VSCodeCaches
            Clear-TempFiles
        }

        if ($Level -in @("complete", "shutdown")) {
            Clear-ProjectLogs -LogLevel $Level
            Optimize-GitRepository
        }

        # Limpieza de VS Code (si está ejecutándose)
        if ($Level -eq "shutdown" -or $PreShutdown) {
            Invoke-VSCodeCleanup -CleanupLevel "complete"
        } else {
            Invoke-VSCodeCleanup -CleanupLevel $Level
        }

        $EndTime = Get-Date
        $Duration = $EndTime - $StartTime

        Write-Log "=== LIMPIEZA COMPLETADA EXITOSAMENTE ===" "SUCCESS"
        Write-Log "Tiempo total: $($Duration.TotalSeconds) segundos" "INFO"

        return $true

    } catch {
        Write-Log "ERROR CRÍTICO en limpieza: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Función de resumen post-limpieza
function Show-CleanupSummary {
    Write-Log "=== RESUMEN DE LIMPIEZA ===" "INFO"

    # Verificar cachés restantes
    $RemainingCaches = @()

    $CacheChecks = @(
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        "src\__pycache__"
    )

    foreach ($Cache in $CacheChecks) {
        if (Test-Path $Cache) {
            $RemainingCaches += $Cache
        }
    }

    if ($RemainingCaches.Count -eq 0) {
        Write-Log "[OK] Todos los caches principales eliminados" "SUCCESS"
    } else {
        Write-Log "[WARN] Caches restantes: $($RemainingCaches -join ', ')" "WARN"
    }

    # Mostrar procesos VS Code si existen
    $VSCodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue
    if ($VSCodeProcesses.Count -gt 0) {
        Write-Log "VS Code procesos activos: $($VSCodeProcesses.Count)" "INFO"
    } else {
        Write-Log "[OK] No hay procesos VS Code activos" "SUCCESS"
    }
}

# EJECUCIÓN PRINCIPAL
Write-Host "=== SCRIPT DE LIMPIEZA COMPLETA - SiK Python Game ===" -ForegroundColor Cyan
Write-Host "Nivel: $Level" -ForegroundColor White

# Confirmación para niveles avanzados
if ($Level -in @("complete", "shutdown") -and !$Force) {
    Write-Host "[WARN] ADVERTENCIA: Limpieza nivel '$Level' eliminara:" -ForegroundColor Yellow
    Write-Host "   - Todos los caches de herramientas" -ForegroundColor Yellow
    Write-Host "   - Logs antiguos del proyecto" -ForegroundColor Yellow
    Write-Host "   - Archivos temporales" -ForegroundColor Yellow
    if ($Level -eq "shutdown") {
        Write-Host "   - Cerrara pestanas de VS Code" -ForegroundColor Yellow
    }

    $Confirmation = Read-Host "¿Continuar? (s/N)"
    if ($Confirmation -ne "s" -and $Confirmation -ne "S") {
        Write-Log "Operación cancelada por el usuario" "INFO"
        exit 0
    }
}

# Ejecutar limpieza
$Success = Invoke-ComprehensiveCleanup -Level $Level

if ($Success) {
    Show-CleanupSummary
    Write-Host "[SUCCESS] LIMPIEZA COMPLETADA EXITOSAMENTE" -ForegroundColor Green
    Write-Host "[LOG] Log guardado en: $LogFile" -ForegroundColor Cyan
} else {
    Write-Host "[ERROR] ERROR EN LIMPIEZA - Ver log para detalles" -ForegroundColor Red
    Write-Host "[LOG] Log: $LogFile" -ForegroundColor Cyan
    exit 1
}
