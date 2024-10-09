# ea-fc-fifa-team-generator

## About

Hey there! I kicked off this project after diving into career mode with AZ Alkmaar in EA FC24 and being less than impressed with the player faces in the Eredivisie. So, I decided to shake things up by randomizing all the players across the three different leagues in English football. It’s not just about making things look better; I’m using this as a chance to get a grip on Python, random algorithms, and AI tools. It’s been a fun journey, and I’m excited to see where it goes!

his project is still a work in progress, and I’m looking forward to adding settings, drafting women players, and even incorporating EA FC25 and a drafting game in the future. It’s been a fun journey, and I can’t wait to see where it goes! Let me know if you need any more adjustments!

## Install Project

```sh
git clone git@github.com:Quilfort/ea-fc-fifa-team-generator.git # if using SSH
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### or

For Mac

```sh
make setup
```

## Run Project

```sh
python main.py
```

## Dataset

### Original Dataset

The dataset for EA FC24 is created by Davis Nyagami ([@nyagami](https://www.kaggle.com/nyagami)).
You can download the dataset from Kaggle by clicking on [this link](https://www.kaggle.com/datasets/nyagami/fc-24-players-database-and-stats-from-easports)

### Edited Dataset

The edited dataset will be created in `create_own_dataset`. The basic dataset will create a male list with the following attributes

- 'Name'
- 'Nation'
- 'Club'
- 'Position'
- 'Age'
- 'Overall'

---

## Analytics

At the moment, the analytics script is just for the fun. It will display the distribution of the male players in the dataset.

### Linting

```sh
black .
```

```sh
pylint my_project/
```

### Virtual Environment.

##### Activate (Mac)

```sh
source venv/bin/activate
```

##### Activate (Windows)

```sh
venv\Scripts\activate
```

##### Install Packages

```sh
pip [Command]
```

#### Generate or Update Requirements

```sh
pip freeze > requirements.txt
```

##### Deactivate (Mac)

```sh
deactivate
```
