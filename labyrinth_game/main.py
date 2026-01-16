from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input, move_player, show_inventory, take_item, use_item
from labyrinth_game.utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state, command_line):
     #Обрабатывает команду игрока.
    
    parts = command_line.split(' ', 1)
    action = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    # Множество допустимых направлений для односложных команд
    valid_directions = {'north', 'south', 'east', 'west'}
    
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
        case dir if dir in valid_directions:
            # Обработка односложной команды движения
            move_player(game_state, dir)                
        case 'solve':
            if 'treasure_chest' not in room_data['items']: #проверка нахождения в комнате с сокровищем (treasure_chest)
                solve_puzzle(game_state)
            else:
                attempt_open_treasure(game_state) #срабатывает при нахождении с сокровищами          
        case 'take':
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет (например, take torch).")
        case 'open':
            attempt_open_treasure(game_state)
        case 'use':
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет (например, use torch).")
        case 'quit' | 'q' | 'exit':
            game_state['game_over'] = True
            print("Жалкая попытка! Ничего, в следующий раз повезет!")
        case 'help':
            show_help()
        case _:
            print("Неизвестная команда. Попробуйте: help, look, inventory, go, take, use, quit.")
            
def main():
    #создание начального состояния игры
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
        }
    # Приветственное сообщение
    print("\nДобро пожаловать в Лабиринт сокровищ!\n")
    # Описываем стартовую комнату
    describe_current_room(game_state)
    """
    print("Тестирование pseudo_random:") #потому уберу тестирование
    for i in range(10):
        result = pseudo_random(i, 10)
        print(f"seed={i} → {result}")    
            """
    while not game_state['game_over']:
        command_line = get_input("> ")  # Считываем команду
        process_command(game_state, command_line)  # Обрабатываем

if __name__ == "__main__":
    main()
