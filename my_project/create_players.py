"""
This module handles the draft of the different players.
It includes functions to draft goalkeepers based on specific criteria.
"""

import os
import pandas as pd
import numpy as np


def draft_goalkeeper(gk_data, criteria):
    """
    Draft goalkeepers based on the top ratings and save to a CSV file.
    """
    # Number of top keepers to consider
    number_of_top_gk = criteria["premier_league"] + 10

    # Sort by Overall rating in descending order
    gk_sorted = gk_data.sort_values(by="Overall", ascending=False)

    # Select the top goalkeepers
    top_gk = gk_sorted.head(number_of_top_gk)

    # Select keepers for Premier League teams
    if len(top_gk) >= criteria["premier_league"]:
        premier_gk = top_gk.head(criteria["premier_league"])
        remaining_gk = top_gk.tail(10)  # The remaining top 10 keepers
    else:
        premier_gk = top_gk
        remaining_gk = pd.DataFrame()  # No remaining keepers if not enough

    # Prepare data for CSV update
    premier_gk_str = premier_gk.apply(lambda row: ", ".join(map(str, row)), axis=1)

    # Get path from environment variable
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Load the existing draft data, ensure GK column is treated as object
    draft_data = pd.read_csv(output_file_path, dtype={"GK": "object"})

    # Update the GK column for the premier league range
    draft_data.iloc[: criteria["premier_league"], draft_data.columns.get_loc("GK")] = premier_gk_str.values

    # Randomly distribute remaining goalkeepers in the Middle Teams section
    if not remaining_gk.empty:
        middle_start = criteria["premier_league"]
        middle_end = middle_start + criteria["championship"]

        # Check if there are enough middle teams
        if len(draft_data) > middle_start:
            middle_gk_indices = np.random.choice(range(middle_start, middle_end), size=len(remaining_gk), replace=False)
            middle_gk_str = remaining_gk.apply(lambda row: ", ".join(map(str, row)), axis=1)
            draft_data.iloc[middle_gk_indices, draft_data.columns.get_loc("GK")] = middle_gk_str.values

    # Save the updated DataFrame back to CSV
    draft_data.to_csv(output_file_path, index=False)
    print(f"Super draft CSV file updated at: {output_file_path}\n")