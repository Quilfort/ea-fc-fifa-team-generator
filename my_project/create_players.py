"""
This module handles the draft of the different players.
It includes functions to draft player_positions based on specific criteria.
"""

import os
import pandas as pd
import numpy as np


def remove_duplicates(dataframe):
    """
    Remove duplicate players based on their names from the DataFrame.
    """
    dataframe = dataframe.drop_duplicates(subset=["Name"], keep="first")
    return dataframe


def draft_player_position(player_pos_data, criteria, position_column):
    """
    Draft player_positions based on the top ratings and save to a CSV file.
    """
    extra_number = 10
    number_of_top_player_pos = criteria["premier_league"] + extra_number

    player_pos_sorted = player_pos_data.sort_values(by="Overall", ascending=False)
    top_player_pos = player_pos_sorted.head(number_of_top_player_pos)
    top_player_pos = top_player_pos.sample(frac=1).reset_index(drop=True)

    number_of_other_player_pos = (
        criteria["middle_league"] + criteria["bottom_league"] - extra_number
    )
    other_player_pos = player_pos_sorted.iloc[
        number_of_top_player_pos : number_of_top_player_pos + number_of_other_player_pos
    ]

    if len(top_player_pos) >= criteria["premier_league"]:
        premier_player_pos = top_player_pos.head(criteria["premier_league"])
        remaining_player_pos = top_player_pos.tail(extra_number)
    else:
        premier_player_pos = top_player_pos
        remaining_player_pos = pd.DataFrame()

    premier_player_pos_str = premier_player_pos.apply(
        lambda row: ", ".join(map(str, row)), axis=1
    )

    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    draft_data = pd.read_csv(output_file_path, dtype={position_column: "object"})

    draft_data.iloc[
        : criteria["premier_league"], draft_data.columns.get_loc(position_column)
    ] = premier_player_pos_str.values

    if not remaining_player_pos.empty:
        middle_start = criteria["premier_league"]
        middle_end = middle_start + criteria["middle_league"]

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

    draft_data = remove_duplicates(draft_data)

    draft_data.to_csv(output_file_path, index=False)

    draft_middle_low_keepers(other_player_pos, criteria, extra_number, position_column)
    print(f"Super draft CSV file updated at: {output_file_path}\n")


def draft_middle_low_keepers(other_player_pos, criteria, extra_number, position_column):
    """
    Draft middle and bottom league player_positions based on their ratings and fill all remaining slots in the CSV file.
    """

    total_needed_player_pos = criteria["middle_league"] + criteria["bottom_league"]

    other_player_pos_sorted = other_player_pos.sort_values(
        by="Overall", ascending=False
    )
    needed_player_pos = other_player_pos_sorted.head(
        total_needed_player_pos + extra_number
    )
    needed_player_pos = needed_player_pos.sample(frac=1).reset_index(drop=True)

    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")

    draft_data = pd.read_csv(output_file_path, dtype={position_column: "object"})

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

    bottom_start = middle_end
    bottom_end = bottom_start + criteria["bottom_league"]

    if len(draft_data) > bottom_start:
        remaining_needed_for_bottom = criteria["bottom_league"]
        bottom_player_pos = needed_player_pos.iloc[
            len(middle_player_pos) : len(middle_player_pos)
            + remaining_needed_for_bottom
        ]
        bottom_player_pos_str = bottom_player_pos.apply(
            lambda row: ", ".join(map(str, row)), axis=1
        )

        if len(bottom_player_pos) < remaining_needed_for_bottom:
            additional_needed = remaining_needed_for_bottom - len(bottom_player_pos)
            additional_player_pos = needed_player_pos.iloc[-additional_needed:]
            additional_player_pos_str = additional_player_pos.apply(
                lambda row: ", ".join(map(str, row)), axis=1
            )
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

    draft_data = remove_duplicates(draft_data)

    draft_data.to_csv(output_file_path, index=False)
    print(
        f"Super draft CSV file updated for middle and bottom leagues at: {output_file_path}\n"
    )
