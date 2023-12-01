from dataclasses import dataclass
from typing import Any

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Acc:
    value: int

    def execute(self) -> tuple[int, int]:
        return 1, self.value

    def transform(self) -> Any:
        return self


@dataclass(frozen=True)
class Jmp:
    value: int

    def execute(self) -> tuple[int, int]:
        return self.value, 0

    def transform(self) -> Any:
        return Nop(self.value)


@dataclass(frozen=True)
class Nop:
    value: int

    def execute(self) -> tuple[int, int]:
        return 1, 0

    def transform(self) -> Any:
        return Jmp(self.value)


@dataclass(frozen=True)
class Computer:
    instructions: list[Any]

    def execute(self) -> tuple[bool, int]:
        ip: int = 0
        acc: int = 0
        seen: set[int] = set()
        while ip not in seen:
            seen.add(ip)
            move, amount = self.instructions[ip].execute()
            ip += move
            acc += amount
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


def main() -> None:
    computer = get_computer()
    answer.part1(1744, computer.execute()[1])
    answer.part2(1174, computer.fix())


def get_computer() -> Computer:
    def parse_int(raw: str) -> int:
        value = int(raw[1:])
        return value * -1 if raw[0] == "-" else value

    def parse_instruction(line: str) -> Any:
        opcode, raw_value = line.split()
        value = parse_int(raw_value)
        if opcode == "acc":
            return Acc(value)
        elif opcode == "jmp":
            return Jmp(value)
        elif opcode == "nop":
            return Nop(value)
        else:
            raise Exception("Failed")

    return Computer(instructions=list(map(parse_instruction, Parser().lines())))


if __name__ == "__main__":
    main()
