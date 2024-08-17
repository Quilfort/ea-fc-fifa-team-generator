"""
This module handles the creation of a draft for a football league based on specific criteria.
It includes functions to set criteria, create player drafts, and handle file paths.
"""

import os
from dotenv import load_dotenv
import pandas as pd

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
    draft_goalkeeper(gk_data)


def draft_goalkeeper(gk_data):
    """
    Draft goalkeepers based on the top ratings and save to a CSV file.
    """
    number_of_top_gk = 30

    # Sort by Overall rating in descending order
    gk_sorted = gk_data.sort_values(by="Overall", ascending=False)

    # Select the top 30 goalkeepers
    top_gk = gk_sorted.head(number_of_top_gk)

    # Pick the number of goalkeepers based on criteria["premier_league"]
    if len(top_gk) >= criteria["premier_league"]:
        selected_gk = top_gk.sample(n=criteria["premier_league"])
    else:
        selected_gk = top_gk

    # Prepare data for CSV
    # For each player, we'll create a row with their details in the 'GK' column
    draft_data = pd.DataFrame(
        {
            "Name": [None]
            * len(selected_gk),  # Name column is empty as per requirements
            "GK": selected_gk.apply(
                lambda row: ", ".join(map(str, row)), axis=1
            ),  # Concatenate all GK info into a single string
        }
    )

    # Get path from environment variable
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Save to CSV
    draft_data.to_csv(output_file_path, index=False)
    print(f"Super draft CSV file created at: {output_file_path}\n")


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
