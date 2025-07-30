# IDENTIFICADOR DE PROBLEMAS DE TERMINAL
# Reproduce escenarios específicos que causan timeouts

Write-Host "IDENTIFICADOR DE PROBLEMAS DE TERMINAL" -ForegroundColor Cyan
Write-Host "======================================"
Write-Host ""

# Test específico del problema reportado
Write-Host "REPRODUCIENDO ESCENARIO PROBLEMÁTICO..." -ForegroundColor Red
Write-Host ""

Write-Host "1. Estado inicial del repositorio:"
git status --short

Write-Host "`n2. Intentando pre-commit en TODOS los archivos..."
Write-Host "   (Este es el comando que típicamente causa problemas)"

# El comando específico que suele fallar
Write-Host "`n   Ejecutando: poetry run pre-commit run --all-files"
poetry run pre-commit run --all-files

Write-Host "`n3. Estado después de pre-commit:"
git status --short

Write-Host "`n4. Test de comando que puede causar problemas con scripts:"
.\scripts\simple_commit.ps1 "test de problema" 2>&1

Write-Host "`nTEST COMPLETADO - ¿Se produjo algún timeout o bloqueo?"
