import os
import sys
from enum import Enum
from collections import Counter
from functools import cmp_to_key

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3 
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5 
    FOUR_OF_A_KIND = 6 
    FIVE_OF_A_KIND = 7
    
class Hand(): 
    def __init__(self, cards:str, jokers = False) -> None:
        card_values = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 0 if jokers else 11,
            "T": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2
        }
            
        self.cards = cards
        self.card_values = [card_values[c] for c in cards]
        self.counter = Counter(self.card_values)
        # Most common excluding jokers
        n_jokers = self.counter.get(0, 0)
        if n_jokers == 5: #Special case for all jokers
            most_common = 0            
        else: 
            most_common = [n for key, n in self.counter.most_common() if key != 0][0]

        n_distinct_cards = len(self.counter)
        if jokers and n_jokers > 0: 
            n_distinct_cards -= 1
        if most_common + n_jokers == 5:
            self.type = HandType.FIVE_OF_A_KIND
        elif most_common + n_jokers == 4:
            self.type = HandType.FOUR_OF_A_KIND
        elif most_common + n_jokers == 3:            
            self.type = HandType.FULL_HOUSE if n_distinct_cards == 2 else HandType.THREE_OF_A_KIND
        elif most_common + n_jokers == 2:
            self.type = HandType.TWO_PAIR if len(self.counter) == 3 else HandType.ONE_PAIR
        else:
            self.type = HandType.HIGH_CARD    
        print(f"{self.cards}:{self.type}")
            

    def compareTo(self, other: 'Hand') -> int:
        if self.type.value < other.type.value:
            return -1
        elif self.type.value > other.type.value:
            return 1
        else:
            for card, other_card in zip(self.card_values, other.card_values):
                if card < other_card:
                    return -1
                elif card > other_card:
                    return 1                
            return 0

class Day7Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(7)

    def _parse_hands(self, input, jokers = False)-> list: 
        lines = self.input_to_lines(input)
        return [(Hand(cards=cards, jokers=jokers), int(bid)) for cards, bid in [l.split(" ") for l in lines]]

    def _calculate_winnings(self, hands):
        hands = sorted(hands, key=cmp_to_key(lambda i1, i2: i1[0].compareTo(i2[0])))
        sorted_bids = [h[1] for h in hands]
        return sum([bid * (rank + 1) for rank,bid in enumerate(sorted_bids)])
    
    def solve_part_1(self, input, args):        
        hands = self._parse_hands(input=input, jokers=False)
        return self._calculate_winnings(hands)

    
    def solve_part_2(self, input, args):
        hands = self._parse_hands(input=input, jokers=True)        
        return self._calculate_winnings(hands)

if __name__ == '__main__':    
    day7 = Day7Solution()
    day7.run()