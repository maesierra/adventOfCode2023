import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from dijkstar import Graph, find_path

from advent_of_code import Solution
from matrix import Position, dimensions, in_grid


def node(row, col, direction):
    return f"{row}-{col}-{direction}"

class Path():
    def __init__(self, src:Position, dest:Position, direction:str) -> None:
        self.src = src
        self.dest = dest
        self.direction = direction

    def __str__(self) -> str:
        return f"{node(row=self.src.y, col=self.src.x)}=>{node(row=self.dest.y, col=self.dest.x)}"

def cost(u, v, edge, prev_edge):
        cost, direction = edge
        prev_cost = prev_edge[0] if prev_edge else None
        prev_direction = prev_edge[1] if prev_edge else None
        if direction == prev_direction:
            cost += 10000
        return cost

class Day17Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(17)

    def _calculate_paths(self, pos:Position, direction:str, crucible_range) -> list:
        paths = []
        row = pos.y
        col = pos.x
        current_node = node(row, col, direction) 
        if current_node in self.nodes:
            return []
        current_pos = Position(y=row, x=col)
        if direction in ("H", ""):
            for idx in crucible_range:
                if in_grid(self.map, Position(y=row + idx, x=col)):
                    dest_node = node(row=row + idx, col=col, direction="V")
                    path = Path(src=current_pos, dest=Position(y=row + idx, x=col), direction="V")
                    cost = sum(self.transposed_map[col][row + 1:row + idx + 1])
                    self.graph.add_edge(current_node, dest_node, (cost, "V"))
                    paths.append(path)
                if in_grid(self.map, Position(y=row - idx, x=col)):
                    dest_node = node(row=row - idx, col=col, direction="V")
                    path = Path(src=current_pos, dest=Position(y=row - idx, x=col), direction="V")
                    cost = sum(self.transposed_map[col][row - idx:row])
                    self.graph.add_edge(current_node, dest_node, (cost, "V"))
                    paths.append(path)
            self.nodes[current_node] = True
        if direction in ("V", ""):
            for idx in crucible_range:
                if in_grid(self.map, Position(y=row, x=col + idx)):
                    dest_node = node(row=row, col=col + idx, direction="H")
                    path = Path(src=current_pos, dest=Position(y=row, x=col + idx), direction="H")
                    cost = sum(self.map[row][col + 1:col + idx + 1])
                    self.graph.add_edge(current_node, dest_node, (cost, "H"))
                    paths.append(path)
                if in_grid(self.map, Position(y=row, x=col - idx)):
                    dest_node = node(row=row, col=col - idx, direction="H")
                    path = Path(src=current_pos, dest=Position(y=row, x=col - idx), direction="H")
                    cost = sum(self.map[row][col - idx:col])
                    self.graph.add_edge(current_node, dest_node, (cost, "H"))
                    paths.append(path)
            self.nodes[current_node] = True     
        return paths
        

    def _parse_map(self, input, ultra_crucible = True):
        self.map = [[int(c) for c in line] for line in self.input_to_lines(input)]
        self.n_rows, self.n_cols = dimensions(self.map)
        self.transposed_map = [[row[c] for row in self.map] for c in range(0, self.n_cols)]
        self.graph = Graph()
        self.nodes = {}
        crucible_range = range(4, 11) if ultra_crucible else range(1, 4)
        paths = self._calculate_paths(pos=Position(y=0, x=0), direction="", crucible_range=crucible_range)
        while paths:
            new_paths = []
            for path in paths:
                new_paths.extend(self._calculate_paths(path.dest, path.direction, crucible_range=crucible_range))
            paths = new_paths


    def calculate_cost(self, input, ultra_crucible = False):
        self._parse_map(input, ultra_crucible=ultra_crucible)
        src = node(0, 0, "")
        total_cost = None
        for direction in ["H", "V"]: 
            try:
                path = find_path(graph=self.graph, s=src, d=node(self.n_rows - 1, self.n_cols - 1, direction), cost_func=cost)
                if total_cost is None or path.total_cost < total_cost:
                    total_cost = path.total_cost
            except:
                pass
        return total_cost

    def solve_part_1(self, input, args):
        return self.calculate_cost(input, ultra_crucible=False)

    def solve_part_2(self, input, args):
        return self.calculate_cost(input, ultra_crucible=True)

if __name__ == '__main__':    
    day17 = Day17Solution()
    day17.run()