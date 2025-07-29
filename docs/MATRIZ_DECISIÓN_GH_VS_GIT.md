# Matriz de Decisión: GitHub CLI vs Git Tradicional

## 🎯 Objetivo
Definir claramente cuándo usar `gh` vs `git` para maximizar eficiencia basándose en la documentación oficial.

## 📖 Fuente
Basado en documentación oficial: https://cli.github.com/manual/

## 🚀 Regla Principal: **SIEMPRE PREFERIR GitHub CLI** cuando sea posible

## 📊 Matriz de Decisión por Tarea

### 🟢 **USAR GitHub CLI (`gh`) - PRIORITARIO**

#### 🏢 **Gestión de Repositorios**
```powershell
# Información del repositorio
gh repo view                    # ✅ Información completa + estadísticas
gh repo view --web             # ✅ Abrir en navegador
gh repo list --limit 10       # ✅ Listar repositorios

# Operaciones de repositorio
gh repo create nuevo-proyecto  # ✅ Crear con configuración automática
gh repo fork owner/repo        # ✅ Fork con configuración remota
gh repo clone owner/repo       # ✅ Clone con configuración automática
gh repo sync                   # ✅ Sincronizar fork con upstream
gh repo rename nuevo-nombre    # ✅ Renombrar con actualización automática
```

#### 🎫 **Issues y Tickets**
```powershell
gh issue list --state open     # ✅ Listar issues con estado
gh issue create --title "Bug"  # ✅ Crear con template
gh issue view 123 --web       # ✅ Ver en navegador
gh issue close 123            # ✅ Cerrar con comentario automático
gh issue comment 123 --body "Texto"  # ✅ Comentar
```

#### 🔄 **Pull Requests**
```powershell
gh pr create --fill            # ✅ Crear con info automática
gh pr list --state open       # ✅ Listar PRs con estado
gh pr checkout 321            # ✅ Checkout con branch automático
gh pr merge 321 --squash      # ✅ Merge con validaciones
gh pr view 321 --web         # ✅ Ver en navegador
gh pr review 321 --approve   # ✅ Review con comentarios
```

#### 📦 **Releases y Distribución**
```powershell
gh release create v1.0.0      # ✅ Crear release
gh release upload v1.0.0 archivo.zip  # ✅ Subir assets
gh release list               # ✅ Listar releases
gh release view v1.0.0 --web # ✅ Ver en navegador
```

#### ⚡ **GitHub Actions**
```powershell
gh workflow list              # ✅ Listar workflows
gh workflow run "CI"          # ✅ Ejecutar workflow manualmente
gh run list --limit 5        # ✅ Ver ejecuciones recientes
gh run view 123456           # ✅ Ver logs de ejecución
```

#### 🔍 **Búsqueda Global**
```powershell
gh search repos "python game" # ✅ Buscar repositorios
gh search code "pygame"       # ✅ Buscar código en GitHub
gh search issues "bug"        # ✅ Buscar issues
gh search prs "feature"       # ✅ Buscar pull requests
```

#### 🌐 **Navegación Rápida**
```powershell
gh browse                     # ✅ Abrir repo en navegador
gh browse --settings          # ✅ Abrir configuración
gh browse 123                 # ✅ Abrir issue/PR específico
```

#### 📋 **Estado y Monitoreo**
```powershell
gh status                     # ✅ Estado de issues y PRs
gh pr status                  # ✅ Estado específico de PRs
gh issue status               # ✅ Estado específico de issues
```

### 🟡 **USAR Git Tradicional - SOLO para Trabajo Local**

#### 📁 **Control de Versiones Local**
```powershell
git add archivo.py            # ✅ Staging de archivos
git add .                     # ✅ Staging de todos los cambios
git commit -m "mensaje"       # ✅ Commit local
git commit --amend            # ✅ Modificar último commit
```

#### 🔄 **Branching Local**
```powershell
git branch feature/nueva      # ✅ Crear branch local
git checkout feature/nueva    # ✅ Cambiar branch
git switch main               # ✅ Cambiar branch (moderno)
git merge feature/nueva       # ✅ Merge local
```

