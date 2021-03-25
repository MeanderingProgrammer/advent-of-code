from collections import defaultdict

from aoc_parser import Parser


FILE_NAME = 'data'


def modifier(r_id, amount, f):
    def result(registers):
        current = registers[r_id]
        registers[r_id] = f(current, amount)
    return result



MODIFIERS = {
    'inc': lambda r_id, amount: modifier(r_id, amount, lambda a, b: a + b),
    'dec': lambda r_id, amount: modifier(r_id, amount, lambda a, b: a - b)
}


def condition(r_id, value, f):
    def result(registers):
        current = registers[r_id]
        return f(current, value)
    return result


CONDITIONS = {
    '>': lambda r_id, value: condition(r_id, value, lambda a, b: a > b),
    '<': lambda r_id, value: condition(r_id, value, lambda a, b: a < b),
    '==': lambda r_id, value: condition(r_id, value, lambda a, b: a == b),
    '!=': lambda r_id, value: condition(r_id, value, lambda a, b: a != b),
    '>=': lambda r_id, value: condition(r_id, value, lambda a, b: a >= b),
    '<=': lambda r_id, value: condition(r_id, value, lambda a, b: a <= b)
}


class Instruction:

    def __init__(self, raw):
        parts = raw.split()
        self.modifier = MODIFIERS[parts[1]](parts[0], int(parts[2]))
        self.condition = CONDITIONS[parts[5]](parts[4], int(parts[6]))

    def apply(self, registers):
        does_meet = self.condition(registers)
        if does_meet:
            self.modifier(registers)



def main():
    registers = defaultdict(int)
    instructions = get_instructions()

    maxes = []
    for instruction in instructions:
        instruction.apply(registers)
        maxes.append(max(registers.values()))
    # Part 1: 7296
    print('Part 1: {}'.format(max(registers.values())))
    # Part 2: 8186
    print('Part 2: {}'.format(max(maxes)))


def get_instructions():
    instructions = []
    for line in Parser(FILE_NAME).lines():
        instructions.append(Instruction(line))
    return instructions


if __name__ == '__main__':
    main()

