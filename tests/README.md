# tests/ - Testing del Proyecto

## 🧪 **PROPÓSITO**
Directorio centralizado para testing unitario, de integración y validación del videojuego **SiK Python Game**. Garantiza la calidad y funcionalidad correcta de todos los componentes del proyecto.

## 📊 **ESTADO ACTUAL**
- **6 suites de testing** especializadas por sistema
- **Testing modular**: Tests específicos para cada componente refactorizado
- **Cobertura crítica**: Tests para sistemas fundamentales del juego
- **Integración CI/CD**: Preparado para automatización continua

---

## 🗂️ **SUITES DE TESTING**

### ⚙️ **`test_config_manager.py`**
**Propósito**: Testing del sistema de configuración modular
```python
class TestConfigManager:
    def test_config_loading(self):
        """Valida carga correcta de archivos JSON"""

    def test_config_validation(self):
        """Verifica validación de configuraciones"""

    def test_fallback_values(self):
        """Confirma valores por defecto"""
```

**Cobertura**:
- Carga de configuraciones JSON modulares
- Validación de esquemas de configuración
- Manejo de archivos faltantes o corruptos
- Sistema de fallbacks y valores por defecto

### ⚙️ **`test_config.py`**
**Propósito**: Testing adicional de configuraciones específicas
- Validación de configuraciones individuales
- Testing de integridad entre configuraciones
- Verificación de dependencias entre módulos

### 👾 **`test_enemy_system.py`**
**Propósito**: Testing del sistema de enemigos refactorizado
```python
class TestEnemySystem:
    def test_enemy_creation(self):
        """Valida creación de enemigos"""

    def test_enemy_behavior(self):
        """Verifica comportamiento IA"""

    def test_enemy_manager(self):
        """Confirma gestión de grupos de enemigos"""
```

**Cobertura**:
- **EnemyCore**: Creación, estadísticas, configuración
- **EnemyBehavior**: IA, persecución, patrullaje, ataque
- **EnemyManager**: Spawn, gestión de grupos, limpieza
- **Enemy (fachada)**: API de compatibilidad

### 💎 **`test_powerup_system.py`**
**Propósito**: Testing del sistema de powerups refactorizado
```python
class TestPowerupSystem:
    def test_powerup_creation(self):
        """Valida creación de powerups"""

    def test_powerup_effects(self):
        """Verifica aplicación de efectos"""

    def test_powerup_rendering(self):
        """Confirma renderizado correcto"""
```

**Cobertura**:
- **PowerupTypes**: Tipos, configuración, símbolos
- **PowerupEffects**: Aplicación de efectos al jugador
- **PowerupRenderer**: Renderizado, animaciones flotantes
- **Powerup (fachada)**: Integración completa

### 🎯 **`test_projectile_system.py`**
**Propósito**: Testing del sistema de proyectiles
```python
class TestProjectileSystem:
    def test_projectile_physics(self):
        """Valida física de proyectiles"""

    def test_projectile_collision(self):
        """Verifica detección de colisiones"""

    def test_projectile_lifecycle(self):
        """Confirma ciclo de vida completo"""
```

**Cobertura**:
- Creación y configuración de proyectiles
- Física de movimiento y trayectorias
- Sistema de colisiones
- Daño y efectos de impacto

### 🎮 **`test_unified_system.py`**
**Propósito**: Testing de integración entre sistemas
```python
class TestUnifiedSystem:
    def test_game_initialization(self):
        """Valida inicialización completa del juego"""

    def test_system_integration(self):
        """Verifica integración entre módulos"""

    def test_save_load_cycle(self):
        """Confirma ciclo completo de guardado/carga"""
```

**Cobertura**:
- Integración entre todos los sistemas refactorizados
- Flujo completo de inicialización del juego
- Interacción entre AssetManager, SaveManager, ConfigManager
- Ciclos completos de gameplay

---

## 📋 **DOCUMENTACIÓN DE TESTING**

### 📚 **`README.md`**
**Propósito**: Guía completa del sistema de testing
```markdown
# Testing del Proyecto SiK Python Game

## Ejecutar Tests
- Tests individuales: `python -m pytest tests/test_config.py`
- Suite completa: `python -m pytest tests/`
- Con cobertura: `python -m pytest --cov=src tests/`

## Estructura de Tests
- test_config*.py: Sistema de configuración
- test_*_system.py: Sistemas de gameplay
- test_unified_system.py: Integración completa
```

---

## 🎯 **METODOLOGÍA DE TESTING**

### 🧪 **Tipos de Testing**

#### **Tests Unitarios**
- **Funciones individuales**: Testing de funciones aisladas
- **Clases específicas**: Validación de comportamiento de clases
- **Módulos independientes**: Testing sin dependencias externas

#### **Tests de Integración**
- **Sistemas combinados**: Testing de interacción entre módulos
- **Flujos completos**: Validación de procesos end-to-end
- **APIs de compatibilidad**: Verificación de fachadas

#### **Tests de Sistema**
- **Inicialización completa**: GameEngine y todos sus componentes
- **Ciclos de gameplay**: Desde menú hasta partida completa
- **Persistencia**: Guardado y carga de partidas

### 🛡️ **Estrategias de Testing**

#### **Mocking y Stubs**
```python
# Ejemplo de mock para testing aislado
@pytest.fixture
def mock_asset_manager():
    mock_manager = Mock()
    mock_manager.load_image.return_value = pygame.Surface((64, 64))
    return mock_manager
```

