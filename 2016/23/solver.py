import math

import commons.answer as answer
from commons.aoc_computer import Computer
from commons.aoc_parser import Parser


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

    def toggle(self):
        if self.absolute:
            return Jump(self.value, self.register)
        else:
            value = '1' if self.value == '-1' else '-1'
            self.value = value
            return self

    def __repr__(self):
        return str(self)

    def __str__(self):
        operation = '=' if self.absolute else '+='
        return '{} {} {}'.format(self.register, operation, self.value)


class Jump:

    def __init__(self, register, value):
        self.register = register
        self.value = value

    def run(self, computer):
        if computer.get(self.register) != 0:
            computer.move(computer.get(self.value))
        else:
            computer.move(1)

    def toggle(self):
        return Setter(self.value, self.register, True)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Jump {} if {} != 0'.format(self.value, self.register)


class Toggle:

    def __init__(self, register):
        self.register = register

    def run(self, computer):
        ip = computer.ip + computer.get(self.register)
        instructions = computer.instructions
        if ip < len(instructions):
            instruction = instructions[ip]
            instructions[ip] = instruction.toggle()
        computer.move(1)

    def toggle(self):
        return Setter(self.register, '1', False)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Toggle: {}'.format(self.register)
        

def main():
    answer.part1(11662, run_computer(7))
    # Ends up simplifying to n! + 77*86 
    # Did some reverse engineering
    answer.part2(479008222, math.factorial(12) + 77*86)


def run_computer(num_eggs):
    computer = Computer(
        ['a', 'b', 'c', 'd']
    )
    computer.set('a', num_eggs)
    computer.run(get_instructions())
    return computer.get('a')


def get_instructions():
    instructions = []
    for line in Parser().lines():
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
        elif op == 'tgl':
            instruction = Toggle(parts[1])
        else:
            raise Exception('Unknown operation: {}'.format(op))
        instructions.append(instruction)
    return instructions


if __name__ == '__main__':
    main()
