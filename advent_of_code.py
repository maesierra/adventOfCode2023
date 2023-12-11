from abc import ABC, abstractmethod
import argparse
import os

class Solution(ABC):
    def __init__(self, day) -> None:
        super().__init__()
        self.day = day
        self.debug = False

    @abstractmethod
    def solve_part_1(self, input, args=[]): 
        pass

    @abstractmethod
    def solve_part_2(self, input, args=[]): 
        pass

    def input_to_lines(self, input): 
        with open(input, 'r') as file:
            lines = file.read().splitlines()
        return lines    
    
    def group_lines(self, lines: list, delimiter:str = "") -> list:
        res = []
        group = []
        for line in lines:
            if line == delimiter and group:
                res.append(group)
                group = []
            elif line != delimiter:
                group.append(line)
        if group:
            res.append(group)
        return res    


    def run(self, args=[]): 
        parser = argparse.ArgumentParser()
        parser.add_argument('part', nargs='?', default=1)
        parser.add_argument('input', nargs='?', default=f"input_{self.day}")
        args = parser.parse_args()
        input_file = os.path.join(os.path.dirname(__file__), args.input)

        print (f"Day {self.day} Part {args.part} Input {args.input}")
        if int(args.part) == 1: 
            solution = self.solve_part_1(input=input_file, args=args)
        else: 
            solution = self.solve_part_2(input=input_file, args=args)
        print(f"Solution: {solution}")        
        


    