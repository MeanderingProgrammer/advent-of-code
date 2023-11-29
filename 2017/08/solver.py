from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from aoc import answer
from aoc.parser import Parser

Registers = dict[str, int]


def modifier(
    r_id: str, amount: int, f: Callable[[int, int], int]
) -> Callable[[Registers], None]:
    def result(registers: Registers) -> None:
        registers[r_id] = f(registers[r_id], amount)

    return result


MODIFIERS = {
    "inc": lambda r_id, value: modifier(r_id, value, lambda a, b: a + b),
    "dec": lambda r_id, value: modifier(r_id, value, lambda a, b: a - b),
}


def condition(
    r_id: str, value: int, f: Callable[[int, int], bool]
) -> Callable[[Registers], bool]:
    def result(registers: Registers) -> bool:
        return f(registers[r_id], value)

    return result


CONDITIONS = {
    ">": lambda r_id, value: condition(r_id, value, lambda a, b: a > b),
    "<": lambda r_id, value: condition(r_id, value, lambda a, b: a < b),
    "==": lambda r_id, value: condition(r_id, value, lambda a, b: a == b),
    "!=": lambda r_id, value: condition(r_id, value, lambda a, b: a != b),
    ">=": lambda r_id, value: condition(r_id, value, lambda a, b: a >= b),
    "<=": lambda r_id, value: condition(r_id, value, lambda a, b: a <= b),
}


@dataclass(frozen=True)
class Instruction:
    modifier: Callable[[Registers], None]
    condition: Callable[[Registers], bool]

    def apply(self, registers: dict[str, int]) -> None:
        if self.condition(registers):
            self.modifier(registers)


def main() -> None:
    registers: Registers = defaultdict(int)
    maxes: list[int] = []
    for instruction in get_instructions():
        instruction.apply(registers)
        maxes.append(max(registers.values()))
    answer.part1(7296, max(registers.values()))
    answer.part2(8186, max(maxes))


def get_instructions() -> list[Instruction]:
    def parse_instruction(line: str) -> Instruction:
        parts = line.split()
        return Instruction(
            modifier=MODIFIERS[parts[1]](parts[0], int(parts[2])),
            condition=CONDITIONS[parts[5]](parts[4], int(parts[6])),
        )

    return [parse_instruction(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
