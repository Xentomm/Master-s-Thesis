# Master-s-Thesis: The analysis of biomedical signals while playing the logic games

The aim of the study is to investigate changes in biomedical signals such as facial surface temperature distribution (IR thermography), EEG, EKG, or GRS signals during playing logical games such as bridge or chess. The task of the diploma student is to develop a biometric profile of the individual and examine changes in this profile during increased mental activity. In addition, the study will explore the application of AI/ML algorithms to analyze the obtained signals. These algorithms will enable the extraction of meaningful patterns and insights from the complex biomedical data, aiding in the identification of correlations between cognitive activity and physiological responses.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Team Members](#team-members)

## Installation

```bash
$ git clone https://github.com/Xentomm/Master-s-Thesis.git
$ cd project-name
$ python -m venv .env (or conda)
$ source .env/Scripts/actiavate (Windows) | source .env/bin/activate (Linux)
$ python.exe -m pip install --upgrade pip
$ pip install -r requirements.txt
```

## Usage

Run the .bat file or the main.py.

## Features 

Data application features:

- Gathering data from camera and thermal camera
- Gathering data from Advantech DAQ 
- Saving data to .csv and .npz files
- User interface
- Creating logs for basic workflow and click control
- Simple visualization of gathered data

AI/ML features:

- SVM
- Transfer Learining

## Team members

- [Łukasz Erimus](https://github.com/Xentomm)
- [Adrian Jaromin](https://github.com/IcyArcticc)
