import os
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution


class Connection():
    def __init__(self, current: "Pipe", north:"Pipe" = None, south:"Pipe" = None, west:"Pipe" = None, east:"Pipe" = None) -> None:
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.current = current

    def is_connected_to(self, pipe:"Pipe") -> bool:
        return self.north == pipe or self.south == pipe or self.east == pipe or self.west == pipe
    
    def as_tuple(self)-> tuple:
        pipes = [p for p in [self.north, self.south, self.east, self.west] if p]
        return (pipes[0], pipes[1])

    def follow(self, pipe:"Pipe") -> "Pipe":
        pipe1, pipe2 = self.as_tuple()
        return pipe1 if pipe2 == pipe else pipe2
        

class Pipe():
    def __init__(self, shape:str, position:tuple, north:"Pipe" = None, south:"Pipe" = None, west:"Pipe" = None, east:"Pipe" = None) -> None:
        self.position = position
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.connection = None
        self.shape = shape

    def connect(self) -> Connection:
        if not self.connection:            
            if self.shape == "F":
                self.connection = Connection(current=self, south=self.south, east=self.east)
            elif self.shape == "7":
                self.connection = Connection(current=self, south=self.south, west=self.west)
            elif self.shape == "L":
                self.connection = Connection(current=self, north=self.north, east=self.east)
            elif self.shape == "J":
                self.connection = Connection(current=self, north=self.north, west=self.west)
            elif self.shape == "-":
                self.connection = Connection(current=self, east=self.east, west=self.west)
            elif self.shape == "|":
                self.connection = Connection(current=self, north=self.north, south=self.south)
        return self.connection
        

class Day10Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(10)

    def _get_pipe(self, pipes:dict, lines:list, position:tuple) -> Pipe:
        row, col = position
        key = f"{row}-{col}"
        if key in pipes:
            return pipes[key]
        shape = lines[row][col]
        if shape == '.':
            return None
        pipe = Pipe(shape=shape, position=position)
        pipes[key] = pipe
        return pipe

    # Return the start pipe with the shape calculated

    def _parsePipes(self, lines) -> Pipe:        
        pipes = {}
        start = None
        n_rows = len(lines)
        n_columns = len(lines[0])
        for row, line in enumerate(lines):
            for column, c in enumerate([c for c in line]):
                if c == '.':
                    continue
                pipe       = self._get_pipe(pipes, lines, (row, column))
                pipe.north = self._get_pipe(pipes, lines, (row - 1, column)) if row > 0 else None
                pipe.south = self._get_pipe(pipes, lines, (row + 1, column)) if row < (n_rows - 1) else None
                pipe.west  = self._get_pipe(pipes, lines, (row, column - 1))  if column > 0 else None
                pipe.east  = self._get_pipe(pipes, lines, (row, column + 1))  if column < (n_columns - 1) else None                                                
                if c == 'S':
                    start = pipe
        # 1st try to determine S shape
        neighbour_connections = [p.connect() for p in [start.north, start.south, start.east, start.west] if p]
        # There should be only 2 connected to start
        connection1, connection2 = [c for c in neighbour_connections if c.is_connected_to(start)]
        if connection1.north == start and start.south == connection1.current:
            # possible shapes | F 7
            if connection2.south == start and start.north == connection2.current:
                start.shape = '|'
            elif connection2.east == start and start.west == connection2.current:
                start.shape = '7'
            elif connection2.west == start and start.east == connection2.current:
                start.shape = 'F'
        elif connection1.south == start and start.north == connection1.current:
            # possible shapes | L J
            if connection2.north == start and start.south == connection2.current:
                start.shape = '|'
            elif connection2.east == start and start.west == connection2.current:
                start.shape = 'J'
            elif connection2.west == start and start.east == connection2.current:
                start.shape = 'L'
        elif connection1.east == start and start.west == connection1.current:
            # possible shapes - J 7
            if connection2.north == start and start.south == connection2.current:
                start.shape = '7'
            elif connection2.south == start and start.north == connection2.current:
                start.shape = 'J'
            elif connection2.west == start and start.east == connection2.current:
                start.shape = '-'
        elif connection1.west == start and start.east == connection1.current:
            # possible shapes - F L
            if connection2.north == start and start.south == connection2.current:
                start.shape = 'F'
            elif connection2.east == start and start.west == connection2.current:
                start.shape = '-'
            elif connection2.south == start and start.north == connection2.current:
                start.shape = 'L'
        if start.shape == 'S':
            raise Exception("No suitable connection found")
        return start            


    def _get_loop(self, lines) -> list:
        start = self._parsePipes(lines)
        if self.debug:
            print(f"Starting at {start.position}")
        pipes = []
        current_pipe, _ = start.connect().as_tuple()        
        prev_pipe = start
        while current_pipe != start:
            if self.debug:
                print(f"Moved to {current_pipe.position} {current_pipe.shape} Distance {len(pipes)}")
            pipes.append(prev_pipe)
            dest_pipe = current_pipe.connect().follow(prev_pipe)
            prev_pipe = current_pipe
            current_pipe = dest_pipe
        pipes.append(prev_pipe)
        return pipes

    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        pipes = self._get_loop(lines)
        return int(len(pipes) / 2) 
        
    
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        main_loop_pipes = self._get_loop(lines)
        pipe_map = {f"{p.position[0]}-{p.position[1]}":p  for p in main_loop_pipes}

        horizontal_rays = []        
        n_columns = len(lines[0])
        for row, line in enumerate(lines):
            count = 0
            horizontal_rays.append([0]*n_columns)
            for column, c in enumerate(line):
                on_loop = f"{row}-{column}" in pipe_map
                prev_on_loop = f"{row}-{column - 1}" in pipe_map
                next_on_loop = f"{row}-{column + 1}" in pipe_map
                if on_loop and (not prev_on_loop or not next_on_loop):
                    count += 1     
                horizontal_rays[row][column] = count

        enclosed = 0
        for row, line in enumerate(lines):
            for column, c in enumerate(line):
                if not f"{row}-{column}" in pipe_map and horizontal_rays[row][column] % 2 == 1:
                    if self.debug:
                        print(f"Enclosed found at {row}-{column}")
                    enclosed += 1
                
        return enclosed

if __name__ == '__main__':    
    day10 = Day10Solution()
    day10.run()