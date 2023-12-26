import unittest
import os
import sys
from .day25 import Day25Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day25SolutionTest(unittest.TestCase):


    def test_part1(self):
        lines = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""" 
        with text_to_input(lines) as input: 
            solver = Day25Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 54)

    def test_part2(self):
        lines = """
""" 
        with text_to_input(lines) as input: 
            solver = Day25Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 2)


if __name__ == '__main__':
    unittest.main()