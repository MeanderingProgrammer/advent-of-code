from computer import Computer

DEBUG = False


class JumpDroid:

    def __init__(self, finish):
        self.__computer = Computer(self, DEBUG)
        actual_program = [
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
            finish
        ]
        self.__program = self.__transform(actual_program)
        self.buffer = ''
        self.value = None

    def set_memory(self, memory):
        self.__computer.set_memory(memory)

    def run(self):
        while self.__computer.has_next():
            self.__computer.next()

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
    #solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 19357761
    droid = JumpDroid('WALK')
    droid.set_memory(get_memory())
    droid.run()
    print('Final value = {}'.format(droid.value))


def solve_part_2():
    # Part 2 = 1142249706
    droid = JumpDroid('RUN')
    droid.set_memory(get_memory())
    droid.run()
    print('Final value = {}'.format(droid.value))


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
