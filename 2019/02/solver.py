from aoc import answer
from aoc.intcode import Computer
from aoc.parser import Parser


class NoopBus:
    def active(self) -> bool:
        return True

    def get_input(self) -> int:
        return 0

    def add_output(self, value: int) -> None:
        pass


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    answer.part1(6627023, run(memory, 12, 2))
    answer.part2(4019, get_goal(memory))


def run(memory: list[int], v1: int, v2: int) -> int:
    memory = memory.copy()
    memory[1] = v1
    memory[2] = v2
    computer = Computer(NoopBus(), memory)
    computer.run()
    return memory[0]


def get_goal(memory: list[int]) -> int | None:
    for noun in range(100):
        for verb in range(100):
            if run(memory, noun, verb) == 19_690_720:
                return 100 * noun + verb
    return None


if __name__ == "__main__":
    main()
