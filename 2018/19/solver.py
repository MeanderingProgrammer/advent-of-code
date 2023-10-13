from aoc import answer
from aoc.parser import Parser


class Parameter:
    def __init__(self, register):
        self.register = register

    def get(self, value, regs):
        return regs.get(value) if self.register else value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "r" if self.register else "i"


class Operator:
    def __init__(self, register, symbol, f):
        self.v1 = Parameter(True)
        self.v2 = Parameter(register)
        self.symbol = symbol
        self.f = f

    def process(self, instruction, regs):
        a = self.v1.get(instruction.one(), regs)
        b = self.v2.get(instruction.two(), regs)
        regs.set(instruction.three(), self.f(a, b))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{}{}".format(self.symbol, self.v2)


class Add(Operator):
    def __init__(self, register):
        super().__init__(register, "add", lambda x, y: x + y)


class Mult(Operator):
    def __init__(self, register):
        super().__init__(register, "mul", lambda x, y: x * y)


class And(Operator):
    def __init__(self, register):
        super().__init__(register, "ban", lambda x, y: x & y)


class Or(Operator):
    def __init__(self, register):
        super().__init__(register, "bor", lambda x, y: x | y)


class Set:
    def __init__(self, register):
        self.v1 = Parameter(register)

    def process(self, instruction, regs):
        value = self.v1.get(instruction.one(), regs)
        regs.set(instruction.three(), value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "set{}".format(self.v1)


class Comparison:
    def __init__(self, reg1, reg2, symbol, f):
        self.v1 = Parameter(reg1)
        self.v2 = Parameter(reg2)
        self.symbol = symbol
        self.f = f

    def process(self, instruction, regs):
        a = self.v1.get(instruction.one(), regs)
        b = self.v2.get(instruction.two(), regs)
        value = 1 if self.f(a, b) else 0
        regs.set(instruction.three(), value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{}{}{}".format(self.symbol, self.v1, self.v2)


class GreaterThan(Comparison):
    def __init__(self, reg1, reg2):
        super().__init__(reg1, reg2, "gt", lambda x, y: x > y)


class Equals(Comparison):
    def __init__(self, reg1, reg2):
        super().__init__(reg1, reg2, "eq", lambda x, y: x == y)


ALL_INSTRUCTIONS = {
    "addr": Add(True),
    "addi": Add(False),
    "mulr": Mult(True),
    "muli": Mult(False),
    "banr": And(True),
    "bani": And(False),
    "borr": Or(True),
    "bori": Or(False),
    "setr": Set(True),
    "seti": Set(False),
    "gtir": GreaterThan(False, True),
    "gtri": GreaterThan(True, False),
    "gtrr": GreaterThan(True, True),
    "eqir": Equals(False, True),
    "eqri": Equals(True, False),
    "eqrr": Equals(True, True),
}


class Registers:
    def __init__(self, size, ip):
        self.values = [0 for i in range(size)]
        self.ip = ip

    def instruction(self):
        return self.values[self.ip]

    def next(self):
        self.values[self.ip] += 1

    def set(self, index, value):
        self.values[index] = value

    def get(self, index):
        return self.values[index]

    def copy(self):
        return Registers([value for value in self.values], False)

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.values)


class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction.split()

    def opcode(self):
        return self.instruction[0]

    def one(self):
        return int(self.instruction[1])

    def two(self):
        return int(self.instruction[2])

    def three(self):
        return int(self.instruction[3])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.instruction)


def main():
    answer.part1(993, solve_part_1())
    answer.part2(10708912, solve_part_2(10_551_361))


def solve_part_1():
    pointer, instructions = get_instructions()
    regs = Registers(6, pointer)

    while regs.instruction() < len(instructions):
        instruction_index = regs.instruction()
        instruction = instructions[instruction_index]
        ALL_INSTRUCTIONS[instruction.opcode()].process(instruction, regs)
        regs.next()

    return regs.get(0)


def solve_part_2(value):
    # Reverse engineered code to figure out what it's calculating
    result = 0
    for i in range(1, value + 1):
        if value % i == 0:
            result += i
    return result


def get_instructions():
    lines = Parser().lines()
    pointer = int(lines[0].split()[1])
    instructions = [Instruction(line) for line in lines[1:]]
    return pointer, instructions


if __name__ == "__main__":
    main()
