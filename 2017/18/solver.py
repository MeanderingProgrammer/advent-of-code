from aoc import answer
from aoc.parser import Parser
from collections import defaultdict


class Computer:
    def __init__(self, id, instructions):
        self.regs = defaultdict(int)
        self.regs["p"] = id

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
        self.o.append(value)

    def append(self, value):
        self.q.append(value)
        self.waiting = False

    def get(self):
        if len(self.q) == 0:
            return None
        else:
            return self.q.pop(0)

    def run(self):
        while self.ip >= 0 and self.ip < len(self.instructions) and not self.waiting:
            instruction = self.instructions[self.ip]
            instruction.run(self)

        if isinstance(self.o, Computer):
            if self.waiting and not self.o.waiting:
                self.o.run()


class Instruction:
    def __init__(self, value):
        parts = value.split()
        self.op = parts[0]
        self.args = parts[1:]

    def run(self, comp):
        if self.op == "snd":
            comp.send(self.to_value(comp, self.args[0]))
            comp.ip += 1
        elif self.op == "set":
            comp.regs[self.args[0]] = self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == "add":
            comp.regs[self.args[0]] += self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == "mul":
            comp.regs[self.args[0]] *= self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == "mod":
            comp.regs[self.args[0]] %= self.to_value(comp, self.args[1])
            comp.ip += 1
        elif self.op == "rcv":
            value = comp.get()
            if value is None:
                comp.waiting = True
            else:
                comp.regs[self.args[0]] = value
                comp.ip += 1
        elif self.op == "jgz":
            if self.to_value(comp, self.args[0]) > 0:
                comp.ip += self.to_value(comp, self.args[1])
            else:
                comp.ip += 1
        else:
            raise Exception("Unknown operation: {}".format(self.op))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{}: {}".format(self.op, self.args)

    @staticmethod
    def to_value(comp, arg):
        try:
            return int(arg)
        except ValueError:
            return comp.regs[arg]


def main():
    answer.part1(9423, run_1_computers())
    answer.part2(7620, run_2_computers())


def run_1_computers():
    added = []
    comp = Computer(0, get_instructions())
    comp.set_other(added)
    comp.run()
    return added[-1]


def run_2_computers():
    comp1 = Computer(0, get_instructions())
    comp2 = Computer(1, get_instructions())

    comp1.set_other(comp2)
    comp2.set_other(comp1)

    comp1.run()

    return comp2.sent


def get_instructions():
    return [Instruction(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
