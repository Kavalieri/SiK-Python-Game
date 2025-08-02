# SiK Dev-Tools Cleanup and Reorganization
# ========================================
# Autor: SiK Team
# Descripcion: Analiza y limpia dev-tools, archivando elementos obsoletos

param(
    [switch]$AnalyzeOnly,
    [switch]$Execute,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

# Configuracion
$DevToolsPath = Join-Path $ProjectRoot "dev-tools"
$ArchivePath = Join-Path $ProjectRoot "ARCHIVE\2025\dev-tools"

function Write-CleanupHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Yellow
    Write-Host " SiK DEV-TOOLS CLEANUP: $Title" -ForegroundColor Cyan
    Write-Host "====================================================" -ForegroundColor Yellow
}

function Get-FileAnalysis {
    param([string]$FilePath)
    
    $info = @{
        Path = $FilePath
        Name = Split-Path $FilePath -Leaf
        Size = 0
        LastModified = $null
        IsTest = $false
        IsDebug = $false
        IsTemp = $false
        IsObsolete = $false
        Category = "unknown"
    }
    
    if (Test-Path $FilePath) {
        $file = Get-Item $FilePath
        $info.Size = $file.Length
        $info.LastModified = $file.LastWriteTime
        
        # Analizar por nombre
        $name = $info.Name.ToLower()
        
        if ($name -match "^test_|_test\.py$|banco_pruebas") {
            $info.IsTest = $true
            $info.Category = "testing"
        }
        
        if ($name -match "^debug_|diagnose|diagnostic") {
            $info.IsDebug = $true
            $info.Category = "debugging"
        }
        
        if ($name -match "temp|tmp|backup|old|deprecated") {
            $info.IsTemp = $true
            $info.Category = "temporary"
        }
        
        # Analizar contenido para determinar si es obsoleto
        if ($FilePath -match "\.py$") {
            try {
                $content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
                if ($content -match "TODO|FIXME|deprecated|obsolete|no longer used") {
                    $info.IsObsolete = $true
                }
            } catch {
                # Ignorar errores de lectura
            }
        }
        
        # Determinar categoria final
        if ($info.IsTemp) { $info.Category = "temporary" }
        elseif ($info.IsObsolete) { $info.Category = "obsolete" }
        elseif ($info.IsDebug) { $info.Category = "debugging" }
        elseif ($info.IsTest) { $info.Category = "testing" }
        elseif ($name -match "migration|migrate") { $info.Category = "migration" }
        elseif ($name -match "package|build|release") { $info.Category = "packaging" }
        elseif ($name -match "script|automation") { $info.Category = "scripts" }
    }
    
    return $info
}

function Get-DevToolsInventory {
    Write-CleanupHeader "ANALIZANDO INVENTARIO"
    
    $inventory = @{
        Files = @()
        Categories = @{}
        Statistics = @{
            TotalFiles = 0
            TotalSize = 0
            TestFiles = 0
            DebugFiles = 0
            TempFiles = 0
            ObsoleteFiles = 0
        }
    }
    
    # Analizar todos los archivos en dev-tools
    $allFiles = Get-ChildItem $DevToolsPath -Recurse -File
    
    foreach ($file in $allFiles) {
        $analysis = Get-FileAnalysis $file.FullName
        $inventory.Files += $analysis
        
        # Categorizar
        if (-not $inventory.Categories.ContainsKey($analysis.Category)) {
            $inventory.Categories[$analysis.Category] = @()
        }
        $inventory.Categories[$analysis.Category] += $analysis
        
        # Estadisticas
        $inventory.Statistics.TotalFiles++
        $inventory.Statistics.TotalSize += $analysis.Size
        
        if ($analysis.IsTest) { $inventory.Statistics.TestFiles++ }
        if ($analysis.IsDebug) { $inventory.Statistics.DebugFiles++ }
        if ($analysis.IsTemp) { $inventory.Statistics.TempFiles++ }
        if ($analysis.IsObsolete) { $inventory.Statistics.ObsoleteFiles++ }
    }
    
    return $inventory
}

function Show-InventoryReport {
    param([hashtable]$Inventory)
    
    Write-CleanupHeader "REPORTE DE INVENTARIO"
    
    $stats = $Inventory.Statistics
    Write-Host "Total de archivos: $($stats.TotalFiles)" -ForegroundColor Green
    Write-Host "Tamaño total: $([math]::Round($stats.TotalSize / 1KB, 2)) KB" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Por tipo:" -ForegroundColor Cyan
    Write-Host "  Tests: $($stats.TestFiles)" -ForegroundColor White
    Write-Host "  Debug: $($stats.DebugFiles)" -ForegroundColor White
    Write-Host "  Temporales: $($stats.TempFiles)" -ForegroundColor Yellow
    Write-Host "  Obsoletos: $($stats.ObsoleteFiles)" -ForegroundColor Red
    Write-Host ""
    
    Write-Host "Por categoria:" -ForegroundColor Cyan
    foreach ($category in $Inventory.Categories.Keys | Sort-Object) {
        $files = $Inventory.Categories[$category]
        $totalSize = ($files | ForEach-Object { $_.Size } | Measure-Object -Sum).Sum
        Write-Host "  $category`: $($files.Count) archivos ($([math]::Round($totalSize / 1KB, 2)) KB)" -ForegroundColor White
    }
}

