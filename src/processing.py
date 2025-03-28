import numpy as np
from tqdm import tqdm
from numba import jit
HALF_DECK_SIZE = 26


@jit
def add_tricks(graded_deck:np.ndarray, hand_size:int, num_rows:int):
    '''
    Takes a deck and outputs matrix of number of tricks each combination would have against the others
    '''

    # Set up matrices
    tricks = np.zeros((num_rows,num_rows),dtype=np.int8)
    cards = np.zeros((num_rows,num_rows),dtype=np.int8)
    last_win = np.full((num_rows,num_rows), -hand_size, dtype=np.int8)

    # Update matrices
    for i in range(len(graded_deck)):
        winner = graded_deck[i]
        mask = last_win[winner]>=(i-(hand_size-1))
        tricks[winner][mask==False] += 1
        cards[winner][mask==False] += i-last_win[winner][mask==False]
        last_win[:,winner][mask==False] = i
        last_win[winner][mask==False] = i
        
    return tricks, cards