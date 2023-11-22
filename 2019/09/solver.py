from dataclasses import dataclass
from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


@dataclass
class BoostProgram(Bus):
    input: int
    output: Optional[int]

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return self.input

    @override
    def add_output(self, value: int) -> None:
        self.output = value


def main() -> None:
    answer.part1(3512778005, run(1))
    answer.part2(35920, run(2))


def run(setting: int) -> Optional[int]:
    program = BoostProgram(setting, None)
    Computer(bus=program, memory=Parser().int_csv()).run()
    return program.output


if __name__ == "__main__":
    main()
