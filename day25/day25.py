import os
import sys
from collections import deque
from typing import Deque, Dict, List, Set

import numpy
from dijkstar import Graph, find_path

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution


class Component():
    def __init__(self, name:str) -> None:
        self.name = name
        self.connections:Set[Component]  = set()

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other: object) -> bool:
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash((self.name))


class Connection():
    def __init__(self, n1:str, n2:str) -> None:
        if n1 < n2: 
            self.n1 = n1 
            self.n2 = n2
        else: 
            self.n1 = n2
            self.n2 = n1 
        
    def __str__(self) -> str:
        return f"({self.n1}, {self.n2})"
    
    def __eq__(self, other: object) -> bool:
        return self.n1 == other.n1 and self.n2 == other.n2
    
    def __hash__(self) -> int:
        return hash((self.n1, self.n2))
    
class Day25Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(25)
        self.components: Dict[str, Component] = {}
        self.graph = Graph()

    def _get_or_add_component(self, name) -> Component:
        if not self.components.get(name, None): 
            self.components[name] = Component(name)
        return self.components[name]
    
    def _parse_components(self, input) -> Dict[str, Component]:
        for line in self.input_to_lines(input):
            component, connections = line.split(":")
            component = self._get_or_add_component(component)
            for c in connections.strip().split(" "):
                c = self._get_or_add_component(c)                
                component.connections.add(c)
                c.connections.add(component)
                self.graph.add_edge(component.name, c.name, 1)
                self.graph.add_edge(c.name, component.name, 1)
        return self.components
                
    def _print(self, components):
        for name, c in components.items():
            print(f"{name} -> {[str(i) for i in c.connections]} ({len(c.connections)})")
    
    def _group(self, components) -> List[Set[Component]]:
        groups:Dict[Component, Set[Component]] = {}
        for c1 in components.values():
            group:Set[Component] = set(c1.connections)
            to_process:Deque[Component] = deque([i for i in c1.connections])
            while to_process:
              c2 = to_process.popleft()
              for i in c2.connections:
                  if i not in group:
                      group.add(i)                      
                      to_process.appendleft(i)
            groups[c1] = group    
        res = []
        for g in set(["|".join(sorted([str(i) for i in g])) for g in groups.values()]):
            res.append(set([components[n] for n in  g.split("|")]))
        return res

    def solve_part_1(self, input, args):
        components = self._parse_components(input)
        if self.debug: 
            self._print(components)
        all_connections:Dict[Connection, int] = {}
        for c1 in self.components.values():
            for c2 in c1.connections:
                if c1 != c2:
                    all_connections[Connection(c1.name, c2.name)] = 1

        for c in all_connections.keys(): 
            # Cut the connection and calculate the distance to those 2 nodes
            self.graph.remove_edge(c.n1, c.n2)
            all_connections[c] = find_path(self.graph, c.n1, c.n2).total_cost
            self.graph.add_edge(c.n1, c.n2, 1)
            self.graph.add_edge(c.n2, c.n1, 1)
        
        c1, c2, c3 = [k for k, _ in sorted(all_connections.items(), reverse=True, key=lambda x: x[1])[0:3]]
        self.components[c1.n1].connections.remove(self.components[c1.n2])
        self.components[c1.n2].connections.remove(self.components[c1.n1])
        self.components[c2.n1].connections.remove(self.components[c2.n2])
        self.components[c2.n2].connections.remove(self.components[c2.n1])
        self.components[c3.n1].connections.remove(self.components[c3.n2])
        self.components[c3.n2].connections.remove(self.components[c3.n1])
        groups = self._group(components)
        if len(groups) > 1:
            return numpy.prod([len(g) for g in groups])


        raise Exception("No solution found")

    def solve_part_2(self, input, args):
        lines = self.input_to_lines(input)
        print(lines)
        return 2

if __name__ == '__main__':    
    day25 = Day25Solution()
    day25.run([['pdd', 'ccl', 'bsg']])