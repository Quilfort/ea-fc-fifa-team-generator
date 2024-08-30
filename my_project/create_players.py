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
    # Not yet a good name, we call it extra_number. How much extra number of goalkeepers we want to consider
    extra_number = 10

    # Number of top keepers to consider
    number_of_top_gk = criteria["premier_league"] + extra_number

    # Sort by Overall rating in descending order
    gk_sorted = gk_data.sort_values(by="Overall", ascending=False)

    # Select the top goalkeepers
    top_gk = gk_sorted.head(number_of_top_gk)

    # Select other goalkeepers
    number_of_other_gk = (
        criteria["middle_league"] + criteria["bottem_league"]
    ) - extra_number
    other_gk = gk_sorted.iloc[number_of_top_gk : number_of_top_gk + number_of_other_gk]

    # Select keepers for Premier League teams
    if len(top_gk) >= criteria["premier_league"]:
        premier_gk = top_gk.head(criteria["premier_league"])
        remaining_gk = top_gk.tail(extra_number)  # The remaining top 10 keepers
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
    draft_data.iloc[: criteria["premier_league"], draft_data.columns.get_loc("GK")] = (
        premier_gk_str.values
    )

    # Randomly distribute remaining goalkeepers in the Middle Teams section
    if not remaining_gk.empty:
        middle_start = criteria["premier_league"]
        middle_end = middle_start + criteria["middle_league"]

        # Check if there are enough middle teams
        if len(draft_data) > middle_start:
            middle_gk_indices = np.random.choice(
                range(middle_start, middle_end), size=len(remaining_gk), replace=False
            )
            middle_gk_str = remaining_gk.apply(
                lambda row: ", ".join(map(str, row)), axis=1
            )
            draft_data.iloc[middle_gk_indices, draft_data.columns.get_loc("GK")] = (
                middle_gk_str.values
            )

    # Save the updated DataFrame back to CSV
    draft_data.to_csv(output_file_path, index=False)

    draft_middle_low_keepers(other_gk, criteria, extra_number)
    print(f"Super draft CSV file updated at: {output_file_path}\n")


def draft_middle_low_keepers(other_gk, criteria, extra_number):
    """
    Draft middle and bottom league goalkeepers based on their ratings and fill all remaining slots in the CSV file.
    """

    # Calculate total goalkeepers required for middle and bottom leagues
    total_needed_gk = criteria["middle_league"] + criteria["bottem_league"]

    # Sort by Overall rating in descending order
    other_gk_sorted = other_gk.sort_values(by="Overall", ascending=False)

    # Select the required number of goalkeepers plus extra
    needed_gk = other_gk_sorted.head(total_needed_gk + extra_number)

    # Path for the output CSV file
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Load the existing draft data
    draft_data = pd.read_csv(output_file_path, dtype={"GK": "object"})

    # Fill the middle league slots
    middle_start = criteria["premier_league"]
    middle_end = middle_start + criteria["middle_league"]

    if len(draft_data) > middle_start:
        middle_gk = needed_gk.head(criteria["middle_league"])
        middle_gk_str = middle_gk.apply(lambda row: ", ".join(map(str, row)), axis=1)
        middle_gk_indices = np.random.choice(
            range(middle_start, min(middle_end, len(draft_data))),
            size=len(middle_gk),
            replace=False,
        )
        draft_data.iloc[middle_gk_indices, draft_data.columns.get_loc("GK")] = (
            middle_gk_str.values
        )

    # Fill the bottom league slots
    bottom_start = middle_end
    bottom_end = bottom_start + criteria["bottem_league"]

    if len(draft_data) > bottom_start:
        # Remaining keepers for bottom league, including extra
        remaining_needed_for_bottom = criteria["bottem_league"]
        bottom_gk = needed_gk.iloc[
            len(middle_gk) : len(middle_gk) + remaining_needed_for_bottom
        ]
        bottom_gk_str = bottom_gk.apply(lambda row: ", ".join(map(str, row)), axis=1)

        # Check if more keepers are needed than currently selected for bottom
        if len(bottom_gk) < remaining_needed_for_bottom:
            additional_needed = remaining_needed_for_bottom - len(bottom_gk)
            additional_gk = needed_gk.iloc[
                -additional_needed:
            ]  # Select from the extra keepers
            additional_gk_str = additional_gk.apply(
                lambda row: ", ".join(map(str, row)), axis=1
            )
            # Combine the current and additional goalkeepers
            bottom_gk_str = pd.concat([bottom_gk_str, additional_gk_str])

        bottom_gk_indices = np.random.choice(
            range(bottom_start, min(bottom_end, len(draft_data))),
            size=len(bottom_gk_str),
            replace=False,
        )
        draft_data.iloc[bottom_gk_indices, draft_data.columns.get_loc("GK")] = (
            bottom_gk_str.values
        )

    # Save the updated DataFrame back to CSV
    draft_data.to_csv(output_file_path, index=False)
    print(
        f"Super draft CSV file updated for middle and bottom leagues at: {output_file_path}\n"
    )
