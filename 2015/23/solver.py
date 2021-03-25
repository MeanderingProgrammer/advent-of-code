from aoc_computer import Computer
from aoc_parser import Parser


FILE_NAME = 'data'


class Instruction:

    def __init__(self, raw):
        self.op, args = raw.split(' ', 1)
        self.args = [arg for arg in args.split(', ')]

    def run(self, computer):
        if self.op == 'hlf':
            current = computer.get(self.args[0])
            computer.set(self.args[0], current // 2)
            computer.move(1)
        elif self.op == 'tpl':
            current = computer.get(self.args[0])
            computer.set(self.args[0], current * 3)
            computer.move(1)
        elif self.op == 'inc':
            current = computer.get(self.args[0])
            computer.set(self.args[0], current + 1)
            computer.move(1)
        elif self.op == 'jmp':
            amount = int(self.args[0])
            computer.move(amount)
        elif self.op == 'jie':
            current = computer.get(self.args[0])
            amount = int(self.args[1])
            amount = amount if current % 2 == 0 else 1
            computer.move(amount)
        elif self.op == 'jio':
            current = computer.get(self.args[0])
            amount = int(self.args[1])
            amount = amount if current == 1 else 1
            computer.move(amount)
        else:
            raise Exception('Unknown operation: {}'.format(self.op))


def main():
    # Part 1: 170
    print('Part 1: {}'.format(run_computer(False)))
    # Part 2: 247
    print('Part 2: {}'.format(run_computer(True)))


def run_computer(set_a):
    computer = Computer(['a', 'b'])
    if set_a:
        computer.set('a', 1)
    instructions = get_instructions()
    computer.run(instructions)
    return computer.get('b')


def get_instructions():
    return [Instruction(line) for line in Parser(FILE_NAME).lines()]


if __name__ == '__main__':
    main()
