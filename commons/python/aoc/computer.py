from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import override


class Instruction(ABC):
    @abstractmethod
    def run(self, computer: "Computer") -> int:
        pass

    @abstractmethod
    def toggle(self) -> "Instruction":
        pass


@dataclass(kw_only=True)
class Setter(Instruction):
    register: str
    value: str
    absolute: bool

    @override
    def run(self, computer: "Computer") -> int:
        value = computer.get(self.value)
        value = value if self.absolute else computer.get(self.register) + value
        computer.set(self.register, value)
        return 1

    @override
    def toggle(self) -> Instruction:
        if self.absolute:
            return Jump(register=self.value, value=self.register)
        else:
            self.value = "1" if self.value == "-1" else "-1"
            return self


@dataclass(frozen=True, kw_only=True)
class Jump(Instruction):
    register: str
    value: str

    @override
    def run(self, computer: "Computer") -> int:
        if computer.get(self.register) != 0:
            return computer.get(self.value)
        else:
            return 1

    @override
    def toggle(self) -> Instruction:
        return Setter(register=self.value, value=self.register, absolute=True)


@dataclass(frozen=True, kw_only=True)
class Toggle(Instruction):
    register: str

    @override
    def run(self, computer: "Computer") -> int:
        computer.toggle(self.register)
        return 1

    @override
    def toggle(self) -> Instruction:
        return Setter(register=self.register, value="1", absolute=False)


@dataclass(frozen=True, kw_only=True)
class Output(Instruction):
    register: str

    @override
    def run(self, computer: "Computer") -> int:
        value = computer.get(self.register)
        computer.output(value)
        if not self.outputs_valid(computer.outputs):
            raise Exception("Invalid Output Values")
        return 1

    def outputs_valid(self, outputs: list[int]) -> bool:
        last_value = 1 if len(outputs) % 2 == 0 else 0
        return outputs[-1] == last_value

    @override
    def toggle(self) -> Instruction:
        raise Exception("Toggling is not valid for Output")


def parse_instructions(lines: list[str]) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in lines:
        parts = line.split()
        op = parts[0]
        if op == "cpy":
            instruction = Setter(register=parts[2], value=parts[1], absolute=True)
        elif op == "inc":
            instruction = Setter(register=parts[1], value="1", absolute=False)
        elif op == "dec":
            instruction = Setter(register=parts[1], value="-1", absolute=False)
        elif op == "jnz":
            instruction = Jump(register=parts[1], value=parts[2])
        elif op == "tgl":
            instruction = Toggle(register=parts[1])
        elif op == "out":
            instruction = Output(register=parts[1])
        else:
            raise Exception(f"Unknown operation: {op}")
        instructions.append(instruction)
    return instructions


@dataclass
class Computer:
    registers: dict[str, int]
    num_outputs: int | None = None
    instructions: list[Instruction] = field(default_factory=list)
    outputs: list[int] = field(default_factory=list)
    ip: int = 0

    def output(self, value: int) -> None:
        self.outputs.append(value)

    def toggle(self, value: str) -> None:
        ip = self.ip + self.get(value)
        if ip < len(self.instructions):
            instruction = self.instructions[ip]
            self.instructions[ip] = instruction.toggle()

    def get(self, value: str) -> int:
        return self.registers[value] if value in self.registers else int(value)

    def set(self, register: str, value: int) -> None:
        self.registers[register] = value

    def run(self, lines: list[str]) -> None:
        self.instructions = parse_instructions(lines)
        while self.in_range() and not self.met_success():
            instruction = self.instructions[self.ip]
            move = instruction.run(self)
            self.ip += move

    def in_range(self) -> bool:
        return self.ip >= 0 and self.ip < len(self.instructions)

    def met_success(self) -> bool:
        if self.num_outputs is None:
            return False
        return len(self.outputs) >= self.num_outputs
