# SISTEMA DE EMPAQUETADO Y RECURSOS - SiK Python Game

## 1. Empaquetado Universal (PyInstaller)

- El empaquetado se realiza mediante `tools/package_improved.py`, que automatiza la generación del EXE y el ZIP de release.
- El script detecta y añade automáticamente todos los assets, configuraciones y dependencias necesarias.
- El proceso es reproducible y documentado en consola, con logs detallados y validación de estructura.
- El resultado se encuentra en `releases/vX.Y.Z/`.

## 2. Equivalencia de Recursos y Rutas

- Todas las rutas de assets y configuraciones son relativas y centralizadas en archivos JSON bajo `config/`.
- El EXE generado accede a los mismos recursos y configuraciones que el entorno de desarrollo, garantizando equivalencia visual y funcional.
- El sistema de logs y fallbacks avisa de cualquier recurso faltante.

## 3. Configuración Centralizada de Animaciones y Sprites

- Toda la información de animaciones, rutas y tipos de sprite está en `config/animations.json`.
- Se puede modificar, ampliar o corregir cualquier animación o ruta sin tocar el código, solo editando el JSON.
- `AssetManager` y `AnimationManager` leen esta configuración y la aplican en tiempo de ejecución.

## 4. Sistema de Combate Modular y Escalable

- El sistema de combate soporta ataques melee, ranged y de área, definidos en `config/characters.json`.
- Cada ataque es configurable: daño, alcance, animación, sonido, efectos, hitbox, etc.
- El input y la UI son agnósticos al tipo de ataque, permitiendo ampliar el sistema sin modificar la lógica principal.

## 5. Validación y Testing

- El empaquetado se valida ejecutando el EXE en entorno limpio y comprobando equivalencia visual y funcional.
- Los logs y advertencias ayudan a detectar cualquier diferencia o recurso faltante.
- El proceso de testing y validación debe realizarse antes de cada release.

---

**Última actualización:** 2024-07-29

---

Para cualquier ampliación, corrección o duda, consulta este documento y los archivos de configuración en `config/`.
