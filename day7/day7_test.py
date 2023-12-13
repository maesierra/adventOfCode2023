import unittest
import os
import sys
from .day7 import Day7Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day7SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""" 
        with text_to_input(lines) as input: 
            solver = Day7Solution()
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 6440)

    def test_part2(self):
        lines = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""" 
        with text_to_input(lines) as input: 
            solver = Day7Solution()
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 5905)


if __name__ == '__main__':
    unittest.main()