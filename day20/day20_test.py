import unittest
import os
import sys
from .day20 import Day20Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day20SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""" 
        with text_to_input(lines) as input: 
            solver = Day20Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 32000000)

    def test_part1_input2(self):
        lines = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""" 
        with text_to_input(lines) as input: 
            solver = Day20Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 11687500)


    def test_part2_real_input(self):
        input_file = os.path.join(os.path.dirname(__file__), "../", "input_20")
        solver = Day20Solution()
        solver.debug = False
        solution = solver.solve_part_2(input_file, [])
        self.assertGreater(solution, 0)

if __name__ == '__main__':
    unittest.main()