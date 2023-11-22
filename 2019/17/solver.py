from dataclasses import dataclass
from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

Point = tuple[int, int]


def add(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


STATE_MAPPING: dict[str, int] = {"^": 0, ">": 1, "v": 2, "<": 3}
DIRECTIONS: list[Point] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class DroidState:
    def __init__(self, location: Point, scafolding: set[Point], direction: str):
        self.location: Point = location
        self.scafolding: set[Point] = scafolding
        self.direction: Point = DIRECTIONS[STATE_MAPPING[direction]]

    def has_next(self):
        return self.get_direction() is not None

    def get_instruction(self) -> str:
        code, self.direction = self.get_direction()
        until_end = self.move_until_end()
        return f"{code},{until_end}"

    def get_direction(self) -> Optional[tuple[str, Point]]:
        direction_index = DIRECTIONS.index(self.direction)
        left = DIRECTIONS[direction_index - 1]
        if add(self.location, left) in self.scafolding:
            return "L", left
        right = DIRECTIONS[(direction_index + 1) % len(DIRECTIONS)]
        if add(self.location, right) in self.scafolding:
            return "R", right
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
class InstructionCompression:
    instructions: list[str]

    def compress(self) -> Compressed:
        a_s, b_s, c_s = self.compress_instructions(5)
        return Compressed(
            routine=self.create_routine(a_s, b_s, c_s),
            a_function=a_s[0],
            b_function=b_s[0],
            c_function=c_s[0],
        )

    def compress_instructions(self, max_length: int):
        for i in range(1, 1 + max_length):
            a = self.instructions[:i]
            a_s = a, self.get_starts(a)

            start_j = i
            while self.in_bounds(start_j, a_s):
                start_j += len(a)

            for j in range(1 + start_j, 1 + start_j + max_length):
                b = self.instructions[start_j:j]
                b_s = b, self.get_starts(b)

                start_k = j
                while self.in_bounds(start_k, a_s) or self.in_bounds(start_k, b_s):
                    if self.in_bounds(start_k, a_s):
                        start_k += len(a)
                    else:
                        start_k += len(b)

                for k in range(1 + start_k, 1 + start_k + max_length):
                    c = self.instructions[start_k:k]
                    c_s = c, self.get_starts(c)

                    if self.contains_all([a_s, b_s, c_s]):
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

    def in_bounds(self, i: int, function_starts: tuple[list[str], list[int]]) -> bool:
        for start in function_starts[1]:
            if i >= start and i < start + len(function_starts[0]):
                return True
        return False

    def contains_all(self, function_starts: list[tuple[list[str], list[int]]]) -> bool:
        for i in range(len(self.instructions)):
            if not any(
                [
                    self.in_bounds(i, function_start)
                    for function_start in function_starts
                ]
            ):
                return False
        return True

    def create_routine(
        self,
        a_s: tuple[list[str], list[int]],
        b_s: tuple[list[str], list[int]],
        c_s: tuple[list[str], list[int]],
    ):
        i = 0
        routine = []
        while i < len(self.instructions):
            a_end = self.get_end_bound(i, a_s)
            b_end = self.get_end_bound(i, b_s)
            c_end = self.get_end_bound(i, c_s)
            if a_end is not None:
                routine.append("A")
                i = a_end
            elif b_end is not None:
                routine.append("B")
                i = b_end
            elif c_end is not None:
                routine.append("C")
                i = c_end
            else:
                raise Exception("FAILED")
        return routine

    def get_end_bound(self, i: int, function_start: tuple[list[str], list[int]]):
        for start in function_start[1]:
            if i == start:
                return start + len(function_start[0])
        return None


@dataclass
class VacuumDroid(Bus):
    current: Point
    scafolding: set[Point]
    instructions: list[int]
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
            return
        val = chr(value)
        if val == "\n":
            self.current = (0, self.current[1] + 1)
        else:
            if val != ".":
                self.scafolding.add(self.current)
                if val != "#":
                    self.state = DroidState(self.current, self.scafolding, val)
            self.current = add(self.current, (1, 0))

    def get_intersection(self) -> set[Point]:
        intersection = set()
        for point in self.scafolding:
            if all(
                [add(point, direction) in self.scafolding for direction in DIRECTIONS]
            ):
                intersection.add(point)
        return intersection

    def create_path(self) -> None:
        assert self.state is not None
        instructions: list[str] = []
        while self.state.has_next():
            instructions.append(self.state.get_instruction())
        compressed = InstructionCompression(instructions).compress()
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
    droid = VacuumDroid(
        current=(0, 0),
        scafolding=set(),
        instructions=[],
    )
    answer.part1(9876, total_alignment(droid))
    answer.part2(1234055, dust_collected(droid))


def total_alignment(droid: VacuumDroid) -> int:
    run_droid(droid, False)
    intersection = droid.get_intersection()
    alignments = [point[0] * point[1] for point in intersection]
    return sum(alignments)


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
