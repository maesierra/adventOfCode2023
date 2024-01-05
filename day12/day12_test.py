import unittest
import os
import sys
from .day12 import Day12Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day12SolutionTest(unittest.TestCase):

    # def test_options(self):
    #     solver = Day12Solution()
    #     solver.debug = True
    #     test_cases = [
    #         ('???', [1,1], 1),
    #         ('???????', [2, 1], 10),
    #         ('??????', [1,1], 10,),
    #         ('??????????', [2,2], 21,),
    #         ('??????????????????',[1,3,9], 20),
    #         ('??????????????????',[1,3,2,5], 70),
    #     ]
    #     for text, groups, expected in test_cases:            
    #         options = solver._options(text, groups)
    #         self.assertEqual(options, expected)

    # def test_process_line(self):
    #     solver = Day12Solution()
    #     solver.debug = True
    #     test_cases = [
    #         ('???.????.#?.??? 2,2', 7),
    #         ('?###.?#???????#??? 4,2,1,3', 21),
    #         ('.???#???..??.#???? 6,3', 2),
    #         ('???????#????? 1,3', 17),
    #         ('??????.?????#??# 1,3,2,1,1', 9),
    #         ('.??..##??#?#?#????? 2,2,2,1,1,1', 4),
    #         ('????#??##??.????#. 2,5,5', 3),
    #         ('???.??##..?.?????.? 1,3,3', 9),
    #         ('????#???#.?????#?? 7,1,3', 12),
    #         ('????.######..#####. 1,6,5', 4),
    #         ('.??..??...?##. 1,1,3', 4),
    #         ('???.### 1,1,3', 1),
    #         ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
    #         ('????.#...#... 4,1,1', 1),
    #         ('?###???????? 3,2,1', 10),
    #         ('???#.?#????#?.?..?? 3,1,4,1,2', 2),
    #     ]
    #     self.maxDiff = None
    #     res = []
    #     for line, _ in test_cases:
    #         l, groups = line.split(" ")
    #         groups = [int(d) for d in groups.split(",")]
    #         res.append((line, solver.process_line(line=l, groups=groups)))    
    #     self.assertEqual(res, test_cases)
    

    def test_calculate_arrangements(self):
        solver = Day12Solution()
        solver.debug = True
        test_cases = [
            ('??????.?????#??# 1,3,2,1,1', 9),
            ('?###.?#???????#??? 4,2,1,3', 21),
            ('???.????.#?.??? 2,2', 7),
            ('.???#???..??.#???? 6,3', 2),
            ('???????#????? 1,3', 17),
            ('.??..##??#?#?#????? 2,2,2,1,1,1', 4),
            ('????#??##??.????#. 2,5,5', 3),
            ('???.??##..?.?????.? 1,3,3', 9),
            ('????#???#.?????#?? 7,1,3', 12),
            ('????.######..#####. 1,6,5', 4),
            ('.??..??...?##. 1,1,3', 4),
            ('???.### 1,1,3', 1),
            ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
            ('????.#...#... 4,1,1', 1),
            ('?###???????? 3,2,1', 10),
            ('???#.?#????#?.?..?? 3,1,4,1,2', 2),
        ]
        self.maxDiff = None
        res = []
        for line, _ in test_cases:
            l, groups = line.split(" ")
            groups = [int(d) for d in groups.split(",")]
            solver.cache.clear()
            res.append((line, solver.calculate_arrangements(line=l, groups=groups)))    
        self.assertEqual(res, test_cases)
    

    def test_part1(self):
        lines = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""" 
        with text_to_input(lines) as input: 
            solver = Day12Solution()
            solver.debug = True
            solution = solver.solve_part_1(input, [])
            self.assertEqual(solution, 21)

    def test_part1_real_input(self):
        input_file = os.path.join(os.path.dirname(__file__), "../", "input_12")
        solver = Day12Solution()
        solver.debug = False
        solution = solver.solve_part_1(input_file, [])
        self.assertGreater(solution, 0)


    def test_part2(self):
        lines = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""" 
        with text_to_input(lines) as input: 
            solver = Day12Solution()
            # solver.debug = True
            solution = solver.solve_part_2(input, [])
            self.assertEqual(solution, 525152)


if __name__ == '__main__':
    unittest.main()
    