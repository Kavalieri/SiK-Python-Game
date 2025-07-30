# Control de Versiones

## 📝 **Commits y Gestión**
- **Diario**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` para commits cotidianos
- **GitHub CLI**: `gh` para repo, issues, PRs, releases
- **Git local**: Solo `git add`, `git commit`, branching
- **Commits atómicos**: Por cada refactorización

### Gestión de Archivos y Repositorio
- **GitHub CLI prioritario**: usar `gh` para todas las operaciones de repositorio
- **Matriz de decisión**: `docs/MATRIZ_DECISIÓN_GH_VS_GIT.md` (consultar SIEMPRE)
- **Información del repositorio**: `gh repo view` (preferir sobre git status)
- **Gestión de issues/PRs**: `gh issue create`, `gh pr create --fill`
- **Releases y distribución**: `gh release create`, `gh release upload`
- **Git tradicional**: solo para `git add`, `git commit`, operaciones locales
- **Commits atómicos** por cada refactorización o cambio significativo
- **Evitar** movimientos directos en explorador

### 📁 **Gestión Documental Organizada** (NUEVO - OBLIGATORIO)
- **Lógica de archivo**: Ver `docs/LOGICA_GESTION_DOCUMENTAL.md` para proceso completo
- **Directorio activo**: `docs/` SOLO para documentos de trabajo en curso
- **Sistema de archivo**: `docs/ARCHIVO/2025/[categoria]/` para documentos completados
- **Categorías de archivo**: refactorizacion, migracion-sqlite, terminal-powershell, commits-github, configuracion
- **Proceso obligatorio**: Mover documentos completados/sustituidos a archivo correspondiente
- **Mantener docs/ limpio**: Máximo documentos activos esenciales para desarrollo actual
- **Archivar tras completar**: Cada fase/proyecto → mover documentación a ARCHIVO
- **Consulta histórica**: Estructura organizada por año y tema en docs/ARCHIVO/

### Priorización: GitHub CLI vs Git Tradicional
**Usar GitHub CLI (`gh`) para:**
- Obtener información del repositorio y estado general
- Gestionar issues, pull requests y releases
- Navegar rápidamente al repositorio en navegador
- Clonar repositorios y gestionar forks
- Buscar repositorios y contenido en GitHub
- Ejecutar y monitorear GitHub Actions

**Usar Git tradicional solo para:**
- Operaciones locales básicas: `git add`, `git commit`
- Control de versiones local y staging
- Branching local: `git branch`, `git checkout`
- Consultar logs y diferencias locales
- **OBLIGATORIO**: Verificar cambios staged con `git status` antes de cada commit
- **Usar método unificado**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` para commits cotidianos
