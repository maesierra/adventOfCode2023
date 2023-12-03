import unittest
import os
import sys
from .day3 import Day3Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day3SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""" 
        with text_to_input(lines) as input: 
            solver = Day3Solution()
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 4361)

    def test_part2(self):
        lines = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""" 
        with text_to_input(lines) as input: 
            solver = Day3Solution()
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 467835)


if __name__ == '__main__':
    unittest.main()