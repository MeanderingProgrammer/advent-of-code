from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser
from aoc.point import Point

Location = tuple[Point, int]

MIDDLE = (2, 2)


def neighbors(p: Point) -> list[Point]:
    return [
        (p[0], p[1] + 1),
        (p[0], p[1] - 1),
        (p[0] - 1, p[1]),
        (p[0] + 1, p[1]),
    ]


def valid(p: Point) -> bool:
    return p[0] >= 0 and p[0] <= 4 and p[1] >= 0 and p[1] <= 4


INNER: list[list[Point]] = [
    [(x, 0) for x in range(5)],  # bottom row of points
    [(x, 4) for x in range(5)],  # top row of points
    [(4, y) for y in range(5)],  # right most points
    [(0, y) for y in range(5)],  # left most points
]

OUTER: list[Point] = neighbors(MIDDLE)


@dataclass(frozen=True)
class Layout:
    grid: set[Location]
    recursive: bool

    def step(self) -> Self:
        counts: dict[Location, int] = dict()
        for point, depth in self.grid:
            for direction, adjacent in enumerate(neighbors(point)):
                for location in self.adjacent(depth, direction, adjacent):
                    if valid(location[0]):
                        counts[location] = counts.get(location, 0) + 1
        next_grid: set[Location] = set()
        for location, count in counts.items():
            if count == 1 or (count == 2 and location not in self.grid):
                next_grid.add(location)
        return type(self)(next_grid, self.recursive)

    def adjacent(self, depth: int, direction: int, adjacent: Point) -> list[Location]:
        if self.recursive and adjacent == MIDDLE:
            return [(point, depth - 1) for point in INNER[direction]]
        elif self.recursive and not valid(adjacent):
            return [(OUTER[direction], depth + 1)]
        else:
            return [(adjacent, depth)]

    def diversity(self) -> int:
        return sum([pow(2, (y * 5) + x) for ((x, y), _) in self.grid])

    def bugs(self) -> int:
        return len(self.grid)


@answer.timer
def main() -> None:
    grid: set[Location] = set()
    for point, value in Parser().grid().items():
        if value == "#":
            grid.add((point, 0))
    answer.part1(32776479, part_1(grid))
    answer.part2(2017, part_2(grid))


def part_1(start_grid: set[Location]) -> int:
    seen: list[Layout] = []
    layout = Layout(start_grid, False)
    while layout not in seen:
        seen.append(layout)
        layout = layout.step()
    return layout.diversity()


def part_2(start_grid: set[Location]) -> int:
    layout = Layout(start_grid, True)
    for _ in range(200):
        layout = layout.step()
    return layout.bugs()


if __name__ == "__main__":
    main()
