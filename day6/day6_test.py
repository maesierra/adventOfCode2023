import unittest
import os
import sys
from .day6 import Day6Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day6SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """Time:      7  15   30
Distance:  9  40  200""" 
        with text_to_input(lines) as input: 
            solver = Day6Solution()
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 288)

    def test_part2(self):
        lines = """Time:      7  15   30
Distance:  9  40  200""" 
        with text_to_input(lines) as input: 
            solver = Day6Solution()
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 71503)


if __name__ == '__main__':
    unittest.main()