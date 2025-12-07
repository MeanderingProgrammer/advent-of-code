from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self


@dataclass(frozen=True)
class Computer:
    registers: dict[str, int]
    outputs: list[int]

    @classmethod
    def new(cls, overrides: dict[str, int]) -> Self:
        result = cls(dict(a=0, b=0, c=0, d=0), [])
        for key, value in overrides.items():
            result.set(key, value)
        return result

    def run(self, lines: list[str]) -> bool:
        ip = 0
        instructions = [Instruction.new(line) for line in lines]
        while ip >= 0 and ip < len(instructions) and len(self.outputs) < 100:
            move = 1
            instruction = instructions[ip]
            match instruction.operation:
                case Operation.CPY:
                    x, y = instruction.args
                    self.set(y, self.get(x))
                case Operation.INC:
                    (x,) = instruction.args
                    self.set(x, self.get(x) + 1)
                case Operation.DEC:
                    (x,) = instruction.args
                    self.set(x, self.get(x) - 1)
                case Operation.JNZ:
                    x, y = instruction.args
                    if self.get(x) != 0:
                        move = self.get(y)
                case Operation.TGL:
                    (x,) = instruction.args
                    i = ip + self.get(x)
                    if i < len(instructions):
                        instructions[i] = instructions[i].toggle()
                case Operation.OUT:
                    (x,) = instruction.args
                    value = self.get(x)
                    if value != len(self.outputs) % 2:
                        return False
                    self.outputs.append(value)
            ip += move
        return True

    def get(self, value: str) -> int:
        result = self.registers.get(value)
        return result if result is not None else int(value)

    def set(self, key: str, value: int) -> None:
        self.registers[key] = value


@dataclass(frozen=True)
class Instruction:
    operation: Operation
    args: list[str]

    @classmethod
    def new(cls, s: str) -> Self:
        args = s.split()
        operation = Operation(args.pop(0))
        return cls(operation, args)

    def toggle(self) -> Self:
        return type(self)(self.operation.toggle(), self.args)


class Operation(StrEnum):
    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()
    TGL = auto()
    OUT = auto()

    def toggle(self) -> Operation:
        match self:
            case self.CPY:
                return self.JNZ
            case self.INC:
                return self.DEC
            case self.DEC:
                return self.INC
            case self.JNZ:
                return self.CPY
            case self.TGL:
                return self.INC
            case self.OUT:
                raise Exception("toggle invalid for output")
