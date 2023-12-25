import unittest
import os
import sys
from .day24 import Day24Solution, Hailstone

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day24SolutionTest(unittest.TestCase):

    def test_intersect(self):
        test_cases = [
        ("19, 13, 30 @ -2, 1, -2" , "18, 19, 22 @ -1, -1, -2",  (14.333, 15.333)),
        ("19, 13, 30 @ -2, 1, -2" , "20, 25, 34 @ -2, -2, -4",  (11.667, 16.667)),
        ("19, 13, 30 @ -2, 1, -2" , "12, 31, 28 @ -1, -2, -1",  (6.2, 19.4)),
        # ("19, 13, 30 @ -2, 1, -2" , "20, 19, 15 @ 1, -5, -3",   None),
        ("18, 19, 22 @ -1, -1, -2", "20, 25, 34 @ -2, -2, -4",  None),
        ("18, 19, 22 @ -1, -1, -2", "12, 31, 28 @ -1, -2, -1",  (-6, -5)),
        # ("18, 19, 22 @ -1, -1, -2", "20, 19, 15 @ 1, -5, -3 ",  None),
        ("20, 25, 34 @ -2, -2, -4", "12, 31, 28 @ -1, -2, -1",  (-2, 3)),
        # ("20, 25, 34 @ -2, -2, -4", "20, 19, 15 @ 1, -5, -3 ",  None),
        # ("12, 31, 28 @ -1, -2, -1", "20, 19, 15 @ 1, -5, -3 ",  None),
        ]
        solver = Day24Solution()
        solver.debug = True
        for line1, line2, expected in test_cases:
            a = Hailstone(line1)
            b = Hailstone(line2)
            res = a.intersect(b)
            if expected == None: 
                self.assertIsNone(res)
            else: 
                self.assertAlmostEqual(res[0], expected[0], places=3)
                self.assertAlmostEqual(res[1], expected[1], places=3)

    def test_part1(self):
        lines = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""" 
        with text_to_input(lines) as input: 
            solver = Day24Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [(7, 27)])
            self.assertEqual(solution, 2)

    def test_part2(self):
        lines = """
""" 
        with text_to_input(lines) as input: 
            solver = Day24Solution()
            solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 2)


if __name__ == '__main__':
    unittest.main()