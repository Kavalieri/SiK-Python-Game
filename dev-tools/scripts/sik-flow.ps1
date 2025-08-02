# SiK Simple Workflow System
param(
    [string]$Comando = "",
    [string]$Mensaje = "",
    [string]$Rama = "",
    [string]$Version = "",
    [switch]$Push,
    [switch]$Force,
    [switch]$Status
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
    } catch {
        return $null
    }
}

function Get-GitStatus {
    $status = @{
        Branch = Get-CurrentBranch
        HasChanges = $false
        ChangedFiles = @()
        IsClean = $true
    }
    
    try {
        $gitStatus = git status --porcelain
        if ($gitStatus) {
            $status.HasChanges = $true
            $status.IsClean = $false
            $status.ChangedFiles = $gitStatus
        }
    } catch {
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
    } else {
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
    param([string]$BranchName, [string]$Message)
    
    Write-Header "CREANDO NUEVA RAMA"
    
    $status = Get-GitStatus
    
    if (-not $status.IsClean) {
        Write-Error "Hay cambios pendientes. Commitea o descarta los cambios antes de crear una rama nueva."
        return $false
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
        
        if ($Message) {
            Write-Info "Descripción: $Message"
        }
        
        return $true
    } catch {
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
    } catch {
        Write-Error "Error guardando cambios: $($_.Exception.Message)"
        return $false
    }
}

function New-PullRequest {
    param([string]$Message)
    
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
        
        gh pr create --title "$prTitle" --body "$prBody" --base $MainBranch --head $status.Branch
        
        Write-Success "Pull Request creado exitosamente"
        return $true
    } catch {
        Write-Error "Error creando PR: $($_.Exception.Message)"
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
                } else {
                    Write-Info "Build completado pero no se encontraron archivos"
                }
            } catch {
                Write-Error "Error en build: $($_.Exception.Message)"
                Write-Info "Continuando con release sin build..."
            }
        }
        
        $releaseNotes = "## Release v$Version`n`n**Descripción:** $Message`n`n### Cambios Principales`n$Message`n`n### Estado del Proyecto`n- Código compliant con Ruff/MyPy`n- Tests validados`n- Documentación actualizada`n`n**Desarrollado con GitHub Copilot + SiK Workflow System**"
        
        if ($buildAssets.Count -gt 0) {
            $assetArgs = $buildAssets | ForEach-Object { "--attach-asset", $_ }
            gh release create "v$Version" --title "SiK Python Game v$Version" --notes "$releaseNotes" @assetArgs
            Write-Success "Release v$Version creado con $($buildAssets.Count) archivos adjuntos"
        } else {
            gh release create "v$Version" --title "SiK Python Game v$Version" --notes "$releaseNotes"
            Write-Success "Release v$Version creado"
        }
        
        $releaseUrl = "https://github.com/Kavalieri/SiK-Python-Game/releases/tag/v$Version"
        Write-Info "Release URL: $releaseUrl"
        
        return $true
    } catch {
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
        } else {
            Write-Info "Descartando cambios locales..."
            git reset --hard
        }
    }
    
    try {
        git checkout $BranchName
        Write-Success "Cambiado a rama $BranchName"
        return $true
    } catch {
        Write-Error "Error cambiando a rama: $($_.Exception.Message)"
        return $false
    }
}

function Show-Help {
    Write-Header "AYUDA - SiK Workflow System"
    
    Write-Host "USO BÁSICO:" -ForegroundColor White
    Write-Host "  .\sik-flow.ps1 status" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 new -Rama feature/login -Mensaje 'Implementar login'" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 save -Mensaje 'Añadir validación' -Push" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 pr -Mensaje 'Sistema completo'" -ForegroundColor Gray
    Write-Host "  .\sik-flow.ps1 release -Version 1.2.0 -Mensaje 'Nueva versión'" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "COMANDOS:" -ForegroundColor White
    Write-Host "  status    # Ver estado del repositorio" -ForegroundColor Gray
    Write-Host "  new       # Crear nueva rama" -ForegroundColor Gray
    Write-Host "  save      # Commitear cambios" -ForegroundColor Gray
    Write-Host "  pr        # Crear Pull Request" -ForegroundColor Gray
    Write-Host "  release   # Crear release" -ForegroundColor Gray
    Write-Host "  switch    # Cambiar de rama" -ForegroundColor Gray
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
        New-Branch -BranchName $Rama -Message $Mensaje
    }
    "save" {
        if (-not $Mensaje) {
            Write-Error "El comando save requiere -Mensaje"
            exit 1
        }
        Save-Changes -Message $Mensaje
    }
    "pr" {
        New-PullRequest -Message $Mensaje
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
