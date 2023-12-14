import os
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

def is_power_of_two(n):
    return (n & (n-1) == 0) and n != 0

def is_smudge(line1, line2):
    return is_power_of_two(line1 ^ line2)

def is_equal_or_smudge(line1, line2):
    return (line1 == line2, is_power_of_two(line1 ^ line2))

class Pattern():
    def __init__(self, rows) -> None:
        self.rows = [int(b.replace("#", "1").replace(".", "0"), 2) for b in rows]
        n_columns = len(rows[0])
        self.columns = [int("".join(["1" if r[i] == "#" else "0" for r in rows]), 2) for i in range(0, n_columns)]

    def _find_reflection(self, lines):
        n_lines = len(lines)
        for i in range(0, n_lines - 1):
            if lines[i] == lines[i + 1]:
                i1 = i - 1
                i2 = i + 2
                matching = True
                while i1 >= 0 and i2 < n_lines and matching:
                    matching = lines[i1] == lines[i2]
                    i1 = i1 - 1
                    i2 = i2 + 1
                if matching:
                    return i + 1
        return None
    
    def _find_reflection(self, lines):
        n_lines = len(lines)
        for i in range(0, n_lines - 1):
            if lines[i] == lines[i + 1]:
                i1 = i - 1
                i2 = i + 2
                matching = True
                while i1 >= 0 and i2 < n_lines and matching:
                    matching = lines[i1] == lines[i2]
                    i1 = i1 - 1
                    i2 = i2 + 1
                if matching:
                    return i + 1
        return None
    
    
    def find_reflection_with_smudge(self, lines):
        n_lines = len(lines)
        for i in range(0, n_lines - 1):
            is_equal,is_smudge = is_equal_or_smudge(lines[i], lines[i + 1])
            n_smudges = 1 if is_smudge else 0
            if is_equal or is_smudge:
                i1 = i - 1
                i2 = i + 2
                matching = True
                while i1 >= 0 and i2 < n_lines and matching:
                    is_equal,is_smudge = is_equal_or_smudge(lines[i1], lines[i2])
                    n_smudges += 1 if is_smudge else 0
                    matching = (is_equal or is_smudge) and n_smudges <= 1
                    i1 = i1 - 1
                    i2 = i2 + 1
                if matching and n_smudges == 1:
                    return i + 1
        
    
    def horizontal_reflection(self):         
        return self._find_reflection(self.rows)

    def vertical_reflection(self):         
        return self._find_reflection(self.columns)


class Day13Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(13)

    def _parse_patterns(self, input):
        lines = self.input_to_lines(input)
        return [Pattern(g) for g in self.group_lines(lines)]

    def solve_part_1(self, input, args):
        patterns = self._parse_patterns(input)
        res = 0
        for pattern in patterns:
            horizontal_reflection = pattern.horizontal_reflection()
            if horizontal_reflection: 
                res += horizontal_reflection * 100
            else: 
                vertical_reflection = pattern.vertical_reflection()
                if vertical_reflection: 
                    res += vertical_reflection
        return res    
    
    def solve_part_2(self, input, args):
        patterns = self._parse_patterns(input)
        res = 0
        for pattern in patterns:
            horizontal_reflection = pattern.find_reflection_with_smudge(pattern.rows)
            if horizontal_reflection: 
                res += horizontal_reflection * 100
            else: 
                vertical_reflection = pattern.find_reflection_with_smudge(pattern.columns)
                if vertical_reflection: 
                    res += vertical_reflection
        return res    

if __name__ == '__main__':    
    day13 = Day13Solution()
    day13.run()