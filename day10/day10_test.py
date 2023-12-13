import unittest
import os
import sys
from .day10 import Day10Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day10SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""" 

# 0 ..╔╗.   ..F7.
# 1 .╔╝║.   .FJ|.
# 2 S╝.╚╗   SJ.L7
# 3 ║╔══╝   |F--J
# 4 ╚╝...   LJ...
#   01234   01234

        with text_to_input(lines) as input: 
            solver = Day10Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 8)

    def test_part2_1(self):
        lines = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""" 
        with text_to_input(lines) as input: 
            solver = Day10Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 4)

    def test_part2_2(self):
        lines = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""" 
        with text_to_input(lines) as input: 
            solver = Day10Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 8)

if __name__ == '__main__':
    unittest.main()