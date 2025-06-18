from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class Transition:
    next_state: str
    write_symbol: str
    direction: str  # 'L', 'R', or 'N'

class TuringMachine:
    """A simple deterministic Turing machine implementation."""
    def __init__(self, transitions: Dict[Tuple[str, str], Transition],
                 start_state: str, blank_symbol: str = ' '):
        self.transitions = transitions
        self.state = start_state
        self.blank_symbol = blank_symbol
        self.tape = {}
        self.head = 0

    def load_tape(self, input_string: str):
        self.tape = {i: ch for i, ch in enumerate(input_string)}
        self.head = 0

    def _read(self) -> str:
        return self.tape.get(self.head, self.blank_symbol)

    def _write(self, symbol: str):
        if symbol == self.blank_symbol:
            self.tape.pop(self.head, None)
        else:
            self.tape[self.head] = symbol

    def step(self):
        symbol = self._read()
        key = (self.state, symbol)
        if key not in self.transitions:
            raise RuntimeError(f"No transition defined for state {self.state} reading '{symbol}'")
        transition = self.transitions[key]
        self._write(transition.write_symbol)
        self.state = transition.next_state
        if transition.direction == 'L':
            self.head -= 1
        elif transition.direction == 'R':
            self.head += 1
        # 'N' means no movement

    def run(self, max_steps: int = 1000) -> str:
        for _ in range(max_steps):
            if self.state == 'halt':
                break
            self.step()
        return self.get_tape()

    def get_tape(self) -> str:
        if not self.tape:
            return ''
        min_index = min(self.tape)
        max_index = max(self.tape)
        return ''.join(self.tape.get(i, self.blank_symbol) for i in range(min_index, max_index + 1))


if __name__ == "__main__":
    # Example: increment a binary number stored on the tape
    transitions = {
        ('s0', '0'): Transition('s0', '0', 'R'),
        ('s0', '1'): Transition('s0', '1', 'R'),
        ('s0', ' '): Transition('s1', ' ', 'L'),
        ('s1', '1'): Transition('s1', '0', 'L'),
        ('s1', '0'): Transition('halt', '1', 'N'),
        ('s1', ' '): Transition('halt', '1', 'N'),
    }
    machine = TuringMachine(transitions, 's0')
    machine.load_tape('1011')
    print("Before:", machine.get_tape())
    result = machine.run()
    print("After :", result)
