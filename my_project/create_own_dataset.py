"""
This module handles the creation of a filtered dataset from an original dataset.
It extracts specific columns and saves the result in an edited directory.
"""

import os
from dotenv import load_dotenv
import pandas as pd


def create_male_dataset():
    """
    Creates a new dataset with selected columns from the original dataset.
    The new dataset includes only:
        'Name', 'Nation', 'Club', 'Position', 'Age', and 'Overall'.
    The new dataset is saved in the edited directory. If the file already exists, it is overwritten.
    """
    print_banner_dataset()

    # Load environment variables
    load_dotenv()

    # Load the base directory from the environment variable
    original_dataset_path = os.getenv("ORIGINAL_DATASET_PATH")

    # Concatenate the base directory with the filename
    male_file_path = os.path.join(original_dataset_path, "male_players.csv")

    # Load the edited directory from the environment variable
    edited_dir = os.getenv("EDITED_DATASET_PATH")

    # Ensure the edited directory exists
    os.makedirs(edited_dir, exist_ok=True)

    # Load the dataset
    datafile = pd.read_csv(male_file_path)

    # Extract the required columns
    columns_to_keep = ["Name", "Nation", "Club", "Position", "Age", "Overall"]
    df_filtered = datafile[columns_to_keep]

    # Create the new file name
    original_file_name = os.path.basename(male_file_path)
    new_file_name = f"{os.path.splitext(original_file_name)[0]}_edited.csv"
    new_file_path = os.path.join(edited_dir, new_file_name)

    # Check if the file already exists
    if os.path.exists(new_file_path):
        print(f"File already exists: {new_file_path}. Overwriting...\n")

    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv(new_file_path, index=False)

    print(f"Processed file saved as: {new_file_path}\n")


def print_banner_dataset():
    """
    Print a banner for the dataset creation process.
    """
    width = 40

    print("=" * width)
    print("Creating your dataset".center(width))
    print("=" * width)


if __name__ == "__main__":
    create_male_dataset()
