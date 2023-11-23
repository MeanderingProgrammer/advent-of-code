from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]
Grid = dict[Point, str]

ALIVE, EMPTY, MIDDLE = "#", ".", (2, 2)


def up(p: Point) -> tuple[str, Point]:
    return ("u", (p[0], p[1] + 1))


def down(p: Point) -> tuple[str, Point]:
    return ("d", (p[0], p[1] - 1))


def left(p: Point) -> tuple[str, Point]:
    return ("l", (p[0] - 1, p[1]))


def right(p: Point) -> tuple[str, Point]:
    return ("r", (p[0] + 1, p[1]))


INNER: dict[str, list[Point]] = dict(
    u=[(x, 0) for x in range(5)],  # bottom row of points
    d=[(x, 4) for x in range(5)],  # top row of points
    l=[(4, y) for y in range(5)],  # right most points
    r=[(0, y) for y in range(5)],  # left most points
)

OUTER: dict[str, Point] = dict(
    u=up(MIDDLE)[1],
    d=down(MIDDLE)[1],
    l=left(MIDDLE)[1],
    r=right(MIDDLE)[1],
)


@dataclass(frozen=True)
class Layout:
    grids: list[Grid]
    recursive: bool

    def step(self) -> Self:
        grids = self.grids
        if self.recursive:
            grids = [self.new_grid()] + grids + [self.new_grid()]

        next_grids = []
        for level, grid in enumerate(grids):
            next_grid = dict()
            for point, value in grid.items():
                if self.recursive and point == MIDDLE:
                    continue
                bugs = self.bugs_adjacent(grids, level, point)
                bug_values = [1] if value == ALIVE else [1, 2]
                next_grid[point] = ALIVE if bugs in bug_values else EMPTY
            next_grids.append(next_grid)
        return type(self)(next_grids, self.recursive)

    def new_grid(self) -> Grid:
        return {point: EMPTY for point in self.grids[0]}

    def bugs_adjacent(self, grids: list[Grid], level: int, point: Point) -> int:
        bugs = 0
        for direction, adjacent in [up(point), down(point), left(point), right(point)]:
            if self.recursive and adjacent == MIDDLE:
                if level - 1 >= 0:
                    bugs += Layout.bugs(grids[level - 1], INNER[direction])
            elif self.recursive and adjacent not in grids[level]:
                if level + 1 < len(grids):
                    bugs += Layout.bugs(grids[level + 1], [OUTER[direction]])
            else:
                bugs += Layout.bugs(grids[level], [adjacent])
        return bugs

    @staticmethod
    def bugs(grid: Grid, points: list[Point]) -> int:
        return sum([grid.get(point) == ALIVE for point in points])

    def diversity(self) -> int:
        return sum([pow(2, (point[1] * 5) + point[0]) for point in self.bug_points()])

    def count_bugs(self) -> int:
        return len(self.bug_points())

    def bug_points(self) -> list[Point]:
        points = []
        for grid in self.grids:
            bugs = [point for point, value in grid.items() if value == ALIVE]
            points.extend(bugs)
        return points


def main():
    answer.part1(32776479, part_1().diversity())
    answer.part2(2017, part_2().count_bugs())


def part_1() -> Layout:
    seen = []
    layout = Layout([get_grid()], False)
    while layout not in seen:
        seen.append(layout)
        layout = layout.step()
    return layout


def part_2() -> Layout:
    layout = Layout([get_grid()], True)
    for _ in range(200):
        layout = layout.step()
    return layout


def get_grid() -> Grid:
    grid = dict()
    for point, value in Parser().as_grid().items():
        grid[(point.x(), point.y())] = value
    return grid


if __name__ == "__main__":
    main()
