from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass(frozen=True)
class Parameter:
    value: int
    mode: int

    def get(self, computer: "Computer"):
        if self.mode in [0, 2]:
            return computer.memory[self.get_position(computer)]
        elif self.mode == 1:
            return self.value
        else:
            raise Exception(f"Unknown parameter mode: {self.mode}")

    def set(self, computer: "Computer", value):
        computer.memory[self.get_position(computer)] = value

    def get_position(self, computer: "Computer"):
        if self.mode == 0:
            position = self.value
        elif self.mode == 2:
            position = computer.base + self.value
        else:
            raise Exception(f"Should not ask for position in mode: {self.mode}")

        # Increase memory by amount needed when indexing past end
        memory = computer.memory
        size_needed = position + 1
        if size_needed > len(memory):
            amount_needed = size_needed - len(memory)
            memory.extend([0] * amount_needed)
        return position


class Halt:
    def set_params(self) -> None:
        pass

    def __len__(self):
        return 0


@dataclass
class Math:
    f: Callable[[int, int], int]
    v1: Optional[Parameter] = None
    v2: Optional[Parameter] = None
    v3: Optional[Parameter] = None

    def set_params(self, v1: Parameter, v2: Parameter, v3: Parameter) -> None:
        self.v1, self.v2, self.v3 = v1, v2, v3

    def process(self, computer: "Computer"):
        assert self.v1 is not None and self.v2 is not None and self.v3 is not None
        result = self.f(self.v1.get(computer), self.v2.get(computer))
        self.v3.set(computer, result)

    def __len__(self):
        return 3


class Addition(Math):
    def __init__(self):
        super().__init__(lambda x, y: x + y)


class Multiplication(Math):
    def __init__(self):
        super().__init__(lambda x, y: x * y)


@dataclass
class Store:
    v1: Optional[Parameter] = None

    def set_params(self, v1: Parameter) -> None:
        self.v1 = v1

    def process(self, computer: "Computer"):
        assert self.v1 is not None
        self.v1.set(computer, computer.bus.get_input())

    def __len__(self):
        return 1


@dataclass
class Load:
    v1: Optional[Parameter] = None

    def set_params(self, v1: Parameter) -> None:
        self.v1 = v1

    def process(self, computer: "Computer"):
        assert self.v1 is not None
        result = self.v1.get(computer)
        computer.bus.add_output(result)

    def __len__(self):
        return 1


@dataclass
class Jump:
    f: Callable[[int], bool]
    v1: Optional[Parameter] = None
    v2: Optional[Parameter] = None

    def set_params(self, v1: Parameter, v2: Parameter) -> None:
        self.v1, self.v2 = v1, v2

    def process(self, computer: "Computer"):
        assert self.v1 is not None and self.v2 is not None
        if self.f(self.v1.get(computer)):
            return self.v2.get(computer)

    def __len__(self):
        return 2


class JumpIfTrue(Jump):
    def __init__(self):
        super().__init__(lambda x: x != 0)


class JumpIfFalse(Jump):
    def __init__(self):
        super().__init__(lambda x: x == 0)


@dataclass
class Equality:
    f: Callable[[int, int], bool]
    v1: Optional[Parameter] = None
    v2: Optional[Parameter] = None
    v3: Optional[Parameter] = None

    def set_params(self, v1: Parameter, v2: Parameter, v3: Parameter) -> None:
        self.v1, self.v2, self.v3 = v1, v2, v3

    def process(self, computer: "Computer"):
        assert self.v1 is not None and self.v2 is not None and self.v3 is not None
        is_true = self.f(self.v1.get(computer), self.v2.get(computer))
        result = 1 if is_true else 0
        self.v3.set(computer, result)

    def __len__(self):
        return 3


class LessThan(Equality):
    def __init__(self):
        super().__init__(lambda x, y: x < y)


class Equals(Equality):
    def __init__(self):
        super().__init__(lambda x, y: x == y)


@dataclass
class BaseAdjuster:
    v1: Optional[Parameter] = None

    def set_params(self, v1: Parameter) -> None:
        self.v1 = v1

    def process(self, computer: "Computer"):
        assert self.v1 is not None
        return computer.base + self.v1.get(computer)

    def __len__(self):
        return 1


INSTRUCTION_FACTORY = {
    1: Addition,
    2: Multiplication,
    3: Store,
    4: Load,
    5: JumpIfTrue,
    6: JumpIfFalse,
    7: LessThan,
    8: Equals,
    9: BaseAdjuster,
    99: Halt,
}


class Instruction:
    def __init__(self, memory: list[int]):
        code = memory[0]
        opcode = code % 100
        if opcode not in INSTRUCTION_FACTORY:
            raise Exception(f"Unknown opcode: {opcode}")

        self.instruction = INSTRUCTION_FACTORY[opcode]()

        parameters = []
        for i in range(len(self.instruction)):
            index = i + 1
            mode = (code % pow(10, index + 2)) // pow(10, index + 1)
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

    def process(self, computer: "Computer"):
        return self.instruction.process(computer)

    def __len__(self):
        return 1 + len(self.instruction)


class Bus(ABC):
    @abstractmethod
    def active(self) -> bool:
        pass

    @abstractmethod
    def get_input(self) -> Any:
        pass

    @abstractmethod
    def add_output(self, value: Any) -> None:
        pass


@dataclass
class Computer[T: Bus]:
    bus: T
    memory: list[int]
    pointer: int = 0
    base: int = 0

    def run(self) -> None:
        while self.has_next() and self.bus.active():
            self.next()

    def has_next(self) -> bool:
        return not self.next_instruction().halt()

    def next(self) -> None:
        instruction = self.next_instruction()
        result = instruction.process(self)
        self.move_pointer(instruction, result)
        self.adjust_base(instruction, result)

    def next_instruction(self) -> Instruction:
        return Instruction(self.memory[self.pointer :])

    def move_pointer(self, instruction: Instruction, result: Optional[int]):
        if instruction.jump() and result is not None:
            self.pointer = result
        else:
            self.pointer += len(instruction)

    def adjust_base(self, instruction: Instruction, result: Optional[int]):
        if instruction.base_adjuster() and result is not None:
            self.base = result
