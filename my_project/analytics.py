import os
import pandas as pd

def analyze_male_players():
    # Define file paths
    edited_file_path = 'dataset/edited/male_players_edited.csv'
    original_file_path = 'dataset/original/male_players.csv'

    # Check if the edited file exists
    if os.path.exists(edited_file_path):
        file_path = edited_file_path
        print("Using the edited dataset.\n")
    else:
        file_path = original_file_path
        print("Edited dataset not found. Using the original dataset.\n")

    # Load the dataset
    datafile = pd.read_csv(file_path)

    # Perform analysis
    total_male_players = len(datafile)
    players_with_high_overall = len(datafile[datafile['Overall'] >= 90])
    goalkeepers = len(datafile[datafile['Position'] == 'GK'])
    unique_positions = datafile['Position'].unique()

    # Print results
    print(f"Total number of male players: {total_male_players}\n")
    print(f"Number of players with an Overall rating of 90 or higher: {players_with_high_overall}")
    print(f"Number of players with Position 'GK': {goalkeepers}")
    print(f"Unique positions: {', '.join(unique_positions)}")

if __name__ == "__main__":
    analyze_male_players()