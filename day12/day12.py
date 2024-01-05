import os
import re
import sys
from collections import Counter, deque
from typing import Deque, Dict, List, Tuple

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

        

class Day12Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(12)
        self.cache:Dict[str, List[List[int]]] = {}

    def calculate_arrangements(self, groups, line, pos = 0, current_group = 0) -> int:
        key = f"{pos}-{current_group}"
        cached = self.cache.get(key, None)
        if cached is not None:
            return cached
        
        #If we reach the end, everything must be consumed
        if pos >= len(line):
            return 1 if current_group == len(groups) else 0
        if current_group > len(groups):
            return 0 #No more groups to consume

        unmatched = line[pos:]        
        c = Counter(unmatched)
        n_unknown = c.get('?', 0)
        if n_unknown + c.get('#', 0) < sum(groups[current_group:]):
            # Not enough ? to be converted into #                
            return 0
        if n_unknown == len(unmatched) and current_group == len(groups):
            return 1
        
        # We try to capture groups or . or # but for ? we only take one
        match = re.search(r"^\.+|\?|#+", unmatched)
        token = match.group()
        n_arrangements = 0
        if token[0] != '#': # ? or .
            # Continue
            n_arrangements += self.calculate_arrangements(groups, line, pos + len(token), current_group)
        if token[0] != '.': # ? or #
            invalid_option = current_group >= len(groups)
            if not invalid_option:
                group = groups[current_group]
                # Invalid option 
                invalid_option = token[0] == '#' and len(token) > group
            if not invalid_option: 
                # We always consume up to group size, regardless if is unknown after
                token = unmatched[:group]
                invalid_option = '.' in token
            if not invalid_option:
                # pos + group + 1 => To take into a account the . after a #
                if pos + group != len(line): #not a exact match                                    
                    invalid_option = line[min(len(line) - 1, pos + group)] == '#'
                pos += group + 1
            if not invalid_option: 
                n_arrangements += self.calculate_arrangements(groups, line, pos, current_group + 1)
        
        self.cache[key] = n_arrangements
        return n_arrangements


    # def _match(self, text:str, group:int):
    #     if len(text) == group:
    #         return True
    #     return False
    
    # def _options(self, text:str, groups:list[int]):
    #     if len(groups) == 1:
    #         return len(text) - groups[0] + 1
    #     elif len(groups) == 0:
    #         return 0        
    #     groups = groups.copy()
    #     required = sum(groups) + (len(groups) - 1)
    #     diff =  len(text) - required
    #     if diff == 0:
    #         return 1
    #     g = groups.pop(0)
    #     n_options = 0 
    #     for i in range(0, diff + 1):
    #         n_options += self._options(text[g + 1 + i:], groups)
    #     return n_options


         

    
    # def _matches(self, text:str, groups:List[int], full=False) -> List[int]:
    #     matched = [len(s) for s in text.split('.') if s]
    #     if matched and matched == (groups if full else groups[:len(matched)]):
    #         return matched
    #     elif len(matched) > 1 and not full:
    #         #See if there is a partial match
    #         matched = matched[:-1]
    #         while matched: 
    #             if matched == groups[:len(matched)]:
    #                 return matched
    #             matched = matched[:-1]
    #         return []
    #     else:
    #         return []
        
    # def _increase_option(self, ancestors, option:str, groups:List[int], n):
    #     for fragment, group in reversed(ancestors):
    #         groups = [group] + groups
    #         option = fragment + option
    #         key = f"{option} {','.join([str(d) for d in groups])}"
    #         self.cache[key] = self.cache.get(key, 0) + n
    #     return n
            


    # def process_line(self, line:str, groups:List[int]) -> int:
    #     n_options = 0
    #     fragments:Deque[Tuple(str, List[int])] = deque()
    #     fragments.appendleft((str(line), groups.copy(), []))
    #     while fragments: 
    #         unmatched, groups, ancestors = fragments.popleft()
    #         cached = self.cache.get(unmatched, None)
    #         if cached:
    #             print(f"using cached result for {unmatched} {cached}")
    #             n_options += cached
    #             continue
    #         current = str(unmatched)            
    #         #Remove all operational from borders
    #         unmatched = unmatched.strip('.')             
    #         current_offset = len(current) - len(unmatched)
    #         c = Counter(unmatched)
    #         n_unknown = c.get('?', 0)
    #         if n_unknown == len(unmatched):
    #             n_options += self._increase_option(ancestors, current, groups, self._options(unmatched, groups))
    #             continue
    #         elif n_unknown == 0:
    #             if self._matches(unmatched, groups, full=True):
    #                 n_options += self._increase_option(ancestors, current, groups, 1)
    #             continue
    #         elif len(groups) == 1 and groups[0] == len(unmatched):
    #             if c.get('.', 0) == 0:
    #                 n_options += self._increase_option(ancestors, current, groups, 1)
    #             continue
    #         #try to determine how many options group 1 has 
    #         # We need to match at least up to group[0], at most len - (sum(remaining_groups) + len(remaining_groups))
    #         group = groups[0]
    #         remaining_groups = groups[1:]
    #         min_remaining_space = sum(remaining_groups) + len(remaining_groups)
    #         # Edge case in which min_remaining_space is fixed to #. Move it to the first ? or . before it
    #         while min_remaining_space < len(unmatched) and unmatched[-min_remaining_space] == '#':
    #             min_remaining_space += 1            
    #         diff = len(unmatched) - min_remaining_space - group + 1    
    #         if diff < 0:
    #             continue            
    #         fragment = unmatched[group + diff:]            
    #         options = []
    #         used_options = set()
    #         fragments_added = set()
    #         for i in range(0, diff):
    #             # We're going to try all the options to put group in the available space. 
    #             # Eg for ????#???#.?????#?? group=7 1,3
    #             # we'll try the options bellow and we'll discard the options that don't match the pattern
    #             # #######......??#??
    #             # .#######.....??#??
    #             # ..#######....??#??
    #             # ...#######...??#??
    #             # ....#######..??#??
    #             # .....#######.??#??
    #             option:str = unmatched[:i].replace('?', '.') + unmatched[i:group + i].replace('?', '#') + unmatched[group + i:group + diff].replace('?', '.')
    #             if option not in used_options: 
    #                 used_options.add(option)
    #                 matched = self._matches(option, groups, full=len(groups) == 1)
    #                 if matched:
    #                     if fragment: 
    #                         # Next fragment will start after the last # in the first matched group plus an extra .
    #                         pos = 0
    #                         while option[pos] == '.':
    #                             pos += 1                            
    #                         pos += matched[0] + 1                                
    #                         next_fragment = unmatched[pos:]
    #                         next_groups = groups[1:]
    #                         if option[:pos] not in fragments_added and next_groups: 
    #                             fragments.appendleft((next_fragment, next_groups, ancestors + [(current[:pos + current_offset], groups[0])]))
    #                             options.append(matched)
    #                             fragments_added.add(option[:pos])
    #                     else: 
    #                         n_options += self._increase_option(ancestors, current, groups, 1)
                

    #     return max(1, n_options)
    

    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        res = 0
        for i, line in enumerate(lines):
            line, groups = line.split(" ")
            groups = [int(d) for d in groups.split(",")]
            self.cache.clear()
            n_options = self.calculate_arrangements(line=line, groups=groups)
            if self.debug:
                print(f"{line} => {n_options}")
            res += n_options
                        
        return res
    
    def solve_part_2(self, input, args):
        # Solve part1 agin to fill the cache
        self.solve_part_1(input, [])
        lines = self.input_to_lines(input)
        sum = 0
        for i, line in enumerate(lines):
            folded_line, folded_groups = line.split(" ")
            folded_groups = [int(d) for d in folded_groups.split(",")]
            line = "?".join([folded_line for i in range(0, 5)])
            groups = []
            for _ in range(0, 5):
                groups.extend(folded_groups)
            self.cache.clear()
            res = self.calculate_arrangements(line=line, groups=groups)
            sum += res
            print(f"Line {i}/{len(lines)} {line} => {res}")            
        return sum

if __name__ == '__main__':    
    day12 = Day12Solution()
    day12.run()
