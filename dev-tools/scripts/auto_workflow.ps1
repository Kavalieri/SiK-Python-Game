# SiK Auto Workflow - Sistema de Activadores Inteligentes
# ========================================================
# Autor: SiK Team (Auto-generado)
# Fecha: 2025-08-02
# Descripcion: Sistema que evalua contexto y gestiona workflow automaticamente
# REGLA FUNDAMENTAL: TODOS los cambios van a traves de ramas, NUNCA commit directo a main

param(
    [string]$Descripcion = "",
    [string]$Archivos = "",
    [switch]$Forzar,
    [switch]$Debug
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

# Configuracion
$ConfigPath = Join-Path $ProjectRoot "config/workflow.json"
$Config = Get-Content $ConfigPath | ConvertFrom-Json

function Write-AutoHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Magenta
    Write-Host " SiK AUTO WORKFLOW: $Title" -ForegroundColor Yellow
    Write-Host "===================================================" -ForegroundColor Magenta
}

function Write-Decision {
    param([string]$Tipo, [string]$Razon, [string]$Accion)
    Write-Host ""
    Write-Host "DECISION AUTOMATICA:" -ForegroundColor Cyan
    Write-Host "  Tipo detectado: $Tipo" -ForegroundColor Green
    Write-Host "  Razon: $Razon" -ForegroundColor Blue
    Write-Host "  Accion: $Accion" -ForegroundColor Yellow
}

function Get-GitStatus {
    try {
        $status = @{
            Rama = (git branch --show-current)
            Cambios = @(git status --porcelain)
            EsMain = $false
            TieneCommitsPendientes = $false
        }
        
        $status.EsMain = $status.Rama -eq $Config.git.main_branch
        $status.TieneCommitsPendientes = $status.Cambios.Count -gt 0
        
        return $status
    } catch {
        Write-Error "Error obteniendo estado Git: $($_.Exception.Message)"
        return $null
    }
}

function Get-ChangeType {
    param([array]$ChangedFiles, [string]$Description)
    
    # Analisis de archivos modificados
    $srcFiles = $ChangedFiles | Where-Object { $_ -match "^src/" }
    $docFiles = $ChangedFiles | Where-Object { $_ -match "^docs/" -or $_ -match "README" }
    $configFiles = $ChangedFiles | Where-Object { $_ -match "^config/" -or $_ -match "\.json$" -or $_ -match "\.yaml$" }
    $devFiles = $ChangedFiles | Where-Object { $_ -match "^dev-tools/" -or $_ -match "\.github/" }
    
    # Analisis de descripcion
    $desc = $Description.ToLower()
    
    # Reglas de deteccion (orden de prioridad)
    if ($desc -match "hotfix|urgente|critico|security|seguridad") {
        return @{
            Tipo = "hotfix"
            Prefijo = "hotfix/"
            Version = "patch"
            Razon = "Palabras clave de emergencia detectadas"
            RequiereNuevaRama = $true
            DirectoAMain = $true
        }
    }
    
    if ($desc -match "fix|bug|error|corrige|arregla|soluciona") {
        return @{
            Tipo = "bugfix"
            Prefijo = "bugfix/"
            Version = "patch"
            Razon = "Palabras clave de correcion detectadas"
            RequiereNuevaRama = $true
            DirectoAMain = $false
        }
    }
    
    if ($docFiles.Count -gt 0 -and $srcFiles.Count -eq 0) {
        return @{
            Tipo = "docs"
            Prefijo = "docs/"
            Version = "patch"
            Razon = "Solo archivos de documentacion modificados"
            RequiereNuevaRama = $true
            DirectoAMain = $false
        }
    }
    
    if ($devFiles.Count -gt 0 -and $srcFiles.Count -eq 0) {
        return @{
            Tipo = "dev-tools"
            Prefijo = "dev/"
            Version = "patch"
            Razon = "Solo herramientas de desarrollo modificadas"
            RequiereNuevaRama = $true
            DirectoAMain = $false
        }
    }
    
    if ($configFiles.Count -gt 0 -and $srcFiles.Count -eq 0) {
        return @{
            Tipo = "config"
            Prefijo = "config/"
            Version = "patch"
            Razon = "Solo archivos de configuracion modificados"
            RequiereNuevaRama = $true
            DirectoAMain = $false
        }
    }
    
    if ($desc -match "feature|caracteristica|nueva|implementa|añade|agrega") {
        $versionBump = if ($desc -match "mayor|breaking|rompe") { "major" } 
                       elseif ($desc -match "menor|minor") { "minor" } 
                       else { "minor" }
        
        return @{
            Tipo = "feature"
            Prefijo = "feature/"
            Version = $versionBump
            Razon = "Nueva funcionalidad detectada"
            RequiereNuevaRama = $true
            DirectoAMain = $false
        }
    }
    
    # Caso por defecto
    return @{
        Tipo = "change"
        Prefijo = "change/"
        Version = "patch"
        Razon = "Cambio general no categorizado"
        RequiereNuevaRama = $true
        DirectoAMain = $false
    }
}

function Get-BranchSuggestion {
    param([string]$Tipo, [string]$Prefijo, [string]$Descripcion)
    
    # Limpiar descripcion para nombre de rama
    $cleanDesc = $Descripcion -replace "[^a-zA-Z0-9\s]", "" -replace "\s+", "-"
    $cleanDesc = $cleanDesc.ToLower().Substring(0, [Math]::Min(30, $cleanDesc.Length))
    
    return "$Prefijo$cleanDesc"
}

