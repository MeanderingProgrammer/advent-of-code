from collections import defaultdict
from itertools import product

from aoc import answer
from aoc.parser import Parser

SINGLE = dict(
    on=lambda _: 1,
    off=lambda _: 0,
    toggle=lambda current: 1 - current,
)

DIMABLE = dict(
    on=lambda current: current + 1,
    off=lambda current: max(current - 1, 0),
    toggle=lambda current: current + 2,
)


class PointRange:
    def __init__(self, bottom_left: str, top_right: str):
        self.bottom_left = self.to_point(bottom_left)
        self.top_right = self.to_point(top_right)

    def get_points(self):
        return product(
            range(self.bottom_left[0], self.top_right[0] + 1),
            range(self.bottom_left[1], self.top_right[1] + 1),
        )

    @staticmethod
    def to_point(coords: str) -> tuple[int, int]:
        values = coords.split(",")
        return (int(values[0]), int(values[1]))


class Direction:
    def __init__(self, value: str):
        values = value.split()
        self.action = values[-4]
        self.point_range = PointRange(values[-3], values[-1])

    def apply(self, grid) -> None:
        for point in self.point_range.get_points():
            grid[point].append(self.action)


def main() -> None:
    grid_values = run_grid()
    answer.part1(400410, state_value(grid_values, SINGLE))
    answer.part2(15343601, state_value(grid_values, DIMABLE))


def run_grid() -> list[list[str]]:
    directions = [Direction(line) for line in Parser().lines()]
    grid = defaultdict(list)
    for direction in directions:
        direction.apply(grid)
    return list(grid.values())


def state_value(grid_values: list[list[str]], impacts) -> int:
    total = 0
    for grid_value in grid_values:
        current = 0
        for state_change in grid_value:
            current = impacts[state_change](current)
        total += current
    return total


if __name__ == "__main__":
    main()
