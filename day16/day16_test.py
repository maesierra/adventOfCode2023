import unittest
import os
import sys
from .day16 import Day16Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day16SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\ 
..../.\\\\..
.-.-/..|..
.|....-|.\ 
..//.|....""" 
        with text_to_input(lines) as input: 
            solver = Day16Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 46)

    def test_part2(self):
        lines = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\ 
..../.\\\\..
.-.-/..|..
.|....-|.\ 
..//.|....""" 
        with text_to_input(lines) as input: 
            solver = Day16Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 51)


if __name__ == '__main__':
    unittest.main()