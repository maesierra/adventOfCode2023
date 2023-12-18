import unittest
import os
import sys
from .day18 import Day18Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day18SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""" 
        with text_to_input(lines) as input: 
            solver = Day18Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 62)

    def test_part1_real_input(self):
        input_file = os.path.join(os.path.dirname(__file__), "../", "input_18")
        solver = Day18Solution()
        solver.debug = True
        solution = solver.solve_part_1(input_file, [])
        self.assertGreater(solution, 0)

    def test_part2(self):
        lines = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""" 
        with text_to_input(lines) as input: 
            solver = Day18Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 952408144115)


if __name__ == '__main__':
    unittest.main()