import os
import re
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Reveal(): 
    def __init__(self, red:int, blue: int, green: int) -> None:
        self.red = red
        self.blue = blue
        self.green = green

    def is_valid(self, red:int, blue: int, green: int) -> bool:   
        return self.red <= red and self.blue <= blue and self.green <= green
    
    def add(self, colour: str, value: int):
        if "red" == colour:
            self.red += value
        elif "green" == colour:
            self.green += value
        elif "blue" == colour:
            self.blue += value

class Game(): 
    def __init__(self, id: int) -> None:
        self.id = id
        self.reveals = []
        pass        
    def is_valid(self, red:int, blue: int, green: int) -> bool:
        return len([r for r in self.reveals if not r.is_valid(red = red, blue = blue, green = green)]) == 0
    
    def power(self) -> int:
        max_red = max([r.red for r in self.reveals])
        max_green = max([r.green for r in self.reveals])
        max_blue = max([r.blue for r in self.reveals])
        power = max_red * max_green * max_blue
        return power

class Day2Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(2)

    def _parseGame(self, line: str) -> Game: 
        match = re.match(r"Game (\d+): (.+)$", line)
        game = Game(int(match.group(1)))
        for r in match.group(2).split(";"):
            reveal = Reveal(0, 0, 0)
            for part in r.split(","):
                m = re.match(r" ?(\d+) (blue|red|green)", part)    
                reveal.add(colour=m.group(2), value=int(m.group(1)))
            game.reveals.append(reveal)     
        return game       

    def _parse_games(self, input):
        return [self._parseGame(l) for l in self.input_to_lines(input)]

    def solve_part_1(self, input, args):
        games = self._parse_games(input)
        valid_games = [game.id for game in games if game.is_valid(red = 12, green = 13, blue = 14)]
        return sum(valid_games)
    
    def solve_part_2(self, input, args):
        games = self._parse_games(input)
        return sum([g.power() for g in games])

if __name__ == '__main__':    
    day2 = Day2Solution()
    day2.run()