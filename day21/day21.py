from collections import deque
import os
from re import sub
import sys
from typing import Deque, List


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from matrix import Position, in_grid


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

    def solve_part_1(self, input, args):
        n_steps = args[0] if len(args) >= 1 else 64
        map = self.input_to_lines(input)
        visited = {}
        start = None
        # Locate start point
        for i, row in enumerate(map):
            for j, c in enumerate(row):
                if c == 'S':
                    start = Position(y=i, x=j)
                    break
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
        
        return len([k for k,v in visited.items() if v % 2 == n_steps % 2])

            
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        print(lines)
        return 2

if __name__ == '__main__':    
    day21 = Day21Solution()
    day21.run([64])