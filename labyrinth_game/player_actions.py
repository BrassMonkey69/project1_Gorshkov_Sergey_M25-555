from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    inventory = game_state.get('player_inventory', [])
    """Проверяем, есть ли предметы в инвентаре"""
    if inventory:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("\nВаш инвентарь пуст.")
          
def get_input(prompt="> "):
    """Запрашивает ввод у пользователя с обработкой ошибок."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении."""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    next_room = room_data['exits'][direction]
        # Проверяем, есть ли выход в указанном направлении
    if direction not in room_data['exits']:
        print("Нельзя пойти в этом направлении.")
        return
     
    # Специальная проверка для treasure_room
    if next_room == 'treasure_room':
        if 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            game_state['current_room'] = next_room
            game_state['steps_taken'] += 1
            describe_current_room(game_state)
            print('Шагов сделано: ', {game_state['steps_taken']}) #для наглядности, потом уберу 
            # Вызываем случайное событие после перемещения
            random_event(game_state)
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return
    # Если не treasure_room — просто перемещаем игрока
    game_state['current_room'] = next_room
    game_state['steps_taken'] += 1
    describe_current_room(game_state)
    print('Шагов сделано: ', {game_state['steps_taken']}) #для наглядности, потом уберу 
    # Вызываем случайное событие после перемещения
    random_event(game_state)
    return
                 
def take_item(game_state, item_name):
    """Подбирает предмет из комнаты."""
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']
    if item_name == 'treasure_chest':
        print('Вы не можете поднять сундук, он слишком тяжелый')
    elif item_name in room_items:
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"\nВы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """Использует предмет из инвентаря."""
    inventory = game_state['player_inventory']
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Стало светлее. Вы видите больше деталей комнаты.")
    elif item_name == 'sword':
        print("Вы чувствуете себя увереннее с мечом в руках.")
        
    #использование treasure_key через команду "use treasure_key"
    elif item_name == 'treasure_key':
        #проверка нахождения в комнате treasure_room с сундуком treasure_chest
        if game_state['current_room'] == 'treasure_room' and 'treasure_chest' in room_data['items']: 
            print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
            room_data['items'].remove('treasure_chest') #убирает treasure_chest из комнаты
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
            return
        else:
            print("Вы не видите что можно открыть этим ключом. Попробуйте поискать в других комнатах")
                
    elif item_name == 'vial':
        inventory.remove(item_name) #убирает пробирку из инвентаря после использования
        inventory.append('empty_vial') #добавляет пустую пробирку в инвентарь
        print('Невиданный прилив уверенности в себе, Вы чувствуете как внутри разливается тепло. \
Вы обнаруживаете полустертую надпись на дне:\nЧрезмерное употреб... ...едит Вашему здоровью.')
    elif item_name == 'crossbow':
        print("Вы радуетесь как ребенок новой находке. Арбалет заряжен, но его хватит только на 1 выстрел.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            inventory.remove(item_name) #убирает шкатулку после открытия
            inventory.append('rusty_key') #добавляет ключ после открытия
            print("Вы открыли шкатулку и нашли ржавый ключ!")
        else:
            print("Шкатулка уже открыта.")
            inventory.remove(item_name) #убирает шкатулку после открытия
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
