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

    visited = set(locations)
    for i, direction in enumerate(data):
        santa = i % santas
        direction = Direction.new(direction)
        locations[santa] = PointHelper.go(locations[santa], direction)
        visited.add(locations[santa])
    return len(visited)


if __name__ == "__main__":
    main()
