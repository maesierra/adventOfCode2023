from math import prod
import os
import sys
from typing import Tuple, Dict
import re


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

debug = False

class Condition():
    def __init__(self, property:str, comparator:str, value:int) -> None:
        self.property = property
        self.comparator = comparator
        self.value = value

    def applies_to(self, part:"Part") -> bool:
        part_value = part.get_property(self.property)
        return part_value < self.value if self.comparator == "<" else part_value > self.value
    
    def __str__(self) -> str:
        return f"{self.property} {self.comparator} {self.value}"


class Rule():
    def __init__(self, destination:"Workflow", condition:Condition = None) -> None:
        self.condition = condition
        self.destination = destination
    
    def applies_to(self, part:"Part") -> bool:
        return self.condition.applies_to(part) if self.condition else True
    
    def accepts(self, part:"Part") -> bool:
        if debug:
            print(f" -> {self.destination.name}")
        return self.destination.accepts(part)
    
    def __str__(self) -> str:
        return f"{self.condition} -> {self.destination.name}"


class Workflow():
    def __init__(self, name:str, rules:list["Rule"] = []) -> None:
        self.name = name
        self.rules = rules
    
    def accepts(self, part:"Part") -> bool:
        for rule in self.rules:
            if rule.applies_to(part):
                return rule.accepts(part)
        
class AcceptWorflow(Workflow):
    def __init__(self):
        super().__init__(name="A")

    def accepts(self, part:"Part") -> bool:
        return True


class RejectWorkflow(Workflow):
    def __init__(self):
        super().__init__(name="R")

    def accepts(self, part:"Part") -> bool:
        return False

class Part():
    def __init__(self, x:int = 0, m:int = 0, a:int = 0, s:int = 0) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def get_property(self, property:str) -> int : 
        if property == "x":
            return self.x
        elif property == "m":
            return self.m
        elif property == "a":
            return self.a
        elif property == "s":
            return self.s
        
    def __str__(self) -> str:
        return f"[x:{self.x},m:{self.m},a:{self.a},s:{self.s}]"

class Day19Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(19)

    def _parse_workflows(self, lines:list[str]) -> Dict[str, "Workflow"]:
        worflows = {}
        worflows["A"] = AcceptWorflow()
        worflows["R"] = RejectWorkflow()
        for line in lines:
            name, rules = line.strip("}").split("{")
            if not worflows.get(name, None):
                worflows[name] = Workflow(name=name, rules=[])
            worflow = worflows[name]
            for rule in rules.split(","):
                m = re.search(r"^(([xmas])([<>])(\d+):)?(.+)$", rule)
                destination = m.group(5)
                if not worflows.get(destination, None):
                    worflows[destination] = Workflow(name=destination, rules=[])
                destination = worflows[destination]
                if m.group(1):
                    rule = Rule(destination=destination, condition=Condition(property=m.group(2), comparator=m.group(3), value=int(m.group(4))))
                else:
                    rule = Rule(destination=destination, condition=None) #Fallback rule
                worflow.rules.append(rule)        
        return worflows
    
    def _parse_parts(self, lines:list[str]) -> list["Part"]:
        parts = []
        for line in lines:
            part = Part()
            for m in re.finditer(r"([xmas])=(\d+)", line):
                property = m.group(1)
                value = int(m.group(2))
                if property == "x":
                    part.x = value
                elif property == "m":
                    part.m = value
                elif property == "a":
                    part.a = value
                elif property == "s":
                    part.s = value
            parts.append(part)
        return parts

    def _parse(self, input) -> Tuple[Dict[str, "Workflow"], list["Part"]]:
        block1, block2 = self.group_lines(self.input_to_lines(input))
        return (self._parse_workflows(block1), self._parse_parts(block2))

    def solve_part_1(self, input, args):        
        global debug
        debug = self.debug
        workflows, parts = self._parse(input)
        initial_workflow = workflows["in"]
        total = 0
        for part in parts:
            if self.debug:
                print(f"Part {part}")
            part_accepted = initial_workflow.accepts(part)
            if part_accepted:
                total += part.x + part.m + part.a + part.s
            if self.debug:
                print(f"Part {part} => {'A' if part_accepted else 'R'}")
            
        return total
    
    def _combinations_accepted(self, workflow:Workflow, combinations:Dict[str, range]) -> int:
        if workflow.name == "A":
            return prod([len(range) for range in combinations.values()])
        elif workflow.name == "R":
            return 0
        res = 0
        fallback = combinations.copy()
        for rule in workflow.rules:
            cond = rule.condition
            if rule.condition: 
                rule_combinations = fallback.copy()
                current = rule_combinations[cond.property]
                current_fallback = fallback[cond.property]
                if cond.comparator == "<":                                        
                    rule_combinations[cond.property] = range(current.start, min(current.stop, cond.value))
                    fallback[cond.property] = range(max(current_fallback.start, cond.value), current_fallback.stop)
                else:
                    rule_combinations[cond.property] = range(max(current.start, cond.value + 1), current.stop)
                    fallback[cond.property] = range(current_fallback.start, min(current_fallback.stop, cond.value + 1))
                r = self._combinations_accepted(rule.destination, rule_combinations)                
            else:
                r = self._combinations_accepted(rule.destination, fallback)
            res += r
        return res

        
    def solve_part_2(self, input, args):
        workflows, _ = self._parse(input)
        initial_workflow = workflows["in"]
        return self._combinations_accepted(initial_workflow, {"x": range(1, 4001), "m": range(1, 4001), "a": range(1, 4001), "s": range(1, 4001)})

if __name__ == '__main__':    
    day19 = Day19Solution()
    day19.run()