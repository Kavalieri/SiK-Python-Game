# Quick Commit - PowerShell
# Commit rapido respetando pre-commit hooks sin limpieza exhaustiva de cache

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

function Invoke-QuickCommit {
    param([string]$CommitMessage)

    Write-Host "COMMIT RAPIDO" -ForegroundColor Cyan
    Write-Host "Respetando pre-commit hooks..." -ForegroundColor White
    Write-Host ("=" * 50)

    try {
        # Verificar cambios
        $status = git status --porcelain
        if (-not $status) {
            Write-Host "No hay cambios para commitear" -ForegroundColor Yellow
            return $true
        }

        # Mostrar resumen
        $lines = $status -split "`n"
        $count = $lines.Count
        Write-Host "$count cambios detectados" -ForegroundColor Blue

        # Agregar cambios
        Write-Host "Agregando cambios..." -ForegroundColor Blue
        git add .
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error agregando cambios" -ForegroundColor Red
            return $false
        }

        # Commit con hooks
        Write-Host "Ejecutando commit..." -ForegroundColor Blue
        git commit -m $CommitMessage
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error en commit" -ForegroundColor Red
            return $false
        }

        # Obtener hash
        $hash = git rev-parse HEAD
        $shortHash = $hash.Substring(0, 8)
        Write-Host "Commit exitoso: $shortHash" -ForegroundColor Green

        return $true

    } catch {
        Write-Host "Error: $_" -ForegroundColor Red
        return $false
    }
}

# Ejecutar
$success = Invoke-QuickCommit -CommitMessage $Message

Write-Host ""
Write-Host ("=" * 50)
if ($success) {
    Write-Host "COMMIT COMPLETADO" -ForegroundColor Green
} else {
    Write-Host "COMMIT FALLO" -ForegroundColor Red
}
Write-Host ("=" * 50)

exit $(if ($success) { 0 } else { 1 })
