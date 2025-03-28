from src.helpers import *
from src.Decks_Class import *
from src.processing import *

import matplotlib.pyplot as plt
import seaborn as sns

def gen_heatmap(hand_size:int = 3):
    Trick_Wins = np.load(SCORES_PATH + 'T_Wins_hand_size' + str(hand_size) + '.npy')
    Trick_Losses = np.load(SCORES_PATH + 'T_Losses_hand_size' + str(hand_size) + '.npy')
    Cards_Wins = np.load(SCORES_PATH + 'C_Wins_hand_size' + str(hand_size) + '.npy')
    Cards_Losses = np.load(SCORES_PATH + 'C_Losses_hand_size' + str(hand_size) + '.npy')

    total = np.load('src/Deck_Counts/Deck_Counts_hand_size' + str(hand_size) + '.npy')

    trick_win_percent = (Trick_Wins)/total
    trick_loss_percent = (Trick_Losses)/total
    create_graphs(trick_win_percent, trick_loss_percent, total, 'Tricks', hand_size)

    cards_win_percent = (Cards_Wins)/total
    cards_loss_percent = (Cards_Losses)/total
    create_graphs(cards_win_percent, cards_loss_percent, total, 'Cards', hand_size)

def create_graphs(win:pd.DataFrame, loss:pd.DataFrame, total:int, name:str, hand_size:int = 3):
    '''
    Function takes in Dataframes of Win Percentage and Loss Percentage.
    Creates and saves a figure with name.
    '''
    mask = np.asarray(win==0)
    
    color_labels = []
    for i in range(0, 2**hand_size):
        player = f"{i:0{hand_size}b}".replace('0', 'R').replace('1', 'B')
        color_labels.append(player)

    n = "{:.0e}".format(int(total))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 12))
    fig.suptitle(f'Penneys Game - {name} \n(n={n})', fontsize=24)
    
    plt.yticks(rotation=0)
    
    display_text = (hand_size <= 4)
        
    ax1 = sns.heatmap(win, 
                annot=display_text, mask = mask, cmap='Reds', fmt='.1%', linewidths=.5,cbar = False, ax=ax1)
    
    ax1.set_title('Win Percentage', fontsize=20)
    ax1.set_xlabel('Player 2', fontsize=16)
    ax1.set_ylabel('Player 1', fontsize=16)
    if display_text:
        ax1.set_yticklabels(labels = color_labels, rotation=0, fontsize=14)
        ax1.set_xticklabels(labels = color_labels, rotation=0, fontsize=14)
    ax1.figure.axes[-1].set_ylabel('Player 1 Win Percentage', size=16)
    
    
    ax2 = sns.heatmap(loss, 
                annot=display_text, mask = mask, cmap='Blues', fmt='.1%', linewidths=.5, cbar = False, ax=ax2)
    
    ax2.set_title('Loss Percentage', fontsize=20)
    ax2.set_xlabel('Player 2', fontsize=16)
    ax2.set_ylabel('Player 1', fontsize=16)
    if display_text:
        ax2.set_yticklabels(labels = color_labels, rotation=0, fontsize=14)
        ax2.set_xticklabels(labels = color_labels, rotation=0, fontsize=14)
    
    plt.savefig(f'figures/{name}_hand_size_{hand_size}_heatmap.png')