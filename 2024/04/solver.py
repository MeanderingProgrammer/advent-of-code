from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper

HEADINGS: list[Point] = []
HEADINGS.extend([(0, 1), (1, 1), (1, 0), (1, -1)])
HEADINGS.extend([(0, -1), (-1, -1), (-1, 0), (-1, 1)])


@answer.timer
def main() -> None:
    grid = Parser().grid()
    answer.part1(2543, part1(grid))
    answer.part2(1930, part2(grid))


def part1(grid: Grid[str]) -> int:
    result: int = 0
    for point in grid:
        for heading in HEADINGS:
            if has(grid, point, heading, "XMAS"):
                result += 1
    return result


def part2(grid: Grid[str]) -> int:
    result: int = 0
    for point in grid:
        if mas(grid, point, 0, -1) and mas(grid, point, -2, 1):
            result += 1
    return result


def mas(grid: Grid[str], start: Point, offset: int, direction: int) -> bool:
    point = PointHelper.add(start, (0, offset))
    heading = (-1, direction)
    return has(grid, point, heading, "MAS") or has(grid, point, heading, "SAM")


def has(grid: Grid[str], point: Point, heading: Point, goal: str) -> bool:
    for ch in goal:
        if grid.get(point) != ch:
            return False
        point = PointHelper.add(point, heading)
    return True


if __name__ == "__main__":
    main()
