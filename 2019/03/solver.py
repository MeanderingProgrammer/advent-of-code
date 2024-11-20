from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper


@dataclass(frozen=True)
class Path:
    distances: dict[Point, int]

    def intersection(self, other: Self) -> list[Point]:
        return [point for point in self.distances if point in other.distances]


@answer.timer
def main() -> None:
    data = Parser().lines()
    p1, p2 = create_path(data[0]), create_path(data[1])
    intersections = p1.intersection(p2)
    answer.part1(870, min(map(PointHelper.len, intersections)))
    answer.part2(
        13698,
        min([p1.distances[point] + p2.distances[point] for point in intersections]),
    )


def create_path(line: str) -> Path:
    point: Point = (0, 0)
    distance: int = 0
    distances: dict[Point, int] = dict()
    for step in line.split(","):
        direction = Direction.from_str(step[0])
        amount = int(step[1:])
        for _ in range(amount):
            point = PointHelper.go(point, direction)
            distance += 1
            if point not in distances:
                distances[point] = distance
    return Path(distances=distances)


if __name__ == "__main__":
    main()
