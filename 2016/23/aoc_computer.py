class Computer:

    def __init__(self, registers, instructions):
        self.registers = {register: 0 for register in registers}

        self.instructions = instructions
        self.ip = 0

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
            print(instruction, self.registers)

    def in_range(self):
        return self.ip >= 0 and self.ip < len(self.instructions)
