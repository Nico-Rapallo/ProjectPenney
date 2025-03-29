import numpy as np
from tqdm import tqdm
from numba import jit


@jit # Decorator converts code to C and runs much faster
def add_tricks(graded_deck:np.ndarray, hand_size:int, num_rows:int) -> tuple[np.ndarray, np.ndarray]:
    '''
    Takes a deck and outputs matrix of number of tricks each combination would have against the others
    '''

    # Set up matrices
    tricks = np.zeros((num_rows,num_rows),dtype=np.int8)
    cards = np.zeros((num_rows,num_rows),dtype=np.int8)
    last_win = np.full((num_rows,num_rows), -hand_size, dtype=np.int8)

    # Update matrices
    for i in range(len(graded_deck)):
        # Set winner to next number in graded deck
        winner = graded_deck[i]

        # Mask positions where last winner was long enough ago 
        # (e.g. can't win on consecutive hands bc only 1 card dealt)
        mask = last_win[winner]>=(i-(hand_size-1))
        
        # Update winners where mask is false
        #   Increment trick by 1
        tricks[winner][mask==False] += 1
        #   Increment card by current position subtracted by position during last win
        cards[winner][mask==False] += i-last_win[winner][mask==False]

        # update last win matrix for winning/losing column/row
        last_win[:,winner][mask==False] = i
        last_win[winner][mask==False] = i
        
    return tricks, cards