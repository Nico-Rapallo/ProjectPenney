from typing import Callable
from datetime import datetime as dt
import pandas as pd
import numpy as np
import os

HALF_DECK_SIZE = 26
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
    Clears all Decks, Seeds, Visualizations, Decks Lengths
    '''

    for file in os.listdir(PATH_TO_LOAD):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove(PATH_TO_LOAD + file)
            
    for file in os.listdir(PATH_LOADED):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove(PATH_LOADED + file)

    for file in os.listdir(SCORES_PATH):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove(SCORES_PATH + file)

    for file in os.listdir('src/' + 'Deck_Counts/'):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove('src/' + 'Deck_Counts/' + file)

    if os.path.exists('src/used_seeds.npy'):
        os.remove('src/used_seeds.npy')

    for file in os.listdir('figures/'):
        if not(file == '.DS_Store' or file == '.ipynb_checkpoints'):
            os.remove('figures/' + file)
    
    return None