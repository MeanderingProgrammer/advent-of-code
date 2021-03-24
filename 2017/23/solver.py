from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


class Computer:

    def __init__(self, instructions, debug):
        self.regs = defaultdict(int)

        if debug:
            self.regs['a'] = 1

        self.instructions = instructions
        self.ip = 0

        self.multiplies = 0

    def run(self):
        while self.ip >= 0 and self.ip < len(self.instructions):
            instruction = self.instructions[self.ip]
            instruction.run(self)


class Intstruction:

    def __init__(self, value):
        parts = value.split()
        self.op = parts[0]
        self.args = parts[1:]

    def run(self, comp):
        if self.op == 'set':
            comp.regs[self.args[0]] = self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == 'sub':
            comp.regs[self.args[0]] -= self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == 'mul':
            comp.regs[self.args[0]] *= self.to_value(comp, self.args[1])
            comp.ip += 1
            comp.multiplies += 1
        elif self.op == 'jnz':
            if self.to_value(comp, self.args[0]) != 0:
                comp.ip += self.to_value(comp, self.args[1])
            else:
                comp.ip += 1
        else:
            raise Exception('Unknown operation: {}'.format(self.op))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.op, self.args)

    @staticmethod
    def to_value(comp, arg):
        try:
            return int(arg)
        except ValueError:
            return comp.regs[arg]


def main():
    # Part 1 = 9409
    run_computer(False)
    # Part 2 = 913
    #run_computer(True) -> Would take too long to run
    count_non_primes(109_900, 126_900, 17)


def run_computer(debug):
    comp = Computer(get_instructions(), debug)
    comp.run()
    print('Multiplies = {}'.format(comp.multiplies))
    print('Value at register h = {}'.format(comp.regs['h']))


def count_non_primes(start, end, step):
    non_primes = 0
    for value in range(start, end + 1, step):
        if not is_prime(value):
            non_primes += 1
    print(non_primes)


def is_prime(value):
    for i in range(2, value):
        if value % i == 0:
            return False
    return True


def get_instructions():
    instructions = []
    for line in Parser(FILE_NAME).lines():
        instructions.append(Intstruction(line))
    return instructions


if __name__ == '__main__':
    main()

