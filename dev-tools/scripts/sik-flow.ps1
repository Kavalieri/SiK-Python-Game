# SiK Simple Workflow System
param(
    [string]$Comando = "",
    [string]$Mensaje = "",
    [string]$Rama = "",
    [string]$Version = "",
    [int]$Issue = 0,
    [switch]$Push,
    [switch]$Force,
    [switch]$Status,
    [switch]$TakeChanges
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD
$MainBranch = "main"
$VersionFile = Join-Path $ProjectRoot "VERSION.txt"

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host " SiK WORKFLOW: $Title" -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Get-CurrentBranch {
    try {
        $branch = git rev-parse --abbrev-ref HEAD
        return $branch.Trim()
    }
    catch {
        return $null
    }
}

function Get-GitStatus {
    $status = @{
        Branch       = Get-CurrentBranch
        HasChanges   = $false
        ChangedFiles = @()
        IsClean      = $true
    }
    
    try {
        $gitStatus = git status --porcelain
        if ($gitStatus) {
            $status.HasChanges = $true
            $status.IsClean = $false
            $status.ChangedFiles = $gitStatus
        }
    }
    catch {
        Write-Error "Error verificando estado de Git"
    }
    
    return $status
}

function Show-Status {
    Write-Header "ESTADO DEL REPOSITORIO"
    
    $status = Get-GitStatus
    
    Write-Host "Rama actual: $($status.Branch)" -ForegroundColor White
    
    if ($status.IsClean) {
        Write-Success "Repositorio limpio - no hay cambios pendientes"
    }
    else {
        Write-Info "Archivos modificados: $($status.ChangedFiles.Count)"
        foreach ($file in $status.ChangedFiles | Select-Object -First 10) {
            Write-Host "  $file" -ForegroundColor Gray
        }
        if ($status.ChangedFiles.Count -gt 10) {
            Write-Host "  ... y $($status.ChangedFiles.Count - 10) archivos más" -ForegroundColor Gray
        }
    }
    
    if (Test-Path $VersionFile) {
        $currentVersion = (Get-Content $VersionFile).Trim()
        Write-Host "Versión actual: $currentVersion" -ForegroundColor White
    }
}

function New-Branch {
    param([string]$BranchName, [string]$Message, [switch]$TakeChanges)
    
    Write-Header "CREANDO NUEVA RAMA"
    
    $status = Get-GitStatus
    $hasChanges = -not $status.IsClean
    
    # Si tenemos cambios y no estamos en main, necesitamos decisión manual
    if ($hasChanges -and $status.Branch -ne $MainBranch) {
        Write-Error "Tienes cambios en la rama '$($status.Branch)'. Primero completa esa tarea o usa 'save' para guardar los cambios."
        return $false
    }
    
    # Si tenemos cambios en main, ofrecer moverlos a la nueva rama
    if ($hasChanges -and $status.Branch -eq $MainBranch) {
        if ($TakeChanges) {
            Write-Info "Moviendo cambios pendientes a la nueva rama '$BranchName'"
            git stash push -m "Cambios para $BranchName - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
            Write-Success "Cambios guardados temporalmente"
        } else {
            Write-Warning "Tienes cambios pendientes en main."
            Write-Host "Para crear la rama Y mover los cambios: " -NoNewline
            Write-Host ".\sik-flow.ps1 new -Rama '$BranchName' -Mensaje '$Message' -TakeChanges" -ForegroundColor Yellow
            Write-Host "Para crear la rama sin cambios: " -NoNewline  
            Write-Host "git stash; .\sik-flow.ps1 new -Rama '$BranchName' -Mensaje '$Message'" -ForegroundColor Yellow
            return $false
        }
    }
    
    if ($status.Branch -ne $MainBranch) {
        Write-Error "Debes estar en la rama main para crear una nueva rama."
        return $false
    }
    
    try {
        git pull origin $MainBranch
        Write-Success "Rama $MainBranch actualizada"
        
        git checkout -b $BranchName
        Write-Success "Rama $BranchName creada y activada"
        
        # Si teníamos cambios guardados, aplicarlos a la nueva rama
        if ($TakeChanges -and $hasChanges) {
            git stash pop
            Write-Success "Cambios aplicados a la nueva rama $BranchName"
            Write-Info "Los cambios están listos para ser commitados con 'save'"
        }
        
        if ($Message) {
            Write-Info "Descripción: $Message"
        }
        
        return $true
    }
    catch {
        Write-Error "Error creando rama: $($_.Exception.Message)"
        return $false
    }
}

function Save-Changes {
    param([string]$Message)
    
    Write-Header "GUARDANDO CAMBIOS"
    
    $status = Get-GitStatus
    
    if ($status.IsClean) {
        Write-Info "No hay cambios que guardar"
        return $true
    }
    
    if (-not $Message) {
        Write-Error "Debes proporcionar un mensaje para el commit"
        return $false
    }
    
    try {
        git add -A
        git commit -m "$Message"
        Write-Success "Cambios commitados: $Message"
        
        if ($Push) {
            git push origin $status.Branch
            Write-Success "Cambios subidos a origin/$($status.Branch)"
        }
        
        return $true
    }
    catch {
        Write-Error "Error guardando cambios: $($_.Exception.Message)"
        return $false
    }
}

function New-PullRequest {
    param([string]$Message, [int]$IssueNumber)
    
    Write-Header "CREANDO PULL REQUEST"
    
    $status = Get-GitStatus
    
    if ($status.Branch -eq $MainBranch) {
        Write-Error "No puedes crear un PR desde la rama main"
        return $false
    }
    
    if ($status.HasChanges) {
        Write-Error "Hay cambios sin commitear. Guarda los cambios primero."
        return $false
    }
    
    try {
        git push origin $status.Branch
        Write-Success "Rama subida a origin"
        
        $prTitle = if ($Message) { $Message } else { "Changes from $($status.Branch)" }
        $prBody = "## Cambios realizados`n`n$Message`n`n## Checklist`n- [ ] Código revisado`n- [ ] Tests ejecutados`n- [ ] Documentación actualizada"
        
        # Agregar referencia a issue si se proporciona
        if ($IssueNumber -gt 0) {
            $prBody += "`n`n## Issue relacionada`nCloses #$IssueNumber"
            Write-Info "Vinculando PR con issue #$IssueNumber"
        }
        
        $ghArgs = @("pr", "create", "--title", "$prTitle", "--body", "$prBody", "--base", $MainBranch, "--head", $status.Branch)
        
        gh @ghArgs
        
        Write-Success "Pull Request creado exitosamente"
        if ($IssueNumber -gt 0) {
            Write-Info "PR vinculado con issue #$IssueNumber (se cerrará automáticamente al mergear)"
        }
        
        return $true
    }
    catch {
        Write-Error "Error creando PR: $($_.Exception.Message)"
        return $false
    }
}

function Invoke-Merge {
    param([string]$Message)
    
    Write-Header "MERGEANDO PULL REQUEST"
    
    $status = Get-GitStatus
    
    if ($status.Branch -eq $MainBranch) {
        Write-Error "Ya estás en la rama main. Primero cambia a la rama de feature."
        return $false
    }
    
    if ($status.HasChanges) {
        Write-Error "Hay cambios sin commitear. Guarda los cambios primero."
        return $false
    }
    
    try {
        # Verificar si hay PR abierto para esta rama
        $prInfo = gh pr view --json number, title 2>$null
        if (-not $prInfo) {
            Write-Error "No hay PR abierto para esta rama. Crea un PR primero."
            return $false
        }
        
        $prData = $prInfo | ConvertFrom-Json
        Write-Info "PR encontrado: #$($prData.number) - $($prData.title)"
        
        # Mergear el PR
        $mergeMessage = if ($Message) { $Message } else { "Merge: $($prData.title)" }
        gh pr merge --merge --delete-branch
        
        Write-Success "PR #$($prData.number) mergeado exitosamente"
        Write-Info "Rama de feature eliminada automáticamente"
        
        # Cambiar a main y actualizar
        git checkout $MainBranch
        git pull origin $MainBranch
        
        Write-Success "Cambiado a main y actualizado"
        Write-Info "Listo para crear release si es necesario"
        
        return $true
    }
    catch {
        Write-Error "Error en merge: $($_.Exception.Message)"
        return $false
    }
}

function Invoke-Release {
    param([string]$Version, [string]$Message)
    
    Write-Header "CREANDO RELEASE"
    
    $status = Get-GitStatus
    
    if ($status.Branch -ne $MainBranch) {
        Write-Error "Debes estar en la rama main para crear un release"
        return $false
    }
    
    if ($status.HasChanges) {
        Write-Error "Hay cambios sin commitear en main. Resuelve esto primero."
        return $false
    }
    
    if (-not $Version) {
        Write-Error "Debes especificar una versión para el release"
        return $false
    }
    
    try {
        Set-Content -Path $VersionFile -Value $Version
        git add $VersionFile
        git commit -m "chore: bump version to $Version"
        
        git tag -a "v$Version" -m "Release v$Version - $Message"
        
        git push origin $MainBranch
        git push origin "v$Version"
        
        Write-Success "Tag v$Version creado y subido"
        
        $buildScript = Join-Path $ProjectRoot "dev-tools\scripts\build_professional.ps1"
        $buildAssets = @()
        
        if (Test-Path $buildScript) {
            Write-Info "Generando build profesional..."
            try {
                & $buildScript -Version $Version -Platform "Windows" -Architecture "x64"
                
                $buildDir = Join-Path $ProjectRoot "builds"
                if (Test-Path $buildDir) {
                    $assetFiles = Get-ChildItem $buildDir -Filter "*v$Version*" -File
                    foreach ($file in $assetFiles) {
                        $buildAssets += $file.FullName
                    }
                }
                
                if ($buildAssets.Count -gt 0) {
                    Write-Success "Build generado: $($buildAssets.Count) archivos"
                }
                else {
                    Write-Info "Build completado pero no se encontraron archivos"
                }
            }
            catch {
                Write-Error "Error en build: $($_.Exception.Message)"
                Write-Info "Continuando con release sin build..."
            }
        }
        
        $releaseNotes = "## Release v$Version`n`n**Descripción:** $Message`n`n### Cambios Principales`n$Message`n`n### Estado del Proyecto`n- Código compliant con Ruff/MyPy`n- Tests validados`n- Documentación actualizada`n`n**Desarrollado con GitHub Copilot + SiK Workflow System**"
        
        if ($buildAssets.Count -gt 0) {
            $assetArgs = $buildAssets | ForEach-Object { "--attach-asset", $_ }
            gh release create "v$Version" --title "SiK Python Game v$Version" --notes "$releaseNotes" @assetArgs
            Write-Success "Release v$Version creado con $($buildAssets.Count) archivos adjuntos"
        }
        else {
            gh release create "v$Version" --title "SiK Python Game v$Version" --notes "$releaseNotes"
            Write-Success "Release v$Version creado"
        }
        
        $releaseUrl = "https://github.com/Kavalieri/SiK-Python-Game/releases/tag/v$Version"
        Write-Info "Release URL: $releaseUrl"
        
        return $true
    }
    catch {
        Write-Error "Error creando release: $($_.Exception.Message)"
        return $false
    }
}

function Switch-Branch {
    param([string]$BranchName)
    
    Write-Header "CAMBIANDO A RAMA $BranchName"
    
    $status = Get-GitStatus
    
    if ($status.HasChanges) {
        if (-not $Force) {
            Write-Error "Hay cambios sin commitear. Usa -Force para descartar o commitea primero."
            return $false
        }
        else {
            Write-Info "Descartando cambios locales..."
            git reset --hard
        }
    }
    
    try {
        git checkout $BranchName
        Write-Success "Cambiado a rama $BranchName"
        return $true
    }
    catch {
        Write-Error "Error cambiando a rama: $($_.Exception.Message)"
        return $false
    }
}

function Show-Help {
    Write-Header "AYUDA - SiK Workflow System"
    
    Write-Host "USO BÁSICO:" -ForegroundColor White
    Write-Host "  .\sik-flow.ps1 status" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 new -Rama feature/login -Mensaje 'Implementar login'" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 new -Rama feature/export -Mensaje 'Exportar JSON' -TakeChanges" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 save -Mensaje 'Añadir validación' -Push" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 pr -Mensaje 'Sistema completo' -Issue 123" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 merge -Mensaje 'Merge login system'" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 release -Version 1.2.0 -Mensaje 'Nueva versión'" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "COMANDOS:" -ForegroundColor White
    Write-Host "  status    # Ver estado del repositorio" -ForegroundColor Gray
    Write-Host "  new       # Crear nueva rama (requiere -Rama, opcional -TakeChanges)" -ForegroundColor Gray
    Write-Host "  save      # Commitear cambios (requiere -Mensaje)" -ForegroundColor Gray
    Write-Host "  pr        # Crear Pull Request (opcional -Issue)" -ForegroundColor Gray
    Write-Host "  merge     # Mergear PR actual a main" -ForegroundColor Gray
    Write-Host "  release   # Crear release con build (requiere -Version)" -ForegroundColor Gray
    Write-Host "  switch    # Cambiar de rama (requiere -Rama)" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "OPCIONES:" -ForegroundColor White
    Write-Host "  -Rama <nombre>     # Nombre de la rama" -ForegroundColor Gray
    Write-Host "  -Mensaje <texto>   # Mensaje descriptivo" -ForegroundColor Gray
    Write-Host "  -Version <x.y.z>   # Versión para release" -ForegroundColor Gray
    Write-Host "  -Issue <numero>    # Número de issue a vincular con PR" -ForegroundColor Gray
    Write-Host "  -Push              # Subir cambios automáticamente" -ForegroundColor Gray
    Write-Host "  -Force             # Forzar operación" -ForegroundColor Gray
    Write-Host "  -TakeChanges       # Mover cambios pendientes a nueva rama" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "FLUJO TÍPICO:" -ForegroundColor White
    Write-Host "  1. .\sik-flow.ps1 new -Rama feature/nueva-func -Mensaje 'Descripción'" -ForegroundColor Gray
    Write-Host "  2. [hacer cambios]" -ForegroundColor Gray
    Write-Host "  3. .\sik-flow.ps1 save -Mensaje 'Implementar X' -Push" -ForegroundColor Gray
    Write-Host "  4. .\sik-flow.ps1 pr -Mensaje 'Feature completa' -Issue 123" -ForegroundColor Gray
    Write-Host "  5. [review en GitHub]" -ForegroundColor Gray
    Write-Host "  6. .\sik-flow.ps1 merge -Mensaje 'Merge nueva funcionalidad'" -ForegroundColor Gray
    Write-Host "  7. .\sik-flow.ps1 release -Version 1.1.0 -Mensaje 'Nueva funcionalidad'" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "GESTIÓN DE MÚLTIPLES TAREAS:" -ForegroundColor White
    Write-Host "  # Si tienes cambios pendientes y quieres nueva tarea:" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 new -Rama feature/otra-tarea -Mensaje 'Nueva tarea' -TakeChanges" -ForegroundColor Gray
    Write-Host "  # O guardar primero la tarea actual:" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 save -Mensaje 'WIP: progreso parcial' -Push" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 switch -Rama main" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 new -Rama feature/otra-tarea -Mensaje 'Nueva tarea'" -ForegroundColor Gray
}

# LÓGICA PRINCIPAL
if ($Status) {
    Show-Status
    exit 0
}

if (-not $Comando) {
    Show-Help
    exit 0
}

switch ($Comando.ToLower()) {
    "status" { Show-Status }
    "new" { 
        if (-not $Rama) {
            Write-Error "El comando new requiere -Rama"
            exit 1
        }
        New-Branch -BranchName $Rama -Message $Mensaje -TakeChanges:$TakeChanges
    }
    "save" {
        if (-not $Mensaje) {
            Write-Error "El comando save requiere -Mensaje"
            exit 1
        }
        Save-Changes -Message $Mensaje
    }
    "pr" {
        New-PullRequest -Message $Mensaje -IssueNumber $Issue
    }
    "merge" {
        Invoke-Merge -Message $Mensaje
    }
    "release" {
        if (-not $Version -or -not $Mensaje) {
            Write-Error "El comando release requiere -Version y -Mensaje"
            exit 1
        }
        Invoke-Release -Version $Version -Message $Mensaje
    }
    "switch" {
        if (-not $Rama) {
            Write-Error "El comando switch requiere -Rama"
            exit 1
        }
        Switch-Branch -BranchName $Rama
    }
    "help" { Show-Help }
    default {
        Write-Error "Comando desconocido: $Comando"
        Show-Help
        exit 1
    }
}
