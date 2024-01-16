from aoc import answer
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper


@answer.timer
def main() -> None:
    answer.part1(2081, run(1))
    answer.part2(2341, run(2))


def run(santas: int) -> int:
    locations: list[Point] = []
    for i in range(santas):
        locations.append((0, 0))

    visited = [location for location in locations]

    for i, direction in enumerate(Parser().string()):
        direction = Direction.from_str(direction)
        santa_index = i % len(locations)
        locations[santa_index] = PointHelper.go(locations[santa_index], direction)
        visited.append(locations[santa_index])

    return len(set(visited))


if __name__ == "__main__":
    main()
