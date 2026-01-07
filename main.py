import os
import keyboard

def clear_console():
    """Очищення консолі."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(selected_index):
    """Відображення меню з виділеним пунктом."""
    menu_items = ["1. Перший пункт", "2. Другий пункт", "3. Третій пункт"]
    clear_console()
    print("Виберіть пункт меню (стрілки вгору/вниз, Enter для вибору):\n")
    for i, item in enumerate(menu_items):
        if i == selected_index:
            print(f"> {item}")  # Виділений пункт
        else:
            print(f"  {item}")

def main():
    selected_index = 0
    menu_items = ["1. Перший пункт", "2. Другий пункт", "3. Третій пункт"]

    display_menu(selected_index)

    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == "down":
            if event.name == "down":
                selected_index = (selected_index + 1) % len(menu_items)
                display_menu(selected_index)
            elif event.name == "up":
                selected_index = (selected_index - 1) % len(menu_items)
                display_menu(selected_index)
            elif event.name == "enter":
                clear_console()
                print(f"Ви вибрали: {menu_items[selected_index]}")
                break

if __name__ == "__main__":
    main()