import unittest
import os
import sys
from .day21 import Day21Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day21SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""" 
        with text_to_input(lines) as input: 
            solver = Day21Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [6])
            self.assertEqual(solution, 16)

    def test_part2_real_input(self):
        input_file = os.path.join(os.path.dirname(__file__), "../", "input_21")
        solver = Day21Solution()
        solver.debug = False
        solution = solver.solve_part_2(input_file, [])
        self.assertGreater(solution, 0)


if __name__ == '__main__':
    unittest.main()