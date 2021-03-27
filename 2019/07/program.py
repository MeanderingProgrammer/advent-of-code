class Parameter:

    def __init__(self, value, mode):
        self.value = value
        self.mode = mode

    def get(self, memory):
        return memory[self.value] if self.mode == 0 else self.value

    def set(self, memory, value):
        memory[self.value] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        mode = 'Position' if self.mode == 0 else 'Immediate'
        return '({} {})'.format(mode, self.value)


class Halt:

    def set_params(self):
        pass

    def __len__(self):
        return 0
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'HALT!'


class MathInstruction:

    def __init__(self, symbol, f):
        self.symbol, self.f = symbol, f
        self.v1, self.v2, self.v3 = None, None, None

    def set_params(self, v1, v2, v3):
        self.v1, self.v2, self.v3 = v1, v2, v3

    def process(self, program):
        memory = program.memory
        result = self.f(self.v1.get(memory), self.v2.get(memory))
        self.v3.set(memory, result)

    def __len__(self):
        return 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} = {} {} {}'.format(self.v3, self.v1, self.symbol, self.v2)


def Addition():
    return MathInstruction('+', lambda x, y: x + y)


def Multiplication():
    return MathInstruction('*', lambda x, y: x * y)


class Store:

    def __init__(self):
        self.v1 = None

    def set_params(self, v1):
        self.v1 = v1

    def process(self, program):
        memory = program.memory
        self.v1.set(memory, program.get_input())

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Storing value at: {}'.format(self.v1)


class Load:

    def __init__(self):
        self.v1 = None

    def set_params(self, v1):
        self.v1 = v1

    def process(self, program):
        memory = program.memory
        result = self.v1.get(memory)
        program.add_output(result)

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Setting output from: {}'.format(self.v1)


class JumpInstruction:

    def __init__(self, symbol, f):
        self.symbol, self.f = symbol, f
        self.v1, self.v2 = None, None

    def set_params(self, v1, v2):
        self.v1, self.v2 = v1, v2

    def process(self, program):
        memory = program.memory
        if self.f(self.v1.get(memory)):
            return self.v2.get(memory)

    def __len__(self):
        return 2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'if {} {} Jump to {}'.format(self.v1, self.symbol, self.v2)

def JumpIfTrue():
    return JumpInstruction('!= 0', lambda x: x != 0)


def JumpIfFalse():
    return JumpInstruction('== 0', lambda x: x == 0)


class EqualityInstruction:

    def __init__(self, symbol, f):
        self.symbol, self.f = symbol, f
        self.v1, self.v2, self.v3 = None, None, None

    def set_params(self, v1, v2, v3):
        self.v1, self.v2, self.v3 = v1, v2, v3

    def process(self, program):
        memory = program.memory
        result = 1 if self.f(self.v1.get(memory), self.v2.get(memory)) else 0
        self.v3.set(memory, result)

    def __len__(self):
        return 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} = 1 if {} {} {} else 0'.format(self.v3, self.v1, self.symbol, self.v2)

def LessThan():
    return EqualityInstruction('<', lambda x, y: x < y)


def Equals():
    return EqualityInstruction('==', lambda x, y: x == y)


class Instruction:

    def __init__(self, memory):
        code = memory[0]
        opcode = code % 100

        if opcode == 1:
            self.instruction = Addition()
        elif opcode == 2:
            self.instruction = Multiplication()
        elif opcode == 3:
            self.instruction = Store()
        elif opcode == 4:
            self.instruction = Load()
        elif opcode == 5:
            self.instruction = JumpIfTrue()
        elif opcode == 6:
            self.instruction = JumpIfFalse()
        elif opcode == 7:
            self.instruction = LessThan()
        elif opcode == 8:
            self.instruction = Equals()
        elif opcode == 99:
            self.instruction = Halt()
        else:
            raise Exception('Unknown opcode: {}'.format(opcode))

        parameters = []
        for i in range(len(self.instruction)):
            index = i+1
            mode = (code % pow(10, index+2)) // pow(10, index+1)
            parameters.append(Parameter(memory[index], mode))

        self.instruction.set_params(*parameters)

    def halt(self):
        return isinstance(self.instruction, Halt)

    def load(self):
        return isinstance(self.instruction, Load)

    def process(self, program):
        return self.instruction.process(program)

    def __len__(self):
        return 1 + len(self.instruction)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.instruction)


class Program:

    def __init__(self, memory, setting, debug=False):
        self.pointer = 0
        self.memory = memory

        self.inputs = [setting]
        self.input_index = 0

        self.debug = debug

        self.outputs = []

    def add_input(self, value):
        self.inputs.append(value)

    def get_input(self):
        result = self.inputs[self.input_index]
        self.input_index += 1
        return result

    def add_output(self, value):
        self.outputs.append(value)

    def get_output(self):
        return self.outputs[-1]

    def run(self, pause_on_load):
        while self.pointer < len(self.memory):
            instruction = Instruction(self.memory[self.pointer:])
            if self.debug:
                print(instruction)
            if instruction.halt():
                return False
            result = instruction.process(self)
            self.pointer = self.pointer + len(instruction) if result is None else result
            if pause_on_load and instruction.load():
                return True
