from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


class Computer:
    def __init__(self, id: int, instructions):
        self.regs = defaultdict(int)
        self.regs["p"] = id
        self.ip = 0
        self.instructions = instructions
        self.sent = 0
        self.o = []
        self.q = []
        self.waiting = False

    def set_other(self, o) -> None:
        self.o = o

    def to_value(self, arg: str) -> int:
        try:
            return int(arg)
        except ValueError:
            return self.regs[arg]

    def send(self, value: int) -> None:
        self.sent += 1
        self.o.append(value)

    def append(self, value: int) -> None:
        self.q.append(value)
        self.waiting = False

    def get(self) -> Optional[int]:
        if len(self.q) == 0:
            return None
        else:
            return self.q.pop(0)

    def run(self) -> None:
        while self.ip >= 0 and self.ip < len(self.instructions) and not self.waiting:
            instruction = self.instructions[self.ip]
            self.ip += instruction.run(self)

        if isinstance(self.o, Computer):
            if self.waiting and not self.o.waiting:
                self.o.run()


@dataclass(frozen=True)
class Instruction:
    op: str
    args: list[str]

    def run(self, comp: Computer) -> int:
        if self.op == "snd":
            comp.send(comp.to_value(self.args[0]))
            return 1
        elif self.op == "set":
            comp.regs[self.args[0]] = comp.to_value(self.args[1])
            return 1
        elif self.op == "add":
            comp.regs[self.args[0]] += comp.to_value(self.args[1])
            return 1
        elif self.op == "mul":
            comp.regs[self.args[0]] *= comp.to_value(self.args[1])
            return 1
        elif self.op == "mod":
            comp.regs[self.args[0]] %= comp.to_value(self.args[1])
            return 1
        elif self.op == "rcv":
            value = comp.get()
            if value is None:
                comp.waiting = True
                return 0
            else:
                comp.regs[self.args[0]] = value
                return 1
        elif self.op == "jgz":
            if comp.to_value(self.args[0]) > 0:
                return comp.to_value(self.args[1])
            else:
                return 1
        else:
            raise Exception(f"Unknown operation: {self.op}")


def main() -> None:
    answer.part1(9423, run_1_computers())
    answer.part2(7620, run_2_computers())


def run_1_computers() -> int:
    added: list[int] = []
    comp = Computer(0, get_instructions())
    comp.set_other(added)
    comp.run()
    return added[-1]


def run_2_computers() -> int:
    comp1 = Computer(0, get_instructions())
    comp2 = Computer(1, get_instructions())
    comp1.set_other(comp2)
    comp2.set_other(comp1)
    comp1.run()
    return comp2.sent


def get_instructions() -> list[Instruction]:
    def parse_instruction(line: str) -> Instruction:
        parts = line.split()
        return Instruction(op=parts[0], args=parts[1:])

    return [parse_instruction(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
