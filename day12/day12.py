import os
import re
import sys
from collections import Counter

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Cache(): 
    def __init__(self) -> None:
        self.dict = {}
    
    def _key(self, fragment:str, groups:list):
        return f"{fragment} {",".join([str(g) for g in groups])}"
    
    def put(self, fragment:str, groups:list, value:int):
        self.dict[self._key(fragment=fragment, groups=groups)] = value

    def get(self, fragment:str, groups:list): 
        return self.dict.get(self._key(fragment=fragment, groups=groups), None)

        

class Day12Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(12)
        self.cache = Cache()

    def calculate_arrangements(self, groups, line, pos = 0, matched="") -> int:
        unmatched_at_start = line[pos:]
        while groups:            
            unmatched = line[pos:]
            cached = self.cache.get(fragment=unmatched, groups=groups)
            # if cached is not None:
            #     if self.debug:
            #         print(f"Cache hit with {unmatched} {groups}")
            #     return cached
            #Basic consistency checks
            c = Counter(unmatched)
            if c.get('?', 0) + c.get('#', 0) < sum(groups):
                # Not enough ? to be converted into #
                print(f"{line} => INVALID (case1) matched={matched} unmatched={line[pos:]} groups={groups}")
                self.cache.put(fragment=unmatched_at_start, groups=groups, value=0)
                return 0
            # Remove all . from the borders                        
            match = re.search(r"^\.+|\?+|#+", unmatched)
            token = match.group()
            if token[0] == '.':
                # Just match the separators
                pos +=  len(token)
                matched += token
                if self.debug:
                    print(f"{line} => matched={matched} unmatched={line[pos:]} groups={groups}")
            elif token[0] == '#':
                size = groups[0]
                # Invalid option
                if len(unmatched) < size or size < len(token):
                    if self.debug:
                        print(f"{line} => INVALID (case2) matched={matched} unmatched={line[pos:]} groups={groups}")
                    self.cache.put(fragment=unmatched_at_start, groups=groups, value=0)
                    return 0
                # We always consume up to group size, regardless if is unknown after
                token = unmatched[:size]
                if '.' in token:
                    # Invalid option
                    if self.debug:
                        print(f"{line} => INVALID (case3) matched={matched} unmatched={line[pos:]} groups={groups}")
                    self.cache.put(fragment=unmatched_at_start, groups=groups, value=0)
                    return 0   
                pos += size
                matched += '#'*size
                groups = groups[1:]
                if not groups:
                    # Need to check if no more #
                    if '#' in unmatched[size:]:
                        if self.debug:
                            print(f"{line} => INVALID (case 4) matched={matched} unmatched={line[pos:]} groups={groups}")
                        self.cache.put(fragment=unmatched_at_start, groups=groups, value=0)
                        return 0
                    if self.debug:                    
                        print(f"{line} => MATCH FOUND(case 1) matched={matched}")
                    self.cache.put(fragment=unmatched_at_start, groups=groups, value=1)
                    return 1                                                
                if unmatched[size] == '#':
                    if self.debug:
                        print(f"{line} => INVALID (case 5) matched={matched} unmatched={line[pos:]} groups={groups}")
                    self.cache.put(fragment=unmatched_at_start, groups=groups, value=0)
                    return 0   

            # elif len(token) == sum(groups) + len(groups) - 1:
            #      if self.debug:
            #             print(f"{line} => MATCH FOUND (case2) matched={matched + '.'.join(['#'*g for g in groups])}")
            #      return 1
            # elif len(token) == len(unmatched):
            #     if self.debug:                    
            #         print(f"{line} => MATCH FOUND (case 3) matched={matched} unmatched={line[pos:]} groups={groups}")                    
            #     return sum([n for n in range(0, len(token) - sum(groups))])
            else:                
                n_arrangements = self.calculate_arrangements(line=matched + '.' + unmatched[1:], pos=pos, groups=groups, matched=matched)
                if not matched or matched[-1] != '#':
                    n_arrangements += self.calculate_arrangements(line=matched + '#' + unmatched[1:], pos=pos, groups=groups, matched=matched)                
                if self.debug:                    
                    print(f"{line} completed with {n_arrangements} found.")
                self.cache.put(fragment=unmatched_at_start, groups=groups, value=n_arrangements)
                return n_arrangements
            

        return n_arrangements
    
        



    def solve_part_1(self, input, args):
        lines = self.input_to_lines(input)
        sum = 0
        for i, line in enumerate(lines):
            line, groups = line.split(" ")
            groups = [int(d) for d in groups.split(",")]                                
            res = self.calculate_arrangements(line=line, groups=groups)
            sum += res
            print(f"Line {i}/{len(lines)} {line} => {res}")            
        return sum
    
    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        sum = 0
        for i, line in enumerate(lines):
            folded_line, folded_groups = line.split(" ")
            folded_groups = [int(d) for d in folded_groups.split(",")]
            line = "?".join([folded_line for i in range(0, 5)])
            groups = []
            for i in range(0, 5):
                groups.extend(folded_groups)
            res = self.calculate_arrangements(line=line, groups=groups)
            sum += res
            print(f"Line {i}/{len(lines)} {line} => {res}")            
        return sum

if __name__ == '__main__':    
    day12 = Day12Solution()
    day12.run()

# 000 ???#.?#????#?.?..?? 3,1,4,1,2 => 0    