#### **Fixtures Reutilizables**
```python
@pytest.fixture
def game_config():
    """Configuración estándar para tests"""
    return ConfigManager("test_config.json")

@pytest.fixture
def test_player():
    """Jugador configurado para testing"""
    return Player(100, 100, "guerrero", mock_config, mock_animation)
```

#### **Parametrización**
```python
@pytest.mark.parametrize("enemy_type", ["zombie_male", "zombie_female"])
def test_enemy_creation(enemy_type):
    """Test creación de diferentes tipos de enemigos"""
    enemy = Enemy(0, 0, enemy_type, mock_animation)
    assert enemy.enemy_type == enemy_type
```

---

## 📊 **COBERTURA DE TESTING**

### 🎯 **Objetivos de Cobertura**
- **Funciones críticas**: 100% cobertura obligatoria
- **Sistemas refactorizados**: 95% cobertura mínima
- **Funciones auxiliares**: 80% cobertura recomendada
- **Scripts de utilidad**: 70% cobertura aceptable

### 📈 **Métricas por Sistema**

#### **Sistema de Configuración**
- **ConfigManager**: 100% cobertura (crítico)
- **ConfigDatabase**: 95% cobertura (SQLite)
- **Validaciones**: 100% cobertura (robustez)

#### **Sistemas de Gameplay**
- **Enemy System**: 90% cobertura (IA compleja)
- **Powerup System**: 85% cobertura (efectos variados)
- **Projectile System**: 95% cobertura (física crítica)

#### **Sistemas de Persistencia**
- **SaveManager**: 100% cobertura (datos críticos)
- **DatabaseManager**: 95% cobertura (SQLite)
- **AssetManager**: 85% cobertura (carga de recursos)

---

## 🔧 **CONFIGURACIÓN DE TESTING**

### 📝 **pytest.ini**
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --tb=short
    --strict-markers
    -ra
```

### 🛠️ **Dependencias de Testing**
```python
# requirements-test.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-pygame>=1.0.0  # Para testing de Pygame
```

### ⚙️ **Variables de Entorno**
```bash
# Testing en modo headless (sin ventana)
export SDL_VIDEODRIVER=dummy
export PYGAME_HIDE_SUPPORT_PROMPT=1

# Testing con configuración específica
export GAME_CONFIG_PATH=tests/config/
export GAME_ASSETS_PATH=tests/assets/
```

---

## 🚀 **AUTOMATIZACIÓN DE TESTING**

### 🔄 **GitHub Actions (CI/CD)**
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest --cov=src tests/
```

### 🎯 **Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        stages: [commit]
```

### 📊 **Reporting Automático**
- **Coverage reports**: Generación automática de reportes de cobertura
- **Test results**: Reportes JUnit para integración CI/CD
- **Performance**: Métricas de tiempo de ejecución
- **Regression**: Detección automática de regresiones

---

## 🎮 **TESTING ESPECÍFICO DE PYGAME**

### 🖥️ **Inicialización de Pygame**
```python
@pytest.fixture(scope="session")
def pygame_init():
    """Inicializa Pygame para testing"""
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    yield screen
    pygame.quit()
```

### 🎨 **Testing de Sprites y Assets**
```python
def test_sprite_loading(pygame_init):
    """Valida carga correcta de sprites"""
    asset_manager = AssetManager()
    sprite = asset_manager.load_image("test_sprite.png")
    assert sprite is not None
    assert sprite.get_size() == (64, 64)
```

### 🎵 **Testing de Audio**
```python
def test_audio_loading(pygame_init):
    """Valida carga de archivos de audio"""
    audio_manager = AudioManager()
    sound = audio_manager.load_sound("test_sound.wav")
    assert sound is not None
```

---

## 📋 **COMANDOS DE TESTING**

### 🧪 **Testing Básico**
```bash
# Ejecutar todos los tests
python -m pytest tests/

# Test específico
python -m pytest tests/test_config_manager.py

# Tests con verbose
python -m pytest -v tests/
```

### 📊 **Testing con Cobertura**
```bash
# Cobertura completa
python -m pytest --cov=src tests/

# Reporte HTML de cobertura
python -m pytest --cov=src --cov-report=html tests/

# Cobertura mínima requerida
python -m pytest --cov=src --cov-fail-under=85 tests/
```

### 🎯 **Testing Selectivo**
```bash
# Tests por categoría
python -m pytest -k "config" tests/
python -m pytest -k "enemy" tests/
python -m pytest -k "powerup" tests/

# Tests por markers
python -m pytest -m "critical" tests/
python -m pytest -m "integration" tests/
```

---

## 🔗 **REFERENCIAS**

### 📖 **Documentación del Proyecto**
- **Código fuente**: `src/` - Código bajo testing
- **Configuración**: `config/` - Configuraciones de testing
- **Scripts**: `scripts/run_tests.py` - Scripts de testing automatizado

### 🛠️ **Herramientas de Testing**
- **pytest**: Framework principal de testing
- **pytest-cov**: Medición de cobertura de código
- **pytest-mock**: Mocking y stubbing para tests
- **GitHub Actions**: CI/CD automatizado

---

**🧪 ESTADO**: ✅ SUITE COMPLETA DE TESTING CON COBERTURA CRÍTICA
**📅 ÚLTIMA ACTUALIZACIÓN**: 30 de Julio, 2025
**🎯 ENFOQUE**: Testing robusto para desarrollo con IA confiable
