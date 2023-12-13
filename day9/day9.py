import os
import sys


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Day9Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(9)

    def _parse_histories(self, input):
        return [[int(n) for n in l.split(" ") if n != ""] for l in self.input_to_lines(input)]
    
    def _print_steps(self, steps:list):
        for i, step in enumerate(steps):
            offset = (i * 2) - 1
            print(f"{' '*offset}{' '.join([str(n) for n in step])}")

    def _calculate_next(self, history, reverse = False):
        steps = [[n for n in history]]
        step = steps[-1]
        while len([n for n in step if n == 0]) !=  len(step):
            new_step = []
            for i, n in enumerate(step):
                if i < len(step) - 1:
                    new_step.append(step[i + 1] - n)
            steps.append(new_step)
            step = steps[-1]
        carry_over = 0        
        idx = 0 if reverse else -1
        for step in reversed(steps[:-1]):
            if reverse: 
                new_value = step[idx] - carry_over
            else: 
                new_value = step[idx] + carry_over
            if reverse:
                step.insert(0, new_value)
            else: 
                step.append(new_value)
            carry_over = step[idx]
        if self.debug:
            self._print_steps(steps)    
        next_value = steps[0][idx]
        return next_value
    

    def solve_part_1(self, input, args):
        histories = self._parse_histories(input)
        res = 0
        for history in histories:            
            next_value = self._calculate_next(history)
            res += next_value
        return res
    

    def solve_part_2(self, input, args):
        histories = self._parse_histories(input)
        res = 0
        for history in histories:            
            next_value = self._calculate_next(history, reverse=True)
            res += next_value
        return res


if __name__ == '__main__':    
    day9 = Day9Solution()
    day9.run()