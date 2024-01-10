from collections import deque
import os
from re import sub
import sys
from tkinter import N
from typing import Deque, Dict, List

from numpy import half



root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from matrix import Position, in_grid, dimensions


from advent_of_code import Solution

class Node():
    def __init__(self, position: Position, connections:List["Node"] = []) -> None:
        self.position = position
        self.connections = connections

    def key(self) -> str:
        return str(self.position)
        
class Day21Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(21)

    def explore(self, n_steps:int, parity: int, start:Position, map:List[str]) -> Dict[str, int]:
        visited: Dict[str, int] = {}
        queue : Deque[tuple(Position, int)] = deque()
        queue.append((start, 0))
        while queue:
            pos, steps = queue.popleft()
            steps += 1
            if steps > n_steps:
                continue
            for p in [pos.clone(y=pos.y - 1), pos.clone(x=pos.x + 1), pos.clone(y=pos.y + 1), pos.clone(x=pos.x - 1)]:
                if in_grid(map, p) and map[p.y][p.x] != '#' and not str(p) in visited:
                    visited[str(p)] = steps
                    queue.append((p, steps))
        
        return {k:v for k,v in visited.items() if v % 2 == parity}

    def start_point(self, map) -> Position:
        # Locate start point
        for i, row in enumerate(map):
            for j, c in enumerate(row):
                if c == 'S':
                    return Position(y=i, x=j)

    def solve_part_1(self, input, args):
        n_steps = args[0] if len(args) >= 1 else 64
        map = self.input_to_lines(input)
        start = self.start_point(map)
        return len(self.explore(n_steps=n_steps, start=start, map=map, parity=n_steps % 2))
            
    def solve_part_2(self, input, args):
        n_steps = args[0] if len(args) >= 1 else 26501365
        map = self.input_to_lines(input)
        start = self.start_point(map)
        n_rows, n_cols = dimensions(map)
        if n_rows != n_cols:
            raise Exception("Input must be square")
        size = n_rows
        center = int(size / 2)
        n = int(n_steps / size)
        print (f"n: {n} size: {size} center: {center}")
        if center != n_steps % size:
            raise Exception("Number of steps should end in a border")
        # we need to explore for odd grids (parity = 1) and even (parity = 0)
        odd = self.explore(n_steps=n_steps, start=start, map=map, parity=1)
        even = self.explore(n_steps=n_steps, start=start, map=map, parity=0)
        # those are the fully contained instances. With a max reach of n_maps + half we need to 
        # take out or include corners outside the rhombus (with steps greater than half)
        odd_corners = len({k:v for k,v in odd.items() if v > center})
        even_corners = len({k:v for k,v in even.items() if v > center})
        # And the quadratic formula
        # (n + 1)^2 * n_odd + n^2 * full - (n+1) * n_corner_odd + n * n_corner_even
        even_factor = n * n
        odd_factor = (n + 1) * (n + 1)
        return odd_factor * len(odd) + even_factor * len(even) - ((n + 1) * odd_corners) + (n * even_corners);

if __name__ == '__main__':    
    day21 = Day21Solution()
    day21.run()