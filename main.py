from src.helpers import *
from src.Decks_Class import *
from src.processing import *
from src.visualization import *

def too_large(min: int, max: int, text:str) -> int:
    print(text)
    output = input()

    try: 
        output = int(output)
    except Exception as e:
        print('Please enter an integer')
        return too_large(min, max, text)
            
    if output <= min:
        print(f'Input too small (minimum: {min})')
        return too_large(min, max, text)

    elif output > max: 
         print(f'Input too large (maximum: {max})')
         return too_large(min, max, text)
    else:
        return output
    
if __name__ == '__main__':
    num_decks = too_large(0, 1_000_000, 'How many decks would you like to generate? (1 million maximum)')
    hand_size = too_large(0, 7, 'How many cards in the hand size? (7 maximum)')

    decks = Deck_Array(num_decks, hand_size)
    decks.run_decks_array()
    gen_heatmap(hand_size)
    print('End')