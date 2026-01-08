import os
import keyboard
from src.connect import connect_data

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(selected_index, connected_file):
    menu_items = ["Choisir un professeur", "Connecter les données", "Convertir les données"]
    clear_console()
    print("Compagnon du fich de service\n")
    for i, item in enumerate(menu_items):
        if i == selected_index:
            print(f"> {item}")
        else:
            print(f"  {item}")
    print("")
    if connected_file:
        print(f"Données connecté: {connected_file}")
    else:
        print("Aucun données connecté.")

def main():
    selected_index = 0
    menu_items = ["Choisir un professeur", "Connecter les données", "Convertir les données"]
    connected_file = None

    while True:
        display_menu(selected_index, connected_file)
        event = keyboard.read_event(suppress=True)
        if event.event_type == "down":
            if event.name == "down":
                selected_index = (selected_index + 1) % len(menu_items)
            elif event.name == "up":
                selected_index = (selected_index - 1) % len(menu_items)
            elif event.name == "enter":
                clear_console()
                if selected_index == 1:  
                    connected_file = connect_data()  
                else:
                    print(f"Vous avez choisi: {menu_items[selected_index]}")
                    input("Appuyez sur Entrée pour revenir au menu...")

if __name__ == "__main__":
    main()