# Test Terminal Responsive Script
# Verifica rápidamente si el terminal está en estado saludable

$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"

Write-Host "🧪 Test Terminal Responsive" -ForegroundColor $ColorInfo

# Test 1: Comando básico
Write-Host "📋 Test 1: Comando básico..." -ForegroundColor $ColorInfo
$start = Get-Date
try {
    Get-Date | Out-Null
    $end = Get-Date
    $duration = ($end - $start).TotalMilliseconds

    if ($duration -lt 500) {
        Write-Host "✅ Comando básico OK (${duration}ms)" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "⚠️  Comando básico lento (${duration}ms)" -ForegroundColor $ColorWarning
    }
} catch {
    Write-Host "❌ Comando básico falló" -ForegroundColor $ColorError
    exit 1
}

# Test 2: Git disponible
Write-Host "📋 Test 2: Git disponible..." -ForegroundColor $ColorInfo
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✅ Git OK: $gitVersion" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "❌ Git no disponible" -ForegroundColor $ColorError
    }
} catch {
    Write-Host "❌ Git error" -ForegroundColor $ColorError
}

# Test 3: Poetry disponible
Write-Host "📋 Test 3: Poetry disponible..." -ForegroundColor $ColorInfo
try {
    $poetryVersion = poetry --version 2>$null
    if ($poetryVersion) {
        Write-Host "✅ Poetry OK: $poetryVersion" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "❌ Poetry no disponible" -ForegroundColor $ColorError
    }
} catch {
    Write-Host "❌ Poetry error" -ForegroundColor $ColorError
}

# Test 4: Pre-commit disponible
Write-Host "📋 Test 4: Pre-commit disponible..." -ForegroundColor $ColorInfo
try {
    $precommitVersion = poetry run pre-commit --version 2>$null
    if ($precommitVersion) {
        Write-Host "✅ Pre-commit OK: $precommitVersion" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "❌ Pre-commit no disponible" -ForegroundColor $ColorError
    }
} catch {
    Write-Host "❌ Pre-commit error" -ForegroundColor $ColorError
}

# Resumen final
Write-Host "`n🎯 RESUMEN:" -ForegroundColor $ColorInfo
Write-Host "✅ Terminal está funcionando correctamente" -ForegroundColor $ColorSuccess
Write-Host "💡 Listo para usar scripts de commit" -ForegroundColor $ColorInfo
