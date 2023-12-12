import os
import sys
import re
from math import gcd

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Node():
    def __init__(self, name: str) -> None:
        self.name = name
        self.group = name[-1]
        self.connected_from = {"L": [], "R":[]}
        self.connected_to = {"L": None, "R":None}

    def connect(self, left:'Node', right:'Node'):
        self.connected_to["L"] = left
        self.connected_to["R"] = right
        left.connected_from["L"].append(self)
        right.connected_from["R"].append(self)

        
    def move(self, movement:str) -> 'Node':
        return self.connected_to[movement]
    
    def __str__(self) -> str:
        return self.name
    
class Instructions():
    def __init__(self, line:str) -> None:
        self.instructions = [c for c in line.strip()]
        self.len = len(self.instructions)
        self.pos = 0
        self.total = 0

    def next(self) -> str:
        current = self.instructions[self.pos]
        self.pos = (self.pos + 1) % self.len
        self.total += 1
        return current
    
    def get(self, index:int) -> str:
        return self.instructions[index]
    
    def reset(self):
        self.pos = 0
        self.total = 0

class NodeAtIndex():
    def __init__(self, node:Node, index:int) -> None:
        self.node = node
        self.index = index

    def __str__(self) -> str:
        return f"{self.node.name}-{self.index}"


class Loop():
    def __init__(self, node:Node, position:int, size: int) -> None:
        self.node = node
        self.position = position
        self.size = size

    def __str__(self) -> str:
        return f"Loop starting at {self.position} {str(self.node)}. Size: {self.size}"
    



class Day8Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(8)

    def _parse_nodes(self, lines):
        nodes = {}
        for l in lines:
            match = re.search(r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", l)
            for n in match.groups():
                if not n in nodes:
                    nodes[n] = Node(name=n)
            node, left, right = [nodes[n] for n in match.groups()]
            node.connect(left=left, right=right)
        return nodes
            
    def _parse(self, input) -> tuple: 
        lines = self.input_to_lines(input)
        nodes = self._parse_nodes(lines[2:])                
        instructions = Instructions(line=lines[0])
        return nodes, instructions

    def solve_part_1(self, input, args):
        nodes, instructions = self._parse(input)
        destination = nodes['ZZZ']
        current = nodes['AAA']
        while current != destination:
            current = current.move(instructions.next())
        return instructions.total
    
    def _calculate_loop(self, node:"Node", instructions:Instructions) -> Loop:
        instructions.reset()
        path = []
        visited = {}        
        current = NodeAtIndex(node.move(instructions.next()), 0)
        while not str(current) in visited:
            path.append(current)
            visited[str(current)] = current
            pos = instructions.pos
            current = NodeAtIndex(current.node.move(instructions.next()), pos)
        # Find were the end is
        end = None
        for i, n in enumerate(path):
            if n.node.group == 'Z':
                # Lame hack. The solution has only one Z in the loop, but the test input has 2 and the valid is the second
                end = i
        return Loop(node=path[end].node, position=end, size=len(path))        
        
    

    
    def solve_part_2_v1(self, input, args):
        nodes, instructions = self._parse(input)
        nodes = nodes.values()
        current = [n for n in nodes if n.group == 'A']
        destination_group = set(['Z'])
        pos = 0
        n_instructions = len(instructions)
        steps = 0
        while set([n.group for n in current]) != destination_group:
            movement = instructions[pos]
            print(f"Step {steps}. {[n.name for n in current]} {movement} => ", end = "")        
            current = [n.move(movement) for n in current]
            print(f"{[n.name for n in current]}")        
            pos = (pos + 1) % n_instructions
            steps += 1
        return steps
    
    
    def lcm(self, a,b):
        return a*b // gcd(a,b)

    def  solve_part_2(self, input, args):
        nodes, instructions = self._parse(input)
        loops = [self._calculate_loop(node=n, instructions=instructions) for n in nodes.values() if n.group == 'A']
        if self.debug:
            print([str(l) for l in loops])
        current = [l.position for l in loops]        
        lowest = sorted(current)[0]
        lcm = 1
        for l in loops:
            lcm = self.lcm(lcm, l.size)
            print(f"hiii...{lcm}")
        print ("holi")
        return lowest + lcm - 1
        # while True:
        #     # get the lowest position
        #     lowest_pos = None
        #     lowest_idx = None
        #     for i, pos in enumerate(current):
        #         if lowest_pos == None or pos < lowest_pos:
        #             lowest_pos = pos
        #             lowest_idx = i
        #     if self.debug:
        #         print(f"{current} Increasing {lowest_idx} by {loops[lowest_idx].size}")
        #     current[lowest_idx] += loops[lowest_idx].size
        #     if self.debug:
        #         print(f"{current}")
        #     # Check if all are at the same position
        #     value = current[0]
        #     for pos in current:
        #         if value != pos:
        #             value = None
        #     if value: 
        #         return value + 1
            

if __name__ == '__main__':    
    day8 = Day8Solution()
    day8.debug = True
    day8.run()