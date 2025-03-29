from src.Decks_Class import Deck_Array
from src.visualization import gen_heatmap
from src.helpers import clear_all

def too_large(min: int, max: int, text:str) -> int:
    '''
    Makes sure user input is valid. 
    Repeats question until valid input.
    '''

    # Ask for user input
    print(text)
    output = input()

    # Make sure input can be converted to integer
    try: 
        output = int(output)
    except Exception as e:
        # If not, ask again
        print('Please enter an integer')
        return too_large(min, max, text)

    #  Makes sure min<input<=max, otherwise ask again
    if output <= min:
        print(f'Input too small (minimum: {min})')
        return too_large(min, max, text)
    elif output > max: 
         print(f'Input too large (maximum: {max})')
         return too_large(min, max, text)
    else:
        return output
    

def run_program(num_decks:int, hand_size:int) -> None:
    # Create new decks_array
    decks = Deck_Array(num_decks, hand_size)
    # Score decks
    decks.run_decks_array()
    # Generate visualizations
    gen_heatmap(hand_size)
    return None

if __name__ == '__main__':

    options = too_large(0, 3, 'Input:\n 1: to run with defualt settings\n 2: to run with custom settings\n 3: to clear all contents')
    if options == 1:
        num_decks = 500_000
        hand_size = 3
        run_program(num_decks, hand_size)
    elif options == 2:

        # 1,000,000 decks is 15.6 MB, file size max for github is 50MB (or 100MB unclear to me)
        # Don't want to cut it close and 1,000,000 takes long enough / is enough decks already
        num_decks = too_large(0, 1_000_000, 'How many decks would you like to generate? (1 million maximum)')

        # Could theoretically go higher than 7, but it starts taking longer and longer to run. 
        # Don't want user to accidently start running code that takes much longer than they realize
        # Also do not really need variation that goes that high
        # Allow user to make hang_size 1 even though that is stupid
        hand_size = too_large(0, 7, 'How many cards in the hand size? (7 maximum)')

        run_program(num_decks, hand_size)

    elif options == 3:
        clear_all()

    else: print('Something went wrong')

    print('End')