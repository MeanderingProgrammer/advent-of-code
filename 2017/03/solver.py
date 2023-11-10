from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser


def main() -> None:
    goal = Parser().integer()
    answer.part1(419, len(build_grid(goal, updater_v1)[0]))
    answer.part2(295229, build_grid(goal, updater_v2)[1])


def build_grid(goal: int, updater) -> tuple[Point, int]:
    point, value = Point(0, 0), 1
    grid = Grid()
    grid[point] = value

    while value < goal:
        up_in = point.up() in grid
        down_in = point.down() in grid
        left_in = point.left() in grid
        right_in = point.right() in grid

        if not up_in and not down_in and not left_in and not right_in:
            point = point.right()
        elif not up_in and not right_in:
            if left_in:
                point = point.up()
            else:
                point = point.left()
        elif not up_in and not left_in:
            if down_in:
                point = point.left()
            else:
                point = point.down()
        elif not down_in and not left_in:
            if right_in:
                point = point.down()
            else:
                point = point.right()
        elif not down_in and not right_in:
            if up_in:
                point = point.right()
            else:
                point = point.up()

        value = updater(value, grid, point)
        grid[point] = value

    return point, value


def updater_v1(previous: int, grid: Grid, point: Point) -> int:
    return previous + 1


def updater_v2(_: int, grid: Grid, point: Point) -> int:
    return sum([grid.get(neighbor, 0) for neighbor in point.adjacent(True)])


if __name__ == "__main__":
    main()
