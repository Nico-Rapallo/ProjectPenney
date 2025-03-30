# Project Penney
### Nico Rapallo
### Professor Smith
### DATA 440: Automations and Workflows
### March 2024

## Overview
This repository generates and scores decks for the card version of Penney's Game and creates heatmap visualizations of win/loss rates. It scores for both trick and total card scoring variants. It is compatable with what any n-card variant of the game where 2<=n<=7 (7 is arbitrary cut-off). It contains 1-million decks pre-generated and scored as well as win/loss rate heatmap visualizations for every hand-size.

---

## Quick Start

Clone Repository:

`git clone https://github.com/Nico-Rapallo/ProjectPenney`

Sync uv sync:

`uv sync`

Run main:

`uv run main.py`

---

## Files included:

`src/`

- Decks_Class.py: Contains class that generates and saves scores for an array of n decks.

- helpers.py: Contains helper functions and variables needed across various other modules.

- processing.py: Contains the function to score a game.

- visualization.py: Contains code to visualize results as a heatmap.

- datadashboard.py: Contains code for assembling PyQt5 user interface.

- qtcomponents.py: Includes code for base parts / widgets for the datadashboard.

- engine.py: Contains ProjectPenney code datadashboard will need to run in a class for it to use.

- used_seeds.npy: Is an array which keeps track of used seeds for reproducability.

- `Scores/`: 
    -  Contains matrices of all wins/losses for given hand size and scoring method. 
    - Files follow naming pattern: `Scores/{Scoring method: T or C}_{Wins or Losses}_hand_size{hand size: number 2 to 7}.npy`

- `Decks/`: 
    -  `to_load/`: Where decks are store temporarily before scoring but after generation
    - `loaded/`: Where scored decks are stored. Note: I have deleted all stored decks in order to push to github, but can still be verified through seed, numdecks, and score tables
    - File name of decks follow patter: `Decks/{to_load / loaded}/seed{seed number: integer}_(hand_size{hand_size: number 2 to 7}).npz`

- `Decks_Counts/`: 
    - Contains count of all decks run for each seed
    - Individual counts stored with file path pattern: `Decks_Counts/Deck_Count_hand_size{hand size: number 2 to 7}.npy`

`figures/`
- All visualizations are stored in figures. 
- File path of figures follow pattern: `figures/{Cards or Tricks}_hand_size_{hand size: number 2 to 7}.npy`

`main.py`:
- Generates and scores n decks based on user input. Updates scores and visualizations.
- Gives user option to 
    0) Launch interface, 
    1) Run default 100k decks with hand size 3, 
    2) Launch terminal interface for custom number of decks and cards, or 
    3) Clear all contents

---

This project is maintained using the [uv package manager](https://docs.astral.sh/uv/).