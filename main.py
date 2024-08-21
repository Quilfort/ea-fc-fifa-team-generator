"""
main.py

This script serves as the entry point for the EA FC Team Generator Tool. 
It controls the execution flow of the tool based on predefined flags 
and prints a banner to welcome users.
"""

from my_project.analytics import analyze_male_players as analyze
from my_project.create_own_dataset import create_male_dataset as create
from my_project.create_super_league import create_draft as draft


def main():
    """
    Main function to run the EA FC Team Generator Tool.
    Controls the flow of the script based on flags.
    """
    print_banner()

    # Flags to control which parts of the tool are run
    make_male_dataset = False
    show_analytics = False
    start_draft = True

    # Create the dataset if the flag is set
    if make_male_dataset:
        create()

    # Show analytics if the flag is set
    if show_analytics:
        analyze()

    # Start the draft if the flag is set
    if start_draft:
        draft()


def print_banner():
    """
    Prints a banner for the EA FC Team Generator Tool.
    Displays the tool's name, creator, and GitHub link.
    """
    width = 40

    print("=" * width)
    print("Welcome to the EA FC Team Generator Tool".center(width))
    print("=" * width)
    print("Created by Quilfort".center(width))
    print("GitHub: https://github.com/Quilfort".center(width))
    print("=" * width)
    print("\n")


if __name__ == "__main__":
    main()
