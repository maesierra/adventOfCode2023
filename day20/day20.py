from doctest import debug
import os
import re
import sys
from typing import Dict, List, Tuple


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from advent_of_code import Solution

class Board():
    def __init__(self, low_pulses:int = 0, high_pulses:int = 0, modules:Dict[str, "Module"] = {}, queue:List[Tuple[bool, "Module", "Module"]] = []) -> None:
        self.low_pulses = low_pulses
        self.high_pulses = high_pulses
        self.modules = modules       
        self.queue = queue
        self.history = {}

    def add_module(self, module:"Module"):
        self.modules[module.name] = module
        self.history[module.name] = {'low': 0, 'high': 0}
        module.board = self

    def push_button(self):
        self.low_pulses += 1
        self.modules["broadcaster"].receive(pulse=False, input=None)
        while self.queue:            
            pulse, from_module, to_module = self.queue.pop(0)
            to_module.receive(pulse=pulse, input=from_module)
            if pulse:
                self.high_pulses += 1
            else: 
                self.low_pulses += 1
            self.history[to_module.name]['high' if pulse else 'low'] += 1            

    def state(self) -> str:
        return [m.state() for m in self.modules.values()]
    
    def connect(self, src:str, dest:str):
        src_module = self.modules.get(src, None)
        dest_module = self.modules.get(dest, None)
        if not src_module:
            return
        if not dest_module:
            dest_module = Module(name=dest, inputs=[], outputs=[], board=None)
            self.add_module(dest_module)

        src_module.add_output(dest_module)
        dest_module.add_input(src_module)

    def send_pulse(self, pulse:bool, from_module:"Module", to_module:"Module"):
        self.queue.append((pulse, from_module, to_module))



class Module():
    def __init__(self, name:str, inputs:list["Module"]=[], outputs:list["Module"]=[], board:Board = None) -> None:
        self.outputs = outputs
        self.inputs = inputs
        self.name = name
        self.board = board

    def send(self, pulse:bool):
        global debug
        for module in self.outputs:
            if debug:
                print(f"{'high' if pulse else 'low'} pulse from {self.name} to {module.name}")            
            self.board.send_pulse(pulse=pulse, from_module=self, to_module=module)

    def receive(self, input:"Module", pulse:bool):
        pass

    def state(self) -> str:
        return ""
    
    def add_output(self, output:"Module"):
        self.outputs.append(output)

    def add_input(self, input:"Module"):
        self.inputs.append(input)

class Broadcast(Module):
    def __init__(self, name:str, inputs:list["Module"]=[], outputs:list["Module"]=[]) -> None:
        super().__init__(name=name, inputs=inputs, outputs=outputs)

    def receive(self, input:"Module", pulse:bool):
        self.send(pulse)

class FlipFlow(Module):
    def __init__(self, name:str,inputs:list["Module"]=[], outputs:list["Module"]=[]) -> None:
        super().__init__(name=name, inputs=inputs, outputs=outputs)
        self.on = False
    
    def receive(self, input:"Module", pulse:bool):
        # ignores high pulses
        if pulse:
            return
        else:
            # Invert
            self.on = not self.on
            self.send(self.on)

    def state(self) -> str:
        return f"{self.name}:{'on' if self.on else 'off'}"

class Conjunction(Module):
    def __init__(self, name:str,inputs:list["Module"]=[], outputs:list["Module"]=[]) -> None:
        super().__init__(name=name, inputs=inputs, outputs=outputs)
        self.memory = [0 for i in inputs]

    def receive(self, input:"Module", pulse:bool):
        for i, module in enumerate(self.inputs):
            if input == module:
                self.memory[i] = 1 if pulse else 0

        if sum(self.memory) == len(self.memory):
            self.send(pulse=False)
        else:
            self.send(pulse=True)
    def add_input(self, input:"Module"):
        super().add_input(input)
        self.memory.append(0)
        
    def state(self) -> str:
        return f"{self.name}:{','.join([str(i) for i in self.memory])}"

class Day20Solution(Solution): 
    def __init__(self) -> None:
        super().__init__(20)

    def _parse_board(self, input) -> Board:
        board = Board(low_pulses=0, high_pulses=0, modules={}, queue=[])
        lines = self.input_to_lines(input)
        connections = {}
        for l in lines:
            m = re.search(r"^([%&]?)(.*) -> (.*)$", l)
            module_name = m.group(2)
            module_type = m.group(1)
            if module_type == "%":
                module = FlipFlow(name=module_name, inputs=[], outputs=[])
            elif module_type == "&":
                module = Conjunction(name=module_name, inputs=[], outputs=[])
            elif module_name == "broadcaster":
                module = Broadcast(name=module_name, inputs=[], outputs=[])
            board.add_module(module)
            connections[module_name] = m.group(3).split(", ")

        for module, connections in connections.items():
            for connected_to in connections:            
                board.connect(module, connected_to)
        
        return board
    
    def _send_button_pushes(self, board:Board, n_button_pushes:int) -> int:
        prev_states = {}
        prev_pulses = []
        n_button_pushes = n_button_pushes
        for n_push in range(0, n_button_pushes):
            key = "|".join(board.state())
            if self.debug:
                print(f"State before {n_push} {key}")
            found = prev_states.get(key, None)
            if found != None:
                cycle_start = found
                cycle_size = n_push - cycle_start
                cycle_low_pulses = board.low_pulses - prev_pulses[found][0]
                cycle_high_pulses = board.high_pulses - prev_pulses[found][1]
                n_loops = int(n_button_pushes / cycle_size)
                offset = (n_button_pushes  - cycle_start) % cycle_size
                extra_low = prev_pulses[cycle_start + offset][0] - prev_pulses[cycle_start][0]
                extra_high = prev_pulses[cycle_start + offset][1] - prev_pulses[cycle_start][1]
                low_pulses = n_loops * cycle_low_pulses + extra_low
                high_pulses = n_loops * cycle_high_pulses + extra_high
                return low_pulses * high_pulses
            prev_states[key] = n_push
            prev_pulses.append((board.low_pulses, board.high_pulses))
            board.push_button()
        return board.low_pulses * board.high_pulses

    def solve_part_1(self, input, args):
        global debug
        debug = self.debug
        board = self._parse_board(input)
        return self._send_button_pushes(board, 1000)
    
    def solve_part_2(self, input, args):
        global debug
        debug = self.debug
        board = self._parse_board(input)
        self._send_button_pushes(board, 1000000)
        print(board.history)
        return 2

if __name__ == '__main__':    
    day20 = Day20Solution()
    day20.run()