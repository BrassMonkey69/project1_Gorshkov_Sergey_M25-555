def show_inventory(game_state):
    inventory = game_state.get('player_inventory', [])
    
    # Проверяем, есть ли предметы в инвентаре
    if inventory:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("\nВаш инвентарь пуст.")
"""    
пытаюсь сделать 2.2 п.4
def get_input(prompt="> "):
    try:
        command = input("\n> ").strip().lower()
        if command in ['инвентарь', 'inventory', 'i']:
            show_inventory(game_state)
        
        elif command in ['осмотреть', 'look', 'l']:
            describe_current_room(game_state)
        
        elif command in ['выход', 'quit', 'q']:
            print("Жалкая попытка! Ничего, в следующий раз повезет!")
            game_state['game_over'] = True
        return get_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
"""