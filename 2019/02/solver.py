from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


class NoopBus(Bus):
    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return 0

    @override
    def add_output(self, value: int) -> None:
        pass


@answer.timer
def main() -> None:
    answer.part1(6627023, run(12, 2))
    answer.part2(4019, get_goal())


def run(v1: int, v2: int) -> int:
    memory = Parser().int_csv()
    memory[1] = v1
    memory[2] = v2
    computer = Computer(NoopBus(), memory)
    computer.run()
    return memory[0]


def get_goal() -> Optional[int]:
    for noun in range(100):
        for verb in range(100):
            if run(noun, verb) == 19_690_720:
                return 100 * noun + verb
    return None


if __name__ == "__main__":
    main()
