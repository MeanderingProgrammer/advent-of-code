from typing import Generator

from aoc import answer
from aoc.board import Grid
from aoc.parser import Parser


class Animator:
    def __init__(
        self,
        force_corners: bool,
        on: set[tuple[int, int]],
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int,
    ):
        self.force_corners = force_corners
        self.on = on
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.add_corners()

    def add_corners(self):
        if self.force_corners:
            self.on.add((self.min_x, self.min_y))
            self.on.add((self.min_x, self.max_y))
            self.on.add((self.max_x, self.min_y))
            self.on.add((self.max_x, self.max_y))

    def step(self) -> None:
        next_on = set()
        for point in self.get_points():
            neighbors_on = self.neighbors_on(point)
            neighbors_needed = [2, 3] if point in self.on else [3]
            if neighbors_on in neighbors_needed:
                next_on.add(point)
        self.on = next_on
        self.add_corners()

    def get_points(self) -> Generator[tuple[int, int], None, None]:
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                yield (x, y)

    def neighbors_on(self, point: tuple[int, int]) -> int:
        adjacents = [
            (point[0] - 1, point[1]),
            (point[0] + 1, point[1]),
            (point[0], point[1] - 1),
            (point[0], point[1] + 1),
            (point[0] - 1, point[1] - 1),
            (point[0] - 1, point[1] + 1),
            (point[0] + 1, point[1] - 1),
            (point[0] + 1, point[1] + 1),
        ]
        return sum([adjacent in self.on for adjacent in adjacents])

    def lights_on(self):
        return len(self.on)


def main() -> None:
    grid = Parser().as_grid()
    answer.part1(1061, run(grid, False))
    answer.part2(1006, run(grid, True))


def run(grid: Grid, force_corners: bool) -> int:
    on = points_on(grid)
    xs, ys = grid.xs(), grid.ys()
    assert ys is not None
    animator = Animator(
        force_corners=force_corners,
        on=on,
        min_x=min(xs),
        max_x=max(xs),
        min_y=min(ys),
        max_y=max(ys),
    )
    for _ in range(100):
        animator.step()
    return animator.lights_on()


def points_on(grid: Grid) -> set[tuple[int, int]]:
    on = set()
    for point, value in grid.items():
        if value == "#":
            on.add((point.x(), point.y()))
    return on


if __name__ == "__main__":
    main()