function Get-CleanupPlan {
    param([hashtable]$Inventory)
    
    Write-CleanupHeader "GENERANDO PLAN DE LIMPIEZA"
    
    $plan = @{
        Archive = @()
        Keep = @()
        Reorganize = @()
        Actions = @()
    }
    
    foreach ($file in $Inventory.Files) {
        $action = @{
            File = $file
            Action = "keep"
            Reason = ""
            TargetPath = ""
        }
        
        # Reglas de decision
        if ($file.IsTemp -or $file.IsObsolete) {
            $action.Action = "archive"
            $action.Reason = "Archivo temporal u obsoleto"
            $action.TargetPath = Join-Path $ArchivePath $file.Category
        }
        elseif ($file.Category -eq "testing" -and $file.Name -match "^test_.*\.py$") {
            # Tests especificos - evaluar individualmente
            if ($file.LastModified -lt (Get-Date).AddDays(-30)) {
                $action.Action = "archive"
                $action.Reason = "Test no modificado en 30+ dias"
                $action.TargetPath = Join-Path $ArchivePath "testing\old"
            } else {
                $action.Action = "reorganize"
                $action.Reason = "Test activo - mantener en testing/"
                $action.TargetPath = Join-Path $DevToolsPath "testing\active"
            }
        }
        elseif ($file.Category -eq "debugging") {
            $action.Action = "archive"
            $action.Reason = "Archivo de debugging - mover a archivo"
            $action.TargetPath = Join-Path $ArchivePath "debugging"
        }
        elseif ($file.Category -eq "migration") {
            if ($file.Name -match "sqlite|database") {
                $action.Action = "keep"
                $action.Reason = "Migracion de DB activa"
            } else {
                $action.Action = "archive"
                $action.Reason = "Migracion completada"
                $action.TargetPath = Join-Path $ArchivePath "migration"
            }
        }
        elseif ($file.Category -eq "scripts") {
            $action.Action = "keep"
            $action.Reason = "Script de desarrollo activo"
        }
        
        # Agregar al plan
        switch ($action.Action) {
            "archive" { $plan.Archive += $action }
            "keep" { $plan.Keep += $action }
            "reorganize" { $plan.Reorganize += $action }
        }
        
        $plan.Actions += $action
    }
    
    return $plan
}

