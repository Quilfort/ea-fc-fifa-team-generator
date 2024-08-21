"""
This module handles the creation of a draft for a football league based on specific criteria.
It includes functions to set criteria, create player drafts, and handle file paths.
"""

import os
from dotenv import load_dotenv
import pandas as pd
from .create_players import draft_goalkeeper

# Configuration dictionary for criteria
criteria = {
    "leagues": None,
    "premier_league": None,
    "championship": None,
    "league_one": None,
}


def create_draft():
    """
    Create a draft for football leagues based on the set criteria.
    This function prints a banner, sets the criteria, creates a player draft,
    and prepares for team drafting.
    """
    # Print Banner
    print_banner_draft()

    set_criteria()

    # Create Player Draft
    create_player_draft()

    # To be updated
    # Created Team Draft


def create_player_draft():
    """
    Create a draft of players.
    """
    datafile = pd.read_csv(get_file_path())

    # Filter for goalkeepers (GK)
    gk_data = datafile[datafile["Position"] == "GK"]
    draft_goalkeeper(gk_data, criteria)


def set_criteria():
    """
    Set criteria for the draft, including the number of leagues and teams.
    """
    # Hardcoded values for English Leagues
    # Can be updated if added options for other leagues
    criteria["leagues"] = 3
    criteria["premier_league"] = 20
    criteria["championship"] = 20
    criteria["league_one"] = 24


def get_file_path():
    """
    Determine the file path for the dataset based on whether the edited
    or original file exists.

    Returns:
        str: The path to the dataset file.
    """
    load_dotenv()

    # Check if the edited dataset exists
    edited_dataset_path = os.getenv("EDITED_DATASET_PATH")
    edited_male_file_path = os.path.join(edited_dataset_path, "male_players_edited.csv")

    # Check if the edited file exists
    if os.path.exists(edited_male_file_path):
        file_path = edited_male_file_path
    else:
        original_dataset_path = os.getenv("ORIGINAL_DATASET_PATH")
        file_path = os.path.join(original_dataset_path, "male_players.csv")

    # Return file path
    return file_path


def print_banner_draft():
    """
    Print a banner for the draft creation process.
    """
    width = 40

    print("=" * width)
    print("Create Draft".center(width))
    print("=" * width)


if __name__ == "__main__":
    create_draft()
