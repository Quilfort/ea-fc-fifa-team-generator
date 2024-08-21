"""
This module handles the draft of the different players.
It includes functions to draft goalkeepers based on specific criteria.
"""

import os
import pandas as pd


def draft_goalkeeper(gk_data, criteria):
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

    # Prepare data for CSV update
    selected_gk_str = selected_gk.apply(lambda row: ", ".join(map(str, row)), axis=1)

    # Get path from environment variable
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Load the existing draft data, ensure GK column is treated as object
    draft_data = pd.read_csv(output_file_path, dtype={"GK": "object"})

    # Update the GK column for the premier league range
    draft_data.iloc[: criteria["premier_league"], draft_data.columns.get_loc("GK")] = (
        selected_gk_str.values
    )

    # Save the updated DataFrame back to CSV
    draft_data.to_csv(output_file_path, index=False)
    print(f"Super draft CSV file updated at: {output_file_path}\n")
