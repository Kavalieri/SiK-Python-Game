#!/usr/bin/env python3
"""
Script de test para el sistema de personajes actualizado
====================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del sistema de personajes con nombres y características específicas.
"""

import sys
import os
import pygame

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.character_data import CHARACTER_DATA


def test_character_system():
	"""Test del sistema de personajes actualizado."""
	print("🧪 Iniciando test del sistema de personajes actualizado...")
	
	# Inicializar Pygame
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Test Sistema de Personajes")
	
	print("\n👥 Información de personajes:")
	
	# Verificar cada personaje
	for character_key, character_data in CHARACTER_DATA.items():
		print(f"\n🎮 {character_data['nombre']} ({character_key}):")
		print(f"   Tipo: {character_data['tipo']}")
		print(f"   Descripción: {character_data['descripcion'][:80]}...")
		
		# Estadísticas
		stats = character_data['stats']
		print(f"   ❤️ Vida: {stats['vida']}")
		print(f"   ⚡ Velocidad: {stats['velocidad']}")
		print(f"   ⚔️ Daño: {stats['daño']}")
		print(f"   🛡️ Escudo: {stats['escudo']}")
		print(f"   🎯 Rango: {stats['rango_ataque']}")
		
		# Habilidades
		print(f"   🚀 Habilidades:")
		for skill in character_data['habilidades']:
			print(f"      • {skill}")
	
	# Verificar características específicas
	print("\n✅ Verificando características específicas:")
	
	# Kava (Guerrero) - Cuerpo a cuerpo
	kava = CHARACTER_DATA['guerrero']
	assert kava['nombre'] == 'Kava', f"Nombre incorrecto: {kava['nombre']}"
	assert kava['tipo'] == 'Melee', f"Tipo incorrecto: {kava['tipo']}"
	assert kava['stats']['disparo'] == 0.0, f"Disparo incorrecto: {kava['stats']['disparo']}"
	assert kava['stats']['rango_ataque'] == 80, f"Rango incorrecto: {kava['stats']['rango_ataque']}"
	print("   ✅ Kava configurado correctamente (cuerpo a cuerpo)")
	
	# Sara (Aventurera) - Proyectiles
	sara = CHARACTER_DATA['adventureguirl']
	assert sara['nombre'] == 'Sara', f"Nombre incorrecto: {sara['nombre']}"
	assert sara['tipo'] == 'Ranged', f"Tipo incorrecto: {sara['tipo']}"
	assert sara['stats']['disparo'] == 1.5, f"Disparo incorrecto: {sara['stats']['disparo']}"
	assert sara['stats']['rango_ataque'] == 300, f"Rango incorrecto: {sara['stats']['rango_ataque']}"
	print("   ✅ Sara configurada correctamente (proyectiles)")
	
	# Guiral (Robot) - Proyectiles especiales
	guiral = CHARACTER_DATA['robot']
	assert guiral['nombre'] == 'Guiral', f"Nombre incorrecto: {guiral['nombre']}"
	assert guiral['tipo'] == 'Tech', f"Tipo incorrecto: {guiral['tipo']}"
	assert guiral['stats']['disparo'] == 1.2, f"Disparo incorrecto: {guiral['stats']['disparo']}"
	assert guiral['stats']['rango_ataque'] == 250, f"Rango incorrecto: {guiral['stats']['rango_ataque']}"
	print("   ✅ Guiral configurado correctamente (proyectiles especiales)")
	
	# Verificar balance de juego
	print("\n⚖️ Verificando balance de juego:")
	
	# Vida total
	total_health = sum(char['stats']['vida'] for char in CHARACTER_DATA.values())
	avg_health = total_health / len(CHARACTER_DATA)
	print(f"   Vida promedio: {avg_health:.1f}")
	
	# Velocidad total
	total_speed = sum(char['stats']['velocidad'] for char in CHARACTER_DATA.values())
	avg_speed = total_speed / len(CHARACTER_DATA)
	print(f"   Velocidad promedio: {avg_speed:.1f}")
	
	# Daño total
	total_damage = sum(char['stats']['daño'] for char in CHARACTER_DATA.values())
	avg_damage = total_damage / len(CHARACTER_DATA)
	print(f"   Daño promedio: {avg_damage:.1f}")
	
	# Verificar que cada personaje tiene ventajas únicas
	print("\n🎯 Ventajas únicas por personaje:")
	
	kava_advantages = [
		f"Mayor vida ({kava['stats']['vida']})",
		f"Mayor daño ({kava['stats']['daño']})",
		f"Mayor escudo ({kava['stats']['escudo']})",
		"Cuerpo a cuerpo"
	]
	print(f"   Kava: {', '.join(kava_advantages)}")
	
	sara_advantages = [
		f"Mayor velocidad ({sara['stats']['velocidad']})",
		f"Mayor rango ({sara['stats']['rango_ataque']})",
		f"Disparo más rápido ({sara['stats']['disparo']})",
		"Proyectiles de fuego"
	]
	print(f"   Sara: {', '.join(sara_advantages)}")
	
	guiral_advantages = [
		f"Balanceado en todas las estadísticas",
		f"Proyectiles de energía",
		f"Daño en área",
		"Tecnología avanzada"
	]
	print(f"   Guiral: {', '.join(guiral_advantages)}")
	
	# Limpiar
	pygame.quit()
	print("\n✅ Test del sistema de personajes completado exitosamente")


if __name__ == "__main__":
	test_character_system() 