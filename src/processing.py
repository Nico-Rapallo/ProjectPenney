import numpy as np
from tqdm import tqdm
from numba import jit
HALF_DECK_SIZE = 26

@jit
def add_tricks(deck, half_deck_size: int = HALF_DECK_SIZE):
    '''
    Takes a deck and outputs matrix of number of tricks each combination would have against the others
    '''
    graded_deck = (deck[:-2] << 2) + (deck[1:-1] << 1) + deck[2:]
    tricks = np.zeros((8,8),dtype=np.int8)
    cards = np.zeros((8,8),dtype=np.int8)
    last_win = np.full((8,8), -3, dtype=np.int8)
    
    for i in range(0, (half_deck_size*2)-2):
        winner = graded_deck[i]
        mask = last_win[winner]>=(i-2)
        tricks[winner][mask==False] += 1
        cards[winner][mask==False] += i-last_win[winner][mask==False]
        last_win[:,winner][mask==False] = i
        last_win[winner][mask==False] = i
    return tricks, cards