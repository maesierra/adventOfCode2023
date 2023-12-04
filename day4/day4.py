import os
import re
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Scratchcard():
    def __init__(self, id: int, winning_numbers:list, numbers:list) -> None:
        self.winning_numbers = winning_numbers
        self.numbers = numbers  
        self.id = id      
        self.processed = False

    def points(self) -> int:
        n_matched = self.n_matched()
        if n_matched == 0:
            return 0
        points = 2 ** (n_matched - 1)
        return int(points)

    def n_matched(self) -> int: 
        return len([value for value in self.numbers if value in self.winning_numbers])
    
    def get_rewads(self, scratchcards:list) -> list:
        n_matched = self.n_matched()
        return [Scratchcard(s.id, s.winning_numbers, s.numbers) for s in scratchcards[self.id :min(len(scratchcards), self.id + n_matched)]]

class Day4Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(4)

    def _parse_scratchcards(self, input) -> list:
        scratchcards = []
        for line in self.input_to_lines(input):
            match = re.match(r"^Card +(\d+): (.*) \| (.*)$", line)            
            if not match:
                raise Exception(f"{line} not matched.")
            winning_numbers = [int(d) for d in match.group(2).split(" ") if d != ""]
            numbers = [int(d) for d in match.group(3).split(" ") if d != ""]
            scratchcards.append(Scratchcard(id = int(match.group(1)), winning_numbers=winning_numbers, numbers=numbers))
        return scratchcards

    def solve_part_1(self, input, args):
        scratchcards = self._parse_scratchcards(input)        
        return sum([c.points() for c in scratchcards])
    
    def solve_part_2(self, input, args):
        scratchcards = self._parse_scratchcards(input)    
        unprocessed = [s for s in scratchcards if not s.processed]
        while unprocessed:
            for card in unprocessed:
                rewards = card.get_rewads(scratchcards)
                scratchcards.extend(rewards)    
                card.processed = True
            unprocessed = [s for s in scratchcards if not s.processed]            
            print(f"Unprocessed: {len(unprocessed)}")
        return len(scratchcards)

if __name__ == '__main__':    
    day4 = Day4Solution()
    day4.run()