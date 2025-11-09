from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


class Mode(Enum):
    POSITION = auto()
    IMMEDIATE = auto()
    RELATIVE = auto()


class Method(Enum):
    GET = auto()
    IDX = auto()


class Bus(Protocol):
    def active(self) -> bool: ...

    def get_input(self) -> int: ...

    def add_output(self, value: int) -> None: ...


@dataclass
class Computer[T: Bus]:
    bus: T
    memory: list[int]
    code: int = 0
    param: int = 0
    pointer: int = 0
    base: int = 0

    def run(self) -> None:
        while self.bus.active() and self.step():
            pass

    def step(self) -> bool:
        done = False
        increment = True

        self.code = self.memory[self.pointer]
        self.param = 0

        match self.code % 100:
            case 1:
                v1, v2 = self.next(Method.GET), self.next(Method.GET)
                self.set(self.next(Method.IDX), v1 + v2)
            case 2:
                v1, v2 = self.next(Method.GET), self.next(Method.GET)
                self.set(self.next(Method.IDX), v1 * v2)
            case 3:
                self.set(self.next(Method.IDX), self.bus.get_input())
            case 4:
                self.bus.add_output(self.next(Method.GET))
            case 5:
                v1, v2 = self.next(Method.GET), self.next(Method.GET)
                if v1 != 0:
                    self.pointer = v2
                    increment = False
            case 6:
                v1, v2 = self.next(Method.GET), self.next(Method.GET)
                if v1 == 0:
                    self.pointer = v2
                    increment = False
            case 7:
                v1, v2 = self.next(Method.GET), self.next(Method.GET)
                self.set(self.next(Method.IDX), 1 if v1 < v2 else 0)
            case 8:
                v1, v2 = self.next(Method.GET), self.next(Method.GET)
                self.set(self.next(Method.IDX), 1 if v1 == v2 else 0)
            case 9:
                self.base += self.next(Method.GET)
            case 99:
                done = True
            case opcode:
                raise Exception(f"unknown opcode: {opcode}")

        self.pointer += 1 if increment else 0

        return not done

    def next(self, method: Method) -> int:
        mode = self.mode()
        self.pointer += 1
        value = self.memory[self.pointer]
        match method:
            case Method.IDX:
                return self.index(mode, value)
            case Method.GET:
                match mode:
                    case Mode.POSITION | Mode.RELATIVE:
                        index = self.index(mode, value)
                        return self.get(index)
                    case Mode.IMMEDIATE:
                        return value

    def mode(self) -> Mode:
        self.param += 1
        n: int = 10 ** (self.param + 1)
        value: int = (self.code // n) % 10
        match value:
            case 0:
                return Mode.POSITION
            case 1:
                return Mode.IMMEDIATE
            case 2:
                return Mode.RELATIVE
            case mode:
                raise Exception(f"unknown mode: {mode}")

    def index(self, mode: Mode, value: int) -> int:
        offset = None
        match mode:
            case Mode.POSITION:
                offset = 0
            case Mode.RELATIVE:
                offset = self.base
            case Mode.IMMEDIATE:
                raise Exception("immediate mode does not support indexing")
        return offset + value

    def get(self, index: int) -> int:
        if index < len(self.memory):
            return self.memory[index]
        else:
            return 0

    def set(self, index: int, value: int) -> None:
        if index >= len(self.memory):
            additional = index + 1 - len(self.memory)
            self.memory.extend([0] * additional)
        self.memory[index] = value
