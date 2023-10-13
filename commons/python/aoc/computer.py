class Computer:

    def __init__(self, registers, num_outputs=None):
        self.registers = {register: 0 for register in registers}
        self.ip = 0
        self.instructions = None

        self.num_outputs = num_outputs
        self.outputs = []

    def output(self, value):
        self.outputs.append(value)

    def get(self, value):
        return self.registers[value] if value in self.registers else int(value)

    def set(self, register, value):
        self.registers[register] = value

    def move(self, amount):
        self.ip += amount

    def run(self, instructions):
        self.instructions = instructions

        while self.in_range() and not self.met_success():
            instruction = instructions[self.ip]
            instruction.run(self)

        self.instructions = None

    def in_range(self):
        return self.ip >= 0 and self.ip < len(self.instructions)

    def met_success(self):
        if self.num_outputs is None:
            return False
        return len(self.outputs) >= self.num_outputs
