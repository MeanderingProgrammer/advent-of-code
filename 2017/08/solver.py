from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser

type Registers = dict[str, int]
type Modifier = Callable[[Registers], None]
type Condition = Callable[[Registers], bool]


def modifier(id: str, value: int, f: Callable[[int, int], int]) -> Modifier:
    def result(registers: Registers) -> None:
        registers[id] = f(registers[id], value)

    return result


MODIFIERS: dict[str, Callable[[str, int], Modifier]] = {
    "inc": lambda id, value: modifier(id, value, lambda a, b: a + b),
    "dec": lambda id, value: modifier(id, value, lambda a, b: a - b),
}


def condition(id: str, value: int, f: Callable[[int, int], bool]) -> Condition:
    def result(registers: Registers) -> bool:
        return f(registers[id], value)

    return result


CONDITIONS: dict[str, Callable[[str, int], Condition]] = {
    ">": lambda id, value: condition(id, value, lambda a, b: a > b),
    "<": lambda id, value: condition(id, value, lambda a, b: a < b),
    "==": lambda id, value: condition(id, value, lambda a, b: a == b),
    "!=": lambda id, value: condition(id, value, lambda a, b: a != b),
    ">=": lambda id, value: condition(id, value, lambda a, b: a >= b),
    "<=": lambda id, value: condition(id, value, lambda a, b: a <= b),
}


@dataclass(frozen=True)
class Instruction:
    modifier: Callable[[Registers], None]
    condition: Callable[[Registers], bool]

    @classmethod
    def new(cls, s: str) -> Self:
        parts = s.split()
        return cls(
            modifier=MODIFIERS[parts[1]](parts[0], int(parts[2])),
            condition=CONDITIONS[parts[5]](parts[4], int(parts[6])),
        )

    def apply(self, registers: dict[str, int]) -> None:
        if self.condition(registers):
            self.modifier(registers)


@answer.timer
def main() -> None:
    instructions = [Instruction.new(line) for line in Parser().lines()]
    registers: Registers = defaultdict(int)
    maxes: list[int] = []
    for instruction in instructions:
        instruction.apply(registers)
        maxes.append(max(registers.values()))
    answer.part1(7296, max(registers.values()))
    answer.part2(8186, max(maxes))


if __name__ == "__main__":
    main()
