import unittest
import os
import sys
from .day12 import Day12Solution

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_utils import text_to_input


class Day12SolutionTest(unittest.TestCase):

    def test_caculate_arragements(self):
        solver = Day12Solution()
        solver.debug = True
        test_cases = [
            # ['???.### 1,1,3', 1],
            # ['.??..??...?##. 1,1,3', 4],
            # ['?#?#?#?#?#?#?#? 1,3,1,6', 1],
            # ['????.#...#... 4,1,1', 1],
            # ['????.######..#####. 1,6,5', 4],
            # ['?###???????? 3,2,1', 10],
            # ['???#.?#????#?.?..?? 3,1,4,1,2', 2],
            ['????#???#.?????#?? 7,1,3', 12]
        ]
        for line, expected in test_cases:
            line, groups = line.split(" ")
            groups = [int(d) for d in groups.split(",")]
            self.assertEqual(solver.calculate_arrangements(line=line, groups=groups), expected)
    
    def test_caculate_arragements_all(self):
        solver = Day12Solution()
        solver.debug = True
        test_cases = [
            ['???.### 1,1,3', 1],
            ['.??..??...?##. 1,1,3', 4],
            ['?#?#?#?#?#?#?#? 1,3,1,6', 1],
            ['????.#...#... 4,1,1', 1],
            ['????.######..#####. 1,6,5', 4],
            ['?###???????? 3,2,1', 10],
            ['???#.?#????#?.?..?? 3,1,4,1,2', 2],
        ]
        for line, expected in test_cases:
            line, groups = line.split(" ")
            groups = [int(d) for d in groups.split(",")]
            self.assertEqual(solver.calculate_arrangements(line=line, groups=groups), expected)
            print(f"{line} => OK")

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
    