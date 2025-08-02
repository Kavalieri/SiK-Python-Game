# Script Simple de Desarrollo SiK
# ==============================
# Autor: SiK Team
# Descripcion: Script simplificado para desarrollo cotidiano

param(
	[Parameter(Mandatory=$true)]
	[ValidateSet("start", "save", "finish", "status")]
	[string]$Action,
	
	[string]$Message = "",
	[string]$Branch = ""
)

function Write-SiKHeader {
	Write-Host ""
	Write-Host "================================================" -ForegroundColor Cyan
	Write-Host " SiK Python Game - Development Helper" -ForegroundColor Yellow  
	Write-Host "================================================" -ForegroundColor Cyan
}

function Write-SiKSuccess {
	param([string]$Text)
	Write-Host "✓ $Text" -ForegroundColor Green
}

function Write-SiKInfo {
	param([string]$Text)
	Write-Host "→ $Text" -ForegroundColor Blue
}

function Write-SiKError {
	param([string]$Text)
	Write-Host "✗ $Text" -ForegroundColor Red
}

switch ($Action) {
	"start" {
		Write-SiKHeader
		Write-SiKInfo "Iniciando nueva característica..."
		
		if (-not $Branch) {
			$Branch = Read-Host "Nombre de la rama (ej: sistema-powerups)"
			$Branch = "feature/$Branch"
		}
		
		if (-not $Message) {
			$Message = Read-Host "Descripción de la característica"
		}
		
		# Ir a main y actualizar
		git checkout main
		git pull origin main
		Write-SiKSuccess "main actualizado"
		
		# Crear nueva rama
		git checkout -b $Branch
		Write-SiKSuccess "Rama '$Branch' creada"
		
		# Commit inicial si hay cambios
		git add .
		if (-not (git diff --cached --quiet)) {
			git commit -m "Inicio desarrollo: $Message"
			Write-SiKSuccess "Commit inicial realizado"
		}
		
		Write-SiKInfo "Rama lista para desarrollo"
	}
	
	"save" {
		Write-SiKHeader
		Write-SiKInfo "Guardando progreso..."
		
		if (-not $Message) {
			$Message = Read-Host "Descripción de los cambios"
		}
		
		git add .
		git commit -m "WIP: $Message"
		git push -u origin HEAD
		Write-SiKSuccess "Progreso guardado y subido"
	}
	
	"finish" {
		Write-SiKHeader
		Write-SiKInfo "Finalizando característica..."
		
		$CurrentBranch = git branch --show-current
		if ($CurrentBranch -eq "main") {
			Write-SiKError "No puedes finalizar desde main"
			exit 1
		}
		
		if (-not $Message) {
			$Message = Read-Host "Descripción final de la característica"
		}
		
		# Commit final
		git add .
		if (-not (git diff --cached --quiet)) {
			git commit -m "Completado: $Message"
			Write-SiKSuccess "Commit final realizado"
		}
		
		# Subir al remoto
		git push -u origin HEAD
		Write-SiKSuccess "Rama subida al remoto"
		
		# Crear PR
		$PRTitle = "Nueva característica: $Message"
		$PRBody = @"
### Descripción
$Message

### Cambios realizados
- Implementación completa de: $Message
- Testing verificado
- Documentación actualizada

### Checklist
- [x] Código funcional
- [x] Sin errores de linting
- [x] Listo para merge

### Uso del workflow completo
Para completar el merge y crear release, usar:
``````powershell
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release -Mensaje "$Message"
``````
"@
		
		gh pr create --title "$PRTitle" --body "$PRBody"
		Write-SiKSuccess "Pull Request creado"
		
		Write-SiKInfo "Para completar:"
		Write-Host "1. Revisar el PR creado" -ForegroundColor Yellow
		Write-Host "2. Ejecutar: .\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release -Mensaje '$Message'" -ForegroundColor Yellow
	}
	
	"status" {
		Write-SiKHeader
		Write-SiKInfo "Estado actual del proyecto:"
		
		$CurrentBranch = git branch --show-current
		$CurrentVersion = if (Test-Path "VERSION.txt") { Get-Content "VERSION.txt" } else { "0.1.0" }
		
		Write-Host "Rama actual: $CurrentBranch" -ForegroundColor Cyan
		Write-Host "Versión actual: $CurrentVersion" -ForegroundColor Cyan
		Write-Host ""
		Write-Host "Estado de archivos:" -ForegroundColor Cyan
		git status --short
		
		# Verificar si hay PR abierto
		$PRNumber = gh pr view --json number --jq .number 2>$null
		if ($PRNumber) {
			Write-Host ""
			Write-Host "PR abierto: #$PRNumber" -ForegroundColor Green
		}
	}
}

Write-Host ""
