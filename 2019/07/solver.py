from itertools import permutations
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


class Amplifier(Bus):
    def __init__(self, memory: list[int], setting: int, pause_on_load: bool):
        self.computer = Computer(bus=self, memory=memory)
        self.inputs = [setting]
        self.outputs = []
        self.load = False
        self.pause_on_load = pause_on_load

    def run(self) -> bool:
        self.load = False
        self.computer.run()
        return self.computer.has_next()

    @override
    def active(self) -> bool:
        if not self.pause_on_load:
            return True
        return not self.load

    @override
    def get_input(self) -> int:
        return self.inputs.pop(0)

    @override
    def add_output(self, value: int) -> None:
        self.load = True
        self.outputs.append(value)


@answer.timer
def main() -> None:
    answer.part1(38834, run_permutations([0, 1, 2, 3, 4], False))
    answer.part2(69113332, run_permutations([5, 6, 7, 8, 9], True))


def run_permutations(sequence: list[int], pause_on_load: bool) -> int:
    values = []
    for possibility in permutations(sequence):
        value = run_sequence(possibility, pause_on_load)
        values.append(value)
    return max(values)


def run_sequence(sequence: tuple[int, ...], pause_on_load: bool):
    amplifiers = [Amplifier(get_memory(), entry, pause_on_load) for entry in sequence]
    output, state = 0, True
    while state:
        for amplifier in amplifiers:
            amplifier.inputs.append(output)
            state &= amplifier.run()
            output = amplifier.outputs[-1]
    return output


def get_memory():
    return Parser().int_csv()


if __name__ == "__main__":
    main()
