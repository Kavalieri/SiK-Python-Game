# Sistemas Automatizados

## ⚡ **SISTEMAS AUTOMATIZADOS**

### 🔄 **Commits y Versionado**
- **Diario**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` (Conventional Commits automático)
- **Completo**: `.\dev-tools\scripts\unified_commit.ps1 "mensaje" -Type "feat" -Scope "ui" -Push`
- **Pre-commit**: Hooks ejecutados ANTES staging (resuelve conflictos)

### Método de Commit Unificado (NUEVO - OBLIGATORIO)
- **Script principal**: `.\dev-tools\scripts\unified_commit.ps1` para commits completos con validaciones
- **Script simple**: `.\dev-tools\scripts\simple_commit.ps1` para uso cotidiano
- **Flujo optimizado**: pre-commit → staging → commit → push (resuelve conflictos de hooks)
- **Conventional Commits**: Formato automático `tipo(ámbito): descripción`
- **Tipos**: feat, fix, docs, refactor, test, chore, perf, style
- **Ámbitos**: core, entities, scenes, ui, utils, config, assets, docs
- **Pre-commit hooks**: Ejecutados ANTES del staging para evitar conflictos
- **Documentación completa**: `docs/METODO_COMMIT_UNIFICADO.md` con guía detallada
- **Uso diario**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"`
- **Uso completo**: `.\dev-tools\scripts\unified_commit.ps1 "mensaje" -Type "feat" -Scope "ui" -Push`

### Flujo Autónomo
- **Continuar automáticamente** hasta puntos de prueba
- **Resolver errores** de forma autónoma
- **Documentar cambios** significativos inmediatamente
