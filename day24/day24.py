import os
import sys
from typing import List, Tuple


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Hailstone():
    def __init__(self, str:str) -> None:
        pos, speed = str.strip().split("@")
        x, y, z = [int(d) for d in pos.split(", ")]
        self.dx, self.dy, self.dz = [int(d) for d in speed.split(", ")]
        # x(t) = x + dx*t
        #Convert the start point and speed in 2 points, at t=0 and t=1
        self.p1:Tuple[int,int, int] = (x, y, z)
        self.p2:Tuple[int,int, int] = (x + self.dx, y + self.dy, z + self.dz)

    def position_in_past(self, pos:Tuple[float, float]) -> bool:
        x, y = pos
        if self.dx < 0 and x > self.p1[0]: 
            return True
        elif self.dx > 0 and x < self.p1[0]:
            return True
        if self.dy < 0 and y > self.p1[1]:
            return True
        elif self.dy > 0 and y < self.p1[1]:
            return True
        return False

    def intersect(self, other:"Hailstone") -> Tuple[float, float]:
        a1 = self.p2[1] - self.p1[1] 
        b1 = self.p1[0] - self.p2[0] 
        c1 = a1*(self.p1[0]) + b1*(self.p1[1])

        a2 = other.p2[1] - other.p1[1]
        b2 = other.p1[0] - other.p2[0]
        c2 = a2*(other.p1[0]) + b2*(other.p1[1])

        determinant = a1*b2 - a2*b1
        if (determinant == 0):
            # parallel lines
            return None
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            return (x, y)
         
    def __str__(self) -> str:
        return f"{self.p1}[{self.dx}, {self.dy}, {self.dz}]"

class Day24Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(24)

    def solve_part_1(self, input, args):
        area = args[0] if len(args) >= 1 else (200000000000000, 400000000000000)
        min_value, max_value = area
        hailstones:List[Hailstone] = [Hailstone(l) for l in self.input_to_lines(input)]
        res = 0
        for i, a in enumerate(hailstones):
            for b in hailstones[i + 1:]:
                if self.debug:
                    print(f"Intersecting {a} / {b} => ", end="")
                intersection = a.intersect(b)
                if intersection is None:
                    if self.debug:
                        print(f"parallel")
                    # parallel
                    continue
                if intersection[0] < min_value or intersection[0] > max_value or intersection[1] < min_value or intersection[1] > max_value:
                    if self.debug:
                        print(f"{intersection} outside of area")
                    # outside of the area
                    continue
                if a.position_in_past(intersection) or b.position_in_past(intersection):
                    # intersection is in the past
                    print(f"{intersection} in the past (a: {a.position_in_past(intersection)}, b: {b.position_in_past(intersection)})")
                    continue
                res += 1                
        return res
    
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        print(lines)
        return 2

if __name__ == '__main__':    
    day24 = Day24Solution()
    day24.run()