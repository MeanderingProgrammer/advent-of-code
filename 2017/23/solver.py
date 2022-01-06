from collections import defaultdict

import commons.answer as answer
from commons.aoc_parser import Parser


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
    answer.part1(9409, run_computer(False))
    # run_computer(True) would take too long to run
    answer.part2(913, count_non_primes(109_900, 126_900, 17))


def run_computer(debug):
    comp = Computer(get_instructions(), debug)
    comp.run()
    return comp.multiplies


def count_non_primes(start, end, step):
    non_primes = 0
    for value in range(start, end + 1, step):
        if not is_prime(value):
            non_primes += 1
    return non_primes


def is_prime(value):
    for i in range(2, value):
        if value % i == 0:
            return False
    return True


def get_instructions():
    return [Intstruction(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
