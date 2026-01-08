import os
import csv
import keyboard
from colorama import Fore, Style
from src.dataprocess import generate_report

def extract_professors(file_path):
    professors = set()
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            if 'Prof' not in reader.fieldnames:
                print(f"{Fore.RED}Колонка 'Prof' не знайдена у файлі.{Style.RESET_ALL}")
                input("Натисніть Enter для повернення в меню...")
                return None
            for row in reader:
                if row['Prof']:
                    professors.add(row['Prof'])
    except Exception as e:
        print(f"{Fore.RED}Помилка при читанні файлу: {e}{Style.RESET_ALL}")
        input("Натисніть Enter для повернення в меню...")
        return None
    return sorted(professors)

def display_professor_menu(professors):
    selected_index = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.BLUE}Sélectionnez un professeur:\n{Style.RESET_ALL}")
        for i, professor in enumerate(professors):
            if i == selected_index:
                print(f"{Fore.CYAN}> {professor}{Style.RESET_ALL}")
            else:
                print(f"  {professor}")

        event = keyboard.read_event(suppress=True)
        if event.event_type == "down":
            if event.name == "down":
                selected_index = (selected_index + 1) % len(professors)
            elif event.name == "up":
                selected_index = (selected_index - 1) % len(professors)
            elif event.name == "enter":
                return professors[selected_index]

def choose_professor(connected_file):
    if not connected_file:
        print(f"{Fore.RED}Aucun fichier connecté. Connectez un fichier avant de continuer.{Style.RESET_ALL}")
        input("Натисніть Enter для повернення в меню...")
        return None

    professors = extract_professors(connected_file)
    if not professors:
        return None

    selected_professor = display_professor_menu(professors)
    generate_report(connected_file, selected_professor)