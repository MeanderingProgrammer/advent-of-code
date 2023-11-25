from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]
Grid = dict[Point, int]
TO_POINT: dict[str, Point] = dict(
    u=(0, 1),
    d=(0, -1),
    r=(1, 0),
    l=(-1, 0),
)
NEXT_DIRECTION: dict[str, str] = dict(
    r="u",
    u="l",
    l="d",
    d="r",
)


def add(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


def adjacent(p: Point) -> list[Point]:
    all_directions = list(TO_POINT.values())
    all_directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
    return [add(p, direction) for direction in all_directions]


def main() -> None:
    goal = Parser().integer()
    answer.part1(419, build_grid(goal, part1)[0])
    answer.part2(295229, build_grid(goal, part2)[1])


def build_grid(goal: int, updater) -> tuple[int, int]:
    point: Point = (0, 0)
    value: int = 1
    grid: Grid = {point: value}
    direction: str = "r"
    while value < goal:
        point = add(point, TO_POINT[direction])
        value = updater(value, grid, point)
        grid[point] = value
        next_direction = NEXT_DIRECTION[direction]
        direction = (
            direction
            if add(point, TO_POINT[next_direction]) in grid
            else next_direction
        )
    return abs(point[0]) + abs(point[1]), value


def part1(previous: int, grid: Grid, point: Point) -> int:
    return previous + 1


def part2(_: int, grid: Grid, point: Point) -> int:
    return sum([grid.get(neighbor, 0) for neighbor in adjacent(point)])


if __name__ == "__main__":
    main()
