from aoc_computer import Computer
from aoc_parser import Parser


FILE_NAME = 'data'


class Setter:

    def __init__(self, register, value, absolute):
        self.register = register
        self.value = value
        self.absolute = absolute

    def run(self, computer):
        value = computer.get(self.value)
        value = value if self.absolute else computer.get(self.register) + value
        computer.set(self.register, value)
        computer.move(1)


class Jump:

    def __init__(self, register, value):
        self.register = register
        self.value = value

    def run(self, computer):
        if computer.get(self.register) != 0:
            computer.move(computer.get(self.value))
        else:
            computer.move(1)


def main():
    # Part 1: 318117
    print('Part 1: {}'.format(run_instructions(False)))
    # Part 2: 9227771
    print('Part 2: {}'.format(run_instructions(True)))


def run_instructions(ignite):
    computer = Computer(['a', 'b', 'c', 'd'])
    if ignite:
        computer.set('c', 1)
    computer.run(get_instructions())
    return computer.get('a')


def get_instructions():
    instructions = []
    for line in Parser(FILE_NAME).lines():
        parts = line.split()
        op = parts[0]
        if op == 'cpy':
            instruction = Setter(parts[2], parts[1], True)
        elif op == 'inc':
            instruction = Setter(parts[1], '1', False)
        elif op == 'dec':
            instruction = Setter(parts[1], '-1', False)
        elif op == 'jnz':
            instruction = Jump(parts[1], parts[2])
        else:
            raise Exception('Unknown operation: {}'.format(op))
        instructions.append(instruction)
    return instructions


if __name__ == '__main__':
    main()
