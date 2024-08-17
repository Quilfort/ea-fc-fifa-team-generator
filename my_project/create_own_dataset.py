import os
from dotenv import load_dotenv, dotenv_values
import pandas as pd



# Function to create a new dataset with only the columns 
# Name, Nation, Club, Position, Age, and Overall from the original dataset. 
# The new dataset will be saved in the edited directory.

def create_male_dataset():

    # Try manually loading
    load_dotenv()

    # Load the base directory from the environment variable
    original_dataset_path = os.getenv('ORIGINAL_DATASET_PATH')
     
    
    print(f"Original Dataset Path: {original_dataset_path}\n")

    # Concatenate the base directory with the filename
    male_file_path = os.path.join(original_dataset_path, 'male_players.csv')

    # Load the edited directory from the environment variable
    edited_dir = os.getenv('EDITED_DATASET_PATH')

    # Ensure the edited directory exists
    os.makedirs(edited_dir, exist_ok=True)

    # Load the dataset
    datafile = pd.read_csv(male_file_path)

    # Extract the required columns
    columns_to_keep = ['Name', 'Nation', 'Club', 'Position', 'Age', 'Overall']
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

     # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv(new_file_path, index=False)

if __name__ == "__main__":
    create_male_dataset()