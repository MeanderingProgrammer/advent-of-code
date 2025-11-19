from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Computer:
    instructions: list[Instruction]

    def execute(self) -> tuple[bool, int]:
        ip: int = 0
        acc: int = 0
        seen: set[int] = set()
        while ip not in seen:
            seen.add(ip)
            instruction = self.instructions[ip]
            match instruction.operation:
                case Operation.ACC:
                    ip += 1
                    acc += instruction.value
                case Operation.JMP:
                    ip += instruction.value
                case Operation.NOP:
                    ip += 1
            if len(self.instructions) == ip:
                return True, acc
        return False, acc

    def fix(self) -> int:
        for i in range(len(self.instructions)):
            self.instructions[i] = self.instructions[i].transform()
            success, acc = self.execute()
            if success:
                return acc
            self.instructions[i] = self.instructions[i].transform()
        raise Exception("Failed")


@dataclass(frozen=True)
class Instruction:
    operation: Operation
    value: int

    @classmethod
    def new(cls, s: str) -> Self:
        operation, raw = s.split()
        value = int(raw[1:])
        value = value * -1 if raw[0] == "-" else value
        return cls(Operation(operation), value)

    def transform(self) -> Self:
        return type(self)(self.operation.transform(), self.value)


class Operation(StrEnum):
    ACC = auto()
    JMP = auto()
    NOP = auto()

    def transform(self) -> Operation:
        match self:
            case Operation.ACC:
                return Operation.ACC
            case Operation.JMP:
                return Operation.NOP
            case Operation.NOP:
                return Operation.JMP


@answer.timer
def main() -> None:
    instructions = [Instruction.new(line) for line in Parser().lines()]
    computer = Computer(instructions)
    answer.part1(1744, computer.execute()[1])
    answer.part2(1174, computer.fix())


if __name__ == "__main__":
    main()
