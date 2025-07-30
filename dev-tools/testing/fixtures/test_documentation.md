# Test Markdown File
# Para verificar hooks de markdown

## Titulo de Prueba

Este es un archivo de prueba para verificar que los hooks funcionan correctamente.

### Lista de verificacion:

- [ ] Hook de ruff
- [ ] Hook de ruff-format
- [ ] Hook de trim trailing whitespace
- [ ] Hook de fix end of files
- [ ] Hook de check yaml
- [ ] Hook de check for added large files

### Codigo de ejemplo:

```python
def ejemplo():
    return "test"
```

### Notas importantes:

1. Este archivo tiene trailing spaces intencionalmente
2. Puede que no tenga newline final
3. Se usa para testear el flujo completo

**Resultado esperado:** Todos los hooks deben pasar o auto-corregir
