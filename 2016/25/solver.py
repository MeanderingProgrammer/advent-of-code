from aoc_computer import Computer
from aoc_parser import Parser


FILE_NAME = 'data'


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


class Output:

    def __init__(self, register):
        self.register = register

    def run(self, computer):
        value = computer.get(self.register)
        computer.output(value)
        computer.move(1)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Output: {}'.format(self.register)
        


def main():
    # Part 1: 198
    print('Part 1: {}'.format(run_until_success()))


def run_until_success():
    i = 0
    while True:
        try:
            run_computer(i)
            return i
        except Exception:
            # Do nothing, move onto next iteration
            pass
        i += 1


def run_computer(initial_value):
    computer = Computer(
        ['a', 'b', 'c', 'd'],
        get_instructions()
    )
    computer.set('a', initial_value)
    computer.run()


def get_instructions():
    instructions = []
    for line in Parser(FILE_NAME).lines():
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
        elif op == 'out':
            instruction = Output(parts[1])
        else:
            raise Exception('Unknown operation: {}'.format(op))
        instructions.append(instruction)
    return instructions


if __name__ == '__main__':
    main()
