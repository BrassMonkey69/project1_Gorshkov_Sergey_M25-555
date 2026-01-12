from labyrinth_game.constants import ROOMS
import math


def describe_current_room(game_state):
    """
    Выводит подробное описание текущей комнаты на основе game_state.
    """
    current_room_name = game_state['current_room']
    
    # Получаем данные о комнате из константы ROOMS
    room_data = ROOMS.get(current_room_name)
    
    # Название комнаты в верхнем регистре с обрамлением
    print(f"== {game_state['current_room'].upper()} ==\n")
    
    # Описание комнаты
    print(room_data['description'])
    
    # Список видимых предметов
    if room_data['items']:
        print("\nЗаметные предметы:")
        for item in room_data['items']:
            print(f"  - {item}")
    
    # Доступные выходы
    print("\nВыходы:")
    for exit in room_data['exits']:
        print(f"  - {exit}")
    
    # Сообщение о загадке
    if room_data['puzzle'] == None:
        print('В этой комнате нет загадок')
    else:
        print("\nКажется, здесь есть загадка (используйте команду solve).")
              

def solve_puzzle(game_state):
    """Позволяет игроку решить загадку в текущей комнате."""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    puzzle = room_data['puzzle']

    if not puzzle:
        print("Загадок здесь нет.")
        return
    question, correct_answer = puzzle
    print(f"\n{question}")
    user_answer = input("Ваш ответ: ").strip()

    if user_answer == correct_answer:
        if current_room == 'laboratory': #проверка нахождения в лаборатории
            print("Правильно! Вы решили загадку, замок шкатулки открылся.")
            print ("Под кучей бумаг с надписями 'Python - лучший язык программирования' Вы находите блестящий ключ!")
            game_state['player_inventory'].append('treasure_key') #добавляет пустую пробирку в инвентарь
                    
        elif print("Правильно! Вы решили загадку."):
            room_data['puzzle'] = None  # убираем загадку
            game_state['steps_taken'] += 1  # награда за решение, надо додумать что-то нормальное
            print("Вы получили бонус за решение загадки!")
    else:
        print("Неверно. Попробуйте снова.")
       

