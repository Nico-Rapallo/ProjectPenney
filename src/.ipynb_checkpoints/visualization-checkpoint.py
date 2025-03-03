from helpers import *
from datagen import *
from processing import *
from Testing import *

import matplotlib.pyplot as plt
import seaborn as sns

SCORES_PATH = 'SCORES/'
TABLES_PATHS = ['T_WINS/', 'T_LOSSES/', 'T_TIES/', 'C_WINS/', 'C_LOSSES/', 'C_TIES/']


def gen_heatmap():
    TRICK_WINS, TRICK_LOSSES, TRICK_TIES, CARDS_WINS, CARDS_LOSSES, CARDS_TIES = get_complete_tables()
    total = TRICK_WINS + TRICK_LOSSES + TRICK_TIES
    trick_win_percent = (TRICK_WINS + TRICK_LOSSES.T)/(total+total.T)
    trick_loss_percent = (TRICK_LOSSES + TRICK_WINS.T)/(total+total.T)
    n = int(total.iloc[1, 0])
    plt.figure(figsize=(10, 9))
    mask = trick_win_percent.isnull()
    sns.heatmap(trick_win_percent, annot=True, mask = mask, cmap='Reds', fmt='.2%', cbar_kws={'label': 'PLayer 1 Win Percentage'})
    plt.title(f'Penneys Game Win Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('win_heatmap.png')
    
    plt.figure(figsize=(10, 9))
    sns.heatmap(trick_loss_percent, annot=True, mask = mask, cmap='Blues', fmt='.2%',cbar_kws={'label': 'PLayer 1 Loss Percentage'})
    plt.title(f'Penneys Game Loss Percentage Heatmap\n(n={n})')
    plt.yticks(rotation=0)
    plt.xlabel('Player 2')
    plt.ylabel('Player 1')
    plt.savefig('loss_heatmap.png')