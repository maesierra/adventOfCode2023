import math
import os
import sys
import re
from typing import Dict, Tuple

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

    def _parse_nodes(self, lines) -> Dict[str, Node]:
        nodes = {}
        for l in lines:
            match = re.search(r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", l)
            for n in match.groups():
                if not n in nodes:
                    nodes[n] = Node(name=n)
            node, left, right = [nodes[n] for n in match.groups()]
            node.connect(left=left, right=right)
        return nodes
            
    def _parse(self, input) -> Tuple[Dict[str, Node], Instructions]: 
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
        return Loop(node=path[end].node, position=end + 1, size=len(path) + 1)        
        
    
    def  solve_part_2(self, input, args):
        nodes, instructions = self._parse(input)
        loops = [self._calculate_loop(node=n, instructions=instructions) for n in nodes.values() if n.group == 'A']
        if self.debug:
            print([(l.node.name, l.position, l.size) for l in loops])
        return math.lcm(*[l.position for l in loops])
        
            

if __name__ == '__main__':    
    day8 = Day8Solution()
    day8.debug = True
    day8.run()