from typing import Callable

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper

type Context = tuple[int, Grid[int], Point]


@answer.timer
def main() -> None:
    goal = Parser().integer()
    answer.part1(419, build_grid(goal, part1)[0])
    answer.part2(295229, build_grid(goal, part2)[1])


def build_grid(goal: int, updater: Callable[[Context], int]) -> tuple[int, int]:
    point = (0, 0)
    direction: Direction = Direction.RIGHT
    value: int = 1
    grid: Grid[int] = {point: value}
    while value < goal:
        point = PointHelper.go(point, direction)
        value = updater((value, grid, point))
        grid[point] = value
        next_direction = direction.left()
        direction = (
            direction
            if PointHelper.go(point, next_direction) in grid
            else next_direction
        )
    return PointHelper.len(point), value


def part1(context: Context) -> int:
    return context[0] + 1


def part2(context: Context) -> int:
    return sum(
        [
            context[1].get(neighbor, 0)
            for neighbor in PointHelper.all_neighbors(context[2])
        ]
    )


if __name__ == "__main__":
    main()
