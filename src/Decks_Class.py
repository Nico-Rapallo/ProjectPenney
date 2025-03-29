import numpy as np
from tqdm import tqdm
import os
from src.processing import add_tricks
from src.helpers import debugger_factory, HALF_DECK_SIZE, HAND_SIZE, PATH_LOADED, PATH_TO_LOAD, SCORES_PATH
from numba import jit

class Deck_Array():
    '''
    Create Deck_Array Class
    Contains functions to create, save, and score decks as well as 

    '''

    def __init__(self, num_decks:int, hand_size:int = HAND_SIZE):

        # Initialize num_decks, seed, hand_size, and num_rows
        self.num_decks = num_decks
        self.seed = self.get_seed()
        self.hand_size = hand_size
        self.num_rows = 2**hand_size

        # Initialize Win/Loss matrices
        self.T_Wins = np.zeros((self.num_rows, self.num_rows), dtype = int)
        self.T_Losses = np.zeros((self.num_rows, self.num_rows), dtype = int)
        self.C_Wins = np.zeros((self.num_rows, self.num_rows), dtype = int)
        self.C_Losses = np.zeros((self.num_rows, self.num_rows), dtype = int)


        # If Score Matrix files do not exist yet, create them.
        #   Trick Matrices
        if not os.path.exists('src/Scores/T_Wins_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/T_Wins_hand_size'+str(self.hand_size)+'.npy', self.T_Wins)
        if not os.path.exists('src/Scores/T_Losses_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/T_Losses_hand_size'+str(self.hand_size)+'.npy', self.T_Losses)
        #   Cards Martices
        if not os.path.exists('src/Scores/C_Wins_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/C_Wins_hand_size'+str(self.hand_size)+'.npy', self.C_Wins)
        if not os.path.exists('src/Scores/C_Losses_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Scores/C_Losses_hand_size'+str(self.hand_size)+'.npy', self.C_Losses)
        
        # Add new number of decks to existing number of decks
        # If deck_counts does not exist, create it.
        if not os.path.exists('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy'):
            np.save('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy', self.num_decks)
        else:
            total_decks = np.load('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy')
            np.save('src/Deck_Counts/Deck_Counts_hand_size'+str(self.hand_size)+'.npy', self.num_decks+total_decks)
        
        # Initialize array of decks, decks_array
        self.decks_array = self.get_decks_array()

        # Save decks
        self.save_decks_array()

        return
        
    def get_seed(self) -> int:
        '''
        Gets next seed. Updates used_seeds to reflect this seed is now used.

        Returns:
            seed (int): seed to be used for deck generation.
        '''
        # used seeds does not exist create it, otherwise load used_seeds
        if not os.path.exists('src/used_seeds.npy'):
            # create used_seeds array with only [-1]
            used_seeds = np.array([-1])
        else:
            # load used_seeds
            used_seeds = np.load('src/used_seeds.npy')

        # Get last seed in array and add one.
        seed = used_seeds[-1]+1

        # Append new seed to end of used_seeds
        used_seeds = np.append(used_seeds, seed)

        # Save updated used_seeds
        np.save('src/used_seeds.npy', used_seeds)

        return int(seed)
   

    def get_decks_array(self, half_deck_size: int = HALF_DECK_SIZE) -> tuple[np.ndarray, np.ndarray]:
        """
        Efficiently generate `n_decks` shuffled decks using NumPy.
        
        Returns:
            decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
            each row is a shuffled deck.
        """

        # initialize deck with ones and zeros
        init_deck = [0]*half_deck_size + [1]*half_deck_size

        # Create 2d array with num_decks copy of initial deck
        decks = np.tile(init_deck, (self.num_decks, 1))
        
        # Creates rng so shuffle can be reproduced
        rng = np.random.default_rng(self.seed)

        # Shuffles all decks
        rng.permuted(decks, axis=1, out=decks)

        return decks

    def save_decks_array(self) -> None:
        '''
        Saves deck array to src/Decks/to_load in compressed form.
        Returns: None
        '''
        
        # Save compressed deck_array
        path = PATH_TO_LOAD + f"seed_{self.seed}.npz"
        np.savez_compressed(path, self.decks_array)
        return None

    def run_decks_array(self) -> None:
        '''
        Scores all decks in decks_array

        Returns: None
        '''

        # Iterates through every deck in decks_array
        for deck in tqdm(self.decks_array, mininterval=1):
            # Create graded_deck,
            #   Array of ints for __ sized binary sequence in deck

            #   Windows is array of every sequence of __ in deck
            windows = np.lib.stride_tricks.sliding_window_view(deck, self.hand_size)
            #   Creates weights for converting binary sequences to ints
            weights = 2 ** np.arange(self.hand_size - 1, -1, -1)

            # T akes dot product of windows and weights which outputs the int that represents each binary sequence
            graded_deck = windows.dot(weights)

            # Calls add_tricks to grade deck. 
            # (Maybe rename add tricks because it also adds cards (named when it only did tricks))
            tricks, cards = add_tricks(graded_deck, self.hand_size, self.num_rows)
            
            # Adds wins and losses for tricks
            # (Losses and Wins are transposes of each other)
            self.T_Wins[(tricks>tricks.T)==True]+=1
            self.T_Losses[(tricks<tricks.T)==True]+=1

            # Adds wins and losses for cards
            self.C_Wins[(cards>cards.T)==True]+=1
            self.C_Losses[(cards<cards.T)==True]+=1

        # save scores
        self.save_scores()

        # move decks from to_load to loaded
        path = PATH_TO_LOAD + f"seed_{self.seed}.npz"
        os.rename(path, path.replace(PATH_TO_LOAD, PATH_LOADED))

        return None
        
    def save_scores(self) -> None:
        '''
        Saves scores
        Returns: None
        '''

        # Update old Trick Wins table with new data
        Total_T_Wins = np.load(SCORES_PATH+'T_Wins_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'T_Wins_hand_size'+str(self.hand_size)+'.npy', self.T_Wins + Total_T_Wins)

        # Update T_Losses
        Total_T_Losses = np.load(SCORES_PATH+'T_Losses_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'T_Losses_hand_size'+str(self.hand_size)+'.npy', self.T_Losses + Total_T_Losses)

        # Update C_Wins
        Total_C_Wins =  np.load(SCORES_PATH+'C_Wins_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'C_Wins_hand_size'+str(self.hand_size)+'.npy', self.C_Wins + Total_C_Wins)

        # Update C_Losses
        Total_C_Losses =  np.load(SCORES_PATH+'C_Losses_hand_size'+str(self.hand_size)+'.npy')
        np.save(SCORES_PATH+'C_Losses_hand_size'+str(self.hand_size)+'.npy', self.C_Losses + Total_C_Losses)
        
        return None