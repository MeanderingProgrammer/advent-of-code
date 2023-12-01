from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Registers:
    values: list[int]

    def set(self, index: int, value: int) -> None:
        self.values[index] = value

    def get(self, index: int) -> int:
        return self.values[index]

    def copy(self) -> Self:
        return type(self)(list(self.values))


@dataclass(frozen=True)
class Instruction:
    instruction: list[int]

    def opcode(self) -> int:
        return self.instruction[0]

    def one(self) -> int:
        return self.instruction[1]

    def two(self) -> int:
        return self.instruction[2]

    def three(self) -> int:
        return self.instruction[3]


@dataclass(frozen=True)
class Parameter:
    register: bool

    def get(self, value: int, regs: Registers) -> int:
        return regs.get(value) if self.register else value


class Operator:
    def __init__(self, register: bool, f: Callable[[int, int], int]):
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
    def __init__(self, reg1: bool, reg2: bool, f: Callable[[int, int], bool]):
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


@dataclass(frozen=True)
class SampleInstruction:
    before: Registers
    instruction: Instruction
    after: Registers

    def test_all(self) -> set[str]:
        meets: set[str] = set()
        for name, instruction in ALL_INSTRUCTIONS.items():
            register_copy = self.before.copy()
            instruction.process(self.instruction, register_copy)
            if register_copy == self.after:
                meets.add(name)
        return meets


def main() -> None:
    groups = Parser().line_groups()
    mapping, many_behaviors = get_mapping(groups[:-2])
    answer.part1(560, many_behaviors)
    answer.part2(622, process_instructions(mapping, groups[-1]))


def get_mapping(groups: list[list[str]]) -> tuple[dict[int, str], int]:
    initial_mapping: dict[int, set[str]] = dict()
    many_behaviors: int = 0
    for sample_instruction in get_sample_instructions(groups):
        opcode = sample_instruction.instruction.opcode()
        possible = sample_instruction.test_all()
        if len(possible) >= 3:
            many_behaviors += 1
        if opcode not in initial_mapping:
            initial_mapping[opcode] = possible
        else:
            initial_mapping[opcode] &= possible
    return collapse(initial_mapping), many_behaviors


def get_sample_instructions(groups: list[list[str]]) -> list[SampleInstruction]:
    def parse_registers(line: str) -> Registers:
        return Registers(list(map(int, line.split(" [")[1][:-1].split(", "))))

    def parse_sample_instruction(lines: list[str]) -> SampleInstruction:
        return SampleInstruction(
            before=parse_registers(lines[0]),
            instruction=parse_instruction(lines[1]),
            after=parse_registers(lines[2]),
        )

    return [parse_sample_instruction(lines) for lines in groups]


def parse_instruction(line: str) -> Instruction:
    return Instruction(list(map(int, line.split())))


def collapse(mapping: dict[int, set[str]]) -> dict[int, str]:
    collapsed: dict[int, str] = dict()
    while len(mapping) > 0:
        for key, options in mapping.items():
            if len(options) > 1:
                continue
            selected_option = list(options)[0]
            collapsed[key] = selected_option
        for key, value in collapsed.items():
            mapping.pop(key, None)
            for values in mapping.values():
                values.discard(value)
    return collapsed


def process_instructions(mapping: dict[int, str], lines: list[str]) -> int:
    regs = Registers([0, 0, 0, 0])
    for line in lines:
        instruction = parse_instruction(line)
        ALL_INSTRUCTIONS[mapping[instruction.opcode()]].process(instruction, regs)
    return regs.get(0)


if __name__ == "__main__":
    main()
