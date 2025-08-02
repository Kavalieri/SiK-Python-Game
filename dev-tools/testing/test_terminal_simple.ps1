# Diagnóstico Terminal Simple - SiK Python Game
# Identifica problemas específicos con timeouts y bloqueos

Write-Host "🔍 DIAGNÓSTICO TERMINAL SIMPLE" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Información básica
Write-Host "`n📊 INFORMACIÓN BÁSICA:" -ForegroundColor Yellow
Write-Host "PowerShell: $($PSVersionTable.PSVersion)"
Write-Host "Directorio: $(Get-Location)"
Write-Host "Usuario: $env:USERNAME"
Write-Host "Fecha: $(Get-Date)"

# Test 1: Comandos básicos
Write-Host "`n✅ TEST 1: Comandos básicos" -ForegroundColor Green
try {
    $result1 = echo "test"
    Write-Host "Echo: OK - $result1"
} catch {
    Write-Host "Echo: ERROR - $_" -ForegroundColor Red
}

try {
    $result2 = Get-Date
    Write-Host "Get-Date: OK - $result2"
} catch {
    Write-Host "Get-Date: ERROR - $_" -ForegroundColor Red
}

# Test 2: Poetry
Write-Host "`n🐍 TEST 2: Poetry" -ForegroundColor Green
try {
    $poetryVersion = poetry --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Poetry: OK - $poetryVersion"
    } else {
        Write-Host "Poetry: ERROR - Exit code $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "Poetry: EXCEPTION - $_" -ForegroundColor Red
}

# Test 3: Pre-commit (el problemático)
Write-Host "`n🧪 TEST 3: Pre-commit" -ForegroundColor Green
try {
    Write-Host "Probando pre-commit version..."
    $precommitVersion = poetry run pre-commit --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pre-commit version: OK - $precommitVersion"
    } else {
        Write-Host "Pre-commit version: ERROR - Exit code $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "Pre-commit: EXCEPTION - $_" -ForegroundColor Red
}

# Test 4: Git
Write-Host "`n🔧 TEST 4: Git" -ForegroundColor Green
try {
    $gitVersion = git --version
    Write-Host "Git: OK - $gitVersion"

    $gitStatus = git status --porcelain
    $changeCount = if ($gitStatus) { ($gitStatus -split "`n").Count } else { 0 }
    Write-Host "Git status: OK - $changeCount cambios"
} catch {
    Write-Host "Git: ERROR - $_" -ForegroundColor Red
}

# Test 5: GitHub CLI
Write-Host "`n🌐 TEST 5: GitHub CLI" -ForegroundColor Green
try {
    $ghVersion = gh --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "GitHub CLI: OK"
    } else {
        Write-Host "GitHub CLI: No disponible" -ForegroundColor Yellow
    }
} catch {
    Write-Host "GitHub CLI: ERROR - $_" -ForegroundColor Red
}

# Test crítico: el que suele fallar
Write-Host "`n⚠️  TEST CRÍTICO: Pre-commit run (simulado)" -ForegroundColor Red
Write-Host "Este es el comando que típicamente causa problemas..."

# Simular sin ejecutar el comando completo
Write-Host "Comando que probaríamos: poetry run pre-commit run --all-files"
Write-Host "Estado: SIMULADO (no ejecutado para evitar bloqueo)"

# Variables de entorno críticas
Write-Host "`n🔧 VARIABLES DE ENTORNO:" -ForegroundColor Green
$vars = @("PATH", "PYTHONPATH", "VIRTUAL_ENV", "POETRY_CACHE_DIR")
foreach ($var in $vars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        $short = if ($value.Length -gt 80) { "$($value.Substring(0, 80))..." } else { $value }
        Write-Host "$var = $short"
    } else {
        Write-Host "$var = (no definida)" -ForegroundColor Yellow
    }
}

Write-Host "`n✅ DIAGNÓSTICO COMPLETADO" -ForegroundColor Green
Write-Host "Si algún test falló, ese es probablemente el problema."
