import unittest
import os
import sys
from .day1 import Day1Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day1SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""" 
        with text_to_input(lines) as input: 
            solver = Day1Solution()
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 142)

    def test_part2(self):
        lines = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""" 
        with text_to_input(lines) as input: 
            solver = Day1Solution()
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 281)


if __name__ == '__main__':
    unittest.main()