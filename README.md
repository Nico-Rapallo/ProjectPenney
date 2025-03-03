## Project Penney

This repository generates and scores decks for the 3-card version of Penney's Game

---

Files included:

`src/`

- Decks_Class.py: Contains class that generates and saves scores for an array of n decks

- helpers.py: Contains helper functions and variables needed across various other modules.

- processing.py: Contains the function to score a games.

- visualization.py: Contains code to visualize results as a heatmap

- `Scores/`: Contains scoring for all decks in terms of total cards (C_WINS, C_LOSSES, C_TIES) and by tricks (T_WINS, T_LOSSES, T_TIES). Also contains `seeds+num_cards`, where seeds and associated number of cards are stored.

- `Decks`: 
    -  `to_load/`: Where decks are store temporarily before scoring but after generation
    - `loaded/`: Where scored decks are stored. Note: I have deleted all stored decks in order to push to github, but can still be verified through seed, numdecks, and score tables

`figures/`

- All visualizations are stored in figures.

main.py: Generates and scores n decks based on user input. Updates scores and visualizations.

---

This project is maintained using the [uv package manager](https://docs.astral.sh/uv/).