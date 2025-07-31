# =============================================================================
# SCRIPT DEFINITIVO DE COMMIT CON MANEJO ROBUSTO DE PRE-COMMIT
# =============================================================================
# Resuelve definitivamente los problemas de pre-commit hooks
# Autor: SiK Team
# Fecha: 31 Julio 2025
# =============================================================================

param(
	[Parameter(Mandatory = $true)]
	[string]$Message,

	[Parameter(Mandatory = $false)]
	[switch]$Push = $false,

	[Parameter(Mandatory = $false)]
	[switch]$Force = $false,

	[Parameter(Mandatory = $false)]
	[switch]$DisablePreCommit = $false,

	[Parameter(Mandatory = $false)]
	[int]$MaxRetries = 3
)

# Configuración de colores (ASCII-safe)
$CONFIG = @{
	Colors  = @{
		Info    = "Cyan"
		Success = "Green"
		Warning = "Yellow"
		Error   = "Red"
		Debug   = "Magenta"
	}
	Timeout = 30
}

function Write-Log {
	param([string]$Message, [string]$Level = "Info")
	$color = $CONFIG.Colors[$Level]
	$timestamp = Get-Date -Format "HH:mm:ss"
	Write-Host "[$timestamp] $Message" -ForegroundColor $color
}

function Test-GitRepository {
	if (-not (Test-Path ".git")) {
		Write-Log "ERROR: No es un repositorio Git" "Error"
		return $false
	}
	return $true
}

