import unittest
import os
import sys
from .day9 import Day9Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day9SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""" 
        with text_to_input(lines) as input: 
            solver = Day9Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 114)

    def test_part2(self):
        lines = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""" 
        with text_to_input(lines) as input: 
            solver = Day9Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 2)


if __name__ == '__main__':
    unittest.main()