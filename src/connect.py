import os
import keyboard
from colorama import Fore, Style

def find_csv_files(directory):
    csv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

def display_csv_menu(csv_files):
    selected_index = 0
    base_directory = os.getcwd()  

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.BLUE}Sélectionnez un fichier à connecter:\n{Style.RESET_ALL}")
        for i, file in enumerate(csv_files):
            relative_path = os.path.relpath(file, base_directory)
            if i == selected_index:
                print(f"{Fore.CYAN}> {relative_path}{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}  {relative_path}{Style.RESET_ALL}")

        event = keyboard.read_event(suppress=True)
        if event.event_type == "down":
            if event.name == "down":
                selected_index = (selected_index + 1) % len(csv_files)
            elif event.name == "up":
                selected_index = (selected_index - 1) % len(csv_files)
            elif event.name == "enter":
                return csv_files[selected_index]

def connect_data():
    current_directory = os.getcwd()
    csv_files = find_csv_files(current_directory)

    if not csv_files:
        print(f"{Fore.RED}Aucun fichier CSV trouvé.\n{Style.RESET_ALL}")
        input(f"{Fore.RED}> Revenir au menu{Style.RESET_ALL}")
        return None

    selected_file = display_csv_menu(csv_files)
    print(f"{Fore.GREEN}Fichier connecté: {selected_file}{Style.RESET_ALL}")
    return selected_file