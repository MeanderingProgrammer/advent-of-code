from commons.aoc_parser import Parser


class Parameter:

    def __init__(self, register):
        self.register = register

    def get(self, value, regs):
        return regs.get(value) if self.register else value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'r' if self.register else 'i'


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
        return '{}{}'.format(self.symbol, self.v2)


class Add(Operator):

    def __init__(self, register):
        super().__init__(register, 'add', lambda x, y: x + y)


class Mult(Operator):

    def __init__(self, register):
        super().__init__(register, 'mul', lambda x, y: x * y)


class And(Operator):

    def __init__(self, register):
        super().__init__(register, 'ban', lambda x, y: x & y)


class Or(Operator):

    def __init__(self, register):
        super().__init__(register, 'bor', lambda x, y: x | y)


class Set:

    def __init__(self, register):
        self.v1 = Parameter(register)

    def process(self, instruction, regs):
        value = self.v1.get(instruction.one(), regs)
        regs.set(instruction.three(), value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'set{}'.format(self.v1)


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
        return '{}{}{}'.format(self.symbol, self.v1, self.v2)


class GreaterThan(Comparison):

    def __init__(self, reg1, reg2):
        super().__init__(reg1, reg2, 'gt', lambda x, y: x > y)


class Equals(Comparison):

    def __init__(self, reg1, reg2):
        super().__init__(reg1, reg2, 'eq', lambda x, y: x == y)


ALL_INSTRUCTIONS = {
    'addr': Add(True),                  
    'addi': Add(False),                 
    'mulr': Mult(True),                 
    'muli': Mult(False),                
    'banr': And(True),                  
    'bani': And(False),                 
    'borr': Or(True),
    'bori': Or(False),
    'setr': Set(True),
    'seti': Set(False),
    'gtir': GreaterThan(False, True),
    'gtri': GreaterThan(True, False), 
    'gtrr': GreaterThan(True, True),
    'eqir': Equals(False, True),
    'eqri': Equals(True, False),
    'eqrr': Equals(True, True)
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
    halt_values = run_analyzed()
    # Part 1: 6619857
    print('Part 1: {}'.format(halt_values[0]))
    # Part 2: 9547924
    print('Part 2: {}'.format(halt_values[-1]))


def run_analyzed():
    current_value, seen = run_inner(0), []
    while current_value not in seen:
        seen.append(current_value)
        current_value = run_inner(current_value)
    return seen


def run_inner(previous):
    # https://github.com/marcodelmastro/AdventOfCode2018/blob/master/Day%2021.ipynb
    counter = previous | 65536
    value = 9010242

    while counter > 0:
        value += counter & 255
        value &= 16777215
        value *= 65899
        value &= 16777215
        counter //= 256

    return value


def run_real(until_first):
    # This should produce the same result as run_analyzed, but is
    # way slower as it actually runs each instruction
    pointer, instructions = get_instructions()
    regs = Registers(6, pointer)

    seen, previous = set(), None

    while regs.instruction() < len(instructions):
        instruction_index = regs.instruction()
        instruction = instructions[instruction_index]
        ALL_INSTRUCTIONS[instruction.opcode()].process(instruction, regs)
        regs.next()

        # 28th instruction compares register 0 to register 5. If they
        # are equal then the program will halt.
        # Since nothing else modifies or uses register 0 we need to
        # keep track of the register 5 values.
        # Once we start repeating we know the last unrepeated value is 
        # what causes the largest number of instructions to run and 
        # still halt the program.
        if instruction_index == 28:
            value = regs.get(5)

            if until_first:
                return value
            
            if value in seen:
                return previous
            else:
                seen.add(value)
                previous = value


def get_instructions():
    lines = Parser().lines()
    pointer = int(lines[0].split()[1])
    instructions = [Instruction(line) for line in lines[1:]]
    return pointer, instructions


if __name__ == '__main__':
    main()
