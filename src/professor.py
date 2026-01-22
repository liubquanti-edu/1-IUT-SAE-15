import os
from math import ceil
import keyboard
import pandas as pd
from colorama import Fore, Style

from src.dataprocess import generate_report

def extract_professors(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de la lecture du fichier : {e}{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
        return None

    if "Prof" not in df.columns:
        print(f"{Fore.RED}La colonne 'Prof' est introuvable dans le fichier.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
        return None

    professors = (
        df["Prof"].dropna().astype(str).str.strip().replace("", pd.NA).dropna().unique().tolist()
    )
    return sorted(professors)

def display_professor_menu(professors):
    selected_index = 0
    max_rows = 10  
    num_columns = ceil(len(professors) / max_rows)  

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.BLUE}Sélectionnez un professeur :\n{Style.RESET_ALL}")

        columns = [professors[i:i + max_rows] for i in range(0, len(professors), max_rows)]
        for row in range(max_rows):
            row_items = []
            for col in range(num_columns):
                if row < len(columns[col]):
                    professor = columns[col][row]
                    if professors.index(professor) == selected_index:
                        row_items.append(f"{Fore.CYAN}> {professor:<20}{Style.RESET_ALL}")
                    else:
                        row_items.append(f"{Fore.BLUE}  {professor:<20}{Style.RESET_ALL}")
                else:
                    row_items.append(" " * 22)  
            print("".join(row_items))

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
        print(f"{Fore.RED}Aucun fichier connecté. Connectez un fichier avant de continuer.{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
        return None

    professors = extract_professors(connected_file)
    if not professors:
        return None

    selected_professor = display_professor_menu(professors)
    generate_report(connected_file, selected_professor)
