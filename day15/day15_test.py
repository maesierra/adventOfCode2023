import unittest
import os
import sys
from .day15 import Day15Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day15SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,p
c-,pc=6,ot=7""" 
        with text_to_input(lines) as input: 
            solver = Day15Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 1320)

    def test_part2(self):
        lines = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,p
c-,pc=6,ot=7""" 
        with text_to_input(lines) as input: 
            solver = Day15Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 145)


if __name__ == '__main__':
    unittest.main()