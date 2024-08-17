from my_project.analytics import analyze_male_players as analyze
from my_project.create_own_dataset import create_male_dataset as create

def main():
    print_banner()
    
    make_male_dataset = False
    show_analytics = False

    if make_male_dataset:
        create()

    if show_analytics:
        analyze()


def print_banner():
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