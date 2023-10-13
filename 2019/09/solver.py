from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser


class BoostProgram:
    def __init__(self, memory, setting):
        self.computer = Computer(self)
        self.computer.set_memory(memory)

        self.inputs = [setting]
        self.outputs = []

    def run(self):
        self.computer.run()

    def get_output(self):
        return self.outputs[0]

    def get_input(self):
        return self.inputs.pop(0)

    def add_output(self, value):
        self.load = True
        self.outputs.append(value)


def main():
    answer.part1(3512778005, run(1))
    answer.part2(35920, run(2))


def run(setting):
    program = get_program(setting)
    program.run()
    return program.get_output()


def get_program(param):
    return BoostProgram(get_memory(), param)


def get_memory():
    return Parser().int_csv()


if __name__ == "__main__":
    main()