def attempt_open_treasure(game_state):
    """Попытка открыть сундук в treasure_room."""
    current_room = game_state['current_room']
    inventory = game_state['player_inventory']
    room_data = ROOMS[current_room]
    
    if current_room != 'treasure_room': #проверка на нахождение в комнате treasure_room
        print("Здесь нет сундука для открытия.")
        return

    if 'treasure_chest' not in room_data['items']: #проверка наличия сундука в комнате
        print("Сундук уже открыт!")
        return

    # Сценарий 1: есть ключ
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest') #убирает treasure_chest из комнаты
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    # Сценарий 2: нет ключа — предлагаем ввести код
    print("Сундук заперт. Хотите попробовать ввести код? (да/нет)")
    choice = input("> ").strip().lower()
    if choice == 'да':
        current_room = game_state['current_room']
        room_data = ROOMS[current_room]
        puzzle = room_data['puzzle']

        if not puzzle:
            print("Загадок здесь нет.")
            return

        question, correct_answer = puzzle
        print(f"\n{question}")
        user_answer = input("Ваш ответ: ").strip()

        if user_answer == correct_answer:
            print("Код верен! Замок щёлкает, сундук открывается!")
            room_data['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
            return
        else:
            print("Неверный код. Сундук остаётся запертым.")
    if choice == 'нет':
        print("Вы отступаете от сундука.")
  
    
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look/l          - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory/i     - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit/exit/q     - выйти из игры")
    print("  help            - показать это сообщение")
    print("  open            - попытка открыть сундук сокровищ")
  
    
def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное целое число в диапазоне [0, modulo) на основе seed.
    
    Использует детерминированный алгоритм на основе синуса для предсказуемых результатов.
    
    Args:
        seed (int): начальное значение (например, количество шагов)
        modulo (int): верхняя граница диапазона (результат будет < modulo)
    Returns:
        int: число в диапазоне [0, modulo)
    """
    # Шаг 1: вычисляем синус от seed * константа_1
    value = math.sin(seed * 12.9898)
    
    
    # Шаг 2: умножаем на константу_2 для «размазывания» значений
    value *= 437578.5499
    
    
    # Шаг 3: выделяем дробную часть (x - целая часть x)
    fractional_part = value - math.floor(value)
    
    
    # Шаг 4: приводим к диапазону [0, modulo)
    scaled = fractional_part * modulo
    
    
    # Шаг 5: отбрасываем дробную часть, возвращаем целое
    return int(scaled)


def trigger_trap(game_state):
    """
    Имитирует срабатывание ловушки с негативными последствиями для игрока.
    
    Если в инвентаре есть предметы — случайно теряется один.
    Если инвентарь пуст — есть шанс получить смертельный урон.
    
    Args:
        game_state (dict): состояние игры (включая инвентарь и флаг game_over)
    """
    print("Ловушка активирована! Пол стал дрожать... Вы применили свой фирменный кувырок. Просто потому что можете.")

    
    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']
    
    if inventory:
        # В инвентаре есть предметы: теряем один случайно выбранный
        num_items = len(inventory)
        # Генерируем случайный индекс предмета (от 0 до num_items - 1)
        lost_index = pseudo_random(steps, num_items)
        lost_item = inventory.pop(lost_index)
        print(f"Вы потеряли предмет: '{lost_item}'!")
    else:
        # Инвентарь пуст: проверяем шанс смертельного урона
        damage_roll = pseudo_random(steps, 10)  # [0, 10)
        if damage_roll < 3:  # 30 % шанс поражения (числа 0, 1, 2)
            print("Пол обрушился! Вы упали в бездну... Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы чудом устояли на ногах! Ловушка не нанесла вреда.")


def random_event(game_state):
    """
    Генерирует случайное событие при перемещении игрока.
    
    С вероятностью ~10% происходит одно из трёх событий:
    - находка монеты;
    - испуг от шороха;
    - срабатывание ловушки в trap_room (при условиях).
    
    Args:
        game_state (dict): состояние игры (инвентарь, комната, шаги и т.д.)
    """
    steps = game_state['steps_taken']
    
    # Шаг 1. Проверяем, произойдёт ли событие вообще (вероятность ~10 %)
    event_roll = pseudo_random(steps, 10)
    if event_roll != 0:
        return  # Событие не произошло, выходим

    # Шаг 2. Выбираем тип события (0–2)
    event_type = pseudo_random(steps + 1, 3)

    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    match event_type:
        case 0:
            # Сценарий 1: Находка монеты
            print("Вы заметили на полу блестящую монетку!")
            room_data['items'].append('coin')
            print("Монета добавлена в комнату.")

        case 1:
            # Сценарий 2: Испуг от шороха
            print("Откуда‑то доносится странный шорох...")
            if 'sword' in game_state['player_inventory']:
                print("Вы выхватываете меч — шорох затихает. Похоже, вы отпугнули существо.")
            elif 'crossbow' in game_state['player_inventory']:
                print('Вы достаете арбалет и стеляете в темноту единственным болтом... Похоже, Вы отпугнули существо, но арбалет больше не поможет, Вы выбрасываете его')
                game_state['player_inventory'].remove('crossbow')
        case 2:
            # Сценарий 3: Срабатывание ловушки в trap_room
            if current_room == 'trap_room' and 'torch' not in game_state['player_inventory']:
                print("Пол под вами заскрипел... Кажется, вы активировали ловушку!")
                trigger_trap(game_state)
            else:
                # Если условия не выполнены, просто сообщаем о странном ощущении
                print("Вам показалось, что пол дрогнул... Но ничего не произошло.")