import os
import re
import sys
import numpy as np
import math


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution
class RaceRecord():
    def __init__(self, time:int, record:int = 0) -> None:
        self.time = time
        self.record = record

    def distance(self, hold_time:int) -> int: 
        return hold_time * (self.time - hold_time)
    # Returns the number of different times 
    def ways_to_beat_v1(self) -> int:
        res = 0
        # Do not bother with either 0 or full hold_time
        for hold_time in range(1, self.time):
            distance = self.distance(hold_time)
            if distance > self.record:
                print (f"Hold: {hold_time} Run: {(self.time - hold_time)} -> {distance} beats {self.record}")
                res += 1
            else: 
                print (f"Hold: {hold_time} Run: {(self.time - hold_time)} -> {distance}")    
        return res

    # Returns the number of different times 
    def ways_to_beat(self) -> int:
        # distance = hold_time * (time - hold_time) => hold_time*hold_time - time*hold_time + distance = 0 => quadratic equation
        max_hold_time, min_hold_time = [int(d) for d in np.roots([1, -self.time, self.record])]
        diff = max_hold_time - min_hold_time        
        # Edge case when the roots are producing the record
        if self.distance(min_hold_time) == self.record or self.distance(max_hold_time) < self.record:
            diff -= 1        
        print (f"Roots {min_hold_time, max_hold_time} for {self.time} trying to beat {self.record} [diff: {diff}]")
        return diff

    

class Day6Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(6)

    def _parse_records(self, lines):
        times = [int(d) for d in lines[0].split(":")[1].split(" ") if d]
        distances = [int(d) for d in lines[1].split(":")[1].split(" ") if d]
        records = [RaceRecord(time=times[pos], record=distances[pos]) for pos in range(0, len(times))]
        return records

    def _solve(self, records):
        res = 1
        for r in records:            
            n = r.ways_to_beat()            
            print(f"Checking {r.time} duration to beat {r.record} => {n}")
            if n > 0:
                res *= n        
            # old_value = r.ways_to_beat_v1()
            # if n != old_value:
            #    print(f"!!!!!!! {n} is differnt from {old_value}")         
        return res


    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        records = self._parse_records(lines)        
        return self._solve(records)
    
    def solve_part_2(self, input, args):
        lines = [l.replace(" ", "") for l in self.input_to_lines(input)]
        records = self._parse_records(lines)        
        return self._solve(records)

if __name__ == '__main__':    
    day6 = Day6Solution()
    day6.run()