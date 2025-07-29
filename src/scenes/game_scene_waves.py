"""
Game Scene Waves - Oleadas y Enemigos
=====================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Lógica de oleadas y gestión de enemigos para la escena principal del juego.
"""

import random

import pygame

from ..entities.enemy_types import EnemyRarity, EnemyTypes

# Constantes descriptivas para tiempos de pausa
TIEMPO_PAUSA_MEJORAS = 3000
TIEMPO_PAUSA_POST_MEJORAS = 1000


class GameSceneWaves:
    """
    Gestión de oleadas y enemigos para GameScene.
    Se integra con el núcleo mediante composición o herencia.

    Args:
        scene: Referencia al núcleo GameScene.
    """

    def __init__(self, scene):
        """
        Inicializa el gestor de oleadas.

        Args:
            scene: Referencia al núcleo GameScene.
        """
        self.scene = scene  # Referencia al núcleo GameScene

    def spawn_enemy(self):
        """
        Genera un nuevo enemigo en el borde del mundo visible.

        Ejemplo:
            >>> gestor_oleadas.spawn_enemy()
        """
        try:
            x, y = self._get_spawn_position()
            enemy_config = self.select_enemy_for_wave()
            enemy = self.scene.enemy_manager.create_enemy(x, y, enemy_config)
            self.scene.enemies.append(enemy)
            self.scene.enemies_spawned_this_wave += 1
            self.scene.logger.debug(
                f"Enemigo {enemy_config.name} generado en ({x}, {y}) - Oleada {self.scene.wave_number}"
            )
        except (ValueError, AttributeError) as e:
            self.scene.logger.error(f"Error al generar enemigo: {e}")

    def _get_spawn_position(self):
        """
        Calcula una posición aleatoria en los bordes del mundo visible.

        Returns:
            tuple[int, int]: Coordenadas (x, y) de la posición de spawn.
        """
        spawn_side = random.randint(0, 3)
        if spawn_side == 0:
            return random.randint(0, 5000), -50
        elif spawn_side == 1:
            return 5050, random.randint(0, 5000)
        elif spawn_side == 2:
            return random.randint(0, 5000), 5050
        else:
            return -50, random.randint(0, 5000)

    def select_enemy_for_wave(self):
        """
        Selecciona el tipo de enemigo basado en la oleada actual.

        Returns:
            Configuración del enemigo seleccionado.

        Ejemplo:
            >>> enemigo = gestor_oleadas.select_enemy_for_wave()
        """
        wave = self.scene.wave_number
        rarities = self._get_rarities_for_wave(wave)
        return self._select_enemy_by_rarity(rarities)

    def _get_rarities_for_wave(self, wave):
        """
        Obtiene las rarezas disponibles para una oleada específica.

        Args:
            wave: Número de la oleada actual.

        Returns:
            list[EnemyRarity]: Lista de rarezas disponibles.
        """
        enemy_rarities = {
            range(1, 4): [EnemyRarity.NORMAL],
            range(4, 7): [EnemyRarity.NORMAL, EnemyRarity.RARE],
            range(7, 11): [EnemyRarity.NORMAL, EnemyRarity.RARE, EnemyRarity.ELITE],
            range(11, 100): [
                EnemyRarity.NORMAL,
                EnemyRarity.RARE,
                EnemyRarity.ELITE,
                EnemyRarity.LEGENDARY,
            ],
        }
        for rarity_range, rarities in enemy_rarities.items():
            if wave in rarity_range:
                return rarities
        return [EnemyRarity.NORMAL]

    def _select_enemy_by_rarity(self, rarities):
        """
        Selecciona un enemigo aleatorio basado en las rarezas disponibles.

        Args:
            rarities: Lista de rarezas disponibles.

        Returns:
            EnemyTypes: Tipo de enemigo seleccionado.
        """
        rand = random.random()
        for rarity in rarities:
            if rand < 0.5:
                return (
                    EnemyTypes.get_random_by_rarity(rarity) or EnemyTypes.ZOMBIE_NORMAL
                )
        return EnemyTypes.ZOMBIE_NORMAL

    def check_wave_completion(self):
        """
        Verifica si la oleada actual está completada y gestiona upgrades.

        Ejemplo:
            >>> gestor_oleadas.check_wave_completion()
        """
        scene = self.scene
        if (
            scene.enemies_spawned_this_wave >= scene.enemies_per_wave
            and len(scene.enemies) == 0
            and not scene.wave_completed
        ):
            scene.wave_completed = True
            scene.wave_number += 1
            scene.enemies_spawned_this_wave = 0
            scene.enemies_per_wave = min(10 + scene.wave_number * 2, 50)
            scene.logger.info(
                f"¡Oleada {scene.wave_number - 1} completada! Mostrando menú de mejoras"
            )
            self._configurar_menu_mejoras()
            scene.paused_for_upgrade = True
            scene.enemy_spawn_timer = pygame.time.get_ticks() + TIEMPO_PAUSA_MEJORAS

    def _configurar_menu_mejoras(self):
        """
        Configura el menú de mejoras y sus callbacks.
        """
        scene = self.scene
        if hasattr(scene, "hud") and hasattr(scene.hud, "menu_manager"):
            menu_manager = scene.hud.menu_manager
            menu_manager.show_menu("upgrade")
            menu_manager.update_upgrade_menu(scene.player.stats.upgrade_points)
            menu_manager.add_callback(
                "continue_after_upgrade", self.on_continue_after_upgrade
            )
            menu_manager.add_callback(
                "upgrade_speed", lambda: scene.player.upgrade_stat("speed", 10)
            )
            menu_manager.add_callback(
                "upgrade_damage", lambda: scene.player.upgrade_stat("damage", 15)
            )
            menu_manager.add_callback(
                "upgrade_health", lambda: scene.player.upgrade_stat("health", 20)
            )
            menu_manager.add_callback(
                "upgrade_shield", lambda: scene.player.upgrade_stat("shield", 25)
            )
            scene.logger.info("Menú de mejoras configurado")

    def on_continue_after_upgrade(self):
        """
        Callback para continuar el juego tras el menú de mejoras.

        Ejemplo:
            >>> gestor_oleadas.on_continue_after_upgrade()
        """
        scene = self.scene
        scene.logger.info("Continuando juego tras mejoras")
        scene.wave_completed = False
        scene.paused_for_upgrade = False
        scene.enemy_spawn_timer = pygame.time.get_ticks() + TIEMPO_PAUSA_POST_MEJORAS
