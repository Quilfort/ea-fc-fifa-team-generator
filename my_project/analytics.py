import os
from dotenv import load_dotenv
import pandas as pd

def analyze_male_players():

    print_banner_analytics()
    # Load the environment variables
    load_dotenv()

    # Check if the edited dataset exists
    edited_dataset_path = os.getenv('EDITED_DATASET_PATH')
    edited_male_file_path = os.path.join(edited_dataset_path, 'male_players_edited.csv')

    # Check if the edited file exists
    if os.path.exists(edited_male_file_path):
        file_path = edited_male_file_path
        print("Using the edited dataset.\n")
    else:
        original_dataset_path = os.getenv('ORIGINAL_DATASET_PATH')
        file_path = os.path.join(original_dataset_path, 'male_players.csv')
        print("Edited dataset not found. Using the original dataset.\n")

    # Load the dataset
    datafile = pd.read_csv(file_path)

    # Perform analysis
    total_male_players = len(datafile)
    players_with_90_overall = len(datafile[datafile['Overall'] >= 90])
    players_with_80_overall = len(datafile[(datafile['Overall'] >= 80) & (datafile['Overall'] < 90)])
    players_with_70_overall = len(datafile[(datafile['Overall'] >= 70) & (datafile['Overall'] < 80)])


    # Define position categories
    # Goalkeepers: GK
    # Defenders: CB, LB, RB, LWB, RWB
    # Midfielders: CM, CDM, CAM, RM, LM
    # Strikers: ST, CF, RW, LW


    goalkeepers_count = len(datafile[datafile['Position'] == 'GK'])
    defenders_count = len(datafile[datafile['Position'].isin(['CB', 'LB', 'RB', 'LWB', 'RWB'])])
    midfielders_count = len(datafile[datafile['Position'].isin(['CM', 'CDM', 'CAM', 'RM', 'LM'])])
    strikers_count = len(datafile[datafile['Position'].isin(['ST', 'CF', 'RW', 'LW'])])

    # Get Unique Position
    # unique_positions = datafile['Position'].unique()
    # print(f"Unique positions: {', '.join(unique_positions)}")

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
    width = 40

    print("=" * width)
    print("Show analyse of dataset".center(width))
    print("=" * width)

if __name__ == "__main__":
    analyze_male_players()