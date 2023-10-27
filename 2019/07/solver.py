from itertools import permutations

from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser


class Amplifier:
    def __init__(self, memory, setting):
        self.computer = Computer(self)
        self.computer.set_memory(memory)

        self.inputs = [setting]

        self.outputs = []
        self.load = False

    def run(self, pause_on_load):
        self.load = False
        while self.computer.has_next() and self.check_load(pause_on_load):
            self.computer.next()
        return self.computer.has_next()

    def check_load(self, pause_on_load):
        if not pause_on_load:
            return True
        return not self.load

    def add_input(self, value):
        self.inputs.append(value)

    def get_output(self):
        return self.outputs[-1]

    def get_input(self):
        return self.inputs.pop(0)

    def add_output(self, value):
        self.load = True
        self.outputs.append(value)


def main():
    answer.part1(38834, run_permutations([0, 1, 2, 3, 4], False))
    answer.part2(69113332, run_permutations([5, 6, 7, 8, 9], True))


def run_permutations(sequence, pause_on_load):
    values = []
    for sequence in permutations(sequence):
        value = run_sequence(sequence, pause_on_load)
        values.append(value)
    return max(values)


def run_sequence(sequence, pause_on_load):
    output, state, amplifiers = 0, True, get_amplifiers(sequence)

    while state:
        for amplifier in amplifiers:
            amplifier.add_input(output)
            state &= amplifier.run(pause_on_load)
            output = amplifier.get_output()

    return output


def get_amplifiers(sequence):
    return [Amplifier(get_memory(), entry) for entry in sequence]


def get_memory():
    return Parser().int_csv()


if __name__ == "__main__":
    main()
