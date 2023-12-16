import os
import sys
import threading


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution
from matrix import Position, in_grid, dimensions
import concurrent.futures

class Tile():
    def __init__(self, type:str) -> None:
        self.type = type
        self.energized = False
        self.split = False

class Beam():
    def __init__(self, pos:Position, direction:str) -> None:
        self.position = Position(x=pos.x, y=pos.y)
        self.direction = direction

class Day16Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(16)

    def _create_grid(self, lines) -> list:
        return [[Tile(c) for c in row.strip()] for row in lines]
    
    def _print_grid(self, grid):
        print("\n".join((
            ["".join(['#' if t.energized else t.type for t in row]) for row in grid]
        )))
        print("\n\n")
    


    # Runs the beam until it exits the grid, returning the split beans
    def _run_beam(self, grid:list, beam:Beam, lock:threading.Lock) -> list:
        pos = beam.position
        split_beams = []
        while in_grid(grid=grid, pos=pos):
            tile = grid[pos.y][pos.x]
            with lock:
                tile.energized = True
            if self.debug:
                self._print_grid(grid=grid)
            if tile.split:
                break
            if tile.type == '-' and beam.direction in ['N', 'S']:
                beam.direction = 'E'
                split_beam = Beam(pos=pos, direction='W')
                split_beam.position.x -= 1
                if in_grid(grid=grid, pos=split_beam.position):
                    split_beams.append(split_beam)
                with lock:
                    tile.split = True
            elif tile.type == '|' and beam.direction in ['E', 'W']:
                beam.direction = 'S'
                split_beam = Beam(pos=pos, direction='N')
                split_beam.position.y -= 1
                if in_grid(grid=grid, pos=split_beam.position):
                    split_beams.append(split_beam)
                with lock:
                    tile.split = True
            elif tile.type == '/' and beam.direction == 'N':
                beam.direction = 'E'
            elif tile.type == '/' and beam.direction == 'S':
                beam.direction = 'W'
            elif tile.type == '/' and beam.direction == 'W':
                beam.direction = 'S'
            elif tile.type == '/' and beam.direction == 'E':
                beam.direction = 'N'
            elif tile.type == '\\' and beam.direction == 'N':
                beam.direction = 'W'
            elif tile.type == '\\' and beam.direction == 'S':
                beam.direction = 'E'
            elif tile.type == '\\' and beam.direction == 'W':
                beam.direction = 'N'
            elif tile.type == '\\' and beam.direction == 'E':
                beam.direction = 'S'


            if beam.direction == 'N':
                pos.y -= 1
            elif beam.direction == 'S':
                pos.y += 1
            elif beam.direction == 'W':
                pos.x -= 1
            else:
                pos.x += 1
        return split_beams
    
    def run_beam(self, lines:list, beam:Beam)-> int:
        grid = self._create_grid(lines=lines)
        beams = [beam]
        while beams:
            futures = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                lock = threading.Lock()
                for beam in beams:
                    futures.append(executor.submit(self._run_beam, grid, beam, lock))
            futures, _ = concurrent.futures.wait(futures)
            beams = []
            for future in futures:
                beams.extend(future.result())
        return sum(sum([1 for t in r if t.energized]) for r in grid)

    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        return self.run_beam(lines=lines, beam=Beam(Position(x=0, y=0), 'E'))
        
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        n_rows, n_cols = dimensions(lines)
        max = 0
        for y in range(0, n_rows):
            res = self.run_beam(lines=lines, beam=Beam(Position(x=0, y=y), 'E'))
            if res > max:
                max = res
            res = self.run_beam(lines=lines, beam=Beam(Position(x=n_cols - 1, y=y), 'W'))
            if res > max:
                max = res
        for x in range(0, n_cols):
            res = self.run_beam(lines=lines, beam=Beam(Position(x=x, y=0), 'S'))
            if res > max:
                max = res
            res = self.run_beam(lines=lines, beam=Beam(Position(x=x, y=n_rows - 1), 'N'))
            if res > max:
                max = res
        return max

if __name__ == '__main__':    
    day16 = Day16Solution()
    day16.run()