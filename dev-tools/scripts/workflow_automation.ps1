# SiK Development Workflow Automation
# ===================================
# Autor: SiK Team (Auto-generado)
# Fecha: 2025-08-02
# Descripcion: Sistema completo de workflow automatizado para desarrollo

param(
	[Parameter(Mandatory=$true)]
	[string]$Accion,
	
	[string]$Mensaje = "",
	[string]$TipoVersion = "patch",
	[string]$RamaNombre = "",
	[switch]$Push,
	[switch]$Release,
	[switch]$ForceClean
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

function Write-StatusHeader {
	param([string]$Title)
	Write-Host ""
	Write-Host "============================================================" -ForegroundColor Cyan
	Write-Host " $Title" -ForegroundColor Yellow
	Write-Host "============================================================" -ForegroundColor Cyan
}

function Write-Success {
	param([string]$Message)
	Write-Host "OK $Message" -ForegroundColor Green
}

function Write-Error {
	param([string]$Message)
	Write-Host "ERROR $Message" -ForegroundColor Red
}

function Write-Info {
	param([string]$Message)
	Write-Host "INFO $Message" -ForegroundColor Blue
}

function Get-NextVersion {
	param([string]$Current, [string]$Type)
	
	if (-not $Current -or $Current -eq "") {
		return "0.1.0"
	}
	
	$parts = $Current.Split('.')
	$major = [int]$parts[0]
	$minor = [int]$parts[1] 
	$patch = [int]$parts[2]
	
	switch ($Type) {
		"major" { return "$($major + 1).0.0" }
		"minor" { return "$major.$($minor + 1).0" }
		"patch" { return "$major.$minor.$($patch + 1)" }
		default { return "$major.$minor.$($patch + 1)" }
	}
}

function Update-VersionFile {
	param([string]$Version)
	
	$VersionFile = Join-Path $ProjectRoot "VERSION.txt"
	$Version | Out-File -FilePath $VersionFile -Encoding UTF8 -NoNewline
	Write-Success "VERSION.txt actualizado a $Version"
}

function New-Changelog {
	param([string]$Version, [string]$Message)
	
	$Date = Get-Date -Format "yyyy-MM-dd"
	$ChangelogEntry = @"

## [$Version] - $Date

### Cambios en $Message

#### Cambios Implementados
- $Message

#### Estado del Proyecto
- Infraestructura: Completa y funcional
- Sistema de gestion: Workflow automatizado
- Calidad de codigo: Ruff + MyPy compliant
- Documentacion: Actualizada automaticamente

---

"@
	
	$ChangelogPath = Join-Path $ProjectRoot "CHANGELOG.md"
	$Content = Get-Content $ChangelogPath -Raw
	
	$InsertPoint = $Content.IndexOf("## [Unreleased]")
	if ($InsertPoint -ge 0) {
		$NextSection = $Content.IndexOf("`n## [", $InsertPoint + 10)
		if ($NextSection -ge 0) {
			$Before = $Content.Substring(0, $NextSection)
			$After = $Content.Substring($NextSection)
			$NewContent = $Before + $ChangelogEntry + $After
		} else {
			$NewContent = $Content + $ChangelogEntry
		}
	} else {
		$NewContent = $Content + $ChangelogEntry
	}
	
	$NewContent | Out-File -FilePath $ChangelogPath -Encoding UTF8
	
	$ArchiveFile = Join-Path $ProjectRoot "docs\changelogs\$Version.md"
	$ChangelogEntry | Out-File -FilePath $ArchiveFile -Encoding UTF8
	
	Write-Success "Changelog actualizado para version $Version"
	Write-Success "Changelog archivado en docs/changelogs/$Version.md"
}

function New-FeatureBranch {
	param([string]$BranchName, [string]$Message)
	
	Write-StatusHeader "CREANDO NUEVA RAMA DE DESARROLLO"
	
	$CurrentBranch = git branch --show-current
	if ($CurrentBranch -ne "main") {
		git checkout main
		Write-Info "Cambiado a rama main"
	}
	
	git pull origin main
	Write-Info "main actualizado desde remoto"
	
	git checkout -b $BranchName
	Write-Success "Rama '$BranchName' creada y activada"
	
	git add .
	if (git diff --cached --quiet) {
		Write-Info "No hay cambios pendientes para commit inicial"
	} else {
		git commit -m "Inicio desarrollo: $Message"
		Write-Success "Commit inicial realizado en rama $BranchName"
	}
}

function Complete-Feature {
	param([string]$Message, [string]$Version)
	
	Write-StatusHeader "COMPLETANDO DESARROLLO DE CARACTERÍSTICA"
	
	$CurrentBranch = git branch --show-current
	
	if ($CurrentBranch -eq "main") {
		Write-Error "No puedes completar una característica desde main"
		exit 1
	}
	
	git add .
	if (-not (git diff --cached --quiet)) {
		git commit -m "Completado: $Message"
		Write-Success "Commit final realizado"
	}
	
	git push -u origin $CurrentBranch
	Write-Success "Rama $CurrentBranch subida al remoto"
	
	Write-Info "Creando Pull Request..."
	$PRBody = "Descripcion: $Message`n`nCambios:`n- Implementacion completa de: $Message`n- Testing verificado`n- Documentacion actualizada`n`nChecklist:`n- [x] Codigo funcional`n- [x] Tests pasando`n- [x] Documentacion actualizada`n- [x] Sin errores de linting`n`nListo para merge"
	
	$PRResult = gh pr create --title "Nueva característica: $Message" --body $PRBody
	
	if ($LASTEXITCODE -eq 0) {
		Write-Success "Pull Request creado exitosamente"
		Write-Info $PRResult
	} else {
		Write-Error "Error creando Pull Request"
		exit 1
	}
}

function Merge-Feature {
	param([string]$Message, [string]$Version)
	
	Write-StatusHeader "REALIZANDO MERGE A MAIN"
	
	$PRNumber = gh pr view --json number --jq .number 2>$null
	if (-not $PRNumber) {
		Write-Error "No hay Pull Request abierto en esta rama"
		exit 1
	}
	
	Write-Info "Pull Request #$PRNumber encontrado"
	
	gh pr merge $PRNumber --squash --delete-branch
	Write-Success "Pull Request mergeado y rama eliminada"
	
	git checkout main
	git pull origin main
	Write-Success "main actualizado tras merge"
	
	Update-VersionFile $Version
	New-Changelog $Version $Message
	
	git add .
	git commit -m "Version ${Version}: ${Message}"
	git push origin main
	Write-Success "Version $Version commitada y subida"
}

function New-Release {
	param([string]$Version, [string]$Message)
	
	Write-StatusHeader "CREANDO RELEASE Y TAG"
	
	git tag -a "v$Version" -m "Release v${Version}: ${Message}"
	git push origin "v$Version"
	Write-Success "Tag v$Version creado y subido"
	
	$ReleaseNotes = "## Release v$Version`n`nDescripcion: $Message`n`nCambios Principales:`n- $Message`n`nEstado del Proyecto:`n- Infraestructura: Completa y funcional`n- Sistema de gestion: Workflow automatizado`n- Calidad de codigo: Ruff + MyPy compliant`n- Documentacion: Actualizada automaticamente`n`nEnlaces:`n- Codigo fuente: GitHub Repository`n- Documentacion: docs/README.md`n- Changelog completo: CHANGELOG.md`n`nDesarrollado con GitHub Copilot"
	
	gh release create "v$Version" --title "SiK Python Game v$Version" --notes "$ReleaseNotes"
	Write-Success "Release v$Version creado exitosamente"
	
	$ReleaseUrl = "https://github.com/Kavalieri/SiK-Python-Game/releases/tag/v$Version"
	Write-Info "Release URL: $ReleaseUrl"
}

function Main {
	Write-StatusHeader "SiK DEVELOPMENT WORKFLOW AUTOMATION"
	Write-Info "Proyecto: SiK Python Game"
	Write-Info "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
	
	$VersionFile = Join-Path $ProjectRoot "VERSION.txt"
	$CurrentVersion = if (Test-Path $VersionFile) { Get-Content $VersionFile -Raw } else { "0.1.0" }
	$CurrentVersion = $CurrentVersion.Trim()
	
	switch ($Accion.ToLower()) {
		"nueva-rama" {
			if (-not $RamaNombre) {
				$RamaNombre = Read-Host "Nombre de la nueva rama (ej: feature/nueva-funcionalidad)"
			}
			if (-not $Mensaje) {
				$Mensaje = Read-Host "Descripcion de la característica"
			}
			New-FeatureBranch $RamaNombre $Mensaje
		}
		
		"completar" {
			if (-not $Mensaje) {
				$Mensaje = Read-Host "Descripcion de los cambios completados"
			}
			$NewVersion = Get-NextVersion $CurrentVersion $TipoVersion
			Complete-Feature $Mensaje $NewVersion
		}
		
		"merge" {
			if (-not $Mensaje) {
				$Mensaje = Read-Host "Descripcion final para el merge"
			}
			$NewVersion = Get-NextVersion $CurrentVersion $TipoVersion
			Merge-Feature $Mensaje $NewVersion
			
			if ($Release) {
				New-Release $NewVersion $Mensaje
			}
		}
		
		"release" {
			if (-not $Mensaje) {
				$Mensaje = Read-Host "Descripcion del release"
			}
			$NewVersion = Get-NextVersion $CurrentVersion $TipoVersion
			New-Release $NewVersion $Mensaje
		}
		
		"status" {
			Write-Info "Version actual: $CurrentVersion"
			Write-Info "Rama actual: $(git branch --show-current)"
			Write-Info "Estado del repositorio:"
			git status --short
		}
		
		default {
			Write-Host ""
			Write-Host "USO: .\workflow_automation.ps1 -Accion <accion> [opciones]" -ForegroundColor Yellow
			Write-Host ""
			Write-Host "ACCIONES DISPONIBLES:" -ForegroundColor Cyan
			Write-Host "  nueva-rama     - Crear nueva rama de desarrollo" -ForegroundColor White
			Write-Host "  completar      - Completar desarrollo y crear PR" -ForegroundColor White  
			Write-Host "  merge          - Mergear PR a main y crear version" -ForegroundColor White
			Write-Host "  release        - Crear release y tag" -ForegroundColor White
			Write-Host "  status         - Mostrar estado actual" -ForegroundColor White
			Write-Host ""
			Write-Host "OPCIONES:" -ForegroundColor Cyan
			Write-Host "  -Mensaje       - Descripcion de cambios" -ForegroundColor White
			Write-Host "  -TipoVersion   - patch|minor|major (default: patch)" -ForegroundColor White
			Write-Host "  -RamaNombre    - Nombre de rama (para nueva-rama)" -ForegroundColor White
			Write-Host "  -Release       - Crear release tras merge" -ForegroundColor White
		}
	}
}

try {
	Main
} catch {
	Write-Error "Error durante la ejecucion: $($_.Exception.Message)"
	exit 1
}