function Get-WorkflowAction {
    param([object]$GitStatus, [object]$ChangeType, [string]$Descripcion)
    
    $actions = @()
    
    # REGLA PRINCIPAL: Si estamos en main y hay cambios pendientes, SIEMPRE crear rama
    if ($GitStatus.EsMain -and $GitStatus.TieneCommitsPendientes) {
        $branchName = Get-BranchSuggestion $ChangeType.Tipo $ChangeType.Prefijo $Descripcion
        $actions += @{
            Comando = "nueva-rama"
            Parametros = @{
                RamaNombre = $branchName
                Mensaje = $Descripcion
            }
            Razon = "Cambios en main requieren nueva rama (REGLA OBLIGATORIA)"
        }
    }
    # Si estamos en una rama feature con cambios
    elseif (-not $GitStatus.EsMain -and $GitStatus.TieneCommitsPendientes) {
        $actions += @{
            Comando = "completar"
            Parametros = @{
                Mensaje = $Descripcion
            }
            Razon = "Continuar trabajo en rama actual"
        }
    }
    # Si no hay cambios pendientes y estamos en rama feature
    elseif (-not $GitStatus.TieneCommitsPendientes -and -not $GitStatus.EsMain) {
        $actions += @{
            Comando = "merge"
            Parametros = @{
                Release = $true
                TipoVersion = $ChangeType.Version
                Mensaje = $Descripcion
            }
            Razon = "Rama lista para merge y release"
        }
    }
    else {
        Write-Host "Sin cambios pendientes en main. Estado limpio." -ForegroundColor Green
        return @()
    }
    
    return $actions
}

function Invoke-WorkflowAction {
    param([object]$Action)
    
    $scriptPath = Join-Path $ProjectRoot "dev-tools/scripts/workflow_automation.ps1"
    
    switch ($Action.Comando) {
        "nueva-rama" {
            $params = $Action.Parametros
            & $scriptPath -Accion "nueva-rama" -RamaNombre $params.RamaNombre -Mensaje $params.Mensaje
        }
        "completar" {
            $params = $Action.Parametros
            & $scriptPath -Accion "completar" -Mensaje $params.Mensaje
        }
        "merge" {
            $params = $Action.Parametros
            $cmdArgs = @("-Accion", "merge", "-Mensaje", $params.Mensaje)
            if ($params.Release) { $cmdArgs += "-Release" }
            if ($params.TipoVersion) { $cmdArgs += "-TipoVersion"; $cmdArgs += $params.TipoVersion }
            & $scriptPath @cmdArgs
        }
    }
}

# EJECUCION PRINCIPAL
# ==================

Write-AutoHeader "ANALIZANDO CONTEXTO"

# Obtener estado actual
$gitStatus = Get-GitStatus
if (-not $gitStatus) { exit 1 }

Write-Host "Estado actual:" -ForegroundColor Cyan
Write-Host "  Rama: $($gitStatus.Rama)" -ForegroundColor Green
Write-Host "  Archivos modificados: $($gitStatus.Cambios.Count)" -ForegroundColor Green
Write-Host "  Es rama main: $($gitStatus.EsMain)" -ForegroundColor Green

# Si no hay descripcion, pedirla
if (-not $Descripcion -and $gitStatus.TieneCommitsPendientes) {
    Write-Host ""
    $Descripcion = Read-Host "Describe los cambios realizados"
}

# Detectar tipo de cambio si hay archivos modificados
if ($gitStatus.TieneCommitsPendientes) {
    $changedFiles = $gitStatus.Cambios | ForEach-Object { $_.Substring(3) }
    $changeType = Get-ChangeType $changedFiles $Descripcion
    
    Write-Decision $changeType.Tipo $changeType.Razon "Auto-determinando workflow"
    
    # Decidir acciones
    $actions = Get-WorkflowAction $gitStatus $changeType $Descripcion
    
    if ($Debug) {
        Write-Host ""
        Write-Host "DEBUG - Acciones devueltas: $($actions.Count)" -ForegroundColor Magenta
        foreach ($action in $actions) {
            Write-Host "  Comando: $($action.Comando)" -ForegroundColor Gray
            Write-Host "  Razon: $($action.Razon)" -ForegroundColor Gray
        }
    }
    
    if ($actions.Count -eq 0) {
        Write-Host "No se requieren acciones." -ForegroundColor Green
        exit 0
    }
    
    # Mostrar plan de ejecucion
    Write-Host ""
    Write-Host "PLAN DE EJECUCION:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $actions.Count; $i++) {
        $action = $actions[$i]
        Write-Host "  $($i+1). $($action.Comando) - $($action.Razon)" -ForegroundColor Cyan
        if ($Debug) {
            Write-Host "      Parametros: $($action.Parametros | ConvertTo-Json -Compress)" -ForegroundColor Gray
        }
    }
    
    # Confirmar ejecucion
    if (-not $Forzar) {
        Write-Host ""
        $confirm = Read-Host "Ejecutar plan automatico? (s/N)"
        if ($confirm -ne "s" -and $confirm -ne "S") {
            Write-Host "Operacion cancelada." -ForegroundColor Yellow
            exit 0
        }
    }
    
    # Ejecutar acciones
    Write-Host ""
    Write-Host "EJECUTANDO WORKFLOW AUTOMATICO..." -ForegroundColor Magenta
    
    foreach ($action in $actions) {
        Write-Host ""
        Write-Host "Ejecutando: $($action.Comando)" -ForegroundColor Yellow
        Write-Host "Razon: $($action.Razon)" -ForegroundColor Blue
        
        try {
            Invoke-WorkflowAction $action
            Write-Host "OK Completado: $($action.Comando)" -ForegroundColor Green
        } catch {
            Write-Host "ERROR en $($action.Comando): $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host "WORKFLOW AUTOMATICO COMPLETADO EXITOSAMENTE" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "No hay cambios pendientes para procesar." -ForegroundColor Green
}
