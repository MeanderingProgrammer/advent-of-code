from dataclasses import dataclass

from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser


@dataclass
class BoostProgram:
    input: int
    output: int | None

    def active(self) -> bool:
        return True

    def get_input(self) -> int:
        return self.input

    def add_output(self, value: int) -> None:
        self.output = value


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    answer.part1(3512778005, run(memory, 1))
    answer.part2(35920, run(memory, 2))


def run(memory: list[int], input: int) -> int | None:
    program = BoostProgram(input, None)
    Computer(bus=program, memory=memory.copy()).run()
    return program.output


if __name__ == "__main__":
    main()
