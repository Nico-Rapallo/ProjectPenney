from src.helpers import *
from src.Decks_Class import *
from src.processing import *
from src.visualization import *

print('How many decks would you like to generate?')
num_decks = int(input())
if num_decks > 5_000_000:
    print('Number too large')
else:
    decks = Deck_Array(num_decks)
    decks.run_decks_array()
    gen_heatmap()
print('End')