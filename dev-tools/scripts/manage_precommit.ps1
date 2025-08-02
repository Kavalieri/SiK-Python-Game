# =============================================================================
# SCRIPT PARA GESTIÓN DE PRE-COMMIT HOOKS
# =============================================================================
# Permite habilitar/deshabilitar/desinstalar pre-commit según necesidades
# Autor: SiK Team
# Fecha: 31 Julio 2025
# =============================================================================

param(
	[Parameter(Mandatory = $true)]
	[ValidateSet("status", "disable", "enable", "uninstall", "reinstall")]
	[string]$Action,

	[Parameter(Mandatory = $false)]
	[switch]$Force = $false
)

$CONFIG = @{
	Colors = @{
		Info    = "Cyan"
		Success = "Green"
		Warning = "Yellow"
		Error   = "Red"
		Debug   = "Magenta"
	}
}

function Write-Log {
	param([string]$Message, [string]$Level = "Info")
	$color = $CONFIG.Colors[$Level]
	$timestamp = Get-Date -Format "HH:mm:ss"
	Write-Host "[$timestamp] $Message" -ForegroundColor $color
}

function Get-PreCommitStatus {
	Write-Log "=== ESTADO ACTUAL DE PRE-COMMIT ===" "Info"

	# Verificar instalación
	try {
		$version = pre-commit --version 2>$null
		Write-Log "Pre-commit instalado: $version" "Success"
	} catch {
		Write-Log "Pre-commit NO instalado" "Warning"
		return $false
	}

	# Verificar configuración
	if (Test-Path ".pre-commit-config.yaml") {
		Write-Log "Archivo de configuración: PRESENTE" "Success"

		# Mostrar hooks configurados
		$config = Get-Content ".pre-commit-config.yaml" | Out-String
		$hooks = ($config | Select-String "- id:" | ForEach-Object { $_.Line.Trim() }) -join ", "
		Write-Log "Hooks configurados: $hooks" "Info"
	} else {
		Write-Log "Archivo de configuración: NO ENCONTRADO" "Warning"
	}

	# Verificar hooks instalados
	try {
		$null = pre-commit install --install-hooks --dry-run 2>&1
		if ($LASTEXITCODE -eq 0) {
			Write-Log "Hooks instalados en .git/hooks" "Success"
		} else {
			Write-Log "Hooks NO instalados en .git/hooks" "Warning"
		}
	} catch {
		Write-Log "No se pudo verificar estado de hooks" "Warning"
	}

	return $true
}

function Disable-PreCommit {
	Write-Log "=== DESHABILITANDO PRE-COMMIT ===" "Warning"

	try {
		# Desinstalar hooks de git
		pre-commit uninstall
		Write-Log "Hooks removidos de .git/hooks" "Success"

		# Renombrar configuración (backup)
		if (Test-Path ".pre-commit-config.yaml") {
			Move-Item ".pre-commit-config.yaml" ".pre-commit-config.yaml.disabled"
			Write-Log "Configuración respaldada como .pre-commit-config.yaml.disabled" "Success"
		}

		Write-Log "Pre-commit DESHABILITADO exitosamente" "Success"
		Write-Log "Los commits ahora se ejecutarán sin hooks" "Info"

	} catch {
		Write-Log "Error deshabilitando pre-commit: $_" "Error"
		return $false
	}

	return $true
}

function Enable-PreCommit {
	Write-Log "=== HABILITANDO PRE-COMMIT ===" "Info"

	try {
		# Restaurar configuración si existe backup
		if (Test-Path ".pre-commit-config.yaml.disabled") {
			Move-Item ".pre-commit-config.yaml.disabled" ".pre-commit-config.yaml"
			Write-Log "Configuración restaurada desde backup" "Success"
		}

		if (-not (Test-Path ".pre-commit-config.yaml")) {
			Write-Log "ERROR: No hay archivo de configuración para habilitar" "Error"
			return $false
		}

		# Instalar hooks
		pre-commit install --install-hooks
		Write-Log "Hooks instalados en .git/hooks" "Success"

		Write-Log "Pre-commit HABILITADO exitosamente" "Success"

	} catch {
		Write-Log "Error habilitando pre-commit: $_" "Error"
		return $false
	}

	return $true
}

