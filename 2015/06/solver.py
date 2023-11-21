from typing import Callable

from aoc import answer
from aoc.parser import Parser

Actions = dict[str, Callable[[int], int]]

SINGLE: Actions = dict(
    on=lambda _: 1,
    off=lambda _: 0,
    toggle=lambda current: 1 - current,
)

DIMABLE: Actions = dict(
    on=lambda current: current + 1,
    off=lambda current: max(current - 1, 0),
    toggle=lambda current: current + 2,
)


class Direction:
    def __init__(self, value: str):
        values = value.split()
        self.action = values[-4]
        self.start = Direction.to_point(values[-3])
        self.end = Direction.to_point(values[-1])

    def apply(self, grid: list[int], actions: Actions) -> None:
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                index = (x * 1_000) + y
                grid[index] = actions[self.action](grid[index])

    @staticmethod
    def to_point(coords: str) -> tuple[int, int]:
        values = coords.split(",")
        return (int(values[0]), int(values[1]))


def main() -> None:
    directions = [Direction(line) for line in Parser().lines()]
    answer.part1(400410, apply_all(directions, SINGLE))
    answer.part2(15343601, apply_all(directions, DIMABLE))


def apply_all(directions: list[Direction], actions: Actions) -> int:
    grid: list[int] = [0] * 1_000_000
    for direction in directions:
        direction.apply(grid, actions)
    return sum(grid)


if __name__ == "__main__":
    main()
