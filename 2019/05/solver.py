import commons.answer as answer
from commons.aoc_parser import Parser
from commons.int_code import Computer


class BasicProgram:

    def __init__(self, memory, system_id):
        self.computer = Computer(self)
        self.computer.set_memory(memory)
        self.system_id = system_id
        self.diagnostic_code = None

    def run(self):
        self.computer.run()

    def get_input(self):
        return self.system_id

    def add_output(self, value):
        self.diagnostic_code = value

def main():
    answer.part1(12234644, run_program(1))
    answer.part2(3508186, run_program(5))


def run_program(system_id):
    program = BasicProgram(get_memory(), system_id)
    program.run()
    return program.diagnostic_code


def get_memory():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
