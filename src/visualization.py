from src.helpers import *
from src.Decks_Class import *
from src.processing import *

import matplotlib.pyplot as plt
import seaborn as sns



def gen_heatmap():
    Trick_Wins, Trick_Losses, Cards_Wins, Cards_Losses = get_complete_tables()

    total = np.sum(np.load('src/Decks/deck_lengths.npy'))

    trick_win_percent = (Trick_Wins)/total
    trick_loss_percent = (Trick_Losses)/total
    create_graphs(trick_win_percent, trick_loss_percent, total, 'Tricks')

    cards_win_percent = (Cards_Wins)/total
    cards_loss_percent = (Cards_Losses)/total
    create_graphs(cards_win_percent, cards_loss_percent, total, 'Cards')

def create_graphs(win:pd.DataFrame, loss:pd.DataFrame, total:int, name:str):
    '''
    Function takes in Dataframes of Win Percentage and Loss Percentage.
    Creates and saves a figure with name.
    '''
    mask = np.asarray(win==0)
    color_labels = ['RRR', 'RRB', 'RBR', 'RBB', 'BRR', 'BRB', 'BBR', 'BBB']
    n = "{:.0e}".format(int(total))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 12))
    fig.suptitle(f'Penneys Game - {name} \n(n={n})', fontsize=24)
    
    plt.yticks(rotation=0)
    ax1 = sns.heatmap(win, 
                annot=True, mask = mask, cmap='Reds', fmt='.2%', linewidths=.5, ax=ax1)
    
    ax1.set_title('Win Percentage', fontsize=20)
    ax1.set_xlabel('Player 2', fontsize=16)
    ax1.set_ylabel('Player 1', fontsize=16)
    ax1.set_yticklabels(labels = color_labels, rotation=0, fontsize=14)
    ax1.set_xticklabels(labels = color_labels, rotation=0, fontsize=14)
    ax1.figure.axes[-1].set_ylabel('Player 1 Win Percentage', size=16)
    
    
    ax2 = sns.heatmap(loss, 
                annot=True, mask = mask, cmap='Blues', fmt='.2%', linewidths=.5, ax=ax2)
    
    ax2.set_title('Loss Percentage', fontsize=20)
    ax2.set_xlabel('Player 2', fontsize=16)
    ax2.set_ylabel('Player 1', fontsize=16)
    ax2.set_yticklabels(labels = color_labels, rotation=0, fontsize=14)
    ax2.set_xticklabels(labels = color_labels, rotation=0, fontsize=14)
    ax1.figure.axes[-1].set_ylabel('Player 1 Loss Percentage', size=16)
    
    plt.savefig(f'figures/{name}_heatmap.png')