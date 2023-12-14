import unittest
import os
import sys
from .day13 import Day13Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day13SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""" 
        with text_to_input(lines) as input: 
            solver = Day13Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 405)

    def test_part2(self):
        lines = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""" 
        with text_to_input(lines) as input: 
            solver = Day13Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 400)


if __name__ == '__main__':
    unittest.main()