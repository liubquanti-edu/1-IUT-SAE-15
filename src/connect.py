import os
import keyboard

def find_csv_files(directory):
    csv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

def display_csv_menu(csv_files):
    selected_index = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Sélectionnez un fichier à connecter:\n")
        for i, file in enumerate(csv_files):
            if i == selected_index:
                print(f"> {file}")
            else:
                print(f"  {file}")

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
        print("Aucun fichier CSV trouvé.\n")
        input("> Revenir au menu")
        return None

    selected_file = display_csv_menu(csv_files)
    return selected_file