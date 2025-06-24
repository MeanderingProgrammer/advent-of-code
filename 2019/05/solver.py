from dataclasses import dataclass
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


@dataclass
class BasicProgram(Bus):
    system_id: int
    diagnostic_code: int | None = None

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
    memory = Parser().int_csv()
    answer.part1(12234644, run_program(memory, 1))
    answer.part2(3508186, run_program(memory, 5))


def run_program(memory: list[int], system_id: int) -> int | None:
    program = BasicProgram(system_id)
    Computer(bus=program, memory=memory.copy()).run()
    return program.diagnostic_code


if __name__ == "__main__":
    main()
