from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Computer:

    def __init__(self, id, instructions):
        self.regs = defaultdict(int)
        self.regs['p'] = id

        self.instructions = instructions
        self.ip = 0

        self.sent = 0

        self.o = None
        self.q = []
        self.waiting = False

    def set_other(self, o):
        self.o = o

    def send(self, value):
        self.sent += 1
        self.o.q.append(value)
        self.o.waiting = False

    def get(self):
        if len(self.q) == 0:
            return None
        else:
            return self.q.pop(0)

    def run(self):
        while self.ip >= 0 and self.ip < len(self.instructions) and not self.waiting:
            instruction = self.instructions[self.ip]
            instruction.run(self)

        if self.waiting and not self.o.waiting:
            self.o.run()


class Intstruction:

    def __init__(self, value):
        parts = value.split()
        self.op = parts[0]
        self.args = parts[1:]

    def run(self, comp):
        if self.op == 'snd':
            comp.send(self.to_value(comp, self.args[0]))
            comp.ip += 1
        elif self.op == 'set':
            comp.regs[self.args[0]] = self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == 'add':
            comp.regs[self.args[0]] += self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == 'mul':
            comp.regs[self.args[0]] *= self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == 'mod':
            comp.regs[self.args[0]] %= self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == 'rcv':
            value = comp.get()
            if value is None:
                comp.waiting = True
            else:
                comp.regs[self.args[0]] = value
                comp.ip += 1
        elif self.op == 'jgz':
            if self.to_value(comp, self.args[0]) > 0:
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
    comp1 = Computer(0, get_instructions())
    comp2 = Computer(1, get_instructions())

    comp1.set_other(comp2)
    comp2.set_other(comp1)

    comp1.run()

    # Part 2 = 7620
    print(comp2.sent)


def get_instructions():
    instructions = []
    for line in Parser(FILE_NAME).lines():
        instructions.append(Intstruction(line))
    return instructions


if __name__ == '__main__':
    main()

