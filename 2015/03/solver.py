from aoc import answer
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper


@answer.timer
def main() -> None:
    data = Parser().string()
    answer.part1(2081, run(data, 1))
    answer.part2(2341, run(data, 2))


def run(data: str, santas: int) -> int:
    locations: list[Point] = []
    for i in range(santas):
        locations.append((0, 0))

    visited = [location for location in locations]

    for i, direction in enumerate(data):
        direction = Direction.from_str(direction)
        santa_index = i % len(locations)
        locations[santa_index] = PointHelper.go(locations[santa_index], direction)
        visited.append(locations[santa_index])

    return len(set(visited))


if __name__ == "__main__":
    main()
