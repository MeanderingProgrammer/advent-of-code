from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.board import Direction, Point
from aoc.parser import Parser


@dataclass(frozen=True)
class Path:
    points: set[Point]
    step_counts: dict[Point, int]

    def intersection(self, other: Self) -> set[Point]:
        return self.points & other.points

    def steps(self, location: Point) -> int:
        return self.step_counts[location]


@answer.timer
def main() -> None:
    data = Parser().lines()
    p1, p2 = create_path(data[0]), create_path(data[1])
    intersections = p1.intersection(p2)
    answer.part1(870, min(list(map(len, intersections))))
    answer.part2(
        13698, min([p1.steps(point) + p2.steps(point) for point in intersections])
    )


def create_path(line: str) -> Path:
    points: list[Point] = [Point(0, 0)]
    step_counts: dict[Point, int] = dict()
    steps: int = 0
    for part in line.split(","):
        direction = Direction.from_str(part[0])
        for _ in range(int(part[1:])):
            steps += 1
            next_point = points[-1].go(direction)
            points.append(next_point)
            if next_point not in step_counts:
                step_counts[next_point] = steps
    return Path(
        points=set(points[1:]),
        step_counts=step_counts,
    )


if __name__ == "__main__":
    main()
