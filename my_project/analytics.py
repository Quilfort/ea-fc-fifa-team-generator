"""
This module performs analysis on a dataset of male players.
It provides statistics such as total number of players, distribution of overall ratings,
and distribution of player positions.
"""

from dotenv import load_dotenv
import pandas as pd
from .create_super_league import get_file_path


def analyze_male_players():
    """
    Analyzes the dataset of male players to provide various statistics.
    It checks for the presence of an edited dataset first;
    if not found, it falls back to the original dataset.
    The function prints:
    - Total number of male players
    - Distribution of players by overall rating (90+, 80-89, 70-79)
    - Distribution of players by position (Goalkeepers, Defenders, Midfielders, Strikers)
    """
    # Print Banner
    print_banner_analytics()

    # Load the environment variables
    load_dotenv()

    # Load the dataset
    file_path = get_file_path()
    datafile = pd.read_csv(file_path)

    # Perform analysis
    total_male_players = len(datafile)
    players_with_90_overall = len(datafile[datafile["Overall"] >= 90])
    players_with_80_overall = len(
        datafile[(datafile["Overall"] >= 80) & (datafile["Overall"] < 90)]
    )
    players_with_70_overall = len(
        datafile[(datafile["Overall"] >= 70) & (datafile["Overall"] < 80)]
    )

    # Define position categories
    # Goalkeepers: GK
    # Defenders: CB, LB, RB, LWB, RWB
    # Midfielders: CM, CDM, CAM, RM, LM
    # Strikers: ST, CF, RW, LW

    goalkeepers_count = len(datafile[datafile["Position"] == "GK"])
    defenders_count = len(
        datafile[datafile["Position"].isin(["CB", "LB", "RB", "LWB", "RWB"])]
    )
    midfielders_count = len(
        datafile[datafile["Position"].isin(["CM", "CDM", "CAM", "RM", "LM"])]
    )
    strikers_count = len(datafile[datafile["Position"].isin(["ST", "CF", "RW", "LW"])])

    # Print results
    print(f"Total number of male players: {total_male_players}\n")

    print("Overall rating distribution:")
    print(f"Players with rating of 90 or higher: {players_with_90_overall}")
    print(f"Players with rating between 80 and 89: {players_with_80_overall}")
    print(f"Players with rating of between 70 and 79: {players_with_70_overall}\n")

    print("Overall position distribution:")
    print(f"Goalkeepers: {goalkeepers_count}")
    print(f"Defenders: {defenders_count}")
    print(f"Midfielders: {midfielders_count}")
    print(f"Strikers: {strikers_count}")


def print_banner_analytics():
    """
    Prints a banner for the analytics section of the script.
    """
    width = 40

    print("=" * width)
    print("Show analysis of dataset".center(width))
    print("=" * width)


if __name__ == "__main__":
    analyze_male_players()
