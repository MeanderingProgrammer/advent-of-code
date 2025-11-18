from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Computer:
    registers: dict[str, int]

    def run(self, instructions: list[Instruction]) -> None:
        ip = 0
        while ip >= 0 and ip < len(instructions):
            move = 1
            instruction = instructions[ip]
            match instruction.operation:
                case Operation.HLF:
                    (x,) = instruction.args
                    self.set(x, self.get(x) // 2)
                case Operation.TPL:
                    (x,) = instruction.args
                    self.set(x, self.get(x) * 3)
                case Operation.INC:
                    (x,) = instruction.args
                    self.set(x, self.get(x) + 1)
                case Operation.JMP:
                    (x,) = instruction.args
                    move = int(x)
                case Operation.JIE:
                    (x, y) = instruction.args
                    if self.get(x) % 2 == 0:
                        move = int(y)
                case Operation.JIO:
                    (x, y) = instruction.args
                    if self.get(x) == 1:
                        move = int(y)
            ip += move

    def get(self, register: str) -> int:
        return self.registers[register]

    def set(self, register: str, value: int) -> None:
        self.registers[register] = value


@dataclass(frozen=True)
class Instruction:
    operation: Operation
    args: list[str]

    @classmethod
    def new(cls, s: str) -> Self:
        operation, args = s.split(" ", 1)
        return cls(Operation(operation), args.split(", "))


class Operation(StrEnum):
    HLF = auto()
    TPL = auto()
    INC = auto()
    JMP = auto()
    JIE = auto()
    JIO = auto()


@answer.timer
def main() -> None:
    instructions = [Instruction.new(line) for line in Parser().lines()]
    answer.part1(170, run(instructions, 0))
    answer.part2(247, run(instructions, 1))


def run(instructions: list[Instruction], a: int) -> int:
    computer = Computer(registers=dict(a=a, b=0))
    computer.run(instructions)
    return computer.get("b")


if __name__ == "__main__":
    main()
