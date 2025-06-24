from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


class Computer:
    def __init__(self, id: int, instructions: list["Instruction"]):
        self.regs: dict[str, int] = defaultdict(int)
        self.regs["p"] = id
        self.ip: int = 0
        self.instructions: list[Instruction] = instructions
        self.sent: int = 0
        self.o: list[int] | Self = []
        self.q: deque[int] = deque()
        self.waiting: bool = False

    def run(self) -> None:
        while self.has_next() and not self.waiting:
            instruction = self.instructions[self.ip]
            self.ip += instruction.run(self)

        if isinstance(self.o, Computer):
            if self.waiting and not self.o.waiting:
                self.o.run()

    def has_next(self) -> bool:
        return self.ip >= 0 and self.ip < len(self.instructions)

    def set_other(self, o: list[int] | Self) -> None:
        self.o = o

    def to_value(self, arg: str) -> int:
        if arg >= "a" and arg <= "z":
            return self.regs[arg]
        else:
            return int(arg)

    def send(self, value: int) -> None:
        self.sent += 1
        self.o.append(value)

    def append(self, value: int) -> None:
        self.q.append(value)
        self.waiting = False

    def get(self) -> int | None:
        if len(self.q) == 0:
            return None
        else:
            return self.q.popleft()


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


@answer.timer
def main() -> None:
    lines = Parser().lines()
    instructions = [parse_instruction(line) for line in lines]
    answer.part1(9423, part1(instructions))
    answer.part2(7620, part2(instructions))


def parse_instruction(line: str) -> Instruction:
    parts = line.split()
    return Instruction(op=parts[0], args=parts[1:])


def part1(instructions: list[Instruction]) -> int:
    added: list[int] = []
    comp = Computer(0, instructions)
    comp.set_other(added)
    comp.run()
    return added[-1]


def part2(instructions: list[Instruction]) -> int:
    comp1 = Computer(0, instructions)
    comp2 = Computer(1, instructions)
    comp1.set_other(comp2)
    comp2.set_other(comp1)
    comp1.run()
    return comp2.sent


if __name__ == "__main__":
    main()
