import numpy as np
from tqdm import tqdm
import os
from src.processing import *
from src.helpers import *
from numba import jit

HAND_SIZE = 3

class Deck_Array():
    def __init__(self, num_decks:int, hand_size:int = HAND_SIZE):
        self.num_decks = num_decks
        self.seed = self.get_seed()

        self.hand_size = hand_size
        self.num_rows = 2**hand_size
        self.T_Wins = np.zeros((self.num_rows, self.num_rows), dtype = int)
        self.T_Losses = np.zeros((self.num_rows, self.num_rows), dtype = int)
        self.C_Wins = np.zeros((self.num_rows, self.num_rows), dtype = int)
        self.C_Losses = np.zeros((self.num_rows, self.num_rows), dtype = int)


        # If necessary files do not exist yet, create them.
        if not os.path.exists('src/Scores/T_Wins_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/T_Wins_hand_size'+str(self.hand_size)+'.npy', self.T_Wins)
        if not os.path.exists('src/Scores/T_Losses_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/T_Losses_hand_size'+str(self.hand_size)+'.npy', self.T_Losses)

        if not os.path.exists('src/Scores/C_Wins_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/C_Wins_hand_size'+str(self.hand_size)+'.npy', self.C_Wins)
        if not os.path.exists('src/Scores/C_Losses_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/C_Losses_hand_size'+str(self.hand_size)+'.npy', self.C_Losses)
    
        if not os.path.exists('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy', self.num_decks)
        else:
            total_decks = np.load('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy')
            np.save('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy', self.num_decks+total_decks)
        
        self.decks_array = self.get_decks_array()
        self.save_decks_array()

        return
        
    def get_seed(self):
        if not os.path.exists('src/used_seeds.npy'):
            used_seeds = np.array([-1])
            # deck_lengths = np.array([0])
        else:
            used_seeds = np.load('src/used_seeds.npy')
            # deck_lengths = np.load('src/Decks/deck_lengths.npy')
        seed = used_seeds[-1]+1
        used_seeds = np.append(used_seeds, seed)
        # deck_lengths = np.append(deck_lengths, self.num_decks)
        # np.save('src/Decks/deck_lengths.npy', deck_lengths)
        np.save('src/used_seeds.npy', used_seeds)
        return int(seed)
   

    def get_decks_array(self, half_deck_size: int = HALF_DECK_SIZE) -> tuple[np.ndarray, np.ndarray]:
        """
        Efficiently generate `n_decks` shuffled decks using NumPy.
        
        Returns:
            decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
            each row is a shuffled deck.
        """
        init_deck = [0]*half_deck_size + [1]*half_deck_size
        decks = np.tile(init_deck, (self.num_decks, 1))
        rng = np.random.default_rng(self.seed)
        rng.permuted(decks, axis=1, out=decks)
        return decks

    def save_decks_array(self) -> str:
        path = PATH_TO_LOAD + f"seed_{self.seed}.npz"
        np.savez_compressed(path, self.decks_array)
        return

    def run_decks_array(self) -> None:        
        for deck in tqdm(self.decks_array, mininterval=1):
            # Create graded_deck
            windows = np.lib.stride_tricks.sliding_window_view(deck, self.hand_size)
            weights = 2 ** np.arange(self.hand_size - 1, -1, -1)
            graded_deck = windows.dot(weights)

            tricks, cards = add_tricks(graded_deck, self.hand_size, self.num_rows)

            self.T_Wins[(tricks>tricks.T)==True]+=1
            self.T_Losses[(tricks<tricks.T)==True]+=1

            self.C_Wins[(cards>cards.T)==True]+=1
            self.C_Losses[(cards<cards.T)==True]+=1

        self.save_scores()
        path = PATH_TO_LOAD + f"seed_{self.seed}.npz"
        os.rename(path, path.replace(PATH_TO_LOAD, PATH_LOADED))
        return
        
    def save_scores(self):
        seed_path = f'seed_{self.seed}'


        Total_T_Wins = np.load(SCORES_PATH+'T_Wins_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'T_Wins_hand_size'+str(self.hand_size)+'.npy', self.T_Wins + Total_T_Wins)

        Total_T_Losses = np.load(SCORES_PATH+'T_Losses_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'T_Losses_hand_size'+str(self.hand_size)+'.npy', self.T_Losses + Total_T_Losses)

        Total_C_Wins =  np.load(SCORES_PATH+'C_Wins_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'C_Wins_hand_size'+str(self.hand_size)+'.npy', self.C_Wins + Total_C_Wins)

        Total_C_Losses =  np.load(SCORES_PATH+'C_Losses_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'C_Losses_hand_size'+str(self.hand_size)+'.npy', self.C_Losses + Total_C_Losses)
        
        return None