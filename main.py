from my_project.analytics import analyze_male_players as analyze
from my_project.create_own_dataset import create_male_dataset as create
def main():

    
    make_male_dataset = False
    show_analytics = True

    if make_male_dataset:
        create()

    if show_analytics:
        analyze()

if __name__ == "__main__":
    main()