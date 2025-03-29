from typing import Callable
from datetime import datetime as dt
import pandas as pd
import numpy as np
import os

# Set half_deck_size (can be changed later for other variations)
HALF_DECK_SIZE = 26

# Set default hand size (I let user change this)
HAND_SIZE = 3

# Set paths
PATH_TO_LOAD = 'src/Decks/to_load/'
PATH_LOADED = 'src/Decks/loaded/'
SCORES_PATH = 'src/SCORES/'

def debugger_factory(show_args = True) -> Callable:
    def debugger(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if show_args:
                print(f'{func.__name__} was called with:')
                print('Positional arguments:\n', args)
                print('Keyword arguments:\n', kwargs)
            t0 = dt.now()
            results = func(*args, **kwargs)
            print(f'{func.__name__} ran for {dt.now() - t0}')
            return results
        return wrapper
    return debugger

def clear_all() -> None:
    '''
    Clears all Decks, Total Deck Counter, Seeds, and Visualizations.
    Used during testing to reset. User may also want to use to start from scratch.

    Returns: None
    '''

    # Clear all decks
    for file in os.listdir(PATH_TO_LOAD):
        # Could not figure out why .gitignore is not working, so manually ignore .DS_Store and .ipynb_checkpoints
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove(PATH_TO_LOAD + file) 
    for file in os.listdir(PATH_LOADED):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove(PATH_LOADED + file)

    # Clear all scores
    for file in os.listdir(SCORES_PATH):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove(SCORES_PATH + file)

    # Clear Deck_Counts
    for file in os.listdir('src/' + 'Deck_Counts/'):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove('src/' + 'Deck_Counts/' + file)

    # Clear used seeds (make sure it exists)
    if os.path.exists('src/used_seeds.npy'):
        os.remove('src/used_seeds.npy')

    # Clear all figures
    for file in os.listdir('figures/'):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove('figures/' + file)
    
    return None