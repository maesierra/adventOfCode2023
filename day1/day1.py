import os
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Day1Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(1)

    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        print("Hello")
        print(lines)
        return 0
    
    def solve_part_2(self, input, args):
        print(input)
        return 2

if __name__ == '__main__':    
    day1 = Day1Solution()
    day1.run()