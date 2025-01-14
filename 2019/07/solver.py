from itertools import permutations
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


class Amplifier(Bus):
    def __init__(self, memory: list[int], setting: int, pause: bool):
        self.computer = Computer(bus=self, memory=memory)
        self.inputs = [setting]
        self.outputs = []
        self.load = False
        self.pause = pause

    def run(self) -> bool:
        self.load = False
        self.computer.run()
        return not self.active()

    @override
    def active(self) -> bool:
        return not self.pause or not self.load

    @override
    def get_input(self) -> int:
        return self.inputs.pop(0)

    @override
    def add_output(self, value: int) -> None:
        self.load = True
        self.outputs.append(value)


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    answer.part1(38834, run(memory, [0, 1, 2, 3, 4], False))
    answer.part2(69113332, run(memory, [5, 6, 7, 8, 9], True))


def run(memory: list[int], sequence: list[int], pause: bool) -> int:
    values = []
    for possibility in permutations(sequence):
        value = check(memory, possibility, pause)
        values.append(value)
    return max(values)


def check(memory: list[int], sequence: tuple[int, ...], pause: bool) -> int:
    amplifiers = [Amplifier(memory.copy(), entry, pause) for entry in sequence]
    output, state = 0, True
    while state:
        for amplifier in amplifiers:
            amplifier.inputs.append(output)
            state &= amplifier.run()
            output = amplifier.outputs[-1]
    return output


if __name__ == "__main__":
    main()
