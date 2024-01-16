from dataclasses import dataclass

from aoc import answer
from aoc.board import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper


@dataclass
class Animator:
    force_corners: bool
    on: set[Point]
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def add_corners(self) -> None:
        if self.force_corners:
            self.on.add((self.min_x, self.min_y))
            self.on.add((self.min_x, self.max_y))
            self.on.add((self.max_x, self.min_y))
            self.on.add((self.max_x, self.max_y))

    def step(self) -> None:
        next_on: set[Point] = set()
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                point = (x, y)
                neighbors_on = self.neighbors_on(point)
                neighbors_needed = [2, 3] if point in self.on else [3]
                if neighbors_on in neighbors_needed:
                    next_on.add(point)
        self.on = next_on
        self.add_corners()

    def neighbors_on(self, point: Point) -> int:
        return sum(
            [adjacent in self.on for adjacent in PointHelper.neighbors_diagonal(point)]
        )

    def lights_on(self) -> int:
        return len(self.on)


@answer.timer
def main() -> None:
    grid = Parser().as_grid()
    answer.part1(1061, run(grid, False))
    answer.part2(1006, run(grid, True))


def run(grid: Grid, force_corners: bool) -> int:
    on = points_on(grid)
    xs, ys = grid.xs(), grid.ys()
    animator = Animator(
        force_corners=force_corners,
        on=on,
        min_x=min(xs),
        max_x=max(xs),
        min_y=min(ys),
        max_y=max(ys),
    )
    animator.add_corners()
    for _ in range(100):
        animator.step()
    return animator.lights_on()


def points_on(grid: Grid) -> set[Point]:
    on: set[Point] = set()
    for point, value in grid.items():
        if value == "#":
            on.add((point.x, point.y))
    return on


if __name__ == "__main__":
    main()
