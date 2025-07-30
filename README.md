# 🎮 SiK Python Game

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Poetry](https://img.shields.io/badge/poetry-1.5+-orange.svg)](https://python-poetry.org)
[![Pygame-ce](https://img.shields.io/badge/pygame--ce-2.4+-green.svg)](https://pyga.me)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Videojuego 2D bullet hell desarrollado 100% con IA | Python + Pygame-ce + Poetry**

*Un experimento pionero en desarrollo de videojuegos asistido por inteligencia artificial*

[🚀 Instalación Rápida](#-instalación-rápida) • [🎯 Cómo Jugar](#-cómo-jugar) • [🤝 Contribuir](#-contribuir) • [📚 Documentación](#-documentación)

</div>

## 🌟 ¿Qué es SiK Python Game?

SiK Python Game es un **videojuego 2D bullet hell** que representa un hito en el desarrollo de software: **todo el código, arquitectura y documentación han sido generados mediante la colaboración entre desarrolladores humanos y agentes de inteligencia artificial avanzados**.

### 🤖 Desarrollo 100% Asistido por IA

> **Experimento pionero**: Cada línea de código, decisión arquitectónica y mejora de rendimiento ha sido creada mediante la colaboración inteligente entre humanos e IA.

**Lo que hace especial a este proyecto:**
- 🧠 **Arquitectura inteligente**: Diseñada por agentes de IA especializados
- 🔄 **Refactorización automática**: Mejoras continuas basadas en análisis de IA
- 📚 **Documentación viva**: Comentarios y guías generados automáticamente
- 🧪 **Testing inteligente**: Scripts de verificación creados por IA
- ⚡ **Optimización continua**: Rendimiento mejorado mediante análisis automatizado

## 🎯 Características del Juego

<table>
<tr>
<td width="50%">

### 🎮 **Gameplay**
- **Bullet hell 2D**: Esquiva oleadas de proyectiles
- **3 personajes únicos**: Cada uno con habilidades especiales
- **Sistema de progressión**: Mejora tus estadísticas
- **Múltiples niveles**: Dificultad escalada dinámicamente

### 🎨 **Visual & Audio**
- **Fondo dinámico**: Desierto procedural con efectos atmosféricos
- **Animaciones fluidas**: Sistema de estados avanzado
- **Efectos de partículas**: Arena, calor y viento realistas
- **Audio inmersivo**: Música y efectos sincronizados

</td>
<td width="50%">

### 🛠️ **Tecnología**
- **Python 3.11+**: Lenguaje principal
- **Pygame-ce**: Motor gráfico moderno
- **Poetry**: Gestión de dependencias
- **SQLite**: Base de datos integrada
- **Arquitectura modular**: Fácil de extender

### ⚙️ **Desarrollo**
- **Pre-commit hooks**: Calidad de código automática
- **Testing automatizado**: Pytest + coverage
- **Documentación completa**: Instrucciones jerárquicas
- **GitHub CLI**: Flujo de trabajo optimizado

</td>
</tr>
</table>

## 🚀 Instalación Rápida

### Prerrequisitos
- 🐍 **Python 3.11+** ([Descargar](https://python.org))
- 📦 **Poetry** ([Instalar](https://python-poetry.org/docs/#installation))
- 🔧 **Git** ([Descargar](https://git-scm.com/))

### Instalación en 3 pasos

```powershell
# 1. Clonar el repositorio
git clone https://github.com/Kavalieri/SiK-Python-Game.git
cd SiK-Python-Game

# 2. Instalar dependencias
poetry install

# 3. ¡Ejecutar!
poetry run python src/main.py
```

### Instalación para Desarrollo

```powershell
# Configurar entorno completo de desarrollo
poetry install --with dev

# Configurar hooks de calidad
poetry run pre-commit install

# Verificar instalación
poetry run python src/main.py --debug
```

## 🎯 Cómo Jugar

### Controles

<table>
<tr>
<th>🎮 Acción</th>
<th>⌨️ Teclado</th>
<th>🖱️ Ratón</th>
<th>🎮 Gamepad</th>
</tr>
<tr>
<td>Movimiento</td>
<td><code>WASD</code> / <code>↑↓←→</code></td>
<td>-</td>
<td>Stick izquierdo</td>
</tr>
<tr>
<td>Disparar</td>
<td><code>Espacio</code> / <code>J</code></td>
<td>Clic izquierdo</td>
<td><code>A</code> / <code>X</code></td>
</tr>
<tr>
<td>Pausa</td>
<td><code>Escape</code></td>
<td>-</td>
<td><code>Start</code></td>
</tr>
<tr>
<td>Menú</td>
<td><code>Escape</code></td>
<td>Clic derecho</td>
<td><code>B</code></td>
</tr>
</table>

### Personajes Disponibles

| Personaje | Tipo | Especialidad | Velocidad | Daño |
|-----------|------|--------------|-----------|------|
| 🗡️ **Kava (Guerrero)** | Melee | Combate cercano | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 🏹 **Adventure Girl** | Ranged | Ataques a distancia | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 🤖 **Robot** | Hybrid | Versatilidad | ⭐⭐ | ⭐⭐⭐⭐ |

## 📁 Arquitectura del Proyecto

```
📦 SiK-Python-Game/
├── 🎮 src/                     # Código fuente principal
│   ├── 🔧 core/               # Motor del juego
│   ├── 👾 entities/           # Personajes, enemigos, proyectiles
│   ├── 🎭 scenes/             # Escenas del juego
│   ├── 🖼️ ui/                 # Interfaz de usuario
│   └── ⚙️ utils/              # Utilidades y sistemas
├── 🎨 assets/                 # Recursos del juego
├── 📚 docs/                   # Documentación
├── 🧪 tests/                  # Tests automatizados
├── 🛠️ dev-tools/              # Herramientas de desarrollo
└── 💾 saves/                  # Partidas guardadas
```

## 🔧 Desarrollo

### Scripts de Desarrollo Principales

```powershell
# Ejecutar el juego
poetry run python src/main.py

# Ejecutar tests
poetry run pytest tests/ -v

# Verificar calidad de código
poetry run ruff check src/
poetry run ruff format src/

# Commit con calidad automática
.\dev-tools\scripts\simple_commit.ps1 "mensaje"

# Limpieza del entorno
.\dev-tools\scripts\vscode_cleanup_sendkeys.ps1 -Level "light"
```

### Estándares de Calidad

- ✅ **0 errores Ruff** + **0 warnings MyPy**
- ✅ **100% cobertura de tests** mínimo
- ✅ **Máximo 150 líneas** por archivo
- ✅ **Documentación completa** en español
- ✅ **Type hints** obligatorios

## 🗂️ Estado Actual del Proyecto

### ✅ Completado
- 🎮 **Motor base**: Funcionamiento completo
- 👾 **3 personajes**: Con habilidades únicas
- 🎨 **Sistema visual**: Animaciones + efectos
- 💾 **Sistema de guardado**: SQLite + encriptación
- 🧪 **Testing**: Cobertura automatizada
- 📚 **Documentación**: Sistema jerárquico

### 🔄 En Desarrollo
- 🗄️ **Migración SQLite**: Sistema mixto inteligente
- 📋 **Refactorización**: 29 archivos críticos >150 líneas
- ⚡ **Optimización**: Rendimiento y memoria
- 🎯 **Nuevas mecánicas**: Powerups y combos

### 📊 Métricas del Proyecto
- **29 archivos** requieren refactorización (>150 líneas)
- **9 archivos críticos** (>200 líneas) - prioridad máxima
- **4,267 líneas** de código analizadas
- **20.4% cobertura** de tests (en mejora continua)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este proyecto es especial porque combina desarrollo humano con asistencia de IA.

### 🚀 Cómo Contribuir

1. **📋 Fork** el repositorio
2. **🌿 Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **📝 Consulta** las instrucciones en [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
4. **✅ Verifica** que tu código cumple los estándares:
   ```powershell
   poetry run ruff check src/
   poetry run pytest tests/
   ```
5. **� Commit** usando el sistema unificado:
   ```powershell
   .\dev-tools\scripts\simple_commit.ps1 "feat: descripción de tu cambio"
   ```
6. **🚀 Push** a tu rama (`git push origin feature/AmazingFeature`)
7. **🔄 Abre** un Pull Request

### � Antes de Contribuir

- 📖 **Lee** [`docs/REFACTORIZACION_ESTADO_ACTUAL.md`](docs/REFACTORIZACION_ESTADO_ACTUAL.md)
- 🎯 **Consulta** las [instrucciones jerárquicas](.github/instructions/) por tema
- ⚡ **Límite absoluto**: 150 líneas por archivo
- 🧪 **Testing**: Mantén 100% cobertura mínima
- 📚 **Documenta**: Actualiza [`docs/FUNCIONES_DOCUMENTADAS.md`](docs/FUNCIONES_DOCUMENTADAS.md)

### 🎯 Áreas Prioritarias de Contribución

| Prioridad | Área | Descripción | Dificultad |
|-----------|------|-------------|------------|
| 🔥 **CRÍTICA** | Refactorización | 9 archivos >200 líneas | ⭐⭐⭐ |
| �️ **ALTA** | Migración SQLite | Sistema mixto inteligente | ⭐⭐⭐⭐ |
| 🎮 **MEDIA** | Nuevas mecánicas | Powerups y combos | ⭐⭐ |
| 🎨 **MEDIA** | Assets | Gráficos y sonidos | ⭐ |
| 🧪 **BAJA** | Testing | Cobertura adicional | ⭐⭐ |

## � Documentación

### 📖 Documentación Principal
- 📋 [**Estado de Refactorización**](docs/REFACTORIZACION_ESTADO_ACTUAL.md) - **CONSULTAR PRIMERO**
- �️ [**Plan Migración SQLite**](docs/PLAN_MIGRACION_SQLITE.md) - Esquemas y checklist
- � [**Funciones Documentadas**](docs/FUNCIONES_DOCUMENTADAS.md) - Catálogo completo
- 🔧 [**Flujo de Menús**](docs/FLUJO_MENUS_GUARDADO.md) - Sistema de navegación

### � Instrucciones para IA (Sistema Jerárquico)
- 🏠 [**Principal**](.github/copilot-instructions.md) - Instrucciones base
- 📁 [**Módulos específicos**](.github/instructions/) - 11 temas organizados
- 🔄 [**Refactorización**](.github/instructions/refactorizacion.instructions.md)
- 🗄️ [**Migración SQLite**](.github/instructions/migracion-sqlite.instructions.md)

### �️ Herramientas de Desarrollo
- 🧹 [**Limpieza VS Code**](dev-tools/scripts/vscode_cleanup_sendkeys.ps1)
- 📝 [**Commits Unificados**](dev-tools/scripts/simple_commit.ps1)
- 🧪 [**Testing**](dev-tools/testing/) - Scripts de verificación

## 🔬 Investigación y Metodología IA

### 💡 Lo que Hace Especial a Este Proyecto

Este proyecto demuestra el **futuro del desarrollo de software**: la colaboración simbiótica entre humanos e IA para crear código de calidad profesional.

**Metodología desarrollada:**
1. 🧠 **Análisis de requisitos** por agentes especializados
2. 🏗️ **Diseño arquitectónico** automático con mejores prácticas
3. 💻 **Generación de código** siguiendo estándares estrictos
4. 🧪 **Testing automatizado** y verificación continua
5. 📚 **Documentación viva** que evoluciona con el código

### 📊 Resultados del Experimento

- ✅ **4,267+ líneas** de código generadas por IA
- ✅ **Arquitectura modular** diseñada automáticamente
- ✅ **Sistema de testing** creado inteligentemente
- ✅ **Documentación completa** generada dinámicamente
- ✅ **Optimizaciones** aplicadas por análisis automatizado

## 🐛 Reportar Issues

¿Encontraste un problema? ¡Ayúdanos a mejorar!

### 📋 Información a Incluir

```markdown
**Descripción del problema:**
[Describe qué esperabas que pasara vs qué pasó realmente]

**Pasos para reproducir:**
1. Ejecutar `poetry run python src/main.py`
2. Hacer clic en '...'
3. Ver error

**Entorno:**
- OS: [Windows 11, macOS, Linux]
- Python: [3.11.x]
- Poetry: [1.5.x]

**Logs:**
[Pegar contenido relevante de `logs/game.log`]
```

### 🔍 Antes de Reportar

- ✅ Verifica los [**logs**](logs/game.log) del juego
- ✅ Revisa la [**configuración**](config.json)
- ✅ Consulta [**issues existentes**](https://github.com/Kavalieri/SiK-Python-Game/issues)
- ✅ Prueba con la [**última versión**](https://github.com/Kavalieri/SiK-Python-Game)

## 🎖️ Reconocimientos

### 🤝 Colaboradores

<table>
<tr>
<td align="center">
<strong>🤖 Agentes de IA</strong><br>
<em>Arquitectura y código principal</em>
</td>
<td align="center">
<strong>👥 Equipo SiK</strong><br>
<em>Dirección y supervisión</em>
</td>
<td align="center">
<strong>🌟 Comunidad</strong><br>
<em>Feedback y mejoras</em>
</td>
</tr>
</table>

### 🙏 Agradecimientos Especiales

- **GitHub Copilot** - Asistente principal de código
- **Pygame-ce Community** - Motor gráfico moderno
- **Python Community** - Lenguaje y ecosistema
- **Poetry Team** - Gestión de dependencias elegante

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**. Consulta [LICENSE](LICENSE) para más detalles.

## 🔗 Enlaces Útiles

- 🏠 [**Repositorio**](https://github.com/Kavalieri/SiK-Python-Game)
- 📖 [**Wiki**](https://github.com/Kavalieri/SiK-Python-Game/wiki)
- 🐛 [**Issues**](https://github.com/Kavalieri/SiK-Python-Game/issues)
- 💬 [**Discusiones**](https://github.com/Kavalieri/SiK-Python-Game/discussions)
- 📦 [**Releases**](https://github.com/Kavalieri/SiK-Python-Game/releases)

---

<div align="center">

**🤖 Desarrollado con Inteligencia Artificial por el equipo SiK**

*Pioneros en el desarrollo de software asistido por IA*

⭐ **¡Dale una estrella si te gusta el proyecto!** ⭐

</div>
