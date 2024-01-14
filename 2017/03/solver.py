from aoc import answer
from aoc.board import Direction, Point
from aoc.parser import Parser

Grid = dict[Point, int]


@answer.timer
def main() -> None:
    goal = Parser().integer()
    answer.part1(419, build_grid(goal, part1)[0])
    answer.part2(295229, build_grid(goal, part2)[1])


def build_grid(goal: int, updater) -> tuple[int, int]:
    point = Point(0, 0)
    direction: Direction = Direction.RIGHT
    value: int = 1
    grid: Grid = {point: value}
    while value < goal:
        point = point.go(direction)
        value = updater(value, grid, point)
        grid[point] = value
        next_direction = Direction.counter_clockwise(direction)
        direction = direction if point.go(next_direction) in grid else next_direction
    return len(point), value


def part1(previous: int, grid: Grid, point: Point) -> int:
    return previous + 1


def part2(_: int, grid: Grid, point: Point) -> int:
    return sum([grid.get(neighbor, 0) for neighbor in point.neighbors_diagonal()])


if __name__ == "__main__":
    main()
