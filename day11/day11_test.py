import unittest
import os
import sys
from .day11 import Day11Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day11SolutionTest(unittest.TestCase):


    def test_part1_v1(self):
        lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""" 
        with text_to_input(lines) as input: 
            solver = Day11Solution()
            solver.debug = True
            solution = solver.solve_part_1_v1(input, [])
            self.assertEqual(solution, 374)

    def test_part1(self):
        lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""" 
        with text_to_input(lines) as input: 
            solver = Day11Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 374)

    def test_part2_10(self):
        lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""" 
        with text_to_input(lines) as input: 
            solver = Day11Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [9])
            self.assertEqual(solution, 1030)

    def test_part2_v1_10(self):
        lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""" 
        with text_to_input(lines) as input: 
            solver = Day11Solution()
            solver.debug = True
            solution = solver.solve_part_1_v1(input, [9])
            self.assertEqual(solution, 1030)

    def test_part2_100(self):
            lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""" 
            with text_to_input(lines) as input: 
                solver = Day11Solution()
                solver.debug = True
                solution = solver.solve_part_1(input, [99])
                self.assertEqual(solution, 8410)

    def test_part2_v1_100(self):
        lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""" 
        with text_to_input(lines) as input: 
            solver = Day11Solution()
            solver.debug = True
            solution = solver.solve_part_1_v1(input, [99])
            self.assertEqual(solution, 8410)
if __name__ == '__main__':
    unittest.main()