"""
This module handles the creation of a draft for a football league based on specific criteria.
It includes functions to set criteria, create player drafts, and handle file paths.
"""

import os
from dotenv import load_dotenv
import pandas as pd
from .create_players import draft_player_position
from .create_players import draft_top_cbs
from .create_players import draft_middle_bottom_cbs

# Configuration dictionary for criteria
criteria = {
    "leagues": None,
    "premier_league": None,
    "middle_league": None,
    "bottom_league": None,
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
    # Load the dataset
    datafile = pd.read_csv(get_file_path())

    unique_positions = get_unique_positions(datafile)

    # Create Empty CSV file and get unique positions
    create_csv_file(unique_positions)

    # Filter data by position and update the CSV
    for position in unique_positions:
        # Skip "CB1" and "CB2"
        if position in ["CB", "CB1", "CB2"]:
            continue

        position_data = datafile[datafile["Position"] == position]
        draft_player_position(position_data, criteria, position)

    # For CB positions
    cb_data = datafile[datafile["Position"] == "CB"]
    extra_number = 10
    remaining_cbs = draft_top_cbs(cb_data, criteria, extra_number)
    draft_middle_bottom_cbs(remaining_cbs, criteria, extra_number)


def create_csv_file(unique_positions):
    """
    Create a CSV file with columns for all unique positions found in the dataset.
    """
    # Calculate the total number of rows
    total_premier = criteria["premier_league"]
    total_championship = criteria["middle_league"]
    total_league_one = criteria["bottom_league"]

    # Create row names
    top_names = [f"Top {i+1}" for i in range(total_premier)]
    middle_names = [f"Middle {i+1}" for i in range(total_championship)]
    bottom_names = [f"Bottom {i+1}" for i in range(total_league_one)]

    # Combine all row names
    all_names = top_names + middle_names + bottom_names

    # Ensure columns for all unique positions
    columns_dict = {
        position: pd.Series([None] * len(all_names), dtype="object")
        for position in unique_positions
    }

    # Create an empty DataFrame with the specified number of rows and correct dtypes
    draft_data = pd.DataFrame(columns_dict)

    # Insert the 'Name' column as the first column
    draft_data.insert(0, "Name", pd.Series(all_names, dtype="object"))

    # Get path from environment variable
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Save the empty DataFrame to CSV
    draft_data.to_csv(output_file_path, index=False)
    print(f"Empty draft CSV file created at: {output_file_path}\n")
    return unique_positions


def set_criteria():
    """
    Set criteria for the draft, including the number of leagues and teams.
    """
    # Hardcoded values for English Leagues
    # Can be updated if added options for other leagues
    criteria["leagues"] = 3
    criteria["premier_league"] = 20
    criteria["middle_league"] = 20
    criteria["bottom_league"] = 24


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


def get_unique_positions(datafile):
    """
    Get unique positions from the dataset and return them as a list.
    If "CB" is present, replace it with "CB1" and "CB2".
    """
    # Define the desired order of positions
    desired_order = [
        "GK",
        "LWB",
        "LB",
        "CB",
        "RB",
        "RWB",
        "CDM",
        "CM",
        "LM",
        "CAM",
        "RM",
        "LW",
        "CF",
        "ST",
        "RW",
    ]
    # Identify unique positions in the dataset
    unique_positions = datafile["Position"].unique()

    # Filter unique positions based on the desired order and keep the specified order
    ordered_positions = [pos for pos in desired_order if pos in unique_positions]

    # Check if "CB" is in the list and replace it with "CB1" and "CB2"
    if "CB" in ordered_positions:
        # Find the index of "CB" and replace it with "CB1" and "CB2"
        index = ordered_positions.index("CB")
        ordered_positions[index : index + 1] = ["CB1", "CB2"]

    return ordered_positions


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
