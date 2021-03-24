class Computer:

    def __init__(self, registers, instructions):
        self.registers = {register: 0 for register in registers}

        self.instructions = instructions
        self.ip = 0

        self.outputs = None

    def output(self, value):
        if self.outputs is not None:
            expected = 1 if self.outputs == 0 else 0
            if value != expected:
                raise Exception('Expected alternating pattern: {} {}'.format(self.outputs, value))
        self.outputs = value

    def get(self, value):
        return self.registers[value] if value in self.registers else int(value)

    def set(self, register, value):
        self.registers[register] = value

    def move(self, amount):
        self.ip += amount

    def run(self):
        while self.in_range():
            instruction = self.instructions[self.ip]
            instruction.run(self)

    def in_range(self):
        return self.ip >= 0 and self.ip < len(self.instructions)