function Show-CleanupPlan {
    param([hashtable]$Plan)
    
    Write-CleanupHeader "PLAN DE LIMPIEZA"
    
    Write-Host "ARCHIVAR ($($Plan.Archive.Count) archivos):" -ForegroundColor Red
    foreach ($action in $Plan.Archive) {
        Write-Host "  X $($action.File.Name) -> $($action.TargetPath)" -ForegroundColor Yellow
        Write-Host "    Razon: $($action.Reason)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "MANTENER ($($Plan.Keep.Count) archivos):" -ForegroundColor Green
    foreach ($action in $Plan.Keep) {
        Write-Host "  + $($action.File.Name)" -ForegroundColor Green
        Write-Host "    Razon: $($action.Reason)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "REORGANIZAR ($($Plan.Reorganize.Count) archivos):" -ForegroundColor Cyan
    foreach ($action in $Plan.Reorganize) {
        Write-Host "  -> $($action.File.Name) -> $($action.TargetPath)" -ForegroundColor Cyan
        Write-Host "    Razon: $($action.Reason)" -ForegroundColor Gray
    }
}

function Invoke-CleanupPlan {
    param([hashtable]$Plan)
    
    Write-CleanupHeader "EJECUTANDO LIMPIEZA"
    
    $summary = @{
        Archived = 0
        Kept = 0
        Reorganized = 0
        Errors = 0
    }
    
    # Crear directorios de archivo
    $archiveDirs = $Plan.Archive | ForEach-Object { $_.TargetPath } | Sort-Object -Unique
    foreach ($dir in $archiveDirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "Directorio de archivo creado: $dir" -ForegroundColor Blue
        }
    }
    
    # Ejecutar acciones de archivo
    foreach ($action in $Plan.Archive) {
        try {
            $targetFile = Join-Path $action.TargetPath $action.File.Name
            Move-Item $action.File.Path $targetFile -Force
            Write-Host "Archivado: $($action.File.Name)" -ForegroundColor Yellow
            $summary.Archived++
        } catch {
            Write-Host "Error archivando $($action.File.Name): $($_.Exception.Message)" -ForegroundColor Red
            $summary.Errors++
        }
    }
    
    # Ejecutar reorganizacion
    foreach ($action in $Plan.Reorganize) {
        try {
            $targetDir = Split-Path $action.TargetPath -Parent
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            
            $targetFile = Join-Path $action.TargetPath $action.File.Name
            Move-Item $action.File.Path $targetFile -Force
            Write-Host "Reorganizado: $($action.File.Name)" -ForegroundColor Cyan
            $summary.Reorganized++
        } catch {
            Write-Host "Error reorganizando $($action.File.Name): $($_.Exception.Message)" -ForegroundColor Red
            $summary.Errors++
        }
    }
    
    # Los archivos "keep" no requieren accion
    $summary.Kept = $Plan.Keep.Count
    
    return $summary
}

function New-CleanDevToolsStructure {
    Write-CleanupHeader "CREANDO ESTRUCTURA LIMPIA"
    
    # Nueva estructura de dev-tools
    $newStructure = @(
        "scripts",           # Scripts principales (workflow, build, etc.)
        "testing\active",    # Tests activos y importantes
        "testing\fixtures",  # Datos de prueba
        "packaging",         # Scripts de empaquetado
        "migration",         # Scripts de migracion de DB
        "docs"              # Documentacion de desarrollo
    )
    
    foreach ($dir in $newStructure) {
        $fullPath = Join-Path $DevToolsPath $dir
        if (-not (Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "Creado: dev-tools\$dir" -ForegroundColor Green
        }
    }
    
    # Crear README actualizado
    $readmeContent = @"
# SiK Development Tools
## Herramientas de Desarrollo Limpias y Organizadas

### Estructura:

#### scripts/
Scripts principales de desarrollo:
- sik.ps1 - Comando principal de workflow
- workflow_automation.ps1 - Sistema de workflow completo
- build_professional.ps1 - Sistema de build profesional
- build_release.ps1 - Integracion de releases

#### testing/
- active/ - Tests activos y mantenidos
- fixtures/ - Datos de prueba reutilizables

#### packaging/
Scripts y configuracion de empaquetado

#### migration/
Scripts de migracion de base de datos

#### docs/
Documentacion tecnica de desarrollo

### Archivos Obsoletos
Los archivos obsoletos han sido archivados en ARCHIVE/2025/dev-tools/

### Uso
- Para desarrollo normal: .\dev-tools\scripts\sik.ps1
- Para builds: .\dev-tools\scripts\build_professional.ps1
- Para tests: archivos en testing/active/
"@
    
    Set-Content -Path (Join-Path $DevToolsPath "README.md") -Value $readmeContent -Encoding UTF8
    Write-Host "README.md actualizado" -ForegroundColor Green
}

# EJECUCION PRINCIPAL
# ==================

Write-CleanupHeader "INICIANDO LIMPIEZA DE DEV-TOOLS"

# Verificar que estamos en el directorio correcto
if (-not (Test-Path $DevToolsPath)) {
    Write-Error "Directorio dev-tools no encontrado: $DevToolsPath"
    exit 1
}

# Analizar inventario
$inventory = Get-DevToolsInventory
Show-InventoryReport $inventory

# Generar plan de limpieza
$plan = Get-CleanupPlan $inventory
Show-CleanupPlan $plan

if ($AnalyzeOnly) {
    Write-Host ""
    Write-Host "MODO ANALISIS - No se ejecutaron cambios" -ForegroundColor Yellow
    Write-Host "Usa -Execute para aplicar el plan de limpieza" -ForegroundColor Yellow
    exit 0
}

if (-not $Execute -and -not $Force) {
    Write-Host ""
    $confirm = Read-Host "Ejecutar plan de limpieza? (s/N)"
    if ($confirm -ne "s" -and $confirm -ne "S") {
        Write-Host "Operacion cancelada" -ForegroundColor Yellow
        exit 0
    }
}

# Ejecutar limpieza
$summary = Invoke-CleanupPlan $plan

# Crear estructura limpia
New-CleanDevToolsStructure

# Mostrar resumen final
Write-CleanupHeader "RESUMEN DE LIMPIEZA"
Write-Host "Archivos archivados: $($summary.Archived)" -ForegroundColor Yellow
Write-Host "Archivos reorganizados: $($summary.Reorganized)" -ForegroundColor Cyan
Write-Host "Archivos mantenidos: $($summary.Kept)" -ForegroundColor Green
Write-Host "Errores: $($summary.Errors)" -ForegroundColor Red

if ($summary.Errors -eq 0) {
    Write-Host ""
    Write-Host "LIMPIEZA COMPLETADA EXITOSAMENTE" -ForegroundColor Green
    Write-Host "dev-tools/ esta ahora limpio y organizado" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "LIMPIEZA COMPLETADA CON ERRORES" -ForegroundColor Yellow
    Write-Host "Revisar errores arriba" -ForegroundColor Yellow
}
