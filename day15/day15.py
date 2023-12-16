import os
import re
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Lens():
    def __init__(self, label:str, focal_length:int) -> None:
        self.label = label
        self.focal_length = focal_length

class Box():
    def __init__(self, n) -> None:
        self.n = n
        self.lenses = []
        self.lenses_map = {}

    def remove(self, label:str):
        index = self.lenses_map.pop(label, None)
        if index is None:
            return
        for l in self.lenses[index + 1:]:
            self.lenses_map[l.label] -= 1 
        self.lenses = self.lenses[:index] + self.lenses[index + 1:]
    
    def replace(self, lens:Lens):
        index = self.lenses_map.get(lens.label, None)
        if index is not None:
            self.lenses[index] = lens
            return
        self.lenses.append(lens)
        self.lenses_map[lens.label] = len(self.lenses) - 1

    def focusing_power(self):
        return sum([(self.n + 1) * (i + 1) * lens.focal_length for i, lens in enumerate(self.lenses)])

class Day15Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(15)

    def hash(self, string:str) -> int :
        hash = 0
        for c in string:
            hash += ord(c)
            hash *= 17
            hash = hash % 256
        return hash

    def _parse_instructions(self, input) ->list :
        lines = self.input_to_lines(input)
        return "".join(lines).split(",")

    def solve_part_1(self, input, args):
        instructions = self._parse_instructions(input)
        return sum([self.hash(p) for p in instructions])
    
    def solve_part_2(self, input, args):
        boxes = [Box(n) for n in range(0, 256)]
        for instruction in self._parse_instructions(input):
            m = re.search(f"([a-z]+)([-=])(\d*)", instruction)
            op = m.group(2)
            label = m.group(1)
            box = boxes[self.hash(label)]
            if op == "-":
                box.remove(label)
            else:
                lens = Lens(label=label, focal_length=int(m.group(3)))
                box.replace(lens)
        return sum([b.focusing_power() for b in boxes if len(b.lenses) > 0])

if __name__ == '__main__':    
    day15 = Day15Solution()
    day15.run()