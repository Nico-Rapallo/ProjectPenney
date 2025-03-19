from typing import Callable
from datetime import datetime as dt
import pandas as pd
import numpy as np
import os

HALF_DECK_SIZE = 26
PATH_TO_LOAD = 'src/Decks/to_load/'
PATH_LOADED = 'src/Decks/loaded/'
SCORES_PATH = 'src/SCORES/'
TABLES_PATHS = ['T_WINS/', 'T_LOSSES/', 'T_TIES/', 'C_WINS/', 'C_LOSSES/', 'C_TIES/']
ALL_PLAYERS =[[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]

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

def get_complete_tables():
    T_Wins = np.zeros((8, 8), dtype = int)
    T_Losses = np.zeros((8, 8), dtype = int)
    T_Ties = np.zeros((8, 8), dtype = int)
    C_Wins = np.zeros((8, 8), dtype = int)
    C_Losses = np.zeros((8, 8), dtype = int)
    C_Ties = np.zeros((8, 8), dtype = int)
    
    for table in TABLES_PATHS:
        for file in os.listdir(SCORES_PATH + table):
            if file == '.DS_Store': continue
            new_table = np.load(SCORES_PATH + table + file)
            if table == 'T_WINS/':T_Wins += new_table
            elif table == 'T_LOSSES/':T_Losses += new_table   
            elif table == 'C_WINS/':C_Wins += new_table  
            elif table == 'C_LOSSES/':C_Losses += new_table 
            
    
    labels = list(map(str, ALL_PLAYERS))
    T_Wins = pd.DataFrame(T_Wins, labels, labels)
    T_Losses = pd.DataFrame(T_Losses, labels, labels)
    
    C_Wins = pd.DataFrame(C_Wins, labels, labels)
    C_Losses = pd.DataFrame(C_Losses, labels, labels)
    
    return T_Wins, T_Losses, C_Wins, C_Losses

def get_converged_decimal():

    T_Wins, T_Losses, T_Ties, C_Wins, C_Losses, C_Ties = get_complete_tables()
    Total = T_Wins+T_Losses+T_Ties
    Total = Total+Total.T

    Tricks = T_Wins + T_Losses.T
    Tricks = Tricks/Total

    i_tricks = 0
    converged = True
    while converged == True:
        i_tricks+=1
        for x in range(8):
            for y in range(x,8):
                if x==y:
                    continue
                if (round((Tricks).iloc[x,y] - (Tricks).iloc[7-x,7-y], i_tricks)!=0):
                    converged = False
                    i_tricks-=1
                    break

    Cards = C_Wins+C_Losses.T
    Cards = Cards/Total

    i_cards = 0
    converged = True
    while converged == True:
        i_cards+=1
        for x in range(8):
            for y in range(x,8):
                if x==y:
                    continue
                if (round((Cards).iloc[x,y] - (Cards).iloc[7-x,7-y], i_cards)!=0):
                    converged = False
                    i_cards-=1
                    break
    
    return i_tricks, i_cards