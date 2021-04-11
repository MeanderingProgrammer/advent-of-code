from commons.aoc_parser import Parser
from commons.int_code import Computer


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
    # Part 1: 3512778005
    print('Part 1: {}'.format(run(1)))
    # Part 2: 35920
    print('Part 2: {}'.format(run(2)))


def run(setting):
    program = get_program(setting)
    program.run()
    return program.get_output()


def get_program(param):
    return BoostProgram(get_memory(), param)


def get_memory():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
