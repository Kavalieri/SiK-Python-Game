# SiK Development Checklist Generator
# ===================================
# Autor: SiK Team
# Descripcion: Genera checklist automatico para cada rama segun el tipo de cambio

param(
    [Parameter(Mandatory=$true)]
    [string]$TipoCambio,
    [Parameter(Mandatory=$true)]
    [string]$RamaNombre,
    [Parameter(Mandatory=$true)]
    [string]$Descripcion
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

function New-Checklist {
    param([string]$Tipo, [string]$Rama, [string]$Desc)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $checklistContent = @"
# Checklist de Desarrollo - $Rama
## Generado: $timestamp
## Tipo: $Tipo
## Descripcion: $Desc

### FASE 1: PLANIFICACION
- [ ] Analizar impacto del cambio
- [ ] Revisar dependencias afectadas
- [ ] Verificar compatibilidad con version actual
- [ ] Documentar enfoque de implementacion

### FASE 2: DESARROLLO
"@

    # Checklist especifico por tipo
    switch ($Tipo) {
        "feature" {
            $checklistContent += @"

- [ ] Implementar funcionalidad principal
- [ ] Crear tests unitarios
- [ ] Verificar integracion con sistema existente
- [ ] Actualizar documentacion de API
- [ ] Probar edge cases
- [ ] Verificar performance
"@
        }
        "bugfix" {
            $checklistContent += @"

- [ ] Reproducir el bug consistentemente
- [ ] Identificar causa raiz
- [ ] Implementar solucion minima
- [ ] Crear test de regresion
- [ ] Verificar que no introduce nuevos bugs
- [ ] Probar en diferentes escenarios
"@
        }
        "hotfix" {
            $checklistContent += @"

- [ ] Confirmar criticidad del issue
- [ ] Implementar solucion rapida y segura
- [ ] Test de regresion inmediato
- [ ] Verificar que no rompe funcionalidad critica
- [ ] Preparar rollback plan
- [ ] Documentar para post-mortem
"@
        }
        "docs" {
            $checklistContent += @"

- [ ] Revisar claridad y precision
- [ ] Verificar enlaces y referencias
- [ ] Comprobar formato y estructura
- [ ] Actualizar tabla de contenidos si aplica
- [ ] Revisar ortografia y gramatica
"@
        }
        "dev-tools" {
            $checklistContent += @"

- [ ] Probar script/herramienta funciona correctamente
- [ ] Verificar compatibilidad con entorno actual
- [ ] Documentar uso y parametros
- [ ] Comprobar que no afecta flujo existente
- [ ] Actualizar documentacion de desarrollo
"@
        }
        "config" {
            $checklistContent += @"

- [ ] Validar sintaxis de configuracion
- [ ] Probar en entorno de desarrollo
- [ ] Verificar backward compatibility
- [ ] Documentar cambios en configuracion
- [ ] Considerar migracion de configuraciones existentes
"@
        }
        default {
            $checklistContent += @"

- [ ] Implementar cambios requeridos
- [ ] Probar funcionalidad
- [ ] Verificar que no rompe codigo existente
- [ ] Actualizar documentacion relevante
"@
        }
    }

    $checklistContent += @"


### FASE 3: VALIDACION
- [ ] Ejecutar todos los tests
- [ ] Verificar 0 errores de linting (Ruff)
- [ ] Confirmar 0 warnings de MyPy
- [ ] Probar en entorno limpio
- [ ] Validar con poetry run python src/main.py
- [ ] Revisar logs por errores o warnings

### FASE 4: DOCUMENTACION
- [ ] Actualizar CHANGELOG.md (automatico)
- [ ] Documentar cambios en docs/registro/
- [ ] Actualizar README si es necesario
- [ ] Revisar que documentacion API esta actualizada

### FASE 5: REVISION FINAL
- [ ] Codigo cumple convenciones del proyecto
- [ ] Archivos no exceden 250 lineas
- [ ] Nombres de variables/funciones en español
- [ ] Type hints completos
- [ ] Docstrings en español
- [ ] Sin hardcoding (usar configuracion)

### FASE 6: PULL REQUEST
- [ ] Crear PR con template completo
- [ ] Incluir descripcion detallada de cambios
- [ ] Referenciar issues relacionados
- [ ] Solicitar revision de codigo
- [ ] Verificar CI/CD passes

### NOTAS DE DESARROLLO
```
Fecha inicio: $timestamp
Rama: $Rama
Descripcion: $Desc

Observaciones:
- 

Problemas encontrados:
- 

Decisiones tecnicas:
- 

```

### CHECKLIST FINAL ANTES DE MERGE
- [ ] Todos los items anteriores completados
- [ ] PR aprobado por reviewer
- [ ] CI/CD exitoso
- [ ] Tests de integracion pasando
- [ ] Documentacion actualizada
- [ ] Ready para produccion
"@

    return $checklistContent
}

# Generar checklist
$checklist = New-Checklist $TipoCambio $RamaNombre $Descripcion

# Guardar en archivo
$checklistDir = Join-Path $ProjectRoot "tmp"
if (-not (Test-Path $checklistDir)) {
    New-Item -ItemType Directory -Path $checklistDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$fileName = "checklist_$($RamaNombre.Replace('/', '_'))_$timestamp.md"
$checklistPath = Join-Path $checklistDir $fileName

Set-Content -Path $checklistPath -Value $checklist -Encoding UTF8

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host " CHECKLIST GENERADO" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Archivo: $fileName" -ForegroundColor Cyan
Write-Host "Ubicacion: $checklistPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usa este checklist para guiar tu desarrollo:" -ForegroundColor Yellow
Write-Host "- [ ] Marca cada item completado" -ForegroundColor Blue
Write-Host "- [ ] Agrega notas en la seccion correspondiente" -ForegroundColor Blue  
Write-Host "- [ ] Revisa completamente antes del PR" -ForegroundColor Blue
Write-Host ""

return $checklistPath
