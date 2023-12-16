import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution


class Grid():
    def __init__(self, grid) -> None:
        self.grid = grid
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])

    def index(self, row:int, column:int): 
        return (self.n_cols * row) + column

    def at(self, row:int, column:int):
        return self.grid[row][column]
    
    def set(self, row:int, column:int, value):
        self.grid[row][column] = value

    def row(self, row:int):
        index = self.index(row=row, column=0)
        return self.grid[index:index + self.n_cols]
    
    def tilt(self, direction):                        
        if direction == 'N': 
            for row in range(1, self.n_rows):
                for column in range(0, self.n_cols):
                    if self.at(row, column) != 'O':
                        continue
                    j = row                
                    while j > 0 and self.at(j - 1,column) == '.':
                        self.set(j - 1, column,  'O')
                        self.set(j,column, '.')
                        j -= 1
        elif direction == 'S':
            for row in range(self.n_rows - 2, -1, -1):
                for column in range(0, self.n_cols):
                    if self.at(row,column) != 'O':
                        continue
                    j = row                
                    while j < (self.n_rows - 1) and self.at(j + 1,column) == '.':
                        self.set(j + 1,column,  'O')
                        self.set(j,column, '.')
                        j += 1
        elif direction == 'W': 
            for column in range(1, self.n_cols):
                for row in range(0, self.n_rows):
                    if self.at(row,column) != 'O':
                        continue
                    j = column                
                    while j > 0 and self.at(row,j - 1) == '.':
                        self.set(row,j - 1, 'O')
                        self.set(row,j, '.')
                        j -= 1
        elif direction == 'E': 
            for column in range(self.n_cols - 2, -1, -1):
                for row in range(0, self.n_rows):
                    if self.at(row,column) != 'O':
                        continue
                    j = column                
                    while j < (self.n_cols - 1) and self.at(row,j + 1) == '.':
                        self.set(row,j + 1, 'O')
                        self.set(row,j, '.')
                        j += 1

    def calculate_load(self):
        total_load = 0
        for row in range(0, self.n_rows):
            load = self.n_rows - row
            total_load += sum([1 for c in self.grid[row] if c == 'O']) * load            
        return total_load      
    
    def cycle(self) -> "Grid": 
        self.tilt('N')
        self.tilt('W')
        self.tilt('S')
        self.tilt('E')
        return self
    
    def __hash__(self) -> int:
        return hash("".join(["".join(row) for row in self.grid]))

    def print(self):        
        return "\n".join(["".join(row) for row in self.grid])
    

class Day14Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(14)

    def _parse_grid(self, input) -> Grid:
        lines = self.input_to_lines(input)
        grid = Grid([[c for c in row] for row in lines])
        return grid

        
    
    def solve_part_1(self, input, args):
        grid = self._parse_grid(input)
        grid.tilt('N')
        if self.debug:
            print(grid.print())    
        return grid.calculate_load()


    
    def solve_part_2(self, input, args):
        previous_states = {}
        previous_loads = {}        
        grid = self._parse_grid(input)
        cycle = 0
        n_cycles = 1000000000
        while cycle < n_cycles: 
            if self.debug and cycle % 100000 == 0: 
                print(f"cycle {cycle}")                            
            key = f"{hash(grid)}"
            found = previous_states.get(key, None)
            if found:
                loop_start = found
                loop_size = cycle - loop_start
                offset = (n_cycles - 1 - loop_start) % loop_size
                return previous_loads[loop_start + offset]                
            else:                
                previous_states[key] = cycle
                grid.cycle()
                previous_loads[cycle] = grid.calculate_load()
                    
            print(f"load after {cycle} {grid.calculate_load()}")      
            cycle += 1
        return grid.calculate_load()

if __name__ == '__main__':    
    day14 = Day14Solution()
    day14.run()