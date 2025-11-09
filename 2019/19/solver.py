from dataclasses import dataclass

from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser
from aoc.point import Point


@dataclass
class Beam:
    point: Point
    called: bool = False
    value: int | None = None

    def active(self) -> bool:
        return True

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
        beam = Beam(point)
        Computer(bus=beam, memory=self.memory.copy()).run()
        result = beam.value
        assert result is not None
        return result

    def left_most(self, y: int) -> int:
        x = self.beam_starts.get(y - 1, 0)
        while self.test((x, y)) != 1:
            x += 1
        self.beam_starts[y] = x
        return x

    def can_bound(self, point: Point, offset: int) -> bool:
        edge = (point[0] + offset, point[1] - offset)
        return self.test(edge) == 1


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    tester = Tester(memory=memory, beam_starts=dict())
    answer.part1(160, affected_points(tester, 50))
    answer.part2(9441282, bounding_point(tester, 100))


def affected_points(tester: Tester, size: int) -> int:
    result = 0
    for y in range(size):
        for x in range(size):
            result += tester.test((x, y))
    return result


def bounding_point(tester: Tester, size: int) -> int:
    row, offset = 1_000, size - 1
    while not tester.can_bound((tester.left_most(row), row), offset):
        row += 1
    x, y = tester.left_most(row), row - offset
    return (10_000 * x) + y


if __name__ == "__main__":
    main()
