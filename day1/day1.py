import os
import re
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Day1Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(1)

    def _extract_number(self, line): 
        r = re.findall(r"[0-9]", line)
        return int(r[0] + r[-1])
    
    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        numbers = [self._extract_number(l) for l in lines]
        return sum(numbers)
    
    def _extract_number_with_text_digits(self, line): 
        digits_map = {
            "one" : "1",
            "two" : "2",
            "three" : "3",
            "four" : "4",
            "five" : "5",
            "six" : "6",
            "seven" : "7",
            "eight" : "8",
            "nine" : "9",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "0": "0"
        }
        digits = []
        for pos in range(0, len(line)): 
            match = re.match(r"[0-9]|one|two|three|four|five|six|seven|eight|nine", line[pos:])
            if match: 
                digits.append(digits_map[match.group()])
        return int(digits[0]+ digits[-1])
    
    
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        numbers = [self._extract_number_with_text_digits(l) for l in lines]
        return sum(numbers)

if __name__ == '__main__':    
    day1 = Day1Solution()
    day1.run()