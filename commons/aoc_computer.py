class Computer:

    def __init__(self, registers):
        self.registers = {register: 0 for register in registers}
        self.ip = 0

    def get(self, value):
        return self.registers[value] if value in self.registers else int(value)

    def set(self, register, value):
        self.registers[register] = value

    def move(self, amount):
        self.ip += amount

    def run(self, instructions):
        while self.in_range(instructions):
            instruction = instructions[self.ip]
            instruction.run(self)

    def in_range(self, instructions):
        return self.ip >= 0 and self.ip < len(instructions)
