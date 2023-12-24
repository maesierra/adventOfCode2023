import os
import sys

import numpy as np


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution
import matrix

class PartNumber():
    def __init__(self, number:str, x: int, y: int) -> None:
        self.number = number
        self.x = x
        self.y = y

    def contains(self, x: int, y: int):
        return self.y == y and x >= self.x and x < self.x + len(self.number)

    def __str__(self) -> str:
         return self.number   

class Gear: 
    def __init__(self, part_1:PartNumber, part_2: PartNumber, x: int, y: int) -> None:
        self.part_1 = part_1
        self.part_2 = part_2
        self.x = x
        self.y = y

    def ratio(self):
        return int(self.part_1.number) * int(self.part_2.number)
    
class Day3Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(3)

    def _parse_part_numbers(self, m:np.ndarray) -> list[PartNumber]:        
        n_rows, n_cols = m.shape
        part_numbers = []
        for y in range(n_rows):
            part_number = None
            for x in range(n_cols):
                item = m.item((y, x))                
                if item.isnumeric(): 
                    if part_number: 
                        part_number.number += item
                    else: 
                        part_number = PartNumber(number=item, x=x, y=y)                            
                elif part_number:
                    if self._is_valid_part_number(m=m, part_number=part_number):
                        part_numbers.append(part_number)
                    part_number = None
                x += 1
            if part_number:
                if self._is_valid_part_number(m=m, part_number=part_number):
                    part_numbers.append(part_number)
        return part_numbers    

    def _is_valid_part_number(self, m: np.ndarray, part_number: PartNumber) -> bool:
        for x in range(part_number.x, part_number.x + len(part_number.number)): 
            neighbours = matrix.neighbours(matrix=m, x=x, y=part_number.y)
            if len([n for n in neighbours if not n.isnumeric() and n != "."])  > 0:
                return True
        return False    


    def solve_part_1(self, input, args):
        m = matrix.string_matrix_from_lines(self.input_to_lines(input))  
        part_numbers = self._parse_part_numbers(m)
        return sum([int(p.number) for p in part_numbers])
    
    def _parse_gears(self, m:np.ndarray) -> list[Gear]:        
        part_numbers = self._parse_part_numbers(m)
        n_rows, n_cols = m.shape
        gears = []
        for y in range(n_rows):
            for x in range(n_cols):
                item = m.item((y, x))                
                if item == "*":
                    found = set()
                    for pos in matrix.neighbours_positions(m, x=x, y=y):
                        for part_number in [p for p in part_numbers if p.contains(x=pos.x, y=pos.y)]:
                            found.add(part_number)
                    if len(found) == 2: 
                        found = list(found)
                        gears.append(Gear(part_1=found[0], part_2=found[1], x=x, y=y))
                x += 1
        return gears    

    def solve_part_2(self, input, args):
        m = matrix.string_matrix_from_lines(self.input_to_lines(input))  
        gears = self._parse_gears(m)        
        return sum([g.ratio() for g in gears])

if __name__ == '__main__':    
    day3 = Day3Solution()
    day3.run()