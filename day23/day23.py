from collections import deque
from doctest import debug
import os
import sys
from typing import Any, Deque, Dict, List, Set, Tuple



root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from dijkstar import Graph, find_path

from advent_of_code import Solution
from matrix import Position, dimensions, in_grid, neighbours


def cost(u, v, edge, prev_edge):
    return -edge

class Node():
    def __init__(self, position:Position) -> None:
        self.position = position
        self.connections:List["Node"] = []

class Day23Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(23)
        self.nodes:Dict["Position", "Node"] = {}

    def _node(self, position:Position):
        if not position in self.nodes:
            self.nodes[position] = Node(position)
        return self.nodes[position]

    def _get_path_in_direction(self, grid:list, pos: Position, x_delta:int, y_delta:int) -> List["Position"]:
        x = pos.x + x_delta
        y = pos.y + y_delta
        n_cols, n_rows = dimensions(grid)
        res = []
        while x >= 0 and x < n_cols and y >= 0 and y < n_rows and grid[y][x] != '#':
            res.append(Position(y=y, x=x))
            x += x_delta
            y += y_delta
        return res
    def _get_vertical_neighbours(self, grid:list, pos:Position): 
        return [p for p in [Position(x=pos.x, y=pos.y + 1), Position(x=pos.x, y=pos.y - 1)] if in_grid(grid, p)]
    def _get_horizontal_neighbours(self, grid:list, pos:Position): 
        return [p for p in [Position(x=pos.x + 1, y=pos.y), Position(x=pos.x - 1, y=pos.y)] if in_grid(grid, p)]

    def _n_steps(self, p1:Position, p2:Position):
        if p1.x == p2.x:
            return abs(p1.y - p2.y)
        else: 
            return abs(p1.x - p2.x)
        
    def _process_path_in_direction(self, pos:Position, horizontal:bool, forward: bool, grid:list, visited:set, use_slopes = True) -> Node:
        x_delta = 0
        y_delta = 0        
        if horizontal:
            x_delta = 1 if forward else -1
            forward_slope = '>' if forward else '<'
        else: 
            y_delta = 1 if forward else -1
            forward_slope = 'v' if forward else '^'
        if not use_slopes:
            # To ignore the slopes we put the forward_slop character as anything
            forward_slope = '@'

        path = self._get_path_in_direction(grid=grid, pos=pos, x_delta=x_delta, y_delta=y_delta)
        if path:
            end = -1
            for i, p in enumerate(path[0:-1]):
                char = grid[p.y][p.x]
                neighbours = self._get_horizontal_neighbours(grid=grid, pos=p) if not horizontal else self._get_vertical_neighbours(grid=grid, pos=p)
                if char != forward_slope and [1 for n in neighbours if grid[n.y][n.x] != '#']:
                    end = i
                    break
                if char not in ['.', forward_slope]:
                    end = i
                    break
                visited.add(f"{p}")
            return self._node(path[end])
        return None
            
                

    def _build_nodes(self, input, use_slopes = True) -> Tuple[Position, Position]:
        lines = self.input_to_lines(input)
        n_rows, n_cols = dimensions(lines)
        for x, c in enumerate(lines[0]):
            if c == '.':
                start = Position(x=x, y=0)
                break
        for x, c in enumerate(lines[-1]):
            if c == '.':
                end = Position(x=x, y=len(lines) - 1)
                break
        
        visited = set()
        for y in range(0, n_rows):
            for x in range(0, n_cols):
                char = lines[y][x]
                if char == '#':
                    continue
                pos = Position(x=x, y=y)
                if f"{pos}" in visited:
                    continue
                node = self._node(pos)
                connections = [
                    self._process_path_in_direction(pos=pos, horizontal=True,  forward=True,  grid=lines, visited=visited, use_slopes=use_slopes),
                    self._process_path_in_direction(pos=pos, horizontal=True,  forward=False, grid=lines, visited=visited, use_slopes=use_slopes),
                    self._process_path_in_direction(pos=pos, horizontal=False, forward=True,  grid=lines, visited=visited, use_slopes=use_slopes),
                    self._process_path_in_direction(pos=pos, horizontal=False, forward=False, grid=lines, visited=visited, use_slopes=use_slopes),
                ]
                for c in connections:
                    if c:
                        node.connections.append(c)
                visited.add(f"{pos}")
        return (start, end)


    
    def _calculate_longest_path(self, start:Position, end:Position) -> int:
        paths:Deque[Tuple(Position, Set[Position], int)] = deque([(n.position, {start, n.position}, self._n_steps(start, n.position)) for n in self.nodes[start].connections])        
        max_steps = 0
        c = 0
        while paths:
            dest, visited, n_steps = paths.popleft()
            c += 1
            if c % 100 == 0:
                print(f"Queue size {len(paths)} current: {dest} n_steps:{n_steps} max: {max_steps}")
            if dest == end:
                if n_steps > max_steps:
                    max_steps = n_steps
                continue
            for n in self.nodes[dest].connections:
                if not n.position in visited: 
                    paths.appendleft((n.position, visited | {n.position}, n_steps + self._n_steps(dest, n.position)))
        return max_steps

    def solve_part_1(self, input, args):
        start, end = self._build_nodes(input)
        return self._calculate_longest_path(start, end)

    def solve_part_2(self, input, args):
        start, end = self._build_nodes(input, use_slopes=False)
        return self._calculate_longest_path(start, end)

if __name__ == '__main__':    
    day23 = Day23Solution()
    day23.run()