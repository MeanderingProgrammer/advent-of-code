from aoc import answer
from aoc.parser import Parser


class Registers:
    def __init__(self, size: int, ip: int):
        self.values = [0 for _ in range(size)]
        self.ip = ip

    def instruction(self) -> int:
        return self.values[self.ip]

    def next(self) -> None:
        self.values[self.ip] += 1

    def set(self, index: int, value: int) -> None:
        self.values[index] = value

    def get(self, index: int) -> int:
        return self.values[index]


class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction.split()

    def opcode(self) -> str:
        return self.instruction[0]

    def one(self) -> int:
        return int(self.instruction[1])

    def two(self) -> int:
        return int(self.instruction[2])

    def three(self) -> int:
        return int(self.instruction[3])


class Parameter:
    def __init__(self, register: bool):
        self.register = register

    def get(self, value: int, regs: Registers) -> int:
        return regs.get(value) if self.register else value


class Operator:
    def __init__(self, register: bool, f):
        self.v1 = Parameter(True)
        self.v2 = Parameter(register)
        self.f = f

    def process(self, instruction: Instruction, regs: Registers) -> None:
        a = self.v1.get(instruction.one(), regs)
        b = self.v2.get(instruction.two(), regs)
        regs.set(instruction.three(), self.f(a, b))


class Add(Operator):
    def __init__(self, register: bool):
        super().__init__(register, lambda x, y: x + y)


class Mult(Operator):
    def __init__(self, register: bool):
        super().__init__(register, lambda x, y: x * y)


class And(Operator):
    def __init__(self, register: bool):
        super().__init__(register, lambda x, y: x & y)


class Or(Operator):
    def __init__(self, register: bool):
        super().__init__(register, lambda x, y: x | y)


class Set:
    def __init__(self, register: bool):
        self.v1 = Parameter(register)

    def process(self, instruction: Instruction, regs: Registers) -> None:
        value = self.v1.get(instruction.one(), regs)
        regs.set(instruction.three(), value)


class Comparison:
    def __init__(self, reg1: bool, reg2: bool, f):
        self.v1 = Parameter(reg1)
        self.v2 = Parameter(reg2)
        self.f = f

    def process(self, instruction: Instruction, regs: Registers) -> None:
        a = self.v1.get(instruction.one(), regs)
        b = self.v2.get(instruction.two(), regs)
        value = 1 if self.f(a, b) else 0
        regs.set(instruction.three(), value)


class GreaterThan(Comparison):
    def __init__(self, reg1: bool, reg2: bool):
        super().__init__(reg1, reg2, lambda x, y: x > y)


class Equals(Comparison):
    def __init__(self, reg1: bool, reg2: bool):
        super().__init__(reg1, reg2, lambda x, y: x == y)


ALL_INSTRUCTIONS = {
    "addr": Add(True),
    "addi": Add(False),
    "mulr": Mult(True),
    "muli": Mult(False),
    "banr": And(True),
    "bani": And(False),
    "borr": Or(True),
    "bori": Or(False),
    "setr": Set(True),
    "seti": Set(False),
    "gtir": GreaterThan(False, True),
    "gtri": GreaterThan(True, False),
    "gtrr": GreaterThan(True, True),
    "eqir": Equals(False, True),
    "eqri": Equals(True, False),
    "eqrr": Equals(True, True),
}


def main() -> None:
    answer.part1(993, solve_part_1())
    answer.part2(10708912, solve_part_2(10_551_361))


def solve_part_1() -> int:
    lines = Parser().lines()
    pointer = int(lines[0].split()[1])
    instructions = [Instruction(line) for line in lines[1:]]
    regs = Registers(6, pointer)
    while regs.instruction() < len(instructions):
        instruction_index = regs.instruction()
        instruction = instructions[instruction_index]
        ALL_INSTRUCTIONS[instruction.opcode()].process(instruction, regs)
        regs.next()
    return regs.get(0)


def solve_part_2(value: int) -> int:
    # Reverse engineered code to figure out what it's calculating
    result = 0
    for i in range(1, value + 1):
        if value % i == 0:
            result += i
    return result


if __name__ == "__main__":
    main()
