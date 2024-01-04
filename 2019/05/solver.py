from dataclasses import dataclass
from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


@dataclass
class BasicProgram(Bus):
    system_id: int
    diagnostic_code: Optional[int] = None

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return self.system_id

    @override
    def add_output(self, value: int) -> None:
        self.diagnostic_code = value


@answer.timer
def main() -> None:
    answer.part1(12234644, run_program(1))
    answer.part2(3508186, run_program(5))


def run_program(system_id: int) -> Optional[int]:
    program = BasicProgram(system_id)
    Computer(bus=program, memory=Parser().int_csv()).run()
    return program.diagnostic_code


if __name__ == "__main__":
    main()
