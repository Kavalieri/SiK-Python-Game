# Test Terminal ASCII Safe
# Script simple para verificar terminal sin caracteres Unicode

Write-Host "=== TERMINAL TEST ===" -ForegroundColor Cyan

# Test 1: Comando basico
Write-Host "Test 1: Comando basico" -ForegroundColor Green
$start = Get-Date
Get-Date | Out-Null
$end = Get-Date
$duration = ($end - $start).TotalMilliseconds
Write-Host "Duracion: ${duration}ms"

# Test 2: Git
Write-Host "Test 2: Git" -ForegroundColor Green
try {
    $gitResult = git --version
    Write-Host "Git OK: $gitResult"
} catch {
    Write-Host "Git ERROR" -ForegroundColor Red
}

# Test 3: Poetry
Write-Host "Test 3: Poetry" -ForegroundColor Green
try {
    $poetryResult = poetry --version
    Write-Host "Poetry OK: $poetryResult"
} catch {
    Write-Host "Poetry ERROR" -ForegroundColor Red
}

# Test 4: Pre-commit
Write-Host "Test 4: Pre-commit" -ForegroundColor Green
try {
    $precommitResult = poetry run pre-commit --version
    Write-Host "Pre-commit OK: $precommitResult"
} catch {
    Write-Host "Pre-commit ERROR" -ForegroundColor Red
}

Write-Host "=== TEST COMPLETADO ===" -ForegroundColor Cyan