function Uninstall-PreCommit {
	Write-Log "=== DESINSTALANDO PRE-COMMIT COMPLETAMENTE ===" "Error"

	if (-not $Force) {
		Write-Log "Esta acción eliminará pre-commit permanentemente" "Warning"
		Write-Log "Usa -Force para confirmar la desinstalación" "Warning"
		return $false
	}

	try {
		# Desinstalar hooks
		if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
			pre-commit uninstall 2>$null
			Write-Log "Hooks removidos de .git/hooks" "Success"
		}

		# Backup de configuración
		if (Test-Path ".pre-commit-config.yaml") {
			Copy-Item ".pre-commit-config.yaml" ".pre-commit-config.yaml.backup"
			Remove-Item ".pre-commit-config.yaml"
			Write-Log "Configuración respaldada y removida" "Success"
		}

		# Desinstalar pre-commit del entorno
		Write-Log "Desinstalando pre-commit de Poetry..." "Info"
		poetry remove pre-commit --group dev

		Write-Log "PRE-COMMIT DESINSTALADO COMPLETAMENTE" "Success"
		Write-Log "Backup guardado en .pre-commit-config.yaml.backup" "Info"

	} catch {
		Write-Log "Error desinstalando pre-commit: $_" "Error"
		return $false
	}

	return $true
}

function Restore-PreCommit {
	Write-Log "=== REINSTALANDO PRE-COMMIT ===" "Info"

	try {
		# Instalar pre-commit
		Write-Log "Instalando pre-commit en Poetry..." "Info"
		poetry add pre-commit --group dev

		# Restaurar configuración si existe backup
		if (Test-Path ".pre-commit-config.yaml.backup") {
			Copy-Item ".pre-commit-config.yaml.backup" ".pre-commit-config.yaml"
			Write-Log "Configuración restaurada desde backup" "Success"
		}

		# Instalar hooks
		if (Test-Path ".pre-commit-config.yaml") {
			pre-commit install --install-hooks
			Write-Log "Hooks instalados exitosamente" "Success"
		} else {
			Write-Log "No hay configuración, pre-commit instalado pero sin hooks" "Warning"
		}

		Write-Log "PRE-COMMIT REINSTALADO EXITOSAMENTE" "Success"

	} catch {
		Write-Log "Error reinstalando pre-commit: $_" "Error"
		return $false
	}

	return $true
}

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

Write-Log "🔧 GESTOR DE PRE-COMMIT HOOKS" "Info"
Write-Log "============================" "Info"
Write-Log "Acción solicitada: $Action" "Info"

switch ($Action.ToLower()) {
	"status" {
		Get-PreCommitStatus
	}

	"disable" {
		$success = Disable-PreCommit
		if ($success) {
			Write-Log "✅ Pre-commit deshabilitado. Usa 'enable' para reactivar." "Success"
		}
	}

	"enable" {
		$success = Enable-PreCommit
		if ($success) {
			Write-Log "✅ Pre-commit habilitado y listo para usar." "Success"
		}
	}

	"uninstall" {
		$success = Uninstall-PreCommit
		if ($success) {
			Write-Log "✅ Pre-commit desinstalado. Usa 'reinstall' si necesitas restaurarlo." "Success"
		}
	}

	"reinstall" {
		$success = Restore-PreCommit
		if ($success) {
			Write-Log "✅ Pre-commit reinstalado y configurado." "Success"
		}
	}

	default {
		Write-Log "Acción no reconocida: $Action" "Error"
		exit 1
	}
}

Write-Log "Operación completada." "Info"
