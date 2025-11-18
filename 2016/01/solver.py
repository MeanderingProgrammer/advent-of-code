from aoc import answer
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper

DIRECTIONS: list[Direction] = [
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
    Direction.LEFT,
]


@answer.timer
def main() -> None:
    instructions = Parser().csv()
    visited = traverse(instructions)
    answer.part1(252, PointHelper.len(visited[-1]))
    answer.part2(143, PointHelper.len(repeated(visited)))


def traverse(instructions: list[str]) -> list[Point]:
    index = 0
    position = (0, 0)
    visited: list[Point] = [position]
    for instruction in instructions:
        change = -1 if instruction[0] == "L" else 1
        index = (index + change) % len(DIRECTIONS)
        for _ in range(int(instruction[1:])):
            position = PointHelper.go(position, DIRECTIONS[index])
            visited.append(position)
    return visited


def repeated(visited: list[Point]) -> Point:
    seen: set[Point] = set()
    for position in visited:
        if position in seen:
            return position
        else:
            seen.add(position)
    raise Exception("Should never get here")


if __name__ == "__main__":
    main()
