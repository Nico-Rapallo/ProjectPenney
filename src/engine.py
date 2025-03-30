from src.Decks_Class import Deck_Array
from src.visualization import gen_heatmap
from src.helpers import clear_all
import os
import matplotlib.pyplot as plt

class Engine():
    def __init__(self):
        self.num_decks = 100_000
        self.hand_size = 3
        self.trick = True
        if os.path.exists('src/Scores/T_Wins_hand_size'+str(self.hand_size)+'.npy'):
            self.fig = gen_heatmap(hand_size=self.hand_size, trick = self.trick)
        else:
            self.fig = plt.figure()
        return
    
    def new_decks(self):
        decks = Deck_Array(self.num_decks, self.hand_size)
        # Score decks
        decks.run_decks_array()
        # Generate visualizations
        self.fig = gen_heatmap(hand_size=self.hand_size, trick = self.trick)
        return None
    
    def change_num_decks(self, input:int):
         self.num_decks = input
         return None
    
    def change_hand_size(self, input:int):
        self.hand_size = input
        return None
    
    def change_score_method(self, cards:bool):
        self.trick = not cards
        return None

    def clear_all_decks(self):
        clear_all()
        self.fig = plt.figure()
        return None