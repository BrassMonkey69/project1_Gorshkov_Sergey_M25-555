from labyrinth_game.constants import ROOMS
#import player_actions  #кажется здесь что-то не так
#import utils           #кажется здесь что-то не так
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import show_inventory
#from labyrinth_game.player_actions import get_input

def main():
    #создание начального состояния игры
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
        }
    # Приветственное сообщение
    print("Добро пожаловать в Лабиринт сокровищ!\n")
    # Описываем стартовую комнату
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        # Считываем команду от пользователя
        command = input("\n> ").strip().lower()
        
        # Обрабатываем команды
        if command in ['инвентарь', 'inventory', 'i']:
            show_inventory(game_state)
        
        elif command in ['осмотреть', 'look', 'l']:
            describe_current_room(game_state)
        
        elif command in ['выход', 'quit', 'q']:
            print("Жалкая попытка! Ничего, в следующий раз повезет!")
            game_state['game_over'] = True
        
if __name__ == "__main__":
    main()