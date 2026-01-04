from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import show_inventory
from labyrinth_game.player_actions import get_input
from labyrinth_game.player_actions import move_player
from labyrinth_game.player_actions import take_item
from labyrinth_game.player_actions import use_item

def process_command(game_state, command):
    """Обрабатывает команду игрока."""
     #Обрабатывает команду игрока.
    parts = command.split(' ', 1)
    action = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    match action:
        case 'look' | 'l':
            describe_current_room(game_state)
        case 'inventory' | 'i':
            show_inventory(game_state)
        case 'go' | 'g':
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление (например, go north).")
        case 'take' | 'взять':
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет (например, take torch).")
        case 'use' | 'использовать':
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет (например, use torch).")
        case 'quit' | 'q' | 'exit':
            game_state['game_over'] = True
            print("Жалкая попытка! Ничего, в следующий раз повезет!")
        case _:
            print("Неизвестная команда. Попробуйте: look, inventory, go, take, use, quit.")
            
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
    
    while not game_state['game_over']:
        command = get_input("> ")  # Считываем команду
        process_command(game_state, command)  # Обрабатываем
    # Основной игровой цикл
#    while not game_state['game_over']:
#        process_command(game_state, command)


if __name__ == "__main__":
    main()