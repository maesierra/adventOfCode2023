import os
import sys
from calendar import c
import more_itertools as mit

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution
from matrix import Position, dimensions, in_grid


class Line():
    def __init__(self, to_pos:Position, distance:int, from_pos:Position = None, after:"Line" = None) -> None:        
        self.to_pos = to_pos
        self.next = None
        self.prev = None
        self.distance = distance
        if after:
            self.prev = after
            after.next = self
            self.from_pos = after.to_pos
        elif from_pos:
            self.from_pos = from_pos

    def is_horizontal(self): 
        return self.from_pos.y == self.to_pos.y
    
    def is_upwards(self):
        return self.from_pos.x < self.to_pos.x if self.is_horizontal() else self.from_pos.y < self.to_pos.y
    
    def contains_y(self, y:int) -> bool:
        min_y = min(self.from_pos.y, self.to_pos.y)
        max_y = max(self.from_pos.y, self.to_pos.y)
        return y >= min_y and y <= max_y


class Map():
    def __init__(self, grid:list["str"]) -> None:
        self.grid = grid
        self.n_rows, self.n_cols = dimensions(grid)
    
    def print(self):
        print("\n")
        print("\n".join(["".join(r) for r in self.grid]))
    
    def enclosing_area(self) -> int:
        horizontal_rays = []        
        for row in range(0, self.n_rows):
            count = 0
            horizontal_rays.append([0]*self.n_cols)
            corner = None
            column = 0
            for column in range(0, self.n_cols):
                shape = self.grid[row][column]
                # | always switch 
                if shape == '|':
                   count += 1
                # ┌┘ or └┐ are convex corners that will switch 
                # ┌┘ or └┘ are concanve corners that will not switch
                elif shape in ['┌', '└'] and not corner: 
                    corner = shape
                elif corner and shape in ['┘', '┐']:
                    if (corner == '┌' and shape == '┘') or (corner == '└' and shape == '┐'):
                        count += 1
                    corner = False                                                
                # - and . can be ignored as they don't change
                horizontal_rays[row][column] = count
        enclosed = 0
        for row, line in enumerate(self.grid):
            for column, c in enumerate(line):
                if c == '.' and horizontal_rays[row][column] % 2 == 1:
                    enclosed += 1
        return enclosed


