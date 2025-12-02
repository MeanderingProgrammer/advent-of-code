from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper


@answer.timer
def main() -> None:
    grid = Parser().grid()
    start = [point for point, value in grid.items() if value == "^"][0]
    path = follow(grid, start)
    assert path is not None
    answer.part1(5516, len(path))
    answer.part2(2008, obstacles(grid, start, path))


def follow(grid: Grid[str], point: Point) -> set[Point] | None:
    seen: set[tuple[Point, Direction]] = set()
    direction = Direction.UP
    while point in grid:
        if (point, direction) in seen:
            return None
        seen.add((point, direction))
        next_point = PointHelper.go(point, direction)
        if grid.get(next_point, ".") == "#":
            direction = direction.right()
        else:
            point = next_point
    return set([p for p, _ in seen])


def obstacles(grid: Grid[str], start: Point, options: set[Point]) -> int:
    result: int = 0
    for point in options:
        if grid.get(point, "#") == "^":
            continue
        grid[point] = "#"
        if follow(grid, start) is None:
            result += 1
        grid[point] = "."
    return result


if __name__ == "__main__":
    main()
