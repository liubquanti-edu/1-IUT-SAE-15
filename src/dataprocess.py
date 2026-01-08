import csv
from datetime import datetime
from colorama import Fore, Style
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_hours(start_time, end_time):
    fmt = "%H:%M:%S"
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)
    delta = end - start
    return delta.total_seconds() / 3600  

def generate_report(connected_file, professor_name):
    if not connected_file:
        print(f"{Fore.RED}Aucun fichier connecté. Veuillez connecter un fichier avant de continuer.{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
        return

    try:
        with open(connected_file, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            required_columns = {'Prof', 'Group', 'Summary', 'HStart', 'HEnd'}
            if not required_columns.issubset(reader.fieldnames):
                print(f"{Fore.RED}Le fichier ne contient pas les colonnes nécessaires : {required_columns - set(reader.fieldnames)}{Style.RESET_ALL}\n")
                input(f"> Revenir au menu")
                return

            modules = {}
            total_td_equivalent = 0

            for row in reader:
                if row['Prof'] != professor_name:
                    continue

                group = row['Group']
                module = row['Summary']
                start_time = row['HStart']
                end_time = row['HEnd']
                hours = calculate_hours(start_time, end_time)

                if module not in modules:
                    modules[module] = {'CM': 0, 'TD': 0, 'TP': 0}

                if group == "Cours":
                    modules[module]['CM'] += hours
                    total_td_equivalent += hours * 1.5
                elif group.startswith("TD"):
                    modules[module]['TD'] += hours
                    total_td_equivalent += hours
                elif group.startswith("TP"):
                    modules[module]['TP'] += hours
                    total_td_equivalent += hours * 0.66
            
            clear_console()

            print(f"{Fore.BLUE}Rapport pour le professeur : {professor_name}{Style.RESET_ALL}\n")
            print(f"{Fore.BLUE}{'Module':<30}{'CM (heures)':<15}{'TD (heures)':<15}{'TP (heures)':<15}{Style.RESET_ALL}")
            for module, hours in modules.items():
                print(f"{Fore.BLUE}{module:<30}{hours['CM']:<15.2f}{hours['TD']:<15.2f}{hours['TP']:<15.2f}{Style.RESET_ALL}")

            print(f"\n{Fore.BLUE}Nombre total d'heures équivalent TD : {total_td_equivalent:.2f}{Style.RESET_ALL}\n")
            input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Erreur lors du traitement du fichier : {e}{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")