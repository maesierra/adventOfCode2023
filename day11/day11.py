import os
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Day11Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(11)

    def _expand_map(self, map, expansion) -> list: 
        expanded = []
        for row in map:
            if len([i for i in row if i]) == 0:
                for _ in range(0, expansion):
                    expanded.append(row)
            expanded.append(row)
        n_columns = len(map[0])    
        for col in range(0, n_columns):
            if len([i for i in [r[col] for r in map] if i]) == 0:
                for i in range(0, len(expanded)):
                    new_row = [c for c in expanded[i]]
                    insert_at = col + (len(new_row) - n_columns)
                    for _ in range(0, expansion):
                        new_row.insert(insert_at, False)                
                    expanded[i] = new_row                
        return expanded
    
    def _map_to_string(self, map):
        str = ""
        for row in map:
            for c in row:
                str += "#" if c else "."
            str += "\n"
        return str + "\n\n"
        
    def _distance(self, g1, g2, expanded_rows=[], expanded_cols=[], expansion = 1):
        y1, x1 = g1
        y2, x2 = g2        
        # need to add the expansion
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        extra_rows = [row for row in expanded_rows if row > min_y and row < max_y]
        extra_cols = [col for col in expanded_cols if col > min_x and col < max_x]
        return abs(x2 - x1) + abs(y2 - y1) + (len(extra_rows)*expansion) + (len(extra_cols)*expansion)

    def solve_part_1_v1(self, input, args):
        lines = self.input_to_lines(input)
        expansion = args[0] if args else 1
        map = [[c == '#' for c in line] for line in lines]
        expanded = self._expand_map(map, expansion)
        if self.debug:
            print()
            print(self._map_to_string(expanded))  
        galaxies = []
        for y, row in enumerate(expanded):
            for x, c in enumerate(row):
                if c:
                    galaxies.append((y, x))
        res = 0
        for i, galaxy in enumerate(galaxies):
            for j, other_galaxy in enumerate(galaxies[i:]):
                if galaxy == other_galaxy: 
                    continue
                distance = self._distance(galaxy, other_galaxy)
                if self.debug:
                    print(f"betewen {i+1}{galaxy} and {j+1+i}{other_galaxy} -> {distance}")
                res += distance
        return res
    
    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        map = [[1 if c == '#' else 0 for c in line] for line in lines]
        if self.debug:
            print()
            print(self._map_to_string(map))  
        galaxies = []
        for y, row in enumerate(map):
            for x, c in enumerate(row):
                if c == 1:
                    galaxies.append((y, x))
        res = 0        
        expansion = args[0] if args else 1
        expanded_rows = [i for i, row in enumerate(map) if sum(row) == 0]
        expanded_columns = [j for j in range(0, len(map[0])) if sum([i for i in [row[j] for row in map]]) == 0]
        for i, galaxy in enumerate(galaxies):
            for j, other_galaxy in enumerate(galaxies[i:]):
                if galaxy == other_galaxy: 
                    continue
                distance = self._distance(g1=galaxy, g2=other_galaxy, expanded_rows=expanded_rows, expanded_cols=expanded_columns, expansion=expansion)
                if self.debug:
                    print(f"betewen {i+1}{galaxy} and {j+1+i}{other_galaxy} -> {distance}")
                res += distance
        return res
    
    def solve_part_2(self, input, args):
        return self.solve_part_1(input=input, args=[999999])

if __name__ == '__main__':    
    day11 = Day11Solution()
    day11.run()