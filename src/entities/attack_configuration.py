"""
Attack Configuration - Configuración de ataques del jugador
===========================================================

Autor: SiK Team
Fecha: 30 de Julio, 2025
Descripción: Configuración y estructuras de datos para ataques del jugador.
"""

from typing import Any, Dict, List, Optional, Tuple


class AttackConfig:
    """
    Configuración de un ataque (melee, ranged, area, etc.)
    """

    def __init__(self, data: Dict[str, Any]):
        self.nombre = data.get("nombre", "")
        self.tipo = data.get("tipo", "melee")
        self.damage = data.get("daño", 0)  # Mantener compatibilidad con JSON español
        self.alcance = data.get("alcance", 0)
        self.cooldown = data.get("cooldown", 1.0)
        self.animacion = data.get("animacion", "Attack")
        self.sonido = data.get("sonido", None)
        self.efectos = data.get("efectos", [])
        self.hitbox = data.get("hitbox", None)
        self.proyectil = data.get("proyectil", None)
        self.area = data.get("area", None)


class Attack:
    """
    Instancia de un ataque en ejecución.
    """

    def __init__(self, config: AttackConfig, owner, target_pos: Tuple[int, int]):
        self.config = config
        self.owner = owner
        self.target_pos = target_pos
        self.cooldown_timer = 0.0
        self.active = True


class AttackManager:
    """
    Gestor de configuraciones de ataque y cooldowns.
    """

    def __init__(self, attack_configs: List[AttackConfig]):
        """
        Inicializa el gestor de ataques.

        Args:
            attack_configs: Lista de configuraciones de ataque
        """
        self.attack_configs = attack_configs
        self.current_attack_index = 0
        self.last_attack_time = 0.0

    def get_current_attack(self) -> AttackConfig:
        """Obtiene la configuración del ataque actual."""
        return self.attack_configs[self.current_attack_index]

    def can_attack(self, current_time: float) -> bool:
        """
        Verifica si puede ejecutar el ataque actual.

        Args:
            current_time: Tiempo actual del juego

        Returns:
            True si puede atacar
        """
        attack = self.get_current_attack()
        return current_time - self.last_attack_time >= attack.cooldown

    def set_attack_time(self, current_time: float):
        """
        Actualiza el tiempo del último ataque.

        Args:
            current_time: Tiempo actual del juego
        """
        self.last_attack_time = current_time

    def switch_attack(self, index: int):
        """
        Cambia al ataque especificado.

        Args:
            index: Índice del ataque a usar
        """
        if 0 <= index < len(self.attack_configs):
            self.current_attack_index = index

    def get_attack_count(self) -> int:
        """Obtiene el número total de ataques configurados."""
        return len(self.attack_configs)

    def get_all_attacks(self) -> List[AttackConfig]:
        """Obtiene todas las configuraciones de ataque."""
        return self.attack_configs.copy()

    def get_attack_by_name(self, name: str) -> Optional[AttackConfig]:
        """
        Busca un ataque por nombre.

        Args:
            name: Nombre del ataque

        Returns:
            Configuración del ataque o None si no se encuentra
        """
        for attack in self.attack_configs:
            if attack.nombre == name:
                return attack
        return None
