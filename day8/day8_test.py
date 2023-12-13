import unittest
import os
import sys
from .day8 import Day8Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day8SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""" 
        lines2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
        for lines, expected in zip([lines1, lines2], [2, 6]):
            with text_to_input(lines) as input: 
                solver = Day8Solution()
                solution = solver.solve_part_1(input, [])
                self.assertEqual(solution, expected)

    def test_part2(self):
        lines = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""" 
        with text_to_input(lines) as input: 
            solver = Day8Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 6)

    def test_part2_real_input(self):
        input_file = os.path.join(os.path.dirname(__file__), "../", "input_8")
        solver = Day8Solution()
        solver.debug = True
        solution = solver.solve_part_2(input_file, [])
        self.assertGreater(solution, 0)
            

if __name__ == '__main__':
    unittest.main()