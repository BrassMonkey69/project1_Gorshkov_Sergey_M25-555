#from labyrinth_game.main import game_state
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

def show_inventory(game_state):
    inventory = game_state.get('player_inventory', [])
    
    # Проверяем, есть ли предметы в инвентаре
    if inventory:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("\nВаш инвентарь пуст.")
          
#пытаюсь сделать 2.2 п.4
def get_input(prompt="> "):
    #Запрашивает ввод у пользователя с обработкой ошибок.
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении."""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if direction in room_data['exits']:
        game_state['current_room'] = room_data['exits'][direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False

def take_item(game_state, item_name):
    """Подбирает предмет из комнаты."""
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']

    if item_name in room_items:
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"\nВы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """Использует предмет из инвентаря."""
    inventory = game_state['player_inventory']
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Стало светлее. Вы видите больше деталей комнаты.")
    elif item_name == 'sword':
        print("Вы чувствуете себя увереннее с мечом в руках.")
    elif item_name == 'vial':
        print('Невиданный прилив уверенности в себе, Вы чувствуете как внутри разливается тепло. Вы обнаруживаете полустертую надпись на дне "Чрезмерное употреб... ...едит Вашему здоровью.')
    elif item_name == 'crossbow':
        print("Вы радуетесь как ребенок новой находке. Арбалет заряжен, но его хватит только на 1 выстрел.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Вы открыли шкатулку и нашли ржавый ключ!")
        else:
            print("Шкатулка уже открыта.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
