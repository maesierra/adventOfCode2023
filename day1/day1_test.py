import unittest
import os
import sys
from .day1 import Day1Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day1SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """a
b
c
d
e
""" 
        with text_to_input(lines) as input: 
            solver = Day1Solution()
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 0)

    def test_part2(self):
        lines = """a
b
c
d
e
""" 
        with text_to_input(lines) as input: 
            solver = Day1Solution()
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 2)


if __name__ == '__main__':
    unittest.main()