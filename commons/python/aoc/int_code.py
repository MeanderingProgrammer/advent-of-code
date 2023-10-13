class Parameter:

    def __init__(self, value, mode):
        self.__value = value
        self.__mode = mode

    def get(self, computer):
        if self.__mode in [0, 2]:
            return computer.memory[self.__get_position(computer)]
        elif self.__mode == 1:
            return self.__value
        else:
            raise Exception('Unknown parameter mode: {}'.format(self.__mode))

    def set(self, computer, value):
        computer.memory[self.__get_position(computer)] = value

    def __get_position(self, computer):
        if self.__mode == 0:
            position = self.__value
        elif self.__mode == 2:
            position = computer.base + self.__value
        else:
            raise Exception('Should not ask for position in mode: {}'.format(self.__mode))

        # Increase memory by amount needed when indexing past end
        memory = computer.memory
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
        return '({} {})'.format(modes[self.__mode], self.__value)


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
        self.__symbol, self.__f = symbol, f
        self.__v1, self.__v2, self.__v3 = None, None, None

    def set_params(self, v1, v2, v3):
        self.__v1, self.__v2, self.__v3 = v1, v2, v3

    def process(self, computer):
        result = self.__f(self.__v1.get(computer), self.__v2.get(computer))
        self.__v3.set(computer, result)

    def __len__(self):
        return 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} = {} {} {}'.format(self.__v3, self.__v1, self.__symbol, self.__v2)


class Addition(Math):

    def __init__(self):
        super().__init__('+', lambda x, y: x + y)


class Multiplication(Math):

    def __init__(self):
        super().__init__('*', lambda x, y: x * y)


class Store:

    def __init__(self):
        self.__v1 = None

    def set_params(self, v1):
        self.__v1 = v1

    def process(self, computer):
        self.__v1.set(computer, computer.bus.get_input())

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Storing value at: {}'.format(self.__v1)


class Load:

    def __init__(self):
        self.__v1 = None

    def set_params(self, v1):
        self.__v1 = v1

    def process(self, computer):
        result = self.__v1.get(computer)
        computer.bus.add_output(result)

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Setting output from: {}'.format(self.__v1)


class Jump:

    def __init__(self, symbol, f):
        self.__symbol, self.__f = symbol, f
        self.__v1, self.__v2 = None, None

    def set_params(self, v1, v2):
        self.__v1, self.__v2 = v1, v2

    def process(self, computer):
        if self.__f(self.__v1.get(computer)):
            return self.__v2.get(computer)

    def __len__(self):
        return 2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'if {} {} Jump to {}'.format(self.__v1, self.__symbol, self.__v2)


class JumpIfTrue(Jump):

    def __init__(self):
        super().__init__('!= 0', lambda x: x != 0)


class JumpIfFalse(Jump):

    def __init__(self):
        super().__init__('== 0', lambda x: x == 0)


class Equality:

    def __init__(self, symbol, f):
        self.__symbol, self.__f = symbol, f
        self.__v1, self.__v2, self.__v3 = None, None, None

    def set_params(self, v1, v2, v3):
        self.__v1, self.__v2, self.__v3 = v1, v2, v3

    def process(self, computer):
        is_true = self.__f(self.__v1.get(computer), self.__v2.get(computer))
        result = 1 if is_true else 0
        self.__v3.set(computer, result)

    def __len__(self):
        return 3

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} = 1 if {} {} {} else 0'.format(self.__v3, self.__v1, self.__symbol, self.__v2)


class LessThan(Equality):

    def __init__(self):
        super().__init__('<', lambda x, y: x < y)


class Equals(Equality):

    def __init__(self):
        super().__init__('==', lambda x, y: x == y)


class BaseAdjuster:

    def __init__(self):
        self.__v1 = None

    def set_params(self, v1):
        self.__v1 = v1

    def process(self, computer):
        return computer.base + self.__v1.get(computer)

    def __len__(self):
        return 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Changing base to {}'.format(self.__v1)


INSTRUCTION_FACTORY = {
    1: lambda: Addition(),
    2: lambda: Multiplication(),
    3: lambda: Store(),
    4: lambda: Load(),
    5: lambda: JumpIfTrue(),
    6: lambda: JumpIfFalse(),
    7: lambda: LessThan(),
    8: lambda: Equals(),
    9: lambda: BaseAdjuster(),
    99: lambda: Halt(),
}


class Instruction:

    def __init__(self, memory):
        code = memory[0]
        opcode = code % 100

        if opcode not in INSTRUCTION_FACTORY:
            raise Exception('Unknown opcode: {}'.format(opcode))

        self.__instruction = INSTRUCTION_FACTORY[opcode]()

        parameters = []
        for i in range(len(self.__instruction)):
            index = i+1
            mode = (code % pow(10, index+2)) // pow(10, index+1)
            parameters.append(Parameter(memory[index], mode))

        self.__instruction.set_params(*parameters)

    def halt(self):
        return isinstance(self.__instruction, Halt)

    def load(self):
        return isinstance(self.__instruction, Load)

    def jump(self):
        return isinstance(self.__instruction, Jump)

    def base_adjuster(self):
        return isinstance(self.__instruction, BaseAdjuster)

    def process(self, computer):
        return self.__instruction.process(computer)

    def __len__(self):
        return 1 + len(self.__instruction)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__instruction)


class Computer:

    def __init__(self, bus, debug=False):
        self.memory, self.__pointer, self.base = None, None, 0
        self.bus, self.__debug = bus, debug

    def set_memory(self, memory):
        self.memory, self.__pointer, self.base = memory, 0, 0

    def run(self):
        while self.has_next():
            self.next()

    def has_next(self):
        return not self.__next_instruction().halt()

    def next(self):
        instruction = self.__next_instruction()
        if self.__debug:
            print(instruction)

        result = instruction.process(self)
        self.__move_pointer(instruction, result)
        self.__adjust_base(instruction, result)

    def __next_instruction(self):
        return Instruction(self.memory[self.__pointer:])

    def __move_pointer(self, instruction, result):
        if instruction.jump() and result is not None:
            self.__pointer = result
        else:
            self.__pointer += len(instruction)

    def __adjust_base(self, instruction, result):
        if instruction.base_adjuster() and result is not None:
            self.base = result
