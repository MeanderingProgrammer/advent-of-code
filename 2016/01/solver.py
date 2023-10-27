from aoc import answer
from aoc.board import Point
from aoc.parser import Parser

DIRECTIONS = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]


def main():
    visited = traverse()
    answer.part1(252, len(visited[-1]))
    answer.part2(143, len(repeated(visited)))


def traverse():
    index, position = 0, Point(0, 0)
    visited = [position]

    for instruction in Parser().csv():
        change = -1 if instruction[0] == "L" else 1
        index = (index + change) % len(DIRECTIONS)
        amount = int(instruction[1:])
        for _ in range(amount):
            position += DIRECTIONS[index]
            visited.append(position)

    return visited


def repeated(visited):
    seen = set()
    for position in visited:
        if position in seen:
            return position
        else:
            seen.add(position)
    raise Exception("Should never get here")


if __name__ == "__main__":
    main()
