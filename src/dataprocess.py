import os
from typing import Optional

import pandas as pd
from colorama import Fore, Style


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def _normalize_group(group_value: str) -> Optional[str]:
    if group_value == "Cours":
        return "CM"
    if isinstance(group_value, str) and group_value.startswith("TD"):
        return "TD"
    if isinstance(group_value, str) and group_value.startswith("TP"):
        return "TP"
    return None


def generate_report(connected_file, professor_name):
    if not connected_file:
        print(f"{Fore.RED}Aucun fichier connecté. Veuillez connecter un fichier avant de continuer.{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
        return

    try:
        df = pd.read_csv(connected_file)

        required_columns = {"Prof", "Group", "Summary", "HStart", "HEnd"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            print(f"{Fore.RED}Le fichier ne contient pas les colonnes nécessaires : {missing_columns}{Style.RESET_ALL}\n")
            input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
            return

        df_prof = df[df["Prof"] == professor_name].copy()
        if df_prof.empty:
            print(f"{Fore.RED}Aucune donnée trouvée pour {professor_name}.{Style.RESET_ALL}\n")
            input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
            return

        df_prof["HStart_dt"] = pd.to_datetime(df_prof["HStart"], format="%H:%M:%S", errors="coerce")
        df_prof["HEnd_dt"] = pd.to_datetime(df_prof["HEnd"], format="%H:%M:%S", errors="coerce")
        df_prof["hours"] = (df_prof["HEnd_dt"] - df_prof["HStart_dt"]).dt.total_seconds() / 3600
        df_prof["hours"] = df_prof["hours"].fillna(0).clip(lower=0)

        df_prof["GroupNorm"] = df_prof["Group"].apply(_normalize_group)
        df_prof = df_prof[df_prof["GroupNorm"].notna()]
        if df_prof.empty:
            print(f"{Fore.RED}Aucune donnée exploitable pour {professor_name}.{Style.RESET_ALL}\n")
            input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")
            return

        multipliers = {"CM": 1.5, "TD": 1.0, "TP": 0.66}
        df_prof["td_equiv"] = df_prof["hours"] * df_prof["GroupNorm"].map(multipliers)

        summary_hours = (
            df_prof.pivot_table(
                index="Summary",
                columns="GroupNorm",
                values="hours",
                aggfunc="sum",
                fill_value=0,
            )
            .reindex(columns=["CM", "TD", "TP"], fill_value=0)
            .sort_index()
        )

        summary_equiv = df_prof.groupby("Summary")["td_equiv"].sum()
        summary = summary_hours.join(summary_equiv, how="left").rename(columns={"td_equiv": "EqTD"})

        total_cm_eq = df_prof.loc[df_prof["GroupNorm"] == "CM", "hours"].sum() * multipliers["CM"]
        total_td_eq = df_prof.loc[df_prof["GroupNorm"] == "TD", "hours"].sum() * multipliers["TD"]
        total_tp_eq = df_prof.loc[df_prof["GroupNorm"] == "TP", "hours"].sum() * multipliers["TP"]
        total_td_equivalent = df_prof["td_equiv"].sum()

        clear_console()

        print(f"{Fore.BLUE}Rapport pour le professeur : {professor_name}{Style.RESET_ALL}\n")
        print(f"{Fore.BLUE}{'Module':<30}{'CM':<15}{'TD':<15}{'TP':<15}{'EQ':<18}{Style.RESET_ALL}")
        for module, row in summary.iterrows():
            cm_hours = row.get("CM", 0)
            td_hours = row.get("TD", 0)
            tp_hours = row.get("TP", 0)
            eq_td_hours = row.get("EqTD", 0)
            print(
                f"{Fore.BLUE}{module:<30}{cm_hours:<15.2f}{td_hours:<15.2f}{tp_hours:<15.2f}{eq_td_hours:<18.2f}{Style.RESET_ALL}"
            )

        print(
            f"\n{Fore.BLUE}CM équivalent TD : {total_cm_eq:.2f}\nTD équivalent TD : {total_td_eq:.2f}\nTP équivalent TD : {total_tp_eq:.2f}{Style.RESET_ALL}"
        )
        print(f"{Fore.BLUE}Nombre total d'heures équivalent TD : {total_td_equivalent:.2f}{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Erreur lors du traitement du fichier : {e}{Style.RESET_ALL}\n")
        input(f"{Fore.CYAN}> Revenir au menu{Style.RESET_ALL}")