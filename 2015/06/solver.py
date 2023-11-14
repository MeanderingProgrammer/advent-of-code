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


class Direction:
    def __init__(self, value: str):
        values = value.split()
        self.action = values[-4]
        self.start = Direction.to_point(values[-3])
        self.end = Direction.to_point(values[-1])

    def apply(self, grid: list[list[tuple[int, int]]]) -> None:
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                lit, bright = grid[x][y]
                grid[x][y] = (SINGLE[self.action](lit), DIMABLE[self.action](bright))

    @staticmethod
    def to_point(coords: str) -> tuple[int, int]:
        values = coords.split(",")
        return (int(values[0]), int(values[1]))


def main() -> None:
    grid = run_grid()
    answer.part1(400410, sum_grid(grid, 0))
    answer.part2(15343601, sum_grid(grid, 1))


def run_grid() -> list[list[tuple[int, int]]]:
    directions = [Direction(line) for line in Parser().lines()]
    grid: list[list[tuple[int, int]]] = [[(0, 0)] * 1_000 for _ in range(1_000)]
    for direction in directions:
        direction.apply(grid)
    return grid


def sum_grid(grid: list[list[tuple[int, int]]], index: int) -> int:
    total = 0
    for column in grid:
        for value in column:
            total += value[index]
    return total


if __name__ == "__main__":
    main()
