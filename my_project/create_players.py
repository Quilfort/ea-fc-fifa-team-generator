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

    draft_middle_low_leagues(other_player_pos, criteria, extra_number, position_column)
    # print(f"Super draft CSV file updated at: {output_file_path}\n")


def draft_middle_low_leagues(other_player_pos, criteria, extra_number, position_column):
    """
    Draft middle and bottom league player_positions based on their ratings
     and fill all remaining slots in the CSV file.
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
    # print(
    #     f"Super draft CSV file updated for middle and bottom leagues at: {output_file_path}\n"
    # )


def draft_top_cbs(datafile, criteria, extra_number):
    """
    Draft player_positions for multiple based on the top ratings and save to a CSV file.
    """

    # Filter data for CB position
    cb_data = datafile[datafile["Position"] == "CB"]

    # Sort CBs by Overall rating
    cb_sorted = cb_data.sort_values(by="Overall", ascending=False)

    # Select top CBs (double the amount for premier league plus extra)
    number_of_top_cbs = (criteria["premier_league"] * 2) + extra_number
    top_cbs = cb_sorted.head(number_of_top_cbs)

    # Shuffle the top CBs
    top_cbs = top_cbs.sample(frac=1).reset_index(drop=True)

    # Split top CBs for CB1 and CB2
    cb1_top = top_cbs.iloc[: len(top_cbs) // 2]
    cb2_top = top_cbs.iloc[len(top_cbs) // 2 :]

    # Convert to string format
    cb1_top_str = cb1_top.apply(lambda row: ", ".join(map(str, row)), axis=1)
    cb2_top_str = cb2_top.apply(lambda row: ", ".join(map(str, row)), axis=1)

    # Read the existing draft data
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")
    draft_data = pd.read_csv(output_file_path)

    # Ensure CB1 and CB2 columns are of type object (string)
    draft_data["CB1"] = draft_data["CB1"].astype("object")
    draft_data["CB2"] = draft_data["CB2"].astype("object")

    # Update CB1 and CB2 columns for premier league
    draft_data.loc[: criteria["premier_league"] - 1, "CB1"] = cb1_top_str.values[
        : criteria["premier_league"]
    ]
    draft_data.loc[: criteria["premier_league"] - 1, "CB2"] = cb2_top_str.values[
        : criteria["premier_league"]
    ]

    # Save the updated draft data
    draft_data.to_csv(output_file_path, index=False)

    return cb_sorted.iloc[number_of_top_cbs:]


def draft_middle_bottom_cbs(remaining_cbs, criteria, extra_number):
    """
    Draft middle and bottom league player_positions for multple positions based on their ratings
     and fill all remaining slots in the CSV file.
    """
    # Calculate the number of CBs needed for middle and bottom leagues
    total_needed_cbs = (criteria["middle_league"] + criteria["bottom_league"]) * 2

    # Select and shuffle the needed CBs
    needed_cbs = remaining_cbs.head(total_needed_cbs + extra_number)
    needed_cbs = needed_cbs.sample(frac=1).reset_index(drop=True)

    # Split CBs for middle and bottom leagues
    middle_cbs = needed_cbs.head(criteria["middle_league"] * 2)
    bottom_cbs = needed_cbs.iloc[len(middle_cbs) : total_needed_cbs]

    # Further split for CB1 and CB2
    cb1_middle = middle_cbs.iloc[::2]
    cb2_middle = middle_cbs.iloc[1::2]
    cb1_bottom = bottom_cbs.iloc[::2]
    cb2_bottom = bottom_cbs.iloc[1::2]

    # Convert to string format
    cb1_middle_str = cb1_middle.apply(lambda row: ", ".join(map(str, row)), axis=1)
    cb2_middle_str = cb2_middle.apply(lambda row: ", ".join(map(str, row)), axis=1)
    cb1_bottom_str = cb1_bottom.apply(lambda row: ", ".join(map(str, row)), axis=1)
    cb2_bottom_str = cb2_bottom.apply(lambda row: ", ".join(map(str, row)), axis=1)

    # Read the existing draft data
    leagues_path = os.getenv("LEAGUES_PATH")
    output_file_path = os.path.join(leagues_path, "super_draft.csv")
    draft_data = pd.read_csv(output_file_path)

    # Ensure CB1 and CB2 columns are of type object (string)
    draft_data["CB1"] = draft_data["CB1"].astype("object")
    draft_data["CB2"] = draft_data["CB2"].astype("object")

    # Update CB1 and CB2 columns for middle and bottom leagues
    middle_start = criteria["premier_league"]
    middle_end = middle_start + criteria["middle_league"]
    bottom_start = middle_end
    bottom_end = bottom_start + criteria["bottom_league"]

    draft_data.loc[middle_start : middle_end - 1, "CB1"] = cb1_middle_str.values
    draft_data.loc[middle_start : middle_end - 1, "CB2"] = cb2_middle_str.values
    draft_data.loc[bottom_start : bottom_end - 1, "CB1"] = cb1_bottom_str.values
    draft_data.loc[bottom_start : bottom_end - 1, "CB2"] = cb2_bottom_str.values

    # Save the updated draft data
    draft_data.to_csv(output_file_path, index=False)
