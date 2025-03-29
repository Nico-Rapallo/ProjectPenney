from src.helpers import SCORES_PATH
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def gen_heatmap(hand_size:int = 3) -> None:
    '''
    Generates heatmaps for cards and tricks. Takes hand size as arguement. 
    
    Returns: None
    '''

    # Loads Win and Loss matrices for Tricks and Cards of certain hand size
    Trick_Wins = np.load(SCORES_PATH + 'T_Wins_hand_size' + str(hand_size) + '.npy')
    Trick_Losses = np.load(SCORES_PATH + 'T_Losses_hand_size' + str(hand_size) + '.npy')
    Cards_Wins = np.load(SCORES_PATH + 'C_Wins_hand_size' + str(hand_size) + '.npy')
    Cards_Losses = np.load(SCORES_PATH + 'C_Losses_hand_size' + str(hand_size) + '.npy')

    # Loads number of total generated and scored decks of certain hand size. 
    total = np.load('src/Deck_Counts/Deck_Counts_hand_size' + str(hand_size) + '.npy')

    # Calculates win and loss percentage matrices for tricks
    trick_win_percent = (Trick_Wins)/total
    trick_loss_percent = (Trick_Losses)/total

    # Create tricks figures
    create_graphs(trick_win_percent, trick_loss_percent, total, 'Tricks', hand_size)

    # Calculates win and loss percentage matrices for cards
    cards_win_percent = (Cards_Wins)/total
    cards_loss_percent = (Cards_Losses)/total

    # Create cards figures
    create_graphs(cards_win_percent, cards_loss_percent, total, 'Cards', hand_size)
    
    return None

def create_graphs(win:pd.DataFrame, loss:pd.DataFrame, total:int, name:str, hand_size:int = 3)->None:
    '''
    Function takes in Dataframes of Win Percentage and Loss Percentage.
    Creates and saves a figure with name.

    Returns: None
    '''

    # Masks diagonal
    mask = np.asarray(win==0)
    
    # Creates x and y axis labels
    color_labels = []
    # Creates hand size bit binary string for each number 0 - 2^hand size and replaces 0 with R and 1 with B
    for i in range(0, 2**hand_size):
        player = f"{i:0{hand_size}b}".replace('0', 'R').replace('1', 'B')
        color_labels.append(player)

    # Sets n = total and formats in scientific notation
    n = "{:.0e}".format(int(total))

    # Creates figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 12))

    # Sets title for entire figure
    fig.suptitle(f'Penneys Game - {name} \n(n={n})', fontsize=24)
    
    # Rotate y-axis ticks to be more legible
    plt.yticks(rotation=0)
    
    # Creates boolean true if hand size<=4, false otherwise. 
    # Do not want to display text if there are too many labels and boxes too small to fit
    display_text = (hand_size <= 4)
        
    # creates win heatmap
    ax1 = sns.heatmap(win, 
                        annot=display_text, 
                        mask = mask, 
                        cmap='Reds', 
                        fmt='.1%', 
                        linewidths=.5,
                        cbar = False, 
                        ax=ax1)
    
    # Set title and axis labels
    ax1.set_title('Win Percentage (for P1)', fontsize=20)
    ax1.set_xlabel('Player 2', fontsize=16)
    ax1.set_ylabel('Player 1', fontsize=16)

    # set x and y tick labels (only if hand_size <= 4)
    # If user really wants to figure out which hand plays which on larger figure instead of just observing pattern,
    # they can figure it out bc numbers are still listed, can be mentally converted to binary then to red and black
    if display_text:
        ax1.set_yticklabels(labels = color_labels, rotation=0, fontsize=14)
        ax1.set_xticklabels(labels = color_labels, rotation=0, fontsize=14)
    
    # Create loss heatmap
    ax2 = sns.heatmap(loss, 
                        annot=display_text, 
                        mask = mask, 
                        cmap='Blues', 
                        fmt='.1%', 
                        linewidths=.5, 
                        cbar = False, ax=ax2)
    
    # Set title and axis labels
    ax2.set_title('Loss Percentage (for P1)', fontsize=20)
    ax2.set_xlabel('Player 2', fontsize=16)
    ax2.set_ylabel('Player 1', fontsize=16)

    # set x and y tick labels (only if hand_size <= 4)
    if display_text:
        ax2.set_yticklabels(labels = color_labels, rotation=0, fontsize=14)
        ax2.set_xticklabels(labels = color_labels, rotation=0, fontsize=14)
    
    # Save figure with correct trick/card label and hand size
    plt.savefig(f'figures/{name}_hand_size_{hand_size}_heatmap.png')