import unittest
import os
import sys
from .day14 import Day14Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day14SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = (
"""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        with text_to_input(lines) as input: 
            solver = Day14Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 136)

    def test_part2(self):
        lines = (
"""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        with text_to_input(lines) as input: 
            solver = Day14Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 64)


if __name__ == '__main__':
    unittest.main()