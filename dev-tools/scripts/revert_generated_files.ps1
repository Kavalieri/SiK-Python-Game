# Script para revertir archivos generados o modificados debido a caché

# Cambiar al directorio raíz del repositorio
Set-Location -Path "e:\GitHub\SiK-Python-Game"

# Detectar archivos no rastreados
Write-Host "Detectando archivos no rastreados..." -ForegroundColor Yellow
$untrackedFiles = git ls-files --others --exclude-standard

if ($untrackedFiles) {
    Write-Host "Archivos no rastreados detectados:" -ForegroundColor Cyan
    $untrackedFiles | ForEach-Object { Write-Host $_ }

    # Eliminar archivos no rastreados
    Write-Host "Eliminando archivos no rastreados..." -ForegroundColor Yellow
    $untrackedFiles | ForEach-Object { Remove-Item -Path $_ -Force }
    Write-Host "Archivos no rastreados eliminados." -ForegroundColor Green
} else {
    Write-Host "No se detectaron archivos no rastreados." -ForegroundColor Green
}

# Detectar archivos modificados
Write-Host "Detectando archivos modificados..." -ForegroundColor Yellow
$modifiedFiles = git diff --name-only

if ($modifiedFiles) {
    Write-Host "Archivos modificados detectados:" -ForegroundColor Cyan
    $modifiedFiles | ForEach-Object { Write-Host $_ }

    # Revertir cambios en archivos modificados
    Write-Host "Revirtiendo cambios en archivos modificados..." -ForegroundColor Yellow
    git restore $modifiedFiles
    Write-Host "Cambios revertidos." -ForegroundColor Green
} else {
    Write-Host "No se detectaron archivos modificados." -ForegroundColor Green
}

Write-Host "Proceso completado." -ForegroundColor Green
