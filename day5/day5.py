import os
import sys
import re
import time
import more_itertools as mit


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
    
    def to_dest(self, value:int) -> int:
        return (value - self.src_start) + self.dest_start
    
    def contained_in_dest(self, value:int) -> int:
        return value >= self.dest_start and value < self.dest_start + self.len
    
    def from_dest(self, value:int) -> int:
        return (value - self.dest_start) + self.src_start

class SeedMap():
    def __init__(self, src:str, dest:str) -> None:
        self.src = src
        self.dest = dest
        self.ranges = []
        self.min = None
        self.max = None
        

    def add_range(self, src_start, dest_start, len):
        self.ranges.append(Range(src_start=src_start, dest_start=dest_start, len=len))
        self.ranges = sorted(self.ranges, key=lambda r: r.src_start)
        self.min = self.ranges[0].src_start
        self.max = self.ranges[-1].src_start + len

    def to_dest(self, value:int) -> int:
        if value < self.min or value > self.max:
            return value
        for r in self.ranges:
            if r.contains(value):
                return r.to_dest(value)
        return value    
    
    def from_dest(self, value:int) -> int:
        if len([r for r in self.ranges if r.contained_in_dest(value)]) > 1:
            raise Exception(f"{value} Found in multiple ranges in {self.src}")
        for r in self.ranges:
            if r.contained_in_dest(value):
                return r.from_dest(value)
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
    
    def _translate_to_dest(self, value:int, src:str, dest:str, maps:dict) -> int: 
        current_map = src
        current_value = value
        while current_map != dest:
            map = maps[current_map]
            new_value = map.to_dest(current_value)
            # print(f"Translated from {current_map} {current_value} to {map.dest} {new_value}")
            current_value = new_value
            current_map = map.dest
        return current_value
    
    def _translate_from_dest(self, value:int, src:str, dest:str, maps:dict) -> int: 
        map = mit.nth([m for m in maps.values() if m.dest == dest], 0)
        current_value = value
        while map:
            new_value = map.from_dest(current_value)
            current_value = new_value
            map = mit.nth([m for m in maps.values() if m.dest == map.src], 0)
        return current_value

    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        seeds = [int(s) for s in re.split(r"[ :]", lines[0]) if s.isnumeric()]
        maps = self._parse_maps(lines=lines)
        locations = [self._translate_to_dest(value=s, src="seed", dest="location", maps=maps) for s in seeds]
        return min(locations)
    
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        seed_ranges = sorted([range(start, start + len) for start, len in list(mit.chunked([int(s) for s in re.split(r"[ :]", lines[0]) if s.isnumeric()], 2))], key=lambda r: r.start)
        maps = self._parse_maps(lines=lines)        
        # return self.brute_force_direct(maps, seed_ranges)
        return self.brute_force_inverse(maps, seed_ranges)

    def brute_force_inverse(self, maps, seed_ranges):
        value  = 0
        start = time.process_time()
        while True:                        
            seed = self._translate_from_dest(value=value, src="seed", dest="location", maps=maps)            
            if value and value % 10000 == 0:                     
                    print(f"Checking location {value} <= seed {seed}. Elapsed {time.process_time() - start}")                    
                    start = time.process_time()
            # translated = self._translate_to_dest(value=seed, src="seed", dest="location", maps=maps)
            # if translated != value:
            #     raise Exception(f"From {value} to {seed} does not match {seed} to {translated}")
            # print(f"Checking seed: {seed}/{self._translate_to_dest(value=seed, src="seed", dest="location", maps=maps)} => location:{value}")
            for r in seed_ranges:
                if seed in r:
                    return value                            
            value += 1
    def brute_force_direct(self, maps, seed_ranges):
        n_ranges = len(seed_ranges)
        total = sum([r.stop - r.start for r in seed_ranges])       
        skip = 0 
        min = 0
        current = 0
        start = time.process_time()                    
        for current_range, r in enumerate(seed_ranges):      
            if current < skip and r.stop < skip:
                current += r.stop - r.start
                continue                  
            for seed in r:                 
                if current < skip:
                    current += 1
                    continue                               
                if current and current % 1000000 == 0:                     
                    print(f"Checking {current}/{total} [range {current_range}/{n_ranges}]. Elapsed {time.process_time() - start} Min: {min}")                    
                    start = time.process_time()
                location = self._translate_to_dest(value=seed, src="seed", dest="location", maps=maps)
                if not min or location < min:
                    min = location
                current += 1
        return min

if __name__ == '__main__':    
    day5 = Day5Solution()
    day5.run()