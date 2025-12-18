#!/usr/bin/env python3
def main():
    print ("Первая попытка запустить проект!")
    
import constants
import player_actions
import utils

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}
