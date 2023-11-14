from dataclasses import dataclass

from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser

Point = tuple[int, int]


class Beam:
    def __init__(self, memory: list[int], point: Point):
        self.computer = Computer(self)
        self.computer.set_memory(memory)
        self.point = point
        self.called = False
        self.value = None

    def run(self) -> int:
        self.computer.run()
        assert self.value is not None
        return self.value

    def get_input(self) -> int:
        value = self.point[0] if not self.called else self.point[1]
        self.called = not self.called
        return value

    def add_output(self, value: int) -> None:
        self.value = value


@dataclass(frozen=True)
class Tester:
    memory: list[int]
    beam_starts: dict[int, int]

    def test(self, point: Point) -> int:
        return Beam(memory=list(self.memory), point=point).run()

    def left_most(self, y: int) -> int:
        x = self.beam_starts.get(y - 1, 0)
        while self.test((x, y)) != 1:
            x += 1
        self.beam_starts[y] = x
        return x

    def can_bound(self, point: Point, offset: int) -> bool:
        edge = (point[0] + offset, point[1] - offset)
        return self.test(edge) == 1


def main() -> None:
    tester = Tester(memory=Parser().int_csv(), beam_starts=dict())
    answer.part1(160, affected_points(tester, 50))
    answer.part2(9441282, bounding_point(tester, 100))


def affected_points(tester: Tester, size: int) -> int:
    affected = []
    for y in range(size):
        for x in range(size):
            affected.append(tester.test((x, y)))
    return sum(affected)


def bounding_point(tester: Tester, size: int) -> int:
    row, offset = 1_000, size - 1
    while not tester.can_bound((tester.left_most(row), row), offset):
        row += 1
    x, y = tester.left_most(row), row - offset
    return (10_000 * x) + y


if __name__ == "__main__":
    main()
