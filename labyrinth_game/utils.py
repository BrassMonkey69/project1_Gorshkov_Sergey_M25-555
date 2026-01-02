from labyrinth_game.constants import ROOMS

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
        print("\nЗаметные прsедметы:")
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
