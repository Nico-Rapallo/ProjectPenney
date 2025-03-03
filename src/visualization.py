from src.helpers import *
from src.Decks_Class import *
from src.processing import *

import matplotlib.pyplot as plt
import seaborn as sns



def gen_heatmap():
    TRICK_WINS, TRICK_LOSSES, TRICK_TIES, CARDS_WINS, CARDS_LOSSES, CARDS_TIES = get_complete_tables()
    total = TRICK_WINS + TRICK_LOSSES + TRICK_TIES
    total = total+total.T
    trick_win_percent = (TRICK_WINS + TRICK_LOSSES.T)/total
    trick_loss_percent = (TRICK_LOSSES + TRICK_WINS.T)/total
    cards_win_percent = (CARDS_WINS + CARDS_LOSSES.T)/total
    cards_loss_percent = (CARDS_LOSSES + CARDS_WINS.T)/total

    n = "{:.0e}".format(int(total.iloc[1, 0]))
    plt.figure(figsize=(10, 9))
    mask = trick_win_percent.isnull()
    sns.heatmap(trick_win_percent, annot=True, mask = mask, cmap='Reds', fmt='.2%', cbar_kws={'label': 'PLayer 1 Win Percentage'})
    plt.title(f'Penneys Game Win Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('figures/tricks_win_heatmap.png')
    
    plt.figure(figsize=(10, 9))
    sns.heatmap(trick_loss_percent, annot=True, mask = mask, cmap='Blues', fmt='.2%',cbar_kws={'label': 'PLayer 1 Loss Percentage'})
    plt.title(f'Penneys Game Loss Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('figures/tricks_loss_heatmap.png')

    plt.figure(figsize=(10, 9))
    sns.heatmap(cards_win_percent, annot=True, mask = mask, cmap='Reds', fmt='.2%', cbar_kws={'label': 'PLayer 1 Win Percentage'})
    plt.title(f'Penneys Game Win Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('figures/cards_win_heatmap.png')

    plt.figure(figsize=(10, 9))
    sns.heatmap(cards_loss_percent, annot=True, mask = mask, cmap='Blues', fmt='.2%',cbar_kws={'label': 'PLayer 1 Loss Percentage'})
    plt.title(f'Penneys Game Loss Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('figures/cards_loss_heatmap.png')

    plt.figure(figsize=(10, 9))
    sns.heatmap(trick_win_percent-cards_win_percent, annot=True, mask = mask, cmap='vlag', fmt='.2%',cbar_kws={'label': 'PLayer 1 Win Percentage Difference'})
    plt.title(f'Penneys Game Cards vs Tricks Win Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('figures/win_difference_heatmap.png')

    plt.figure(figsize=(10, 9))
    sns.heatmap(trick_loss_percent-cards_loss_percent, annot=True, mask = mask, cmap='vlag', fmt='.2%',cbar_kws={'label': 'PLayer 1 Loss Percentage Difference'})
    plt.title(f'Penneys Game Cards vs Tricks Loss Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('figures/los_difference_heatmap.png')