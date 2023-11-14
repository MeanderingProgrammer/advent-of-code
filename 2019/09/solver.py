from dataclasses import dataclass
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


@dataclass
class BoostProgram(Bus):
    inputs: list[int]
    outputs: list[int]

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return self.inputs.pop(0)

    @override
    def add_output(self, value: int) -> None:
        self.outputs.append(value)


def main() -> None:
    answer.part1(3512778005, run(1))
    answer.part2(35920, run(2))


def run(setting: int) -> int:
    program = BoostProgram([setting], [])
    Computer(bus=program, memory=Parser().int_csv()).run()
    return program.outputs[0]


if __name__ == "__main__":
    main()
