from aoc import answer
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper

Grid = dict[Point, int]


@answer.timer
def main() -> None:
    goal = Parser().integer()
    answer.part1(419, build_grid(goal, part1)[0])
    answer.part2(295229, build_grid(goal, part2)[1])


def build_grid(goal: int, updater) -> tuple[int, int]:
    point = (0, 0)
    direction: Direction = Direction.RIGHT
    value: int = 1
    grid: Grid = {point: value}
    while value < goal:
        point = PointHelper.go(point, direction)
        value = updater(value, grid, point)
        grid[point] = value
        next_direction = Direction.counter_clockwise(direction)
        direction = (
            direction
            if PointHelper.go(point, next_direction) in grid
            else next_direction
        )
    return PointHelper.len(point), value


def part1(previous: int, grid: Grid, point: Point) -> int:
    return previous + 1


def part2(_: int, grid: Grid, point: Point) -> int:
    return sum(
        [grid.get(neighbor, 0) for neighbor in PointHelper.neighbors_diagonal(point)]
    )


if __name__ == "__main__":
    main()
