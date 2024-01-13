from aoc import answer
from aoc.board import Direction, Point
from aoc.parser import Parser

DIRECTIONS: list[Direction] = [
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
    Direction.LEFT,
]


@answer.timer
def main() -> None:
    visited = traverse()
    answer.part1(252, len(visited[-1]))
    answer.part2(143, len(repeated(visited)))


def traverse() -> list[Point]:
    index = 0
    position = Point(0, 0)
    visited: list[Point] = [position]
    for instruction in Parser().csv():
        change = -1 if instruction[0] == "L" else 1
        index = (index + change) % len(DIRECTIONS)
        for _ in range(int(instruction[1:])):
            position = position.go(DIRECTIONS[index])
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
