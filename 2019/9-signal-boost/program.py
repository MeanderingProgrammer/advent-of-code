class Parameter:

    def __init__(self, value, mode):
        self.value = value
        self.mode = mode

    def get(self, program):
        if self.mode in [0, 2]:
            return program.memory[self.get_position(program)]
        elif self.mode == 1:
            return self.value
        else:
            raise Exception('Unknown parameter mode: {}'.format(self.mode))

    def set(self, program, value):
        program.memory[self.get_position(program)] = value

    def get_position(self, program):
        if self.mode == 0:
            position = self.value
        elif self.mode == 2:
            position = program.base + self.value
        else:
            raise Exception('Should not ask for position in mode: {}'.format(self.mode))

        # Increase memory by amount needed when indexing past end
        memory = program.memory
        size_needed = position + 1
        if size_needed > len(memory):
            amount_needed = size_needed - len(memory)
            for i in range(amount_needed):
                memory.append(0)
        return position

    def __repr__(self):
        return str(self)

    def __str__(self):
        modes = {
            0: 'Position',
            1: 'Immediate',
            2: 'Relative'
        }
        return '({} {})'.format(modes[self.mode], self.value)


class Halt:

    def set_params(self):
        pass

    def __len__(self):
        return 0
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'HALT!'


class Math:

    def __init__(self, symbol, f):
        self.symbol, self.f = symbol, f
        self.v1, self.v2, self.v3 = None, None, None

    def set_params(self, v1, v2, v3):
        self.v1, self.v2, self.v3 = v1, v2, v3

    def process(self, program):
        result = self.f(self.v1.get(program), self.v2.get(program))
        self.v3.set(program, result)

    def __len__(self):
        return 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} = {} {} {}'.format(self.v3, self.v1, self.symbol, self.v2)


class Addition(Math):

    def __init__(self):
        super().__init__('+', lambda x, y: x + y)


class Multiplication(Math):

    def __init__(self):
        super().__init__('*', lambda x, y: x * y)


class Store:

    def __init__(self):
        self.v1 = None

    def set_params(self, v1):
        self.v1 = v1

    def process(self, program):
        self.v1.set(program, program.get_input())

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
        result = self.v1.get(program)
        program.add_output(result)

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Setting output from: {}'.format(self.v1)


class Jump:

    def __init__(self, symbol, f):
        self.symbol, self.f = symbol, f
        self.v1, self.v2 = None, None

    def set_params(self, v1, v2):
        self.v1, self.v2 = v1, v2

    def process(self, program):
        if self.f(self.v1.get(program)):
            return self.v2.get(program)

    def __len__(self):
        return 2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'if {} {} Jump to {}'.format(self.v1, self.symbol, self.v2)


class JumpIfTrue(Jump):

    def __init__(self):
        super().__init__('!= 0', lambda x: x != 0)


class JumpIfFalse(Jump):

    def __init__(self):
        super().__init__('== 0', lambda x: x == 0)


class Equality:

    def __init__(self, symbol, f):
        self.symbol, self.f = symbol, f
        self.v1, self.v2, self.v3 = None, None, None

    def set_params(self, v1, v2, v3):
        self.v1, self.v2, self.v3 = v1, v2, v3

    def process(self, program):
        is_true = self.f(self.v1.get(program), self.v2.get(program))
        result = 1 if is_true else 0
        self.v3.set(program, result)

    def __len__(self):
        return 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} = 1 if {} {} {} else 0'.format(self.v3, self.v1, self.symbol, self.v2)


class LessThan(Equality):

    def __init__(self):
        super().__init__('<', lambda x, y: x < y)


class Equals(Equality):

    def __init__(self):
        super().__init__('==', lambda x, y: x == y)


class BaseAdjuster:

    def __init__(self):
        self.v1 = None

    def set_params(self, v1):
        self.v1 = v1

    def process(self, program):
        return program.base + self.v1.get(program)

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Changing base to {}'.format(self.v1)


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
        elif opcode == 9:
            self.instruction = BaseAdjuster()
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

    def jump(self):
        return isinstance(self.instruction, Jump)

    def base_adjuster(self):
        return isinstance(self.instruction, BaseAdjuster)

    def process(self, program):
        return self.instruction.process(program)

    def __len__(self):
        return 1 + len(self.instruction)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.instruction)

class State:

    def __init__(self, halt, output):
        self.halt = halt
        self.output = output


class Program:

    def __init__(self, memory, setting, debug=False):
        self.pointer = 0
        self.base = 0

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

    def run(self):
        while self.pointer < len(self.memory):
            instruction = Instruction(self.memory[self.pointer:])
            if self.debug:
                print(instruction)
            if instruction.halt():
                return State(True, False)
            result = instruction.process(self)
            self.move_pointer(instruction, result)
            self.adjust_base(instruction, result)

    def run_output(self):
        while self.pointer < len(self.memory):
            instruction = Instruction(self.memory[self.pointer:])
            if self.debug:
                print(instruction)
            if instruction.halt():
                return State(True, False)
            result = instruction.process(self)
            self.move_pointer(instruction, result)
            self.adjust_base(instruction, result)
            if instruction.load():
                return State(False, True)

    def move_pointer(self, instruction, result):
        if instruction.jump() and result is not None:
            self.pointer = result
        else:
            self.pointer = self.pointer + len(instruction)

    def adjust_base(self, instruction, result):
        if instruction.base_adjuster() and result is not None:
            self.base = result
