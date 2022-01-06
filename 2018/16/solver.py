import commons.answer as answer
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

    def __init__(self, values, parse=True):
        self.values = [int(part) for part in values.split(', ')] if parse else values

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
        self.instruction = [int(part) for part in instruction.split()]

    def opcode(self):
        return self.instruction[0]

    def one(self):
        return self.instruction[1]

    def two(self):
        return self.instruction[2]

    def three(self):
        return self.instruction[3]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.instruction)


class SampleInstruction:

    def __init__(self, parts):
        self.before = Registers(parts[0].split(' [')[1][:-1])
        self.instruction = Instruction(parts[1])
        self.after = Registers(parts[2].split(' [')[1][:-1])

    def opcode(self):
        return self.instruction.opcode()

    def test_all(self):
        meets = set()
        for instruction in ALL_INSTRUCTIONS.values():
            before_copy = self.before.copy()
            instruction.process(self.instruction, before_copy)
            if before_copy == self.after:
                meets.add(str(instruction))
        return meets

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = [
            'Before: {}'.format(self.before),
            '{}'.format(self.instruction),
            'After: {}'.format(self.after)
        ]
        return '\n'.join(result)


def main():
    groups = Parser().line_groups()
    instructions = get_sample_instructions(groups)

    mapping, behave_as_at_least_3 = {}, 0
    for instruction in instructions:
        opcode = instruction.opcode()
        possible = instruction.test_all()
        if len(possible) >= 3:
            behave_as_at_least_3 += 1
        if opcode not in mapping:
            mapping[opcode] = possible
        else:
            mapping[opcode] &= possible
    answer.part1(560, behave_as_at_least_3)

    mapping = collapse(mapping)
    regs = Registers([0, 0, 0, 0], False)
    for instruction in groups[-1]:
        instruction = Instruction(instruction)
        ALL_INSTRUCTIONS[mapping[instruction.opcode()]].process(instruction, regs)
    answer.part2(622, regs.get(0))


def get_sample_instructions(groups):
    return [SampleInstruction(instruction) for instruction in groups[:-2]]


def collapse(mapping):
    new_mapping = {}

    while len(mapping) > 0:
        for key in mapping:
            value = mapping[key]
            if len(value) == 1:
                new_mapping[key] = list(value)[0]
        
        for key in new_mapping:
            value = new_mapping[key]
            mapping.pop(key, None)
            for values in mapping.values():
                values.discard(value)

    return new_mapping


if __name__ == '__main__':
    main()