class Day18Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(18)

    def _parse_lines(self, input, use_hex = False) -> list["Line"]:
        start = Position(x=0, y=0)
        current = start
        lines = []        
        for l in self.input_to_lines(input):
            direction, distance, hex = l.split(" ")
            if use_hex: 
                hex = hex.strip("()#")
                distance = int(hex[:5], 16)
                direction = hex[5]
                if direction == "0":
                    direction = "R"
                elif direction == "1":
                    direction = "D"
                elif direction == "2":
                    direction = "L"
                elif direction == "3":
                    direction = "U"
                else:
                    raise Exception(f"Unknown direction {direction}")
            else: 
                distance = int(distance)
            if direction == "D":
                dest = Position(x=current.x, y = current.y + distance)
            elif direction == "U":
                dest = Position(x=current.x, y = current.y - distance)
            elif direction == "L":
                dest = Position(y=current.y, x = current.x - distance)
            elif direction == "R":
                dest = Position(y=current.y, x = current.x + distance)
            if len(lines) == 0:
                line = Line(from_pos=current, to_pos=dest, distance=distance)
            else: 
                line = Line(after=lines[-1], to_pos=dest, distance=distance)
            lines.append(line)
            current = dest
        return lines
    
    def calculate_area(self, lines:list["Line"]) -> int:
        boxes = self.calculate_boxes(lines)
        
        area = 0
        for i, box in enumerate(boxes):
            p1, p2 = box
            width = abs(p1.x - p2.x) + 1
            heigth = abs(p1.y - p2.y) + 1
            area += width * heigth
            for other in boxes[i + 1:]:
                p3, p4 = other
                if p3.x > p2.x or p3.y > p2.y or p4.x < p1.x or p4.y < p1.y:
                    continue
                intersect_width  = min(p2.x, p4.x) - max(p1.x, p3.x) + 1
                intersect_height = min(p2.y, p4.y) - max(p1.y, p3.y) + 1
                area -= intersect_width * intersect_height
        return area
        

    def calculate_boxes(self, lines:list["Line"]) -> list:
        boxes = []
        #let's cut all the horizontal lines into boxes
        cut_rows = sorted(list(set(l.from_pos.y for l in lines if l.is_horizontal())))
        vertical_lines = [l for l in lines if not l.is_horizontal()]
        for y1, y2 in [i for i in zip(list(cut_rows), list(cut_rows[1:]))]:
            lines_cut = sorted([l for l in vertical_lines if l.contains_y(y1) and l.contains_y(y2)], key=lambda x: x.from_pos.x)
            for l1, l2 in mit.chunked(lines_cut, 2):
                boxes.append((Position(x=l1.from_pos.x, y=y1), Position(x=l2.from_pos.x, y=y2)))                
        return boxes
    
    
    def _connect_lines(self, line1:Line, line2:Line) -> str:
        horizontal = line1.is_horizontal()
        upwards = line1.is_upwards()
        if horizontal:
            if upwards:
                return '┐' if line2.is_upwards() else '┘'
            else: 
                return '┌' if line2.is_upwards() else '└'
        else:
            if upwards:
                return '└' if line2.is_upwards() else '┘'
            else:
                return '┌' if line2.is_upwards() else '┐'
            
    def _get_bounds(self, lines:list) -> tuple:
        min_x = None    
        min_y = None
        max_x = 0
        max_y = 0
        line = lines[0]
        current = Position(line.from_pos.x, line.from_pos.y)
        while line:
            horizontal = line.is_horizontal()
            upwards = line.is_upwards()
            if horizontal:
                current.x += line.distance * (1 if upwards else -1)
            else:
                current.y += line.distance * (1 if upwards else -1)
            max_x = max(max_x, current.x)
            max_y = max(max_y, current.y)
            min_x = min(min_x, current.x) if min_x is not None else current.x
            min_y = min(min_y, current.y) if min_y is not None else current.y
            line = line.next
        return (min_x, min_y, max_x, max_y)
    
    def _get_map(self, lines:list) -> Map:
        min_x, min_y, max_x, max_y = self._get_bounds(lines)
        n_rows = max_y - min_y + 1
        n_cols = max_x - min_x + 1
        grid = [['.' for _ in range(0, n_cols)] for _ in range(0, n_rows)]
        line = lines[0]
        current = Position(line.from_pos.x, line.from_pos.y)
        while line:
            horizontal = line.is_horizontal()
            upwards = line.is_upwards()
            for idx in range(0, line.distance):
                if horizontal:
                    current.x += (1 if upwards else -1)
                    shape = '-'
                else:
                    current.y += (1 if upwards else -1)
                    shape = '|'
                if idx == line.distance - 1:
                    shape = self._connect_lines(line, line.next if line.next else lines[0])
                adjusted = Position(y=current.y - min_y, x=current.x - min_x)
                if not in_grid(grid, adjusted):
                    raise Exception(f"Bad pos {adjusted.x} {adjusted.y}")
                else: 
                    grid[adjusted.y][adjusted.x] = shape       
            line = line.next
        return Map(grid)


    def solve_part_1_v1(self, input, args):
        lines = self._parse_lines(input)
        map = self._get_map(lines)
        if self.debug:
            map.print()
        
        # To determine the digging area we need the total perimeter distance + enclosed area
        perimeter = sum([l.distance for l in lines])
        enclosed = map.enclosing_area()            
        return perimeter + enclosed
    
    def solve_part_1(self, input, args):
        lines = self._parse_lines(input)                
        if self.debug:
            self._get_map(lines).print()        
        return self.calculate_area(lines)
    
    def solve_part_2(self, input, args):
        lines = self._parse_lines(input, use_hex=True)
        return self.calculate_area(lines)

if __name__ == '__main__':    
    day18 = Day18Solution()
    day18.run()