# Guía de Commits Profesionales - SiK Python Game

## 🎯 Objetivo
Establecer un sistema profesional, controlado y documentado para commits y push usando las herramientas disponibles.

## 🛠️ Herramientas Utilizadas

### Configuración Base
- **Git CLI** con template de commits
- **Pre-commit hooks** para validación automática
- **Conventional Commits** en español
- **GitHub CLI** para operaciones avanzadas - [Manual oficial](https://cli.github.com/manual/)
- **Script PowerShell** personalizado para workflow
- **Matriz de decisión**: `docs/MATRIZ_DECISIÓN_GH_VS_GIT.md` para optimización

## 📋 Tipos de Commit

### Tipos Principales (en español)
```
feat     - Nueva funcionalidad
fix      - Corrección de bug
docs     - Cambios en documentación
style    - Cambios de formato (no afectan lógica)
refactor - Refactorización de código
test     - Añadir o modificar tests
chore    - Tareas de mantenimiento
perf     - Mejoras de rendimiento
```

### Ámbitos del Proyecto
```
core      - Motor del juego, gestores principales
entities  - Jugador, enemigos, proyectiles
scenes    - Menús, gameplay, transiciones
ui        - HUD, menús, componentes visuales
utils     - Utilidades, helpers, configuración
config    - Archivos de configuración JSON
assets    - Recursos gráficos y sonoros
docs      - Documentación del proyecto
```

## 🚀 Workflows Disponibles

### 1. Commit Manual Profesional con GitHub CLI
```powershell
# Verificar estado del repositorio (PREFERIR gh sobre git)
gh repo view --json name,description,pushedAt
gh issue list --state open

# Ejecutar validaciones
poetry run pre-commit run --all-files

# Commit con template
git add .
git commit
# (Se abre editor con template de .gitmessage)

# Push y crear PR si necesario
git push origin main
gh pr create --title "feat: nueva funcionalidad" --body "Descripción detallada"
```

### 2. Script Automatizado
```powershell
# Commit básico
.\scripts\commit_profesional.ps1 -Mensaje "añade sistema de enemigos"

# Commit con tipo y ámbito específico
.\scripts\commit_profesional.ps1 -Tipo "feat" -Ambito "entities" -Mensaje "añade detección de colisiones"

# Commit con push automático
.\scripts\commit_profesional.ps1 -Mensaje "corrige error de memoria" -Tipo "fix" -Push

# Forzar commit (saltear pre-commit si necesario)
.\scripts\commit_profesional.ps1 -Mensaje "hotfix crítico" -Force -Push
```

### 3. GitHub CLI Avanzado
```powershell
# Crear issue automático para bug
gh issue create --title "Bug: Error en carga de assets" --body "Descripción detallada"

# Commit y crear PR automático
git commit -m "fix(assets): corrige error de carga de texturas"
git push origin main
gh pr create --title "Corrección de assets" --body "Detalles de la corrección"

# Release automatizado
gh release create v0.2.0 --title "Nueva versión estable" --notes-file CHANGELOG.md

# Búsqueda con PowerShell (NO usar grep)
git log --oneline | Select-String "feat"
Get-Content CHANGELOG.md | Select-String "v0.2"
```

## ✅ Validaciones Automáticas

### Pre-commit Hooks Activos
1. **Ruff** - Linting y formateo automático
2. **Trailing whitespace** - Elimina espacios finales
3. **End of file fixer** - Asegura nueva línea al final
4. **YAML check** - Valida archivos de configuración
5. **Large files check** - Previene archivos >50MB
6. **Merge conflict check** - Detecta conflictos no resueltos
7. **Debug statements** - Detecta prints/debugs olvidados

### Validaciones del Script
- ✅ **Verificación de repositorio Git**
- ✅ **Ejecución de pre-commit hooks**
- ✅ **Confirmación del usuario**
- ✅ **Construcción automática del mensaje**
- ✅ **Información detallada del commit**

## 📊 Ejemplos de Commits Profesionales

### Buenos Ejemplos
```
feat(entities): añade sistema de IA para enemigos zombie
fix(ui): corrige error de superposición en menú principal
refactor(core): divide asset_manager.py según límite 150 líneas
docs: actualiza FUNCIONES_DOCUMENTADAS.md con nuevas APIs
perf(utils): optimiza carga de texturas en AssetManager
test(entities): añade tests unitarios para sistema de colisiones
chore: actualiza dependencias de pygame-ce a v2.4.1
```

### Template Completo
```
feat(entities): añade sistema de detección de colisiones

Implementa detección de colisiones robusta entre jugador y enemigos
usando algoritmo AABB optimizado. Incluye sistema de invencibilidad
temporal y feedback visual para el jugador.

Closes #45
```

## 🔄 Proceso Recomendado

### Para Cambios Pequeños (< 5 archivos)
1. `gh repo view` - Verificar estado general del repositorio
2. `poetry run pre-commit run --all-files` - Validar calidad
3. `git add .` - Añadir cambios
4. `git commit` - Usar template interactivo
5. `git push origin main` - Push controlado
6. `gh issue create` - Crear issue de seguimiento si necesario

### Para Refactorizaciones Grandes
1. Usar script automatizado con confirmación
2. `gh issue create` - Crear issue de seguimiento
3. Commits atómicos por responsabilidad
4. `gh pr create` - PR opcional para revisión

### Para Releases
1. Actualizar `CHANGELOG.md`
2. Commit de preparación
3. `gh release create` con notas automáticas
4. Tag semántico (v0.2.0, v0.2.1, etc.)

## 🎯 Beneficios del Sistema

✅ **Trazabilidad completa** - Historial claro y profesional
✅ **Calidad garantizada** - Validaciones automáticas
✅ **Productividad** - Scripts automatizados
✅ **Documentación automática** - Enlaces a issues y PRs
✅ **Rollback seguro** - Commits atómicos y bien documentados
✅ **Colaboración** - Estándares claros para todo el equipo

---

**Usar este sistema para todos los commits del proyecto SiK Python Game**
