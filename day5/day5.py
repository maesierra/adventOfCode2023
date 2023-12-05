import os
import sys
import re
import numpy as np


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Range():
    def __init__(self, src_start:int, dest_start:int, len:int) -> None:
        self.src_start = src_start
        self.dest_start = dest_start
        self.len = len

    def contains(self, value:int) -> int:
        return value >= self.src_start and value < self.src_start + self.len
    
    def translate(self, value:int) -> int:
        return (value - self.src_start) + self.dest_start

class SeedMap():
    def __init__(self, src:str, dest:str) -> None:
        self.src = src
        self.dest = dest
        self.ranges = []
        

    def add_range(self, src_start, dest_start, len):
        self.ranges.append(Range(src_start=src_start, dest_start=dest_start, len=len))

    def translate(self, value:int) -> int:
        for r in self.ranges:
            if r.contains(value):
                return r.translate(value)
        return value    
        
class Day5Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(5)

    def _parse_maps(self, lines:list) -> list:
        maps = {}
        for group in self.group_lines(lines[2:]):
            match = re.match(r"(.*)-to-(.*) map:", group[0])
            map = SeedMap(src=match.group(1), dest=match.group(2))
            for line in group[1:]:
                dest_start, src_start, len = [int(n) for n in line.split(" ") if n]
                map.add_range(src_start=src_start, dest_start=dest_start, len=len)
            maps[map.src] = map
        return maps
    
    def _translate(self, value:int, src:str, dest:str, maps:dict) -> int: 
        current_map = src
        current_value = value
        while current_map != dest:
            map = maps[current_map]
            new_value = map.translate(current_value)
            print(f"Translated from {current_map} {current_value} to {map.dest} {new_value}")
            current_value = new_value
            current_map = map.dest
        return current_value

    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        seeds = [int(s) for s in re.split(r"[ :]", lines[0]) if s.isnumeric()]
        maps = self._parse_maps(lines=lines)
        locations = [self._translate(value=s, src="seed", dest="location", maps=maps) for s in seeds]
        return min(locations)
    
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        seed_ranges = np.array_split([int(s) for s in re.split(r"[ :]", lines[0]) if s.isnumeric()], 2)
        maps = self._parse_maps(lines=lines)
        return 2

if __name__ == '__main__':    
    day5 = Day5Solution()
    day5.run()