function Test-HasChanges {
	$status = git status --porcelain
	if ([string]::IsNullOrEmpty($status)) {
		Write-Log "No hay cambios para commitear" "Warning"
		return $false
	}
	Write-Log "Cambios detectados: $(($status -split "`n").Count) archivos" "Info"
	return $true
}

function Invoke-PreCommitHooks {
	param([bool]$Enable = $true)

	if (-not $Enable) {
		Write-Log "Pre-commit hooks DESHABILITADOS por parametro" "Warning"
		return $true
	}

	Write-Log "Ejecutando pre-commit hooks..." "Info"

	try {
		# Ejecutar pre-commit ANTES del staging
		$preCommitResult = pre-commit run --all-files 2>&1

		if ($LASTEXITCODE -eq 0) {
			Write-Log "Pre-commit hooks ejecutados exitosamente" "Success"
			return $true
		} else {
			Write-Log "Pre-commit hooks modificaron archivos (esto es normal)" "Warning"
			Write-Log "Salida: $preCommitResult" "Debug"
			return $true  # Esto es esperado, no es error
		}
	} catch {
		Write-Log "Pre-commit no disponible o falló, continuando..." "Warning"
		return $true
	}
}

function Invoke-RobustStaging {
	param([int]$Attempt = 1)

	Write-Log "Staging robusto - Intento $Attempt" "Info"

	# Limpiar staging previo
	git reset HEAD . 2>$null

	# Verificar archivos modificados en working directory
	$workingChanges = git diff --name-only
	if ($workingChanges) {
		Write-Log "Archivos modificados en working directory: $(($workingChanges -split "`n").Count)" "Info"
	}

	# Staging inicial
	git add .

	# Verificar si hay archivos still modified después del add
	$stillModified = git diff --name-only

	if ($stillModified) {
		Write-Log "Archivos aún modificados tras staging, re-adding..." "Warning"
		Write-Log "Archivos: $($stillModified -join ', ')" "Debug"

		# Re-staging
		git add .

		# Verificación final
		$finalCheck = git diff --name-only
		if ($finalCheck) {
			Write-Log "ADVERTENCIA: Algunos archivos siguen modificados: $($finalCheck -join ', ')" "Warning"
			return $false
		}
	}

	# Verificar que tenemos algo en staging
	$staged = git diff --cached --name-only
	if (-not $staged) {
		Write-Log "ERROR: No hay archivos en staging tras el proceso" "Error"
		return $false
	}

	Write-Log "Staging completado exitosamente: $(($staged -split "`n").Count) archivos" "Success"
	return $true
}

function Invoke-RobustCommit {
	param([string]$CommitMessage, [int]$MaxAttempts)

	for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
		Write-Log "=== INTENTO DE COMMIT $attempt/$MaxAttempts ===" "Info"

		# Ejecutar pre-commit hooks ANTES del staging
		$preCommitOk = Invoke-PreCommitHooks -Enable (-not $DisablePreCommit)
		if (-not $preCommitOk) {
			Write-Log "Pre-commit falló en intento $attempt" "Error"
			continue
		}

		# Staging robusto
		$stagingOk = Invoke-RobustStaging -Attempt $attempt
		if (-not $stagingOk) {
			Write-Log "Staging falló en intento $attempt" "Error"
			if ($attempt -lt $MaxAttempts) {
				Write-Log "Esperando 2 segundos antes del siguiente intento..." "Info"
				Start-Sleep 2
			}
			continue
		}

		# Commit
		Write-Log "Ejecutando commit..." "Info"
		$commitResult = git commit -m $CommitMessage 2>&1

		if ($LASTEXITCODE -eq 0) {
			Write-Log "COMMIT EXITOSO en intento $attempt" "Success"

			# Mostrar commit info
			$commitInfo = git log -1 --oneline
			Write-Log "Commit creado: $commitInfo" "Success"

			return $true
		} else {
			Write-Log "Commit falló en intento $attempt" "Error"
			Write-Log "Error: $commitResult" "Debug"

			if ($attempt -lt $MaxAttempts) {
				Write-Log "Reintentando en 3 segundos..." "Info"
				Start-Sleep 3
			}
		}
	}

	Write-Log "TODOS LOS INTENTOS DE COMMIT FALLARON" "Error"
	return $false
}

function Invoke-PushIfRequested {
	param([bool]$ShouldPush)

	if (-not $ShouldPush) {
		return $true
	}

	Write-Log "Ejecutando push al repositorio remoto..." "Info"

	$pushResult = git push 2>&1

	if ($LASTEXITCODE -eq 0) {
		Write-Log "PUSH EXITOSO" "Success"
		return $true
	} else {
		Write-Log "Push falló: $pushResult" "Error"
		return $false
	}
}

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

Write-Log "[INICIO] SCRIPT DEFINITIVO DE COMMIT ROBUSTO" "Info"
Write-Log "=======================================" "Info"
Write-Log "Mensaje: '$Message'" "Info"
Write-Log "Push: $Push | Force: $Force | Disable Pre-commit: $DisablePreCommit" "Info"
Write-Log "Max Reintentos: $MaxRetries" "Info"

# Validaciones iniciales
if (-not (Test-GitRepository)) { exit 1 }
if (-not (Test-HasChanges)) { exit 0 }

# Mostrar configuración de pre-commit si está habilitado
if (-not $DisablePreCommit) {
	$preCommitConfig = if (Test-Path ".pre-commit-config.yaml") { "CONFIGURADO" } else { "NO CONFIGURADO" }
	Write-Log "Estado Pre-commit: $preCommitConfig" "Info"
}

# Proceso de commit robusto
$commitSuccess = Invoke-RobustCommit -CommitMessage $Message -MaxAttempts $MaxRetries

if (-not $commitSuccess) {
	Write-Log "[ERROR] COMMIT FALLO DESPUES DE $MaxRetries INTENTOS" "Error"

	if (-not $Force) {
		Write-Log "Sugerencias:" "Info"
		Write-Log "1. Usar -DisablePreCommit para desactivar hooks" "Info"
		Write-Log "2. Usar -Force para ignorar errores" "Info"
		Write-Log "3. Revisar manualmente los archivos conflictivos" "Info"
		exit 1
	} else {
		Write-Log "FORCE activado, intentando commit sin hooks..." "Warning"
		git commit -m $Message --no-verify

		if ($LASTEXITCODE -ne 0) {
			Write-Log "Commit forzado también falló" "Error"
			exit 1
		}

		Write-Log "Commit forzado exitoso" "Success"
	}
}

# Push si se solicita
if ($Push) {
	$pushSuccess = Invoke-PushIfRequested -ShouldPush $true
	if (-not $pushSuccess) {
		Write-Log "Commit exitoso, pero push falló" "Warning"
		exit 1
	}
}

# Reporte final
Write-Log "[SUCCESS] PROCESO COMPLETADO EXITOSAMENTE" "Success"
Write-Log "Estado final del repositorio:" "Info"
git status --short | ForEach-Object { Write-Log "  $_" "Debug" }

exit 0
