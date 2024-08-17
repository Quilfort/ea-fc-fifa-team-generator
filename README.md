# ea-fc-fifa-team-generator

## About

Project is based for the English Leagues

## Install Project

```sh
git clone git@github.com:Quilfort/ea-fc-fifa-team-generator.git # if using SSH
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
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

## Virtual Environment.

#### Activate (Mac)

```sh
source venv/bin/activate
```

#### Activate (Mac)

```sh
venv\Scripts\activate
```

#### Install Packages

```sh
pip [Command]
```

### Generate or Update Requirements

```sh
pip freeze > requirements.txt
```

#### Deactivate (Mac)

```sh
deactivate
```