#### 📋 **Estado y Logs Locales**
```powershell
git status                    # ✅ Estado del working directory
git log --oneline -10         # ✅ Log de commits
git diff                      # ✅ Diferencias en working directory
git show HEAD                 # ✅ Ver último commit
```

#### 🏷️ **Tags Locales**
```powershell
git tag v1.0.0                # ✅ Crear tag local
git tag -d v1.0.0             # ✅ Eliminar tag local
```

#### 🔧 **Configuración Local**
```powershell
git config user.name "nombre" # ✅ Configuración local
git config --list             # ✅ Ver configuración
```

### 🔴 **EVITAR - Git para Operaciones Remotas**

#### ❌ **NO usar git para operaciones remotas cuando gh está disponible**
```powershell
# ❌ EVITAR - gh es mejor
git push origin main          # ❌ Usar: gh pr create (hace push automático)
git pull origin main          # ❌ Usar: gh repo sync
git remote add upstream ...   # ❌ Usar: gh repo fork (configura automático)
git clone https://...         # ❌ Usar: gh repo clone
```

## 🔄 **Workflows Optimizados**

### 📝 **Desarrollo de Feature**
```powershell
# 1. Crear branch local
git checkout -b feature/nueva-funcionalidad

# 2. Desarrollo y commits locales
git add .
git commit -m "feat(core): implementar nueva funcionalidad"

# 3. Crear PR (hace push automático)
gh pr create --title "Nueva funcionalidad" --body "Descripción"
```

### 🐛 **Fix de Bug**
```powershell
# 1. Crear issue si no existe
gh issue create --title "Bug: descripción" --label bug

# 2. Branch local
git checkout -b fix/bug-123

# 3. Fix y commit
git add .
git commit -m "fix(entities): corregir bug en enemigos"

# 4. PR con referencia al issue
gh pr create --title "Fix: bug en enemigos" --body "Fixes #123"
```

### 🚀 **Release**
```powershell
# 1. Tag local
git tag v1.0.0

# 2. Push tag y crear release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Changelog"

# 3. Subir assets si es necesario
gh release upload v1.0.0 dist/game.exe
```

### 🔍 **Investigación y Debug**
```powershell
# Estado general del proyecto
gh repo view
gh status

# Investigar issues y PRs
gh issue list --state open
gh pr list --state open

# Ver logs locales
git log --oneline -10
git status
```

## 🎯 **Principios de Decisión**

### 1. **GitHub CLI PRIMERO**
- Si la tarea involucra GitHub (issues, PRs, releases) → `gh`
- Si la tarea requiere navegación web → `gh browse`
- Si la tarea es de información → `gh repo view`, `gh status`

### 2. **Git SOLO para Local**
- Staging y commits → `git add`, `git commit`
- Branching local → `git branch`, `git checkout`
- Estado local → `git status`, `git log`

### 3. **NUNCA Mezclar**
- NO usar `git push` + `gh pr create` (redundante)
- NO usar `git clone` cuando `gh repo clone` es mejor
- NO usar `git remote` cuando `gh repo fork` configura automático

## 🛠️ **Configuración Óptima**

### Aliases Recomendados
```powershell
# GitHub CLI aliases
gh alias set rv 'repo view'
gh alias set il 'issue list'
gh alias set pl 'pr list'
gh alias set prc 'pr create --fill'

# Git aliases (solo para local)
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm 'commit -m'
```

## 📈 **Beneficios de esta Estrategia**

1. **Eficiencia**: Una herramienta para cada propósito específico
2. **Consistencia**: GitHub CLI maneja automáticamente configuraciones
3. **Integración**: Workflows fluidos entre local y remoto
4. **Productividad**: Menos comandos, más automatización
5. **Menos errores**: GitHub CLI maneja configuraciones complejas

---

**Regla de oro**: Si existe comando `gh` para la tarea, úsalo. Git solo para operaciones locales puras.
