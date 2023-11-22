from dataclasses import dataclass, field
from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

Point = tuple[int, int]
STATE_MAPPING: dict[str, int] = {"^": 0, ">": 1, "v": 2, "<": 3}
DIRECTIONS: list[Point] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def add(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


def adjacent(p: Point) -> list[Point]:
    return [add(p, direction) for direction in DIRECTIONS]


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

    def set_direction(self) -> Optional[str]:
        index = DIRECTIONS.index(self.direction)
        directions = dict(
            L=DIRECTIONS[index - 1],
            R=DIRECTIONS[(index + 1) % len(DIRECTIONS)],
        )
        for code, direction in directions.items():
            if add(self.location, direction) in self.scafolding:
                self.direction = direction
                return code
        return None

    def move_until_end(self) -> int:
        amount = 0
        while add(self.location, self.direction) in self.scafolding:
            self.location = add(self.location, self.direction)
            amount += 1
        return amount


@dataclass(frozen=True)
class Compressed:
    routine: list[str]
    a_function: list[str]
    b_function: list[str]
    c_function: list[str]


@dataclass
class Compression:
    instructions: list[str]

    def compress(self) -> Compressed:
        a_s, b_s, c_s = self.compress_instructions(5)
        return Compressed(
            routine=self.create_routine(dict(A=a_s, B=b_s, C=c_s)),
            a_function=a_s[0],
            b_function=b_s[0],
            c_function=c_s[0],
        )

    def compress_instructions(self, max_length: int):
        for i in range(1, 1 + max_length):
            a = self.instructions[:i]
            a_s = a, self.get_starts(a)

            start_j = self.first_out([a_s])
            assert start_j is not None

            for j in range(1 + start_j, 1 + start_j + max_length):
                b = self.instructions[start_j:j]
                b_s = b, self.get_starts(b)

                start_k = self.first_out([a_s, b_s])
                assert start_k is not None

                for k in range(1 + start_k, 1 + start_k + max_length):
                    c = self.instructions[start_k:k]
                    c_s = c, self.get_starts(c)

                    if self.first_out([a_s, b_s, c_s]) is None:
                        return (a_s, b_s, c_s)
        raise Exception("FAILED")

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

    def first_out(
        self, function_starts: list[tuple[list[str], list[int]]]
    ) -> Optional[int]:
        for i in range(len(self.instructions)):
            if not any(
                [
                    Compression.contains(i, function_start)
                    for function_start in function_starts
                ]
            ):
                return i
        return None

    @staticmethod
    def contains(i: int, function_starts: tuple[list[str], list[int]]) -> bool:
        for start in function_starts[1]:
            if i >= start and i < start + len(function_starts[0]):
                return True
        return False

    def create_routine(
        self, name_function_start: dict[str, tuple[list[str], list[int]]]
    ) -> list[str]:
        i = 0
        routine = []
        while i < len(self.instructions):
            for name, function_start in name_function_start.items():
                end = Compression.get_end(i, function_start)
                if end is not None:
                    routine.append(name)
                    i = end
                    break
        return routine

    @staticmethod
    def get_end(i: int, function_start: tuple[list[str], list[int]]) -> Optional[int]:
        for start in function_start[1]:
            if i == start:
                return start + len(function_start[0])
        return None


@dataclass
class VacuumDroid(Bus):
    current: Point
    scafolding: list[Point] = field(default_factory=list)
    instructions: list[int] = field(default_factory=list)
    state: Optional[DroidState] = None
    running: bool = False
    value: Optional[int] = None

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
            return add(self.current, (1, 0))
        elif value == "#":
            self.scafolding.append(self.current)
            return add(self.current, (1, 0))
        elif value in STATE_MAPPING:
            self.state = DroidState(
                self.current, self.scafolding, DIRECTIONS[STATE_MAPPING[value]]
            )
            self.scafolding.append(self.current)
            return add(self.current, (1, 0))
        else:
            raise Exception("FAILED")

    def get_intersections(self) -> list[Point]:
        return [
            point
            for point in self.scafolding
            if all([p in self.scafolding for p in adjacent(point)])
        ]

    def create_path(self) -> None:
        assert self.state is not None
        instructions = self.state.get_instructions()
        compressed = Compression(instructions).compress()
        self.add_instruction(compressed.routine)
        self.add_instruction(compressed.a_function)
        self.add_instruction(compressed.b_function)
        self.add_instruction(compressed.c_function)
        self.add_instruction(["n"])

    def add_instruction(self, instructions: list[str]) -> None:
        for ch in ",".join(instructions):
            self.instructions.append(ord(ch))
        self.instructions.append(10)


def main() -> None:
    droid = VacuumDroid(current=(0, 0))
    answer.part1(9876, total_alignment(droid))
    answer.part2(1234055, dust_collected(droid))


def total_alignment(droid: VacuumDroid) -> int:
    run_droid(droid, False)
    intersections = droid.get_intersections()
    return sum([point[0] * point[1] for point in intersections])


def dust_collected(droid: VacuumDroid) -> Optional[int]:
    droid.create_path()
    droid.running = True
    run_droid(droid, True)
    return droid.value


def run_droid(droid: VacuumDroid, prompt: bool) -> None:
    memory = Parser().int_csv()
    memory[0] = 2 if prompt else memory[0]
    Computer(bus=droid, memory=memory).run()


if __name__ == "__main__":
    main()
