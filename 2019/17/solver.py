from typing import override

from aoc import answer
from aoc.board import Point
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

STATE_MAPPING = {"^": 0, ">": 1, "v": 2, "<": 3}
DIRECTIONS = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]


class DroidState:
    def __init__(self, location, scafolding, direction):
        self.location = location
        self.scafolding = scafolding
        self.direction = DIRECTIONS[STATE_MAPPING[direction]]

    def has_next(self):
        return self.get_direction() is not None

    def get_instruction(self):
        code, self.direction = self.get_direction()
        return code, self.move_until_end()

    def get_direction(self):
        direction_index = DIRECTIONS.index(self.direction)

        left = DIRECTIONS[direction_index - 1]
        right = DIRECTIONS[(direction_index + 1) % len(DIRECTIONS)]

        if (self.location + left) in self.scafolding:
            return "L", left
        elif (self.location + right) in self.scafolding:
            return "R", right
        else:
            return None

    def move_until_end(self):
        amount = 0
        while (self.location + self.direction) in self.scafolding:
            self.location += self.direction
            amount += 1
        return amount


class VacuumDroid(Bus):
    def __init__(self):
        self.current = Point(0, 0)
        self.state = None
        self.scafolding = set()

        self.instructions = []
        self.index = 0
        self.running = False
        self.value = None

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        if self.index >= len(self.instructions):
            raise Exception("PASSED END")
        value = self.instructions[self.index]
        self.index += 1
        return value

    @override
    def add_output(self, value: int) -> None:
        if self.running:
            self.value = value
            return
        val = chr(value)
        if val == "\n":
            self.current = Point(0, self.current.y() + 1)
        else:
            if val != ".":
                self.scafolding.add(self.current)
                if val != "#":
                    self.state = DroidState(self.current, self.scafolding, val)
            self.current = self.current.right()

    def get_intersections(self):
        intersections = set()
        for point in self.scafolding:
            contains = [adjacent in self.scafolding for adjacent in point.adjacent()]
            if all(contains):
                intersections.add(point)
        return intersections

    def create_path(self):
        assert self.state is not None
        instructions = []
        while self.state.has_next():
            instructions.append(self.state.get_instruction())
        a, a_bounds, b, b_bounds, c, c_bounds = self.compress_instructions(
            instructions, 5
        )
        routine = self.create_routine(a_bounds, b_bounds, c_bounds, len(instructions))
        self.add_instruction(routine)
        self.add_instruction(a)
        self.add_instruction(b)
        self.add_instruction(c)
        self.instructions.append(ord("n"))
        self.instructions.append(10)

    def add_instruction(self, instructions):
        if type(instructions[0]) is str:
            instructions = ",".join(instructions)
        else:
            instructions = ",".join(
                ["{},{}".format(*instruction) for instruction in instructions]
            )
        for ch in instructions:
            self.instructions.append(ord(ch))
        self.instructions.append(10)

    def create_routine(self, a_bounds, b_bounds, c_bounds, end):
        i = 0
        routine = []
        while i < end:
            a_end = self.get_end_bound(i, a_bounds)
            b_end = self.get_end_bound(i, b_bounds)
            c_end = self.get_end_bound(i, c_bounds)
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
                raise Exception("OOOPS")
        return routine

    def compress_instructions(self, instructions, max_length):
        total_instructions = len(instructions)
        for i in range(1, 1 + max_length):
            a = instructions[:i]
            a_bounds = self.get_bounds(a, instructions)

            start_j = i
            while self.in_bounds(start_j, a_bounds):
                start_j += len(a)

            for j in range(1 + start_j, 1 + start_j + max_length):
                b = instructions[start_j:j]
                b_bounds = self.get_bounds(b, instructions)

                start_k = j
                while self.in_bounds(start_k, a_bounds) or self.in_bounds(
                    start_k, b_bounds
                ):
                    if self.in_bounds(start_k, a_bounds):
                        start_k += len(a)
                    else:
                        start_k += len(b)

                for k in range(1 + start_k, 1 + start_k + max_length):
                    c = instructions[start_k:k]
                    c_bounds = self.get_bounds(c, instructions)

                    all_bounds = [a_bounds, b_bounds, c_bounds]
                    if self.contains_all(all_bounds, total_instructions):
                        return (a, a_bounds, b, b_bounds, c, c_bounds)
        raise Exception("Should never get here")

    def get_bounds(self, sublist, main):
        bounds = []
        i = 0
        while i < (len(main) - len(sublist)) + 1:
            contained = True
            for j in range(len(sublist)):
                if main[i + j] != sublist[j]:
                    contained = False
            if contained:
                bounds.append((i, i + len(sublist)))
            i += 1
        return bounds

    def contains_all(self, all_bounds, total_instructions):
        flattened = [bound for bounds in all_bounds for bound in bounds]
        for i in range(total_instructions):
            if not self.in_bounds(i, flattened):
                return False
        return True

    def in_bounds(self, index, bounds):
        for bound in bounds:
            if index >= bound[0] and index < bound[1]:
                return True
        return False

    def get_end_bound(self, index, bounds):
        for bound in bounds:
            if index == bound[0]:
                return bound[1]
        return None


def main():
    droid = VacuumDroid()
    answer.part1(9876, total_alignment(droid))
    answer.part2(1234055, dust_collected(droid))


def total_alignment(droid: VacuumDroid):
    run_droid(droid, False)
    intersections = droid.get_intersections()
    alignments = [get_alignment(intersection) for intersection in intersections]
    return sum(alignments)


def get_alignment(point: Point) -> int:
    return point.x() * point.y()


def dust_collected(droid: VacuumDroid):
    droid.create_path()
    droid.running = True
    run_droid(droid, True)
    return droid.value


def run_droid(droid: VacuumDroid, prompt: bool):
    memory = Parser().int_csv()
    if prompt:
        # Set memory at address 0 to 2 to be prompted for input
        memory[0] = 2
    Computer(bus=droid, memory=memory).run()


if __name__ == "__main__":
    main()
