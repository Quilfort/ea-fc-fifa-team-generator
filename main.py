from my_project.create_own_dataset import create_male_dataset as create_male_dataset
from my_project.analytics import analyze_male_players as analyze_male_players

def main():

    
    make_male_dataset = False
    show_analytics = True

    if make_male_dataset:
        create_male_dataset()

    if show_analytics:
        analyze_male_players()

if __name__ == "__main__":
    main()