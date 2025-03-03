import numpy as np
HALF_DECK_SIZE = 26
def score_game(p1:list[int], 
               p2:list[int], 
               deck:np.array, 
               half_deck_size: int = HALF_DECK_SIZE
              )-> tuple[int, int, int, int]:
    '''
    Function to score game between two players. Outputs total tricks and cards for both players.
    '''
    
    end = 2 # index of most recent card
    p1_tricks = 0
    p2_tricks = 0
    p1_cards = 0
    p2_cards = 0
    last_trick_index = -1 #index of end previous trick # begins at -1 because deck is 0-51
    for end in range (2,2*HALF_DECK_SIZE):
        # Skips if last trick was taken in previous 2 cards
        if end < last_trick_index+3:
            continue
            
        # Checks if p1 takes the trick
        elif deck[end-2] == p1[0] and deck[end-1] == p1[1] and deck[end] == p1[2]:
            # print(f'p1 trick at {end}')
    
            #Update total tricks and cards
            p1_tricks+=1
            p1_cards = p1_cards + end - last_trick_index
            # print(p1_cards)
            # Update last_trick_index
            last_trick_index = end

        elif deck[end-2] == p2[0] and deck[end-1] == p2[1] and deck[end] == p2[2]:

            #Update total tricks and cards
            p2_tricks+=1
            p2_cards += end-last_trick_index
            # print(p2_cards)
            
            # Update last_trick_index
            last_trick_index = end
            
    return p1_tricks, p1_cards, p2_tricks, p2_cards