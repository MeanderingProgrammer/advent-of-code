from aoc import answer
from aoc.parser import Parser
from aoc.point import Point, PointHelper

DIRECTIONS: dict[str, Point] = dict(
    ne=(1, 1),
    nw=(-1, 1),
    se=(1, -1),
    sw=(-1, -1),
    n=(0, 2),
    s=(0, -2),
)


@answer.timer
def main() -> None:
    positions = move_to_end(Parser().csv())
    steps_required: list[int] = [steps(position) for position in positions]
    answer.part1(812, steps_required[-1])
    answer.part2(1603, max(steps_required))


def move_to_end(directions: list[str]) -> list[Point]:
    current: Point = (0, 0)
    positions: list[Point] = [current]
    for direction in directions:
        current = PointHelper.add(current, DIRECTIONS[direction])
        positions.append(current)
    return positions


def steps(position: Point) -> int:
    x_steps = abs(position[0])
    y_teps = abs(position[1]) - x_steps
    return x_steps + max(0, y_teps // 2)


if __name__ == "__main__":
    main()
