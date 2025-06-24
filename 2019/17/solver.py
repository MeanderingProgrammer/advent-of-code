from collections.abc import Generator
from dataclasses import dataclass, field
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser
from aoc.point import Point, PointHelper

STATE_MAPPING: dict[str, int] = {"^": 0, ">": 1, "v": 2, "<": 3}
DIRECTIONS: list[Point] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


@dataclass
class DroidState:
    location: Point
    scafolding: list[Point]
    direction: Point

    def get_instructions(self) -> list[str]:
        instructions: list[str] = []
        code = self.set_direction()
        while code is not None:
            until_end = self.move_until_end()
            instructions.append(f"{code},{until_end}")
            code = self.set_direction()
        return instructions

    def set_direction(self) -> str | None:
        index = DIRECTIONS.index(self.direction)
        directions = dict(
            L=DIRECTIONS[index - 1],
            R=DIRECTIONS[(index + 1) % len(DIRECTIONS)],
        )
        for code, direction in directions.items():
            if PointHelper.add(self.location, direction) in self.scafolding:
                self.direction = direction
                return code
        return None

    def move_until_end(self) -> int:
        amount = 0
        while PointHelper.add(self.location, self.direction) in self.scafolding:
            self.location = PointHelper.add(self.location, self.direction)
            amount += 1
        return amount


@dataclass(frozen=True)
class Instruction:
    function: list[str]
    starts: list[int]

    def contains(self, i: int) -> bool:
        for start in self.starts:
            if i >= start and i < start + len(self.function):
                return True
        return False

    def get_end(self, i: int) -> int | None:
        for start in self.starts:
            if i == start:
                return start + len(self.function)
        return None


@dataclass(frozen=True)
class Compressed:
    routine: list[str]
    a_function: list[str]
    b_function: list[str]
    c_function: list[str]


@dataclass
class Compression:
    instructions: list[str]
    max_length: int

    def compress(self) -> Compressed:
        a, b, c = self.compress_instructions()
        return Compressed(
            routine=self.create_routine(dict(A=a, B=b, C=c)),
            a_function=a.function,
            b_function=b.function,
            c_function=c.function,
        )

    def compress_instructions(self) -> list[Instruction]:
        for a in self.generate_instruction([]):
            for b in self.generate_instruction([a]):
                for c in self.generate_instruction([a, b]):
                    if self.first_out([a, b, c]) is None:
                        return [a, b, c]
        raise Exception("FAILED")

    def generate_instruction(
        self, previous: list[Instruction]
    ) -> Generator[Instruction, None, None]:
        start = self.first_out(previous)
        assert start is not None
        for i in range(1, 1 + self.max_length):
            function = self.instructions[start : start + i]
            yield Instruction(function=function, starts=self.get_starts(function))

    def get_starts(self, function: list[str]) -> list[int]:
        bounds: list[int] = []
        i = 0
        while i < (len(self.instructions) - len(function)) + 1:
            if function == self.instructions[i : i + len(function)]:
                bounds.append(i)
                i += len(function)
            else:
                i += 1
        return bounds

    def first_out(self, instructions: list[Instruction]) -> int | None:
        for i in range(len(self.instructions)):
            if not any([instruction.contains(i) for instruction in instructions]):
                return i
        return None

    def create_routine(self, name_instruction: dict[str, Instruction]) -> list[str]:
        i = 0
        routine: list[str] = []
        while i < len(self.instructions):
            for name, instruction in name_instruction.items():
                end = instruction.get_end(i)
                if end is not None:
                    routine.append(name)
                    i = end
                    break
        return routine


@dataclass
class VacuumDroid(Bus):
    current: Point
    scafolding: list[Point] = field(default_factory=list)
    instructions: list[int] = field(default_factory=list)
    state: DroidState | None = None
    running: bool = False
    value: int | None = None

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return self.instructions.pop(0)

    @override
    def add_output(self, value: int) -> None:
        if self.running:
            self.value = value
        else:
            self.current = self.update_scafolding(chr(value))

    def update_scafolding(self, value: str) -> Point:
        if value == "\n":
            return (0, self.current[1] + 1)
        elif value == ".":
            return PointHelper.add(self.current, (1, 0))
        elif value == "#":
            self.scafolding.append(self.current)
            return PointHelper.add(self.current, (1, 0))
        elif value in STATE_MAPPING:
            self.state = DroidState(
                self.current, self.scafolding, DIRECTIONS[STATE_MAPPING[value]]
            )
            self.scafolding.append(self.current)
            return PointHelper.add(self.current, (1, 0))
        else:
            raise Exception("FAILED")

    def get_intersections(self) -> list[Point]:
        return [
            point
            for point in self.scafolding
            if all([p in self.scafolding for p in PointHelper.neighbors(point)])
        ]

    def create_path(self) -> None:
        assert self.state is not None
        instructions = self.state.get_instructions()
        compressed = Compression(instructions, 5).compress()
        self.add_instruction(compressed.routine)
        self.add_instruction(compressed.a_function)
        self.add_instruction(compressed.b_function)
        self.add_instruction(compressed.c_function)
        self.add_instruction(["n"])

    def add_instruction(self, instructions: list[str]) -> None:
        for ch in ",".join(instructions):
            self.instructions.append(ord(ch))
        self.instructions.append(10)


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    droid = VacuumDroid(current=(0, 0))
    answer.part1(9876, total_alignment(memory, droid))
    answer.part2(1234055, dust_collected(memory, droid))


def total_alignment(memory: list[int], droid: VacuumDroid) -> int:
    run_droid(memory, droid, False)
    intersections = droid.get_intersections()
    return sum([point[0] * point[1] for point in intersections])


def dust_collected(memory: list[int], droid: VacuumDroid) -> int | None:
    droid.create_path()
    droid.running = True
    run_droid(memory, droid, True)
    return droid.value


def run_droid(memory: list[int], droid: VacuumDroid, prompt: bool) -> None:
    memory = memory.copy()
    memory[0] = 2 if prompt else memory[0]
    Computer(bus=droid, memory=memory).run()


if __name__ == "__main__":
    main()
