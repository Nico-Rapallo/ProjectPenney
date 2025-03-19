import numpy as np
from tqdm import tqdm
import os
from src.processing import *
from src.helpers import *

class Deck_Array():
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.seed = self.get_seed()
        
        self.T_Wins = np.zeros((8, 8), dtype = int)
        self.T_Losses = np.zeros((8, 8), dtype = int)
        self.T_Ties = np.zeros((8, 8), dtype = int)
        self.C_Wins = np.zeros((8, 8), dtype = int)
        self.C_Losses = np.zeros((8, 8), dtype = int)
        self.C_Ties = np.zeros((8, 8), dtype = int)

        self.decks_array = self.get_decks_array()
        self.save_decks_array()
        return
        
    def get_seed(self):
        if not os.path.exists('src/Decks/used_seeds.npy'):
            used_seeds = np.array([-1])
            deck_lengths = np.array([0])
        else:
            used_seeds = np.load('src/Decks/used_seeds.npy')
            deck_lengths = np.load('src/Decks/deck_lengths.npy')
        seed = used_seeds[-1]+1
        used_seeds = np.append(used_seeds, seed)
        deck_lengths = np.append(deck_lengths, self.num_decks)
        np.save('src/Decks/deck_lengths.npy', deck_lengths)
        np.save('src/Decks/used_seeds.npy', used_seeds)
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
        path = PATH_TO_LOAD + f"seed_{self.seed}.npy"
        np.save(path, self.decks_array)
        return

    def run_decks_array(self) -> None:        
        for deck in tqdm(self.decks_array):

            tricks, cards = add_tricks(deck)

            self.T_Wins[(tricks>tricks.T)==True]+=1
            self.T_Losses[(tricks<tricks.T)==True]+=1

            self.C_Wins[(cards>cards.T)==True]+=1
            self.C_Losses[(cards<cards.T)==True]+=1

        self.save_scores()
        path = PATH_TO_LOAD + f"seed_{self.seed}.npy"
        os.rename(path, path.replace(PATH_TO_LOAD, PATH_LOADED))
        return
        
    def save_scores(self):
        seed_path = f'seed_{self.seed}.npy'
        
        np.save(SCORES_PATH+'T_WINS/T_Wins_'+seed_path, self.T_Wins)
        np.save(SCORES_PATH+'T_LOSSES/T_Losses_'+seed_path, self.T_Losses)
        np.save(SCORES_PATH+'T_TIES/T_Ties_'+seed_path, self.T_Ties)
        
        np.save(SCORES_PATH+'C_WINS/C_Wins_'+seed_path, self.C_Wins)
        np.save(SCORES_PATH+'C_LOSSES/C_Losses_'+seed_path, self.C_Losses)
        np.save(SCORES_PATH+'C_TIES/C_Ties_'+seed_path, self.C_Ties)
        return