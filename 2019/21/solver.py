import commons.answer as answer
from commons.aoc_parser import Parser
from commons.int_code import Computer


class JumpDroid:

    def __init__(self, actual_program):
        self.__computer = Computer(self)
        self.__program = self.__transform(actual_program)
        self.buffer = ''
        self.value = None

    def set_memory(self, memory):
        self.__computer.set_memory(memory)

    def run(self):
        self.__computer.run()

    def get_input(self):
        self.buffer = ''
        value = self.__program.pop(0)
        return ord(value)

    def add_output(self, value):
        if value < 256:
            self.buffer += chr(value)
        else:
            self.value = value

    @staticmethod
    def __transform(actual_program):
        program = []
        for instruction in actual_program:
            real = [value for value in instruction]
            real.append('\n')
            program.extend(real)
        return program


def main():
    answer.part1(19357761, run_droid([
        # If one ahead is missing always Jump
        'NOT A J',
        # If 3 ahead is missing
        'NOT C T',
        'OR T J',
        # If 2 ahead is missing
        'NOT B T',
        'OR T J',
        # Must always have thing 4 tiles ahead
        'AND D J',
        # Force T to False
        'NOT A T',
        'AND A T',
        # Start the script
        'WALK'
    ]))

    answer.part2(1142249706, run_droid([
        # If one ahead is missing always Jump
        'NOT A J',
        # If 3 ahead is missing
        'NOT C T',
        'OR T J',
        # If 2 ahead is missing
        'NOT B T',
        'OR T J',
        # Must always have thing 4 tiles ahead
        'AND D J',
        # Force T to False
        'NOT A T',
        'AND A T',
        # If after we land is blank
        'OR E T',
        'OR H T',
        'AND T J',
        # Start the script
        'RUN'
    ]))


def run_droid(actual_program):
    droid = JumpDroid(actual_program)
    droid.set_memory(get_memory())
    droid.run()
    return droid.value


def get_memory():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
