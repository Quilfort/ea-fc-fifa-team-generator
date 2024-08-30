"""
This module handles the draft of the different players.
It includes functions to draft player_positions based on specific criteria.
"""

import os
import pandas as pd
import numpy as np


def draft_player_position(player_pos_data, criteria, position_column):
    """
    Draft player_positions based on the top ratings and save to a CSV file.
    """
    # Not yet a good name, we call it extra_number. How much extra number of player_positions we want to consider
    extra_number = 10

    # Number of top keepers to consider
    number_of_top_player_pos = criteria["premier_league"] + extra_number

    # Sort by Overall rating in descending order
    player_pos_sorted = player_pos_data.sort_values(by="Overall", ascending=False)

    # Select the top player_positions
    top_player_pos = player_pos_sorted.head(number_of_top_player_pos)

    # Select other player_positions
    number_of_other_player_pos = (
        criteria["middle_league"] + criteria["bottom_league"]
    ) - extra_number
    other_player_pos = player_pos_sorted.iloc[
        number_of_top_player_pos : number_of_top_player_pos + number_of_other_player_pos
    ]

    # Select keepers for Premier League teams
    if len(top_player_pos) >= criteria["premier_league"]:
        premier_player_pos = top_player_pos.head(criteria["premier_league"])
        remaining_player_pos = top_player_pos.tail(
            extra_number
        )  # The remaining top 10 keepers
    else:
        premier_player_pos = top_player_pos
        remaining_player_pos = pd.DataFrame()  # No remaining keepers if not enough

    # Prepare data for CSV update
    premier_player_pos_str = premier_player_pos.apply(
        lambda row: ", ".join(map(str, row)), axis=1
    )

    # Get path from environment variable
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Load the existing draft data, ensure GK column is treated as object
    draft_data = pd.read_csv(output_file_path, dtype={position_column: "object"})

    # Update the GK column for the premier league range
    draft_data.iloc[
        : criteria["premier_league"], draft_data.columns.get_loc(position_column)
    ] = premier_player_pos_str.values

    # Randomly distribute remaining player_positions in the Middle Teams section
    if not remaining_player_pos.empty:
        middle_start = criteria["premier_league"]
        middle_end = middle_start + criteria["middle_league"]

        # Check if there are enough middle teams
        if len(draft_data) > middle_start:
            middle_player_pos_indices = np.random.choice(
                range(middle_start, middle_end),
                size=len(remaining_player_pos),
                replace=False,
            )
            middle_player_pos_str = remaining_player_pos.apply(
                lambda row: ", ".join(map(str, row)), axis=1
            )
            draft_data.iloc[
                middle_player_pos_indices, draft_data.columns.get_loc(position_column)
            ] = middle_player_pos_str.values

    # Save the updated DataFrame back to CSV
    draft_data.to_csv(output_file_path, index=False)

    # Call draft_middle_low_keepers with the position_column argument
    draft_middle_low_keepers(other_player_pos, criteria, extra_number, position_column)
    print(f"Super draft CSV file updated at: {output_file_path}\n")


def draft_middle_low_keepers(other_player_pos, criteria, extra_number, position_column):
    """
    Draft middle and bottom league player_positions based on their ratings and fill all remaining slots in the CSV file.
    """

    # Calculate total player_positions required for middle and bottom leagues
    total_needed_player_pos = criteria["middle_league"] + criteria["bottom_league"]

    # Sort by Overall rating in descending order
    other_player_pos_sorted = other_player_pos.sort_values(
        by="Overall", ascending=False
    )

    # Select the required number of player_positions plus extra
    needed_player_pos = other_player_pos_sorted.head(
        total_needed_player_pos + extra_number
    )

    # Path for the output CSV file
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    # Load the existing draft data
    draft_data = pd.read_csv(output_file_path, dtype={position_column: "object"})

    # Fill the middle league slots
    middle_start = criteria["premier_league"]
    middle_end = middle_start + criteria["middle_league"]

    if len(draft_data) > middle_start:
        middle_player_pos = needed_player_pos.head(criteria["middle_league"])
        middle_player_pos_str = middle_player_pos.apply(
            lambda row: ", ".join(map(str, row)), axis=1
        )
        middle_player_pos_indices = np.random.choice(
            range(middle_start, min(middle_end, len(draft_data))),
            size=len(middle_player_pos),
            replace=False,
        )
        draft_data.iloc[
            middle_player_pos_indices, draft_data.columns.get_loc(position_column)
        ] = middle_player_pos_str.values

    # Fill the bottom league slots
    bottom_start = middle_end
    bottom_end = bottom_start + criteria["bottom_league"]

    if len(draft_data) > bottom_start:
        # Remaining keepers for bottom league, including extra
        remaining_needed_for_bottom = criteria["bottom_league"]
        bottom_player_pos = needed_player_pos.iloc[
            len(middle_player_pos) : len(middle_player_pos)
            + remaining_needed_for_bottom
        ]
        bottom_player_pos_str = bottom_player_pos.apply(
            lambda row: ", ".join(map(str, row)), axis=1
        )

        # Check if more keepers are needed than currently selected for bottom
        if len(bottom_player_pos) < remaining_needed_for_bottom:
            additional_needed = remaining_needed_for_bottom - len(bottom_player_pos)
            additional_player_pos = needed_player_pos.iloc[
                -additional_needed:
            ]  # Select from the extra keepers
            additional_player_pos_str = additional_player_pos.apply(
                lambda row: ", ".join(map(str, row)), axis=1
            )
            # Combine the current and additional player_positions
            bottom_player_pos_str = pd.concat(
                [bottom_player_pos_str, additional_player_pos_str]
            )

        bottom_player_pos_indices = np.random.choice(
            range(bottom_start, min(bottom_end, len(draft_data))),
            size=len(bottom_player_pos_str),
            replace=False,
        )
        draft_data.iloc[
            bottom_player_pos_indices, draft_data.columns.get_loc(position_column)
        ] = bottom_player_pos_str.values

    # Save the updated DataFrame back to CSV
    draft_data.to_csv(output_file_path, index=False)
    print(
        f"Super draft CSV file updated for middle and bottom leagues at: {output_file_path}\n"
    )
