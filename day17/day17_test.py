import unittest
import os
import sys
from .day17 import Day17Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day17SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""" 
        with text_to_input(lines) as input: 
            solver = Day17Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 102)

    def test_part2(self):
        lines = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""" 
        with text_to_input(lines) as input: 
            solver = Day17Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 94)


if __name__ == '__main__':
    unittest.